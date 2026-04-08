#!/usr/bin/env python3
import json
import os
import sys
from tools.skill_simulator_optimized import MaoSkillSimulatorOptimized

def run_extended_tests():
    """运行扩展后的测试套件"""
    # 读取测试套件
    with open('tests/test_suite.json', 'r', encoding='utf-8') as f:
        test_suite = json.load(f)
    
    simulator = MaoSkillSimulatorOptimized()
    
    print("======================================================================")
    print("毛泽东.skill 扩展测试套件执行")
    print("======================================================================\n")
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    error_tests = 0
    
    # 运行所有测试
    for category in test_suite:
        print(f"📁 测试类别: {category['category']}")
        print("-" * 40 + "\n")
        
        for test in category['tests']:
            total_tests += 1
            test_name = test['name']
            test_input = test['input']
            test_desc = test['description']
            
            print(f"测试: {test_name}")
            print(f"描述: {test_desc}")
            print(f"输入: {test_input}")
            
            try:
                # 生成响应
                response = simulator.generate_response(test_input)
                print(f"响应: {response[:100]}..." if len(response) > 100 else f"响应: {response}")
                
                # 检查测试条件
                passed = False
                if 'expected_keywords' in test:
                    keywords = test['expected_keywords']
                    found_keywords = [kw for kw in keywords if kw in response]
                    passed = len(found_keywords) >= min(3, len(keywords))
                    print(f"关键词检查: 找到 {len(found_keywords)}/{len(keywords)} 个关键词")
                    
                elif 'expected_patterns' in test:
                    patterns = test['expected_patterns']
                    found_patterns = [pt for pt in patterns if pt in response]
                    passed = len(found_patterns) >= min(2, len(patterns))
                    print(f"模式检查: 找到 {len(found_patterns)}/{len(patterns)} 个模式")
                    
                elif 'expected_indicators' in test:
                    indicators = test['expected_indicators']
                    found_indicators = [ind for ind in indicators if ind in response]
                    passed = len(found_indicators) >= min(2, len(indicators))
                    print(f"指示器检查: 找到 {len(found_indicators)}/{len(indicators)} 个指示器")
                
                # 输出结果
                if passed:
                    print(f"✅ {test_name}: passed")
                    passed_tests += 1
                else:
                    print(f"❌ {test_name}: failed")
                    failed_tests += 1
                    
            except Exception as e:
                print(f"⚠️ {test_name}: error - {str(e)}")
                error_tests += 1
            
            print()  # 空行分隔
    
    # 汇总结果
    print("======================================================================")
    print("测试结果汇总")
    print("======================================================================")
    print(f"总计测试: {total_tests}")
    print(f"✅ 通过: {passed_tests}")
    print(f"❌ 失败: {failed_tests}")
    print(f"⚠️ 错误: {error_tests}")
    
    # 计算通过率
    if total_tests > 0:
        pass_rate = (passed_tests / total_tests) * 100
        print(f"\n📊 通过率: {pass_rate:.1f}%")
        
        if pass_rate >= 95:
            print("🎉 测试套件执行成功！通过率达标。")
        elif pass_rate >= 80:
            print("⚠️ 测试套件基本通过，建议进一步优化。")
        else:
            print("❌ 测试套件未达标，需要改进。")
    
    return passed_tests, failed_tests, error_tests

if __name__ == "__main__":
    run_extended_tests()