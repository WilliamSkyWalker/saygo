"""OpenAI-compatible vision client. No hidden retries or plaintext credential storage."""
import base64
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError


def settings_path():
    return Path(os.environ.get('SAYGO_HOME_DIR', Path.home()/'.saygo'))/'desktop.json'


def validate(settings):
    url = settings['base_url'].strip().rstrip('/')
    parsed = urlsplit(url)
    if parsed.username or parsed.password or parsed.query or parsed.fragment or not parsed.hostname:
        raise ValueError('API 地址不能包含密码、查询参数或片段')
    if parsed.scheme != 'https' and not (parsed.scheme == 'http' and parsed.hostname in {'localhost','127.0.0.1','::1'}):
        raise ValueError('API 必须使用 HTTPS；本机服务可使用 HTTP')
    if not settings['model'].strip():
        raise ValueError('请填写支持图像输入的模型名称')
    return {'base_url':url, 'model':settings['model'].strip()}


def credential_id(settings):
    return hashlib.sha256(validate(settings)['base_url'].encode()).hexdigest()


def secure_backend():
    import keyring
    backend = keyring.get_keyring()
    # Never accept an optional plaintext/file backend selected by the environment.
    if type(backend).__module__ not in {'keyring.backends.Windows','keyring.backends.macOS',
                                       'keyring.backends.SecretService','keyring.backends.kwallet'}:
        raise RuntimeError('系统密钥存储不可用。取消“记住 Key”可仅在本次运行使用。')
    return backend


def save_settings(settings, key, remember=False):
    settings = validate(settings)
    if remember:
        if not key:
            raise ValueError('API Key 不能为空')
        secure_backend().set_password('Saygo Desktop', credential_id(settings), key)
    from saygo.integrations.browser_bridge import atomic_json
    path = settings_path(); path.parent.mkdir(parents=True, exist_ok=True)
    atomic_json(path, {**settings, 'remember':remember})


def load_settings():
    path = settings_path()
    return json.loads(path.read_text()) if path.exists() else {'base_url':'https://api.openai.com/v1','model':'','remember':False}


def load_key(settings):
    if not settings.get('remember'):
        return ''
    return secure_backend().get_password('Saygo Desktop', credential_id(settings)) or ''


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('模型服务发生重定向，请直接填写最终 API 地址')


class VisionModel:
    def __init__(self, settings, key):
        self.settings = validate(settings)
        self.key = key

    def complete(self, system, text, images=()):
        content = [{'type':'text','text':text}]
        for label, png in images:
            content += [{'type':'text','text':label}, {'type':'image_url','image_url':{
                'url':'data:image/png;base64,'+base64.b64encode(png).decode()}}]
        body = {'model':self.settings['model'], 'messages':[
            {'role':'system','content':system}, {'role':'user','content':content}], 'max_tokens':1500}
        headers = {'Content-Type':'application/json'}
        if self.key:
            headers['Authorization'] = 'Bearer '+self.key
        request = Request(self.settings['base_url']+'/chat/completions', data=json.dumps(body).encode(), headers=headers)
        try:
            with build_opener(NoRedirect()).open(request, timeout=30) as response:
                data = json.loads(response.read(4*1024*1024))
        except HTTPError as exc:
            # Provider bodies can echo credentials; never show/log them.
            messages = {401:'Token 无效或已过期，请检查 API Token',
                        403:'没有访问权限，请检查 Token 和模型授权',
                        404:'接口或模型不存在，请检查服务地址和模型名称',
                        429:'请求受限或额度不足，请检查服务商配额后重试'}
            message = messages.get(exc.code, '模型服务暂时不可用，请稍后重试' if exc.code >= 500 else '模型请求被拒绝，请检查接口与图像输入支持')
            raise RuntimeError(f'{message}（HTTP {exc.code}）') from None
        except (URLError, TimeoutError):
            raise RuntimeError('无法连接模型服务或请求超时，请检查服务地址和网络') from None
        return data['choices'][0]['message']['content']

    def test(self):
        import io
        from PIL import Image
        raw = io.BytesIO(); Image.new('RGB',(32,32),'red').save(raw,format='PNG')
        result = self.complete('Describe the provided image briefly.', '图片是什么颜色？', [('连接测试',raw.getvalue())])
        return {'message':'图像请求成功；模型回复：'+str(result)[:300]}
