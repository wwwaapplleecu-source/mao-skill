#!/usr/bin/env python3
"""
最终整合测试
验证六层架构所有关键功能点
"""

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_test(name, test_func):
    """运行单个测试"""
    try:
        start = time.time()
        result = test_func()
        elapsed = time.time() - start
        
        if result:
            print(f"  PASS {name} ({elapsed:.3f}s)")
            return True, elapsed
        else:
            print(f"  FAIL {name} ({elapsed:.3f}s)")
            return False, elapsed
            
    except Exception as e:
        print(f"  ERROR {name}: {e}")
        return False, 0

def test_imports():
    """测试导入"""
    from mao_skill_integration_v2 import MaoSkillIntegrationV2
    from six_layer_integration import SixLayerIntegration
    from method_executor import MethodExecutor
    from knowledge_retriever import KnowledgeRetriever
    from analytics_layer import AnalyticsLayer
    return True

def test_v2_integration():
    """测试V2集成"""
    from mao_skill_integration_v2 import MaoSkillIntegrationV2
    integration = MaoSkillIntegrationV2(enable_cache=False, enable_monitoring=False)
    
    # 测试新命令
    response = integration.process_command('/mao help')
    if not response or '❌' in response:
        return False
    
    # 测试分析命令
    response = integration.process_command('/mao 分析团队协作')
    if not response or '❌' in response:
        return False
    
    return True

def test_six_layer():
    """测试六层集成"""
    from six_layer_integration import SixLayerIntegration
    integration = SixLayerIntegration(enable_cache=False, enable_monitoring=False)
    
    result = integration.process_command('/mao help', 'test_user')
    if not result.get('success'):
        return False
    
    return True

def test_backward_compatibility():
    """测试向后兼容"""
    from mao_skill_integration_v2 import MaoSkillIntegrationV2
    integration = MaoSkillIntegrationV2()
    
    # 测试几个老命令
    commands = [
        '/mao-work 分析问题',
        '/mao-persona 写文本',
        '/mao-analyze 矛盾 分析问题',
        '/mao-concepts',
    ]
    
    for cmd in commands:
        response = integration.process_command(cmd)
        if not response or '❌' in response:
            return False
    
    return True

def test_components():
    """测试各组件"""
    # 方法执行层
    from method_executor import MethodExecutor
    executor = MethodExecutor()
    result = executor.execute_method('矛盾', '测试')
    if not result.get('success'):
        return False
    
    # 知识检索层
    from knowledge_retriever import KnowledgeRetriever
    retriever = KnowledgeRetriever()
    result = retriever.get_learning_path('入门')
    if not result.get('success'):
        return False
    
    # 分析决策层
    from analytics_layer import AnalyticsLayer
    analytics = AnalyticsLayer()
    result = analytics.analyze_problem('分析问题')
    if not result.get('success'):
        return False
    
    return True

def test_performance_basic():
    """测试基本性能"""
    from mao_skill_integration_v2 import MaoSkillIntegrationV2
    integration = MaoSkillIntegrationV2(enable_cache=True, enable_monitoring=True)
    
    # 测试响应时间
    commands = [
        '/mao help',
        '/mao 分析问题',
        '/mao learn --path=入门',
    ]
    
    for cmd in commands:
        start = time.time()
        response = integration.process_command(cmd)
        elapsed = time.time() - start
        
        if elapsed > 5.0:  # 超过5秒认为性能问题
            return False
    
    return True

def main():
    """主函数"""
    print("毛泽东.skill 六层架构最终整合测试")
    print("=" * 50)
    
    tests = [
        ("模块导入", test_imports),
        ("V2集成系统", test_v2_integration),
        ("六层集成", test_six_layer),
        ("向后兼容", test_backward_compatibility),
        ("各组件功能", test_components),
        ("基本性能", test_performance_basic),
    ]
    
    results = []
    total_time = 0
    
    for name, test_func in tests:
        success, elapsed = run_test(name, test_func)
        results.append((name, success, elapsed))
        total_time += elapsed
    
    # 统计结果
    print(f"\n" + "=" * 50)
    print("测试结果汇总:")
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, elapsed in results:
        status = "PASS" if success else "FAIL"
        print(f"  {status} {name} ({elapsed:.3f}s)")
    
    print(f"\n通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"总测试时间: {total_time:.2f}s")
    
    # 总体评估
    if passed == total:
        print("\n[SUCCESS] 所有测试通过 - 系统整合成功!")
        return True
    else:
        print("\n[WARNING] 部分测试失败 - 需要检查")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)