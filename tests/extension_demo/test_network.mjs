import test from 'node:test';
import assert from 'node:assert/strict';
import {webcrypto} from 'node:crypto';
import {readFile} from 'node:fs/promises';
globalThis.crypto ||= webcrypto;
// Import the browser ES module without imposing package.json on the repository.
const source = await readFile(new URL('../../extensions/saygo-browser/network.js',import.meta.url),'utf8');
const {NetworkJournal} = await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
const request = (id='1',type='Fetch') => ({requestId:id,timestamp:1,type,request:{url:'https://example.test/api',method:'POST',headers:{a:'b'},postData:'hello'}});

test('HTTP bodies, redirect, failures, cursors and tab isolation', async () => {
  const j = new NetworkJournal(async () => ({body:'{"ok":true}',base64Encoded:false}));
  j.begin(1); j.begin(2);
  await j.event(1,'Network.requestWillBeSent',request());
  await j.event(1,'Network.requestWillBeSent',{...request(),redirectResponse:{status:302,url:'https://example.test/old'}});
  await j.event(1,'Network.responseReceived',{requestId:'1',type:'Fetch',response:{status:200,mimeType:'application/json'}});
  await j.event(1,'Network.loadingFinished',{requestId:'1',timestamp:2,encodedDataLength:12});
  const rows=j.read(1).events;
  assert.equal(rows.at(-1).body,'{"ok":true}');
  assert.equal(rows.at(-2).duration_ms,1000);
  assert.equal(rows[1].kind,'http.redirect');
  assert.equal(j.read(2).events.length,0);
  assert.equal(j.read(1,{after:rows.at(-1).seq}).events.length,0);
  assert.equal(j.read(1,{url:'absent'}).next_cursor,rows.at(-1).seq);
  await j.event(1,'Network.requestWillBeSent',request('2'));
  await j.event(1,'Network.loadingFailed',{requestId:'2',timestamp:2,errorText:'failed'});
  assert.equal(j.read(1).events.at(-1).kind,'http.failed');
});

test('WebSocket text/binary frames, SSE messages and fetch streaming', async () => {
  const j=new NetworkJournal(async () => ({bufferedData:'YWJj'})); j.begin(1);
  await j.event(1,'Network.webSocketCreated',{requestId:'w',url:'wss://example.test/ws'});
  await j.event(1,'Network.webSocketFrameSent',{requestId:'w',response:{opcode:1,payloadData:'hello'}});
  await j.event(1,'Network.webSocketFrameReceived',{requestId:'w',response:{opcode:2,payloadData:'AQI='}});
  await j.event(1,'Network.webSocketClosed',{requestId:'w'});
  await j.event(1,'Network.requestWillBeSent',request('s','EventSource'));
  await j.event(1,'Network.eventSourceMessageReceived',{requestId:'s',eventName:'update',eventId:'2',data:'payload'});
  assert.equal(j.read(1,{kind:'ws'}).events[2].base64_encoded,true);
  assert.equal(j.read(1,{kind:'sse'}).events[0].data,'payload');
  await j.event(1,'Network.requestWillBeSent',request('f'));
  await j.event(1,'Network.responseReceived',{requestId:'f',type:'Fetch',response:{mimeType:'text/event-stream'}});
  await j.event(1,'Network.dataReceived',{requestId:'f',data:'ZGVm'});
  assert.deepEqual(j.read(1,{kind:'stream'}).events.map(e=>e.data),['YWJj','ZGVm']);
});

test('retention, capture identity and stop discard late bodies', async () => {
  let resolve;
  const j=new NetworkJournal(() => new Promise(r=>resolve=r)); j.begin(1);
  await j.event(1,'Network.requestWillBeSent',request());
  const pending=j.event(1,'Network.loadingFinished',{requestId:'1',timestamp:2});
  const capture=j.read(1).capture_id;
  j.end(1); resolve({body:'late'}); await pending;
  assert.equal(j.read(1).events.some(e=>e.kind==='http.body'),false);
  j.begin(1);
  assert.throws(()=>j.read(1,{capture_id:capture}),/Capture changed/);
  for(let i=0;i<1200;i++) await j.event(1,'Network.requestWillBeSent',request(String(i)));
  assert.equal(j.read(1).retained,1200);
  assert.equal(j.read(1).dropped,0);
  assert.equal(j.tabs.get(1).requests.size,1200);
  const id=j.read(1).capture_id; j.clear(1);
  assert.notEqual(j.read(1).capture_id,id);
  assert.equal(j.read(1).events.length,0);
  assert.throws(()=>j.read(1,{limit:201}),/Invalid/);
});

test('body failures are explicit and large frames stay intact', async () => {
  const j=new NetworkJournal(async()=>{throw new Error('evicted');}); j.begin(1);
  await j.event(1,'Network.requestWillBeSent',request());
  await j.event(1,'Network.loadingFinished',{requestId:'1',timestamp:2});
  assert.equal(j.read(1).events.at(-1).unavailable,'evicted');
  await j.event(1,'Network.webSocketCreated',{requestId:'w',url:'wss://example.test/ws'});
  await j.event(1,'Network.webSocketFrameReceived',{requestId:'w',response:{opcode:1,payloadData:'x'.repeat(100000)}});
  const row=j.read(1).events.at(-1);
  assert.equal(row.truncated,false); assert.equal(row.data,'x'.repeat(100000));
});

test('large Unicode bodies, headers, URLs and post data survive all former journal caps', async () => {
  const body=JSON.stringify({records:'内容😀'.repeat(600000), tail:'complete'});
  const j=new NetworkJournal(async()=>({body,base64Encoded:false}));
  for (const tab of [1,2]) {
    j.begin(tab);
    const p=request();
    p.request.url += '?q='+'a'.repeat(40000);
    p.request.headers={first:'b'.repeat(40000),second:'c'.repeat(40000)};
    p.request.postData='d'.repeat(100000);
    await j.event(tab,'Network.requestWillBeSent',p);
    await j.event(tab,'Network.loadingFinished',{requestId:'1',timestamp:2});
    const rows=j.read(tab).events;
    assert.equal(rows[0].url.length,p.request.url.length);
    assert.equal(rows[0].url,p.request.url);
    assert.deepEqual(rows[0].headers,p.request.headers);
    assert.equal(rows[0].post_data,p.request.postData);
    assert.equal(rows.at(-1).body,body);
    assert.equal(rows.at(-1).truncated,false);
  }
  assert.equal(j.read(1).events.at(-1).body,body);
  assert.equal(j.read(1).dropped+j.read(2).dropped,0);
});

test('stream setup preserves every queued chunk and waits before completing the body', async () => {
  let resolve;
  const calls=[];
  const j=new NetworkJournal(async(_tab,method)=>{
    calls.push(method);
    if(method==='Network.streamResourceContent') return new Promise(r=>resolve=r);
    throw new Error('evicted');
  });
  j.begin(1);
  await j.event(1,'Network.requestWillBeSent',request());
  const starting=j.event(1,'Network.responseReceived',{requestId:'1',type:'Fetch',response:{mimeType:'application/x-ndjson'}});
  const pieces=Array.from({length:20},(_,i)=>Buffer.from(`${i}:`+'中😀'.repeat(10000)));
  for(const piece of pieces) await j.event(1,'Network.dataReceived',{
    requestId:'1',data:piece.toString('base64'),dataLength:piece.length});
  const finished=j.event(1,'Network.loadingFinished',{requestId:'1',timestamp:2});
  assert.equal(j.read(1).pending_bodies,1);
  resolve({bufferedData:''});
  await Promise.all([starting,finished]);
  const rows=j.read(1).events;
  assert.deepEqual(rows.filter(e=>e.kind==='stream.chunk').map(e=>e.data),pieces.map(p=>p.toString('base64')));
  const last=rows.at(-1);
  assert.equal(last.kind,'http.body');
  assert.equal(last.base64_encoded,true);
  assert.deepEqual(Buffer.from(last.body,'base64'),Buffer.concat(pieces));
  assert.equal(j.read(1).pending_bodies,0);
});

test('HTTP streaming recovers evicted bodies with split UTF-8 and binary bytes', async () => {
  const payload=Buffer.concat([Buffer.from('开始😀'+'x'.repeat(300000)),Buffer.from([0,255,128])]);
  const initial=payload.subarray(0,8), rest=payload.subarray(8);
  const j=new NetworkJournal(async(_tab,method)=>{
    if(method==='Network.streamResourceContent') return {bufferedData:initial.toString('base64')};
    throw new Error('evicted');
  });
  j.begin(1);
  await j.event(1,'Network.requestWillBeSent',request());
  await j.event(1,'Network.dataReceived',{requestId:'1',dataLength:initial.length});
  await j.event(1,'Network.responseReceived',{requestId:'1',type:'Fetch',response:{mimeType:'application/octet-stream'}});
  await j.event(1,'Network.dataReceived',{requestId:'1',data:rest.toString('base64'),dataLength:rest.length});
  await j.event(1,'Network.loadingFinished',{requestId:'1',timestamp:2});
  const row=j.read(1).events.at(-1);
  assert.equal(row.base64_encoded,true);
  assert.deepEqual(Buffer.from(row.body,'base64'),payload);
  assert.equal(row.unavailable,undefined);
});

test('a lost stream prefix never masquerades as a complete body', async () => {
  const j=new NetworkJournal(async(_tab,method)=>{
    if(method==='Network.streamResourceContent') return {bufferedData:''};
    throw new Error('evicted');
  });
  j.begin(1);
  await j.event(1,'Network.requestWillBeSent',request());
  await j.event(1,'Network.dataReceived',{requestId:'1',dataLength:10});
  await j.event(1,'Network.responseReceived',{requestId:'1',type:'Fetch',response:{mimeType:'application/json'}});
  await j.event(1,'Network.loadingFinished',{requestId:'1',timestamp:2});
  const row=j.read(1).events.at(-1);
  assert.equal(row.body,undefined);
  assert.match(row.unavailable,/evicted/);
  assert.match(row.stream_error,/incomplete/i);
});

test('bursts do not drop response reads after sixteen pending bodies', async () => {
  const resolves=[];
  const j=new NetworkJournal(()=>new Promise(r=>resolves.push(r))); j.begin(1);
  const pending=[];
  for(let i=0;i<25;i++) {
    await j.event(1,'Network.requestWillBeSent',request(String(i)));
    pending.push(j.event(1,'Network.loadingFinished',{requestId:String(i),timestamp:2}));
  }
  assert.equal(resolves.length,25);
  resolves.forEach((r,i)=>r({body:String(i),base64Encoded:false}));
  await Promise.all(pending);
  assert.deepEqual(j.read(1).events.filter(e=>e.kind==='http.body').map(e=>e.body),Array.from({length:25},(_,i)=>String(i)));
});

test('clear discards in-flight stream state and late body results', async () => {
  let resolve;
  const j=new NetworkJournal((_tab,method)=>{
    if(method==='Network.streamResourceContent') return new Promise(r=>resolve=r);
    throw new Error('unexpected body read after clear');
  }); j.begin(1);
  await j.event(1,'Network.requestWillBeSent',request());
  const starting=j.event(1,'Network.responseReceived',{requestId:'1',type:'Fetch',response:{mimeType:'text/event-stream'}});
  j.clear(1);
  await j.event(1,'Network.dataReceived',{requestId:'1',data:'bGF0ZQ==',dataLength:4});
  resolve({bufferedData:'bGF0ZQ=='}); await starting;
  await j.event(1,'Network.loadingFinished',{requestId:'1',timestamp:2});
  assert.equal(j.read(1).events.length,0);
});
