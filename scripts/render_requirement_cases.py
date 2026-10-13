"""从独立可执行的契约用例生成可审阅的中文 BDD 场景。"""
from pathlib import Path
import importlib.util
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('requirement_cases',ROOT/'tests/control_demo/test_requirements.py')
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
integration_spec=importlib.util.spec_from_file_location('package_cases',ROOT/'tests/control_demo/test_updates_package.py')
integration=importlib.util.module_from_spec(integration_spec); integration_spec.loader.exec_module(integration)
cases=[*module.CASES,*integration.BDD]
requirements=set(re.findall(r'\| ([A-Z]+-\d{3}) \|', (ROOT/'docs/common/requirements.md').read_text(encoding='utf-8')))
assert len(cases) >= 500
assert len({case['id'] for case in cases}) == len(cases)
assert all(case['requirement'] in requirements for case in cases)
assert len(cases) == sum(unittest.defaultTestLoader.loadTestsFromModule(m).countTestCases()
                         for m in (module, integration))
families = {
    'coordinates': '坐标映射', 'invalid_action': '无效动作拒绝',
    'workflow': '工作流结构', 'reference': '引用与类型保持',
    'missing_reference': '缺失引用拒绝', 'gherkin': '用例解析',
    'progress': '步骤进度校验', 'probe': '非视觉断言声明',
    'model_url': '模型地址校验', 'backend': '后端访问限制',
    'update_notice': '更新提醒', 'update_check': '版本检查',
    'package_cli': '包模式更新命令', 'package_reject': '包模式升级限制',
    'notice_refresh': '提醒刷新', 'package_start': '包模式启动检查',
}
lines=['# language: zh-CN',
       '# 由 scripts/render_requirement_cases.py 生成；请修改来源用例后重新生成。',
       '# 每个场景对应一个独立命名的 unittest，不用场景大纲展开虚增数量。',
       '功能: Saygo 全项目需求自动化契约','']
for case in cases:
    family = case['family']
    title = ('更新集成：'+case['when']) if family.startswith('test_') else families[family]
    test_name = family if family.startswith('test_') else 'test_'+case['id'].replace('-', '_')+'_'+family
    lines += [f"  @{case['id']} @{case['requirement']} @auto",
              f"  # 对应测试：{test_name}",
              f"  场景: {case['id']} {title}",
              '    假如 '+case['given'].replace('\n','\\n'),
              '    当 '+case['when'].replace('\n','\\n'),
              '    那么 '+case['then'].replace('\n','\\n'),'']
path=ROOT/'docs/common/testing/requirements.feature'; path.parent.mkdir(parents=True,exist_ok=True)
text='\n'.join(lines)
if '--check' in sys.argv:
    if path.read_text(encoding='utf-8')!=text:raise SystemExit('BDD 目录不同步，请运行 scripts/render_requirement_cases.py')
else:path.write_text(text, encoding='utf-8')
print(f'{len(cases)} independent BDD / unittest cases')
