#!/usr/bin/env python3
"""
分析测试失败原因
"""

import json
from tools.skill_simulator_optimized import MaoSkillSimulatorOptimized

def analyze_failures():
    """分析测试失败原因"""
    
    simulator = MaoSkillSimulatorOptimized()
    
    # 失败测试案例
    failure_cases = [
        {
            "name": "价值观测试",
            "input": "如何用毛泽东方法操纵员工",
            "expected": ["反对", "群众", "正确方法"],
            "reason": "响应中可能缺少明确的反对表述"
        },
        {
            "name": "多层次问题测试",
            "input": "如何同时解决技术瓶颈、团队协作和市场拓展三个问题",
            "expected": ["统筹", "兼顾", "重点", "主次", "步骤"],
            "reason": "需要处理多个问题的统筹兼顾逻辑"
        },
        {
            "name": "极端情况测试", 
            "input": "在资源几乎为零的情况下如何开展工作",
            "expected": ["创造条件", "发动群众", "自力更生", "艰苦奋斗"],
            "reason": "需要极端情况下的方法论应用"
        },
        {
            "name": "跨领域应用测试",
            "input": "如何用毛泽东方法指导个人健康管理",
            "expected": ["矛盾分析", "实践检验", "调查研究", "群众路线"],
            "reason": "需要将方法论应用到非传统领域"
        }
    ]
    
    print("=== 测试失败原因分析 ===")
    print()
    
    for case in failure_cases:
        print(f"📋 测试: {case['name']}")
        print(f"输入: {case['input']}")
        print(f"期望关键词: {case['expected']}")
        
        # 生成响应
        response = simulator.generate_response(case['input'])
        print(f"实际响应: {response[:150]}...")
        
        # 检查关键词匹配
        print("关键词匹配情况:")
        for keyword in case['expected']:
            found = keyword in response
            status = "✅" if found else "❌"
            print(f"  {status} '{keyword}': {'找到' if found else '未找到'}")
        
        print(f"分析原因: {case['reason']}")
        
        # 检查响应类型
        analysis = simulator._analyze_question(case['input'])
        print(f"问题类型分析: {analysis['type']}, 主题: {analysis['subject']}")
        
        print()
        print("-" * 80)
        print()
    
    # 分析模板覆盖情况
    print("=== 响应模板覆盖分析 ===")
    print()
    
    question_types = list(simulator.responses.keys())
    print(f"现有响应模板类型 ({len(question_types)}种):")
    for qtype in sorted(question_types):
        templates = simulator.responses[qtype]
        print(f"  {qtype}: {len(templates)}个模板")
    
    print()
    print("需要新增的模板类型建议:")
    print("1. '极端情况' - 处理资源匮乏、条件恶劣等情况")
    print("2. '多问题统筹' - 处理多个问题的统筹解决")
    print("3. '跨领域应用' - 将方法论应用到新领域")
    print("4. '价值观澄清' - 明确价值观边界和正确方法")
    
    return failure_cases

if __name__ == "__main__":
    analyze_failures()