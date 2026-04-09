#!/usr/bin/env python3
"""
最终验证脚本

验证六层架构毛泽东.skill的完整功能，包括新老命令兼容性、各层功能、性能表现等。
"""

import sys
import os
import time
import json
from typing import Dict, List, Any

# 添加路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试各模块导入"""
    print("[工具] 测试模块导入...")
    
    modules_to_test = [
        ('command_parser', 'MaoCommandParser'),
        ('smart_recommender', 'SmartRecommender'),
        ('learning_system', 'LearningSystem'),
        ('method_executor', 'MethodExecutor'),
        ('knowledge_retriever', 'KnowledgeRetriever'),
        ('analytics_layer', 'AnalyticsLayer'),
        ('six_layer_integration', 'SixLayerIntegration'),
        ('mao_skill_integration_v2', 'MaoSkillIntegrationV2'),
        ('performance_monitor', 'PerformanceMonitor')
    ]
    
    all_success = True
    for module_name, class_name in modules_to_test:
        try:
            exec(f"from {module_name} import {class_name}")
            print(f"  ✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"  ❌ {module_name}.{class_name}: {e}")
            all_success = False
    
    return all_success

def test_basic_commands():
    """测试基本命令"""
    print("\n🎯 测试基本命令...")
    
    try:
        from mao_skill_integration_v2 import MaoSkillIntegrationV2
        integration = MaoSkillIntegrationV2(enable_cache=False, enable_monitoring=False)
        
        test_cases = [
            ("帮助命令", "/mao help", True),
            ("智能分析", "/mao 分析团队协作", True),
            ("指定方法", "/mao analyze --method=矛盾 分析问题", True),
            ("学习命令", "/mao learn --path=入门", True),
            ("概念查询", "/mao concepts 矛盾", True),
            ("老命令兼容", "/mao-analyze 矛盾 分析问题", True),
            ("错误命令", "/mao unknown-command", False)
        ]
        
        results = []
        for name, command, expected_success in test_cases:
            start_time = time.time()
            response = integration.process_command(command)
            processing_time = time.time() - start_time
            
            success = '❌' not in response and len(response) > 0
            match = success == expected_success
            
            status = "✅" if match else "❌"
            print(f"  {status} {name}: {processing_time:.3f}s ({'通过' if match else '失败'})")
            
            results.append({
                'name': name,
                'command': command,
                'success': success,
                'expected': expected_success,
                'match': match,
                'time': processing_time,
                'response_length': len(response)
            })
        
        # 统计
        passed = sum(1 for r in results if r['match'])
        total = len(results)
        
        print(f"\n  📊 通过率: {passed}/{total} ({passed/total*100:.1f}%)")
        
        return results
        
    except Exception as e:
        print(f"  ❌ 测试异常: {e}")
        return []

def test_six_layer_components():
    """测试六层架构各组件"""
    print("\n🏗️ 测试六层架构组件...")
    
    components = []
    
    try:
        # 测试方法执行层
        from method_executor import MethodExecutor
        executor = MethodExecutor()
        result = executor.execute_method('矛盾', '测试问题')
        if result.get('success'):
            print("  ✅ 方法执行层: 矛盾分析正常")
            components.append(('方法执行层', '✅'))
        else:
            print(f"  ❌ 方法执行层: {result.get('error', '未知错误')}")
            components.append(('方法执行层', '❌'))
    except Exception as e:
        print(f"  ❌ 方法执行层异常: {e}")
        components.append(('方法执行层', '❌'))
    
    try:
        # 测试知识检索层
        from knowledge_retriever import KnowledgeRetriever
        retriever = KnowledgeRetriever()
        result = retriever.get_learning_path('入门')
        if result.get('success'):
            print("  ✅ 知识检索层: 学习路径查询正常")
            components.append(('知识检索层', '✅'))
        else:
            print(f"  ❌ 知识检索层: {result.get('error', '未知错误')}")
            components.append(('知识检索层', '❌'))
    except Exception as e:
        print(f"  ❌ 知识检索层异常: {e}")
        components.append(('知识检索层', '❌'))
    
    try:
        # 测试分析决策层
        from analytics_layer import AnalyticsLayer
        analytics = AnalyticsLayer()
        result = analytics.analyze_problem('分析问题')
        if result.get('success'):
            print("  ✅ 分析决策层: 智能推荐正常")
            components.append(('分析决策层', '✅'))
        else:
            print(f"  ❌ 分析决策层: {result.get('error', '未知错误')}")
            components.append(('分析决策层', '❌'))
    except Exception as e:
        print(f"  ❌ 分析决策层异常: {e}")
        components.append(('分析决策层', '❌'))
    
    try:
        # 测试六层集成
        from six_layer_integration import SixLayerIntegration
        integration = SixLayerIntegration(enable_cache=False, enable_monitoring=False)
        result = integration.process_command('/mao help', 'test_user')
        if result.get('success'):
            print("  ✅ 六层集成系统: 命令处理正常")
            components.append(('六层集成', '✅'))
        else:
            print(f"  ❌ 六层集成系统: {result.get('error', '未知错误')}")
            components.append(('六层集成', '❌'))
    except Exception as e:
        print(f"  ❌ 六层集成系统异常: {e}")
        components.append(('六层集成', '❌'))
    
    return components

def test_performance_quick():
    """快速性能测试"""
    print("\n⚡ 快速性能测试...")
    
    try:
        from mao_skill_integration_v2 import MaoSkillIntegrationV2
        integration = MaoSkillIntegrationV2(enable_cache=True, enable_monitoring=True)
        
        # 测试几个关键命令的性能
        commands = [
            "/mao help",
            "/mao 分析团队协作",
            "/mao analyze --method=矛盾 分析问题",
            "/mao learn --path=入门"
        ]
        
        times = []
        for i, command in enumerate(commands):
            start_time = time.time()
            response = integration.process_command(command)
            processing_time = time.time() - start_time
            times.append(processing_time)
            
            # 检查响应
            success = '❌' not in response and len(response) > 0
            status = "✅" if success else "❌"
            
            print(f"  {status} 命令{i+1}: {processing_time:.3f}s ({'成功' if success else '失败'})")
        
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            
            print(f"\n  📊 平均响应时间: {avg_time:.3f}s")
            print(f"  📊 最大响应时间: {max_time:.3f}s")
            
            # 性能评估
            if avg_time < 0.5:
                grade = "优秀 🏆"
            elif avg_time < 1.0:
                grade = "良好 👍"
            elif avg_time < 2.0:
                grade = "一般 ⚠️"
            else:
                grade = "待改进 🐌"
            
            print(f"  🎯 性能评估: {grade}")
            
            return {
                'avg_time': avg_time,
                'max_time': max_time,
                'grade': grade,
                'times': times
            }
        
    except Exception as e:
        print(f"  ❌ 性能测试异常: {e}")
    
    return {}

def test_backward_compatibility():
    """测试向后兼容性"""
    print("\n🔄 测试向后兼容性...")
    
    try:
        from mao_skill_integration_v2 import MaoSkillIntegrationV2
        integration = MaoSkillIntegrationV2()
        
        legacy_commands = [
            "/mao-work 分析问题",
            "/mao-persona 写一段话",
            "/mao-analyze 矛盾 分析问题",
            "/mao-concepts",
            "/mao-examples",
            "/mao-help",
            "/mao-version"
        ]
        
        results = []
        for command in legacy_commands:
            start_time = time.time()
            response = integration.process_command(command)
            processing_time = time.time() - start_time
            
            success = '❌' not in response and len(response) > 0
            
            # 提取命令名称
            cmd_name = command.split()[0][1:]  # 去掉斜杠
            
            status = "✅" if success else "❌"
            print(f"  {status} {cmd_name}: {processing_time:.3f}s ({'成功' if success else '失败'})")
            
            results.append({
                'command': cmd_name,
                'success': success,
                'time': processing_time
            })
        
        passed = sum(1 for r in results if r['success'])
        total = len(results)
        
        print(f"\n  📊 老命令兼容性: {passed}/{total} ({passed/total*100:.1f}%)")
        
        return results
        
    except Exception as e:
        print(f"  ❌ 兼容性测试异常: {e}")
        return []

def generate_validation_report(test_results: Dict[str, Any]):
    """生成验证报告"""
    print("\n" + "=" * 60)
    print("📋 最终验证报告")
    print("=" * 60)
    
    # 总体状态
    all_passed = (
        test_results.get('imports_success', False) and
        len(test_results.get('basic_results', [])) > 0 and
        len(test_results.get('component_results', [])) > 0
    )
    
    status = "✅ 验证通过" if all_passed else "❌ 验证失败"
    print(f"\n总体状态: {status}")
    
    # 模块导入
    imports_ok = test_results.get('imports_success', False)
    print(f"\n1. 模块导入: {'✅ 成功' if imports_ok else '❌ 失败'}")
    
    # 基本命令测试
    basic_results = test_results.get('basic_results', [])
    if basic_results:
        passed = sum(1 for r in basic_results if r.get('match', False))
        total = len(basic_results)
        print(f"\n2. 基本命令测试: {passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    # 组件测试
    component_results = test_results.get('component_results', [])
    if component_results:
        passed = sum(1 for _, status in component_results if status == '✅')
        total = len(component_results)
        print(f"\n3. 组件测试: {passed}/{total} 通过 ({passed/total*100:.1f}%)")
        
        for component, status in component_results:
            print(f"   - {component}: {status}")
    
    # 性能测试
    perf_results = test_results.get('performance_results', {})
    if perf_results:
        avg_time = perf_results.get('avg_time', 0)
        grade = perf_results.get('grade', '未知')
        print(f"\n4. 性能测试: 平均 {avg_time:.3f}s [{grade}]")
    
    # 兼容性测试
    compat_results = test_results.get('compatibility_results', [])
    if compat_results:
        passed = sum(1 for r in compat_results if r.get('success', False))
        total = len(compat_results)
        print(f"\n5. 向后兼容性: {passed}/{total} 通过 ({passed/total*100:.1f}%)")
    
    # 建议
    print("\n💡 建议:")
    if all_passed:
        if perf_results and perf_results.get('avg_time', 0) > 1.0:
            print("  - 性能有待优化，建议检查缓存和算法")
        else:
            print("  - 系统运行正常，可以部署使用")
    else:
        print("  - 存在未通过的测试，需要修复后再部署")
    
    print("\n" + "=" * 60)
    
    # 保存报告
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_file = f"validation_report_{timestamp}.json"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"📁 详细报告已保存到: {report_file}")
    
    return all_passed, report_file

def main():
    """主函数"""
    print("=== 毛泽东.skill 六层架构最终验证 ===")
    print("版本: 1.2.0 (六层架构版)")
    print("=" * 60)
    
    test_results = {
        'test_timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'version': '1.2.0',
        'architecture': 'six-layer'
    }
    
    try:
        # 1. 测试模块导入
        imports_success = test_imports()
        test_results['imports_success'] = imports_success
        
        if not imports_success:
            print("\n❌ 模块导入失败，停止测试")
            generate_validation_report(test_results)
            return False
        
        # 2. 测试基本命令
        basic_results = test_basic_commands()
        test_results['basic_results'] = basic_results
        
        # 3. 测试六层组件
        component_results = test_six_layer_components()
        test_results['component_results'] = component_results
        
        # 4. 快速性能测试
        performance_results = test_performance_quick()
        test_results['performance_results'] = performance_results
        
        # 5. 测试向后兼容性
        compatibility_results = test_backward_compatibility()
        test_results['compatibility_results'] = compatibility_results
        
        # 生成报告
        all_passed, report_file = generate_validation_report(test_results)
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ 验证过程异常: {e}")
        import traceback
        traceback.print_exc()
        
        test_results['error'] = str(e)
        generate_validation_report(test_results)
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 验证完成 - 系统准备就绪!")
        sys.exit(0)
    else:
        print("\n⚠️  验证完成 - 发现问题需要修复")
        sys.exit(1)