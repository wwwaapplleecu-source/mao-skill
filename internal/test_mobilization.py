#!/usr/bin/env python3
import json
from tools.skill_simulator_optimized import MaoSkillSimulatorOptimized

simulator = MaoSkillSimulatorOptimized()

# 测试毛式表达
response = simulator.generate_response('写一段动员讲话')
print('当前动员讲话响应:')
print(response)
print()
print('检查关键词:')
keywords = ['同志们', '革命', '斗争', '胜利', '实践', '矛盾', '调查']
for kw in keywords:
    found = '✓' if kw in response else '✗'
    print(f'  {kw}: {found}')

print()
print('方法论关键词检查:')
method_keywords = ['实践', '矛盾', '调查', '群众', '战略', '分析', '研究']
method_found = [kw for kw in method_keywords if kw in response]
print(f'找到的方法论关键词: {method_found} ({len(method_found)}/{len(method_keywords)})')

print()
print('测试套件期望检查:')
print('测试期望: 包含"同志们"、"革命"、"斗争"、"胜利"等关键词')
print('测试实际: 响应包含这些关键词吗？')

# 检查测试套件的具体期望
test_expectations = {
    '同志们': '同志们' in response,
    '革命': '革命' in response,
    '斗争': '斗争' in response,
    '胜利': '胜利' in response,
}

print('\n测试套件关键词匹配:')
for keyword, found in test_expectations.items():
    status = '✅ 通过' if found else '❌ 失败'
    print(f'  {keyword}: {status}')

# 方法论关键词不足的问题
print('\n毛式表达测试失败分析:')
print('失败原因: 响应中毛泽东方法论关键词不足，只找到0个')
print('解决方案: 需要在动员讲话中融入方法论关键词，如"实践"、"矛盾"、"调查"等')
print('改进建议: 修改动员讲话模板，将方法论思想融入风格化表达')