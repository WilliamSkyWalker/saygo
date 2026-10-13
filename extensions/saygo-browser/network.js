// Full, in-memory CDP network journal. Independent of visual observations.
const base64Bytes = data => data.length * 3 / 4 - (data.endsWith('==') ? 2 : data.endsWith('=') ? 1 : 0);
export class NetworkJournal {
  constructor(send) { this.send = send; this.tabs = new Map(); }
  begin(tabId) {
    let capture = this.tabs.get(tabId);
    if (capture?.active) return capture;
    capture = {id:crypto.randomUUID(), active:true, reason:null, events:[], requests:new Map(),
      seq:0, pending:0};
    this.tabs.set(tabId, capture);
    return capture;
  }
  end(tabId, reason = 'stopped') {
    const c = this.tabs.get(tabId);
    if (c) { c.active = false; c.reason = reason; c.requests.clear(); }
  }
  clear(tabId) {
    const c = this.tabs.get(tabId);
    if (c) { c.events = []; c.requests.clear(); c.id = crypto.randomUUID(); }
  }
  reset() { this.tabs.clear(); }
  append(c, event) {
    if (!c.active) return;
    c.events.push({...event, seq:++c.seq, time:Date.now()/1000, truncated:false});
  }
  read(tabId, {after=0, limit=100, url='', kind='', capture_id=null} = {}) {
    if (!Number.isSafeInteger(after) || after < 0 || !Number.isInteger(limit) || limit < 1 || limit > 200 ||
        typeof url !== 'string' || typeof kind !== 'string') throw new Error('Invalid network query');
    const c = this.tabs.get(tabId);
    if (!c) return {active:false, reason:'not_started', capture_id:null, events:[], next_cursor:0, dropped:0};
    if (capture_id && capture_id !== c.id) throw new Error('Capture changed; restart polling with cursor 0');
    const selected = [];
    // Sequence numbers remain ordered even after clear; do not copy the whole
    // retained journal on each poll or scan earlier pages again.
    let low=0, high=c.events.length;
    while (low < high) {
      const mid=Math.floor((low+high)/2);
      if (c.events[mid].seq <= after) low=mid+1; else high=mid;
    }
    for (let i=low; i<c.events.length && selected.length<limit; i++) {
      const e=c.events[i];
      if ((!url || (e.url || '').includes(url)) && (!kind || e.kind.startsWith(kind))) selected.push(e);
    }
    return {active:c.active, reason:c.reason, capture_id:c.id, events:selected,
      next_cursor:selected.length === limit ? selected.at(-1).seq : c.seq,
      oldest_cursor:c.events[0]?.seq ?? c.seq+1, dropped:0,
      pending_bodies:c.pending, untracked_requests:0, retained:c.events.length};
  }
  async event(tabId, method, p) {
    const c = this.tabs.get(tabId);
    if (!c?.active || !method.startsWith('Network.')) return;
    const captureId = c.id;
    const current = () => this.tabs.get(tabId) === c && c.active && c.id === captureId;
    const id = p.requestId;
    const put = (url,type) => {
      const r = {url:String(url), type, start:p.timestamp, receivedBytes:0};
      c.requests.set(id,r);
      return r;
    };
    let r = c.requests.get(id);
    const emit = (kind, data={}) => {
      if (current()) this.append(c, {kind, request_id:id, url:r?.url, timestamp:p.timestamp, ...data});
    };
    if (method === 'Network.requestWillBeSent') {
      if (p.redirectResponse) emit('http.redirect', {status:p.redirectResponse.status,
        url:p.redirectResponse.url, headers:p.redirectResponse.headers});
      r = put(p.request.url,p.type);
      emit('http.request', {method:p.request.method, headers:p.request.headers,
        post_data:p.request.postData, has_post_data:p.request.hasPostData || false, resource_type:p.type});
    } else if (method === 'Network.webSocketCreated') {
      r = put(p.url,'WebSocket'); emit('ws.open');
    } else if (!r) {
      return; // Started mid-flight or cleared: never misattribute events.
    } else if (method === 'Network.responseReceived') {
      r.type = p.type;
      emit('http.response', {status:p.response.status, headers:p.response.headers,
        mime_type:p.response.mimeType, protocol:p.response.protocol,
        from_cache:!!p.response.fromDiskCache, from_service_worker:!!p.response.fromServiceWorker});
      // Save bytes while they arrive, before Chrome can evict its response
      // cache. Ordinary HTTP uses these only if getResponseBody fails.
      if (p.type !== 'EventSource') {
        const stream = r.stream = {pending:true, ready:false, queued:[], parts:[], bytes:0,
          expose:/^(text\/event-stream|application\/(x-)?ndjson)/i.test(p.response.mimeType || '')};
        stream.push = data => {
          if (!data || !current()) return;
          stream.parts.push(data); stream.bytes += base64Bytes(data);
          if (stream.expose) emit('stream.chunk', {data, base64_encoded:true});
        };
        stream.done = (async () => {
          try {
            const initial = await this.send(tabId,'Network.streamResourceContent',{requestId:id});
            if (!current()) return;
            stream.push(initial.bufferedData);
            for (const data of stream.queued) stream.push(data);
            stream.ready = true;
          } catch (error) {
            stream.error = String(error.message || error);
            if (stream.expose) emit('stream.unavailable', {error:stream.error});
          } finally { stream.pending = false; stream.queued = []; }
        })();
        await stream.done;
      }
    } else if (method === 'Network.dataReceived') {
      r.receivedBytes += p.dataLength || 0;
      if (p.data && r.stream) {
        if (r.stream.pending) r.stream.queued.push(p.data);
        else if (r.stream.ready) r.stream.push(p.data);
      }
    } else if (method === 'Network.loadingFailed') {
      emit('http.failed', {error:p.errorText, canceled:p.canceled, duration_ms:(p.timestamp-r.start)*1000});
      c.requests.delete(id);
    } else if (method === 'Network.loadingFinished') {
      emit('http.finished', {encoded_bytes:p.encodedDataLength, duration_ms:(p.timestamp-r.start)*1000});
      c.requests.delete(id);
      if (r.type === 'EventSource') return;
      c.pending++;
      try {
        // loadingFinished may arrive before streamResourceContent's reply.
        if (r.stream) await r.stream.done;
        if (!current()) return;
        const body = await this.send(tabId,'Network.getResponseBody',{requestId:id});
        emit('http.body', {body:body.body, base64_encoded:body.base64Encoded});
      } catch (error) {
        if (!current()) return;
        const stream = r.stream;
        if (stream?.ready && stream.bytes === r.receivedBytes) {
          // Base64 chunks have independent padding and may split UTF-8 code
          // points. Combine bytes, never concatenate encoded/decoded text.
          emit('http.body', {body:btoa(stream.parts.map(data=>atob(data)).join('')),
            base64_encoded:true, source:'stream'});
        } else {
          emit('http.body', {unavailable:String(error.message || error),
            stream_error:stream?.error || (stream ? 'Incomplete response stream' : 'Response streaming not started')});
        }
      } finally { c.pending--; }
    } else if (method === 'Network.eventSourceMessageReceived') {
      emit('sse.message', {event_name:p.eventName, event_id:p.eventId, data:p.data});
    } else if (method === 'Network.webSocketWillSendHandshakeRequest') {
      emit('ws.request', {headers:p.request.headers});
    } else if (method === 'Network.webSocketHandshakeResponseReceived') {
      emit('ws.response', {status:p.response.status, headers:p.response.headers});
    } else if (method === 'Network.webSocketFrameSent' || method === 'Network.webSocketFrameReceived') {
      emit(method.endsWith('Sent') ? 'ws.sent' : 'ws.received',
        {opcode:p.response.opcode, data:p.response.payloadData, base64_encoded:p.response.opcode !== 1});
    } else if (method === 'Network.webSocketFrameError') {
      emit('ws.error', {error:p.errorMessage});
    } else if (method === 'Network.webSocketClosed') {
      emit('ws.closed'); c.requests.delete(id);
    }
  }
}
