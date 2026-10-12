"""Requirement-based contracts; each matrix row is an independently named test.

The BDD catalog is generated from these exact inputs and expected outcomes by
scripts/render_requirement_cases.py. No network, GUI or live device is used here.
"""
import contextlib
import copy
import io
import itertools
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from saygo.devices import actions
from saygo.runtime import schema
from saygo.qa import gherkin, step_validator
from saygo.probes import spec
from saygo.desktop import model
from saygo.mcp import backend_policy
from saygo import updates

CASES = []


def add(requirement, family, data, expected, given, when, then):
    number = len(CASES) + 1
    CASES.append(dict(id=f'TC-{number:04}', requirement=requirement, family=family,
                      data=data, expected=expected, given=given, when=when, then=then))


def encoded(value):
    return json.dumps(value, ensure_ascii=False, allow_nan=True, sort_keys=True)


# Explicit coordinate boundary oracles; screen=(400,200), no driver input occurs.
for kind in ['tap', 'hover', 'double_click', 'right_click', 'long_press', 'scroll_at', 'swipe']:
    for x,y,px,py in [(0,0,0,0),(100,100,399,199),(50,50,200,100),
                      (25,75,100,150),(75,25,300,50),(0.25,0.5,1,1),
                      (99.75,99.5,399,199),(12.5,37.5,50,75)]:
        action = {'type':kind, 'coordinate_space':'percent', 'x':x, 'y':y}
        if kind == 'swipe': action = {'type':kind,'x1_pct':x,'y1_pct':y,'x2_pct':50,'y2_pct':50}
        if kind == 'scroll_at': action['amount'] = -.5
        add('OBS-003','coordinates',action,(px,py),
            f'屏幕为 400×200，操作参数为 {encoded(action)}', '准备操作但不派发输入',
            f'屏幕坐标为 ({px}, {py})，原始参数不被修改')
for kind in ['tap','hover','double_click','right_click','long_press','scroll_at']:
    for invalid in [-1,100.01,True,False,None,'50',float('inf'),float('nan')]:
        action={'type':kind,'x':invalid,'y':50,'coordinate_space':'percent','amount':1}
        add('OBS-003','invalid_action',action,None,
            f'屏幕为 400×200，操作参数为 {encoded(action)}','校验动作', '拒绝输入且返回 ValueError')
for kind,field in [('input','text'),('press_key','key'),('open_url','url'),('open_app','target')]:
    for value in ['',None,[],{},1,False]:
        action={'type':kind,field:value}
        add('OBS-008','invalid_action',action,None, f'动作参数为 {encoded(action)}','校验动作','因必需字段不是非空字符串而拒绝')

# Workflow resource validation across supported device kinds and invalid bindings.
for kind in ['android','ios','browser','mac','windows','sqlite']:
    for mutation in ['valid','missing_binding','empty_binding','numeric_binding','invalid_kind',
                     'bad_name','empty_steps','duplicate_step','unknown_resource','bad_version','bad_inputs','missing_action']:
        workflow={'version':1,'resources':{'target':{'kind':kind}},
                  'steps':[{'id':'check','kind':'check','actual':1,'equals':1}]}
        resource=workflow['resources']['target']
        binding='path' if kind=='sqlite' else 'session'
        resource[binding]='fixture.sqlite' if kind=='sqlite' else 'fixture'
        if kind=='sqlite': resource['queries']={'lookup':'SELECT 1'}
        if mutation=='missing_binding': resource.pop(binding)
        elif mutation=='empty_binding': resource[binding]=''
        elif mutation=='numeric_binding': resource[binding]=123
        elif mutation=='invalid_kind': resource['kind']='unsupported'
        elif mutation=='bad_name': workflow['resources']={'../target':resource}
        elif mutation=='empty_steps': workflow['steps']=[]
        elif mutation=='duplicate_step': workflow['steps']*=2
        elif mutation=='unknown_resource': workflow['steps']=[{'id':'shot','kind':'observe','resource':'missing'}]
        elif mutation=='bad_version': workflow['version']=2
        elif mutation=='bad_inputs': workflow['inputs']=[]
        elif mutation=='missing_action': workflow['steps']=[{'id':'act','kind':'action','resource':'target'}]
        add('FLOW-003' if mutation.endswith('binding') else 'FLOW-001','workflow',workflow,mutation=='valid',
            f'工作流为 {encoded(workflow)}','验证工作流',
            '接受并返回独立副本' if mutation=='valid' else '拒绝并返回 ValueError')

# Type-preserving references at scalar, object and list nesting boundaries.
for value in [None,False,True,0,-3,1.25,'001','中文',[],{'count':[1,None]}]:
    for place in ['inputs.value','steps.lookup.value','steps.lookup.rows.0','steps.lookup.rows.1.value','inputs.nested.value','steps.lookup.rows.0.value']:
        context={}
        parts=place.split('.')
        # Build the list-containing contexts explicitly to avoid stringification.
        if place=='inputs.value': context={'inputs':{'value':value}}
        elif place=='steps.lookup.value': context={'steps':{'lookup':{'value':value}}}
        elif place=='steps.lookup.rows.0': context={'steps':{'lookup':{'rows':[value]}}}
        elif place=='steps.lookup.rows.1.value': context={'steps':{'lookup':{'rows':[None,{'value':value}]}}}
        elif place=='inputs.nested.value': context={'inputs':{'nested':{'value':value}}}
        else: context={'steps':{'lookup':{'rows':[{'value':value}]}}}
        add('FLOW-007','reference',{'context':context,'path':place},value,
            f'上下文为 {encoded(context)}','解析精确引用 '+place,
            f'返回 {encoded(value)}，保留 JSON 类型和副本隔离')
for path in ['inputs.missing','steps.lookup.rows.1','steps.unknown','steps.lookup.rows.bad','inputs.value.x','']:
    add('FLOW-007','missing_reference',path,None,'上下文只有 inputs.value=1 与 steps.lookup.rows=[0]',
        '解析引用 '+repr(path),'报告无法解析，不能替换为空值')

# BDD metadata combinations exercise independent supported tags, not fake devices.
for platform,priority,automation in itertools.product(
        ['android','ios','browser','web','desktop','mac','windows','rdp'],
        ['P0','P1','P2'],['auto','partial','manual']):
    data=dict(platform=platform,priority=priority,automation=automation)
    add('QA-002','gherkin',data,data,
        f'Feature 含 Background 和一个带 @{platform} @{priority} @{automation} 的场景',
        '解析并渲染场景','保留三个标签的独立语义、Background 和 When/Then 顺序')

# Exact progression, including invalid pass attempts and insufficient evidence.
for pending in range(1,11):
    for condition in ['pass','fail','in_progress','skip_ahead','go_back','no_evidence','unknown_status']:
        progress={'current_step_index':pending,'current_step_status':'pass',
                  'evidence':'屏幕中央显示蓝色按钮，按钮文字为「继续」，下方有输入框。'}
        decision={'step_progress':progress,'action':{'type':'wait'}}
        if condition in ['pass','fail','in_progress']: progress['current_step_status']=condition
        if condition=='fail': progress['fail_reason']='目标输入框未显示预期内容，需要检查当前页面状态'
        elif condition=='skip_ahead': progress['current_step_index']+=1
        elif condition=='go_back': progress['current_step_index']-=1
        elif condition=='no_evidence': progress['evidence']='已完成'
        elif condition=='unknown_status': progress['current_step_status']='success'
        add('QA-003','progress',{'pending':pending,'decision':decision},condition in ['pass','fail','in_progress'],
            f'共 12 步，待执行第 {pending} 步，模型返回 {encoded(decision)}','验证步骤进度',
            '接受当前步骤判定' if condition in ['pass','fail','in_progress'] else '拒绝且不能推进或派发动作')

# Probe typing and binding; wrappers are real supported directive syntax variants.
values=[('0',0),('-3',-3),('1.25',1.25),('true',True),('FALSE',False),('null',None),
        ('007','007'),('"hello world"','hello world'),('"中文"','中文'),
        ('[1, false, null]',[1,False,None]),('{"name":"a b"}',{'name':'a b'}),('plain','plain')]
for raw,value in values:
    for prefix in ['# saygo-probe: ','  # saygo-probe: ','\t#saygo-probe: ','#  saygo-probe: ']:
        line=prefix+'fixture value='+raw+' enabled'
        add('PROBE-001','probe',line,value,f'步骤后声明 {encoded(line)}','解析指令并检测 case 是否包含 probe',
            f'插件名 fixture，value={encoded(value)} 且类型保持，enabled=true')

# Endpoint acceptance is credential handling, not a live provider compatibility test.
urls=[('https://example.com/v1',True),('https://example.com:8443/v1/',True),
      ('http://localhost:8080/v1',True),('http://127.0.0.1:8080/v1',True),
      ('http://[::1]:8080/v1',True),('http://example.com/v1',False),
      ('https://user:secret@example.com/v1',False),('https://example.com/v1?key=secret',False),
      ('https://example.com/v1#secret',False),('file:///tmp/model',False),
      ('https:///v1',False),('ftp://example.com/v1',False)]
for (url,valid),name in itertools.product(urls,['vision-model',' 模型 ']):
    add('GUI-004','model_url',{'base_url':url,'model':name},valid,
        f'模型配置为 {encoded(dict(base_url=url,model=name))}','校验模型配置',
        '接受并规范化空白及尾斜线' if valid else '在发出请求前拒绝不安全的地址')

for kind,saved,requested in itertools.product(['browser','android'],[None,'extension','playwright'],[None,'extension','playwright']):
    data={'state':{'kind':kind,'browser_backend':saved},'backend':requested}
    accepted=requested!='playwright' and not(kind=='browser' and saved=='playwright')
    add('BROWSER-002','backend',data,accepted,f'保存绑定和请求后端为 {encoded(data)}','通过 MCP 检查后端策略',
        '允许进入操作层' if accepted else '在操作前拒绝 Playwright 并提示扩展后端')

# Availability must survive disabled automatic application and use numeric versions.
for mode,current,candidate,automatic in itertools.product(['package','managed'],
        ['0.4.12','0.4.13','0.9.0','1.0.0'],['0.4.11','0.4.12','0.4.13','0.10.0','1.0.0','2.0.0'],[False,True]):
    available=tuple(map(int,candidate.split('.')))>tuple(map(int,current.split('.')))
    data=dict(mode=mode,current=current,candidate=candidate,automatic=automatic)
    add('UPDATE-001','update_notice',data,available,
        f'安装与缓存为 {encoded(data)}','读取已完成的更新检查结果',
        ('报告可用版本 '+candidate if available else '不提示同版或旧版')+
        ('；automatic=false 并使用 pipx 升级说明' if mode=='package' else '；保留 managed 升级说明'))

for mode,variant in itertools.product(['package','managed'],
        ['newer','older','same','offline','invalid_json','empty','prerelease','withdrawn']):
    add('UPDATE-009','update_check',dict(mode=mode,variant=variant),variant=='newer',
        f'{mode} 安装版本 0.4.12，版本源响应场景为 {variant}', '强制检查版本',
        '只有可安装的更高稳定版本才能报告 available；错误不改变运行时')
for args in [[],['--check'],['--background'],['--auto','off']]:
    add('UPDATE-005','package_cli',args,True,
        'package 安装为 0.4.12，PyPI 存在 0.4.13，旧配置 automatic=true',
        '执行更新入口 '+encoded(args),'查询版本并报告或缓存 0.4.13，不调用 apply，后台模式不污染 stdout')
for args in [['--apply'],['--auto','on']]:
    add('UPDATE-015','package_reject',args,None,'package 安装由 pipx 管理',
        '执行 '+encoded(args),'拒绝自动应用并明确提示 pipx upgrade saygo-agent-control')
for state in ['missing','expired','corrupt','fresh']:
    add('UPDATE-007','notice_refresh',state,state!='fresh',
        'package 更新缓存状态为 '+state,'客户端读取通知','过期、缺失、损坏缓存触发后台刷新；近期缓存不重复查网络')
add('UPDATE-002','package_start',None,None,'package 安装使用 pipx 解释器','启动 MCP',
    '在返回 MCP 子进程前调度独立后台检查，stdout 保持协议专用')


class Device:
    screen_size=(400,200)
    def hover(self,*args): pass
    def double_click(self,*args): pass
    def right_click(self,*args): pass
    def long_press(self,*args): pass
    def scroll_at(self,*args): pass


class RequirementTests(unittest.TestCase):
    def run_case(self, case):
        data=copy.deepcopy(case['data']); expected=case['expected']; family=case['family']
        if family=='coordinates':
            original=copy.deepcopy(data)
            actual=actions.prepare(Device(),data)
            keys=('x1','y1') if data['type']=='swipe' else ('x','y')
            self.assertEqual(tuple(actual[k] for k in keys),expected)
            self.assertEqual(actual['coordinate_space'],'screen'); self.assertEqual(data,original)
        elif family=='invalid_action':
            with self.assertRaises(ValueError): actions.prepare(Device(),data)
        elif family=='workflow':
            if expected:
                result=schema.validate(data); self.assertEqual(result,data)
                result['resources'].clear(); self.assertTrue(data['resources'])
            else:
                with self.assertRaises(ValueError): schema.validate(data)
        elif family=='reference':
            actual=schema.resolve({'$ref':data['path']},data['context'])
            self.assertEqual(actual,expected); self.assertIs(type(actual),type(expected))
            before=copy.deepcopy(data['context'])
            if isinstance(actual,list): actual.append('mutated')
            if isinstance(actual,dict): actual['mutated']=True
            self.assertEqual(data['context'],before)
        elif family=='missing_reference':
            with self.assertRaises(ValueError):
                schema.resolve({'$ref':data},{'inputs':{'value':1},'steps':{'lookup':{'rows':[0]}}})
        elif family=='gherkin':
            raw=f"Feature: Fixture\n Background:\n  Given setup\n @{data['platform']} @{data['priority']} @{data['automation']}\n Scenario: Example\n  When action\n  Then result\n"
            feature=gherkin.parse_feature(raw); scenario=feature.scenarios[0]
            self.assertEqual(scenario.platforms,[data['platform']])
            self.assertEqual(scenario.priority,data['priority']); self.assertEqual(scenario.automation,data['automation'])
            rendered=gherkin.render_case(feature,scenario)
            self.assertLess(rendered.index('Given setup'),rendered.index('When action'))
            self.assertLess(rendered.index('When action'),rendered.index('Then result'))
        elif family=='progress':
            ok,reason=step_validator.validate_step_progress(data['decision'],data['pending'],12)
            self.assertEqual(ok,expected,reason)
            if not ok:self.assertTrue(reason)
        elif family=='probe':
            parsed=spec.parse_directive_line(data)
            self.assertEqual(parsed.name,'fixture'); self.assertEqual(parsed.args['value'],expected)
            self.assertIs(type(parsed.args['value']),type(expected)); self.assertIs(parsed.args['enabled'],True)
            self.assertTrue(spec.has_probe_directive('Then result\n'+data))
        elif family=='model_url':
            if expected:
                self.assertEqual(model.validate(data),{'base_url':data['base_url'].rstrip('/'),'model':data['model'].strip()})
            else:
                with self.assertRaises(ValueError):model.validate(data)
        elif family=='backend':
            with patch.object(backend_policy.ds,'load_state',return_value=data['state']):
                if expected: backend_policy.check('fixture',data['backend'])
                else:
                    with self.assertRaises(backend_policy.UnsupportedBackendError):backend_policy.check('fixture',data['backend'])
        else: self.update_case(family,data,expected)

    def update_case(self,family,data,expected):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            mode=data.get('mode','package') if isinstance(data,dict) else 'package'
            current=data.get('current','0.4.12') if isinstance(data,dict) else '0.4.12'
            installed={'python':sys.executable,'version':current,'runtime_mode':mode}
            updates.write(root/'installation.json',installed)
            updates.write(root/'updates.json',{'automatic':True,'channel':'stable'})
            with patch.object(updates,'current',return_value=installed), patch.object(updates,'apply') as apply:
                if family=='update_notice':
                    updates.write(root/'updates.json',{'automatic':data['automatic'],'channel':'stable'})
                    updates.write(root/'update-state.json',{'current':current,'checked_at':time.time(),
                        'available':True,'release':{'tag_name':'v'+data['candidate']}})
                    info=updates.notice(root)
                    self.assertEqual(info.get('available'),('v'+data['candidate']) if expected else None)
                    self.assertEqual(info['automatic'],False if mode=='package' else data['automatic'])
                    if expected:
                        self.assertIn('url',info)
                        self.assertIn('pipx upgrade saygo-agent-control' if mode=='package' else 'saygo update --apply',info['message'])
                elif family=='update_check':
                    variant=data['variant']; candidate='0.4.13' if variant not in ['older','same'] else {'older':'0.4.11','same':'0.4.12'}[variant]
                    release={'tag_name':'v'+candidate,'draft':variant=='withdrawn','prerelease':variant=='prerelease'}
                    package_version=candidate+'rc1' if variant=='prerelease' else candidate
                    payload=({'releases':{package_version:[{'yanked':variant=='withdrawn','filename':'fixture.whl'}]}}
                             if mode=='package' else [release])
                    if variant=='empty':payload={'releases':{}} if mode=='package' else []
                    raw=b'not JSON' if variant=='invalid_json' else json.dumps(payload).encode()
                    with patch.object(updates,'fetch',return_value=raw,side_effect=OSError('offline') if variant=='offline' else None) as fetch:
                        state=updates.check(root,force=True)
                        self.assertEqual(bool(state.get('available')),expected)
                        if variant in ['offline','invalid_json']:self.assertTrue(state.get('error'))
                        fetch.assert_called_once()
                        self.assertIn('pypi.org' if mode=='package' else 'api.github.com',fetch.call_args.args[0])
                    self.assertEqual(updates.read(root/'installation.json'),installed)
                elif family in ['package_cli','package_reject']:
                    out=io.StringIO(); err=io.StringIO()
                    with patch.object(updates,'fetch',return_value=json.dumps({'releases':{'0.4.13':[{'yanked':False}]}}).encode()) as fetch, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                        if family=='package_reject':
                            with self.assertRaises(SystemExit):updates.main(['--root',str(root),*data])
                            self.assertIn('pipx upgrade saygo-agent-control',err.getvalue())
                        else:
                            self.assertEqual(updates.main(['--root',str(root),*data]),0)
                            fetch.assert_called_once()
                            self.assertEqual(updates.read(root/'update-state.json')['release']['tag_name'],'v0.4.13')
                            if '--background' in data:self.assertEqual(out.getvalue(),'')
                            else:self.assertEqual(json.loads(out.getvalue())['available'],'v0.4.13')
                elif family=='notice_refresh':
                    if data=='corrupt':(root/'update-state.json').write_text('{broken')
                    elif data!='missing': updates.write(root/'update-state.json',{'checked_at':time.time() if data=='fresh' else 1,'current':current,'available':False})
                    # Patch the thread boundary, not fetch: notice must not block on I/O.
                    with patch.object(updates.threading,'Thread') as thread:
                        updates.notice(root)
                        self.assertEqual(thread.call_count>0,expected)
                elif family=='package_start':
                    with patch.object(updates.threading,'Thread') as thread, patch.object(updates,'run_server',return_value=0) as server, contextlib.redirect_stdout(io.StringIO()) as out:
                        self.assertEqual(updates.serve(root,[]),0)
                        names=[c.kwargs.get('name','') for c in thread.call_args_list]
                        self.assertTrue(any('update' in name for name in names),names)
                        self.assertEqual(server.call_args.args[0],sys.executable)
                        self.assertEqual(out.getvalue(),'')
                apply.assert_not_called()


def install(case):
    def test(self): self.run_case(case)
    test.__doc__=case['requirement']+' '+case['then']
    setattr(RequirementTests,'test_'+case['id'].replace('-','_')+'_'+case['family'],test)

for case in CASES: install(case)

if __name__=='__main__':unittest.main()
