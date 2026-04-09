#!/usr/bin/env python3
"""
六层架构性能基准测试

测试毛泽东.skill六层架构的性能表现，包括响应时间、并发处理、缓存效果等。
"""

import time
import json
import statistics
import threading
import concurrent.futures
from typing import Dict, List, Any, Tuple
from datetime import datetime

# 导入六层集成系统
import sys
sys.path.append('.')
from tools.mao_skill_integration_v2 import MaoSkillIntegrationV2

class PerformanceBenchmark:
    """性能基准测试器"""
    
    def __init__(self, enable_cache=True, enable_monitoring=True):
        """初始化性能测试器"""
        self.integration = MaoSkillIntegrationV2(
            enable_cache=enable_cache,
            enable_monitoring=enable_monitoring
        )
        
        # 测试用例
        self.test_cases = self._create_test_cases()
        
        # 测试结果
        self.results = {}
    
    def _create_test_cases(self) -> List[Dict[str, Any]]:
        """创建测试用例"""
        return [
            # 简单命令测试
            {
                'name': '帮助命令',
                'command': '/mao help',
                'description': '测试帮助命令响应',
                'expected_success': True,
                'category': 'simple'
            },
            {
                'name': '智能分析简单问题',
                'command': '/mao 分析团队协作',
                'description': '测试智能分析简单问题',
                'expected_success': True,
                'category': 'analysis'
            },
            {
                'name': '指定方法分析',
                'command': '/mao analyze --method=矛盾 分析公司矛盾',
                'description': '测试指定矛盾分析方法',
                'expected_success': True,
                'category': 'analysis'
            },
            {
                'name': '学习命令',
                'command': '/mao learn --path=入门',
                'description': '测试学习路径查询',
                'expected_success': True,
                'category': 'learning'
            },
            {
                'name': '概念查询',
                'command': '/mao concepts 矛盾',
                'description': '测试概念查询',
                'expected_success': True,
                'category': 'knowledge'
            },
            {
                'name': '老命令兼容性',
                'command': '/mao-analyze 矛盾 分析问题',
                'description': '测试老命令向后兼容',
                'expected_success': True,
                'category': 'compatibility'
            },
            {
                'name': '复杂问题分析',
                'command': '/mao 分析如何改进公司管理流程和团队协作，解决部门之间的矛盾问题',
                'description': '测试复杂问题分析',
                'expected_success': True,
                'category': 'complex'
            },
            {
                'name': '错误命令处理',
                'command': '/mao unknown-command',
                'description': '测试错误命令处理',
                'expected_success': False,
                'category': 'error'
            }
        ]
    
    def run_single_test(self, test_case: Dict[str, Any], warmup: bool = False) -> Dict[str, Any]:
        """
        运行单个测试用例
        
        Args:
            test_case: 测试用例
            warmup: 是否为预热测试
            
        Returns:
            测试结果
        """
        command = test_case['command']
        name = test_case['name']
        
        # 记录开始时间
        start_time = time.time()
        
        try:
            # 执行命令
            response = self.integration.process_command(command)
            
            # 计算处理时间
            processing_time = time.time() - start_time
            
            # 判断是否成功（简单判断：包含错误标记或空响应为失败）
            success = '❌' not in response and len(response) > 0
            
            # 验证预期结果
            expected_success = test_case['expected_success']
            success_match = success == expected_success
            
            result = {
                'name': name,
                'command': command,
                'success': success,
                'expected_success': expected_success,
                'success_match': success_match,
                'processing_time': processing_time,
                'response_length': len(response),
                'response_preview': response[:200] + '...' if len(response) > 200 else response,
                'timestamp': datetime.now().isoformat(),
                'warmup': warmup
            }
            
            if not warmup:
                print(f"  ✓ {name}: {processing_time:.3f}s ({'成功' if success else '失败'})")
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            
            result = {
                'name': name,
                'command': command,
                'success': False,
                'expected_success': test_case['expected_success'],
                'success_match': False,
                'processing_time': processing_time,
                'error': error_msg,
                'timestamp': datetime.now().isoformat(),
                'warmup': warmup
            }
            
            if not warmup:
                print(f"  ✗ {name}: {processing_time:.3f}s (异常: {error_msg})")
            
            return result
    
    def run_batch_tests(self, iterations: int = 10, warmup_iterations: int = 3) -> Dict[str, Any]:
        """
        运行批量测试
        
        Args:
            iterations: 正式测试迭代次数
            warmup_iterations: 预热迭代次数
            
        Returns:
            批量测试结果
        """
        print(f"🧪 开始性能基准测试")
        print(f"   测试用例: {len(self.test_cases)}个")
        print(f"   预热迭代: {warmup_iterations}次")
        print(f"   正式迭代: {iterations}次")
        print("=" * 60)
        
        # 预热（不记录结果）
        if warmup_iterations > 0:
            print("🔧 预热阶段...")
            for i in range(warmup_iterations):
                for test_case in self.test_cases:
                    self.run_single_test(test_case, warmup=True)
        
        # 正式测试
        print(f"\n🚀 正式测试阶段 (迭代{iterations}次)...")
        
        all_results = []
        category_stats = {}
        
        for i in range(iterations):
            print(f"\n迭代 {i+1}/{iterations}:")
            iteration_results = []
            
            for test_case in self.test_cases:
                result = self.run_single_test(test_case, warmup=False)
                iteration_results.append(result)
                
                # 按类别统计
                category = test_case['category']
                if category not in category_stats:
                    category_stats[category] = {
                        'times': [],
                        'success_count': 0,
                        'total_count': 0
                    }
                
                cat_stat = category_stats[category]
                cat_stat['times'].append(result['processing_time'])
                cat_stat['total_count'] += 1
                if result['success']:
                    cat_stat['success_count'] += 1
            
            all_results.append(iteration_results)
        
        # 计算总体统计
        overall_stats = self._calculate_overall_stats(all_results, category_stats)
        
        # 保存结果
        self.results = {
            'test_cases': self.test_cases,
            'iterations': iterations,
            'warmup_iterations': warmup_iterations,
            'overall_stats': overall_stats,
            'category_stats': category_stats,
            'timestamp': datetime.now().isoformat(),
            'integration_version': self.integration.version,
            'integration_architecture': self.integration.architecture
        }
        
        # 打印报告
        self._print_report(overall_stats)
        
        return self.results
    
    def run_concurrency_test(self, concurrent_users: int = 10, requests_per_user: int = 5) -> Dict[str, Any]:
        """
        运行并发测试
        
        Args:
            concurrent_users: 并发用户数
            requests_per_user: 每个用户的请求数
            
        Returns:
            并发测试结果
        """
        print(f"\n⚡ 开始并发压力测试")
        print(f"   并发用户数: {concurrent_users}")
        print(f"   每用户请求数: {requests_per_user}")
        print(f"   总请求数: {concurrent_users * requests_per_user}")
        print("=" * 60)
        
        # 选择几个代表性的测试用例
        representative_cases = [
            tc for tc in self.test_cases 
            if tc['category'] in ['analysis', 'simple', 'learning']
        ][:3]  # 取前3个
        
        if not representative_cases:
            representative_cases = self.test_cases[:3]
        
        test_commands = [case['command'] for case in representative_cases]
        
        def worker(user_id: int) -> List[Dict[str, Any]]:
            """工作线程"""
            results = []
            for i in range(requests_per_user):
                # 轮询使用不同的命令
                command = test_commands[i % len(test_commands)]
                
                start_time = time.time()
                try:
                    response = self.integration.process_command(command, user_id=f"user_{user_id}")
                    success = '❌' not in response and len(response) > 0
                except Exception as e:
                    success = False
                    response = str(e)
                
                processing_time = time.time() - start_time
                
                results.append({
                    'user_id': user_id,
                    'request_id': i,
                    'command': command,
                    'success': success,
                    'processing_time': processing_time,
                    'response_length': len(response)
                })
            
            return results
        
        # 执行并发测试
        start_time = time.time()
        all_results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # 提交任务
            future_to_user = {
                executor.submit(worker, user_id): user_id 
                for user_id in range(concurrent_users)
            }
            
            # 收集结果
            for future in concurrent.futures.as_completed(future_to_user):
                user_id = future_to_user[future]
                try:
                    user_results = future.result()
                    all_results.extend(user_results)
                except Exception as e:
                    print(f"用户{user_id}测试异常: {e}")
        
        total_time = time.time() - start_time
        total_requests = len(all_results)
        
        # 计算并发测试统计
        processing_times = [r['processing_time'] for r in all_results]
        success_count = sum(1 for r in all_results if r['success'])
        
        concurrency_stats = {
            'concurrent_users': concurrent_users,
            'requests_per_user': requests_per_user,
            'total_requests': total_requests,
            'total_time': total_time,
            'requests_per_second': total_requests / total_time if total_time > 0 else 0,
            'success_rate': success_count / total_requests * 100 if total_requests > 0 else 0,
            'avg_processing_time': statistics.mean(processing_times) if processing_times else 0,
            'min_processing_time': min(processing_times) if processing_times else 0,
            'max_processing_time': max(processing_times) if processing_times else 0,
            'p95_processing_time': self._percentile(processing_times, 95) if processing_times else 0,
            'results_sample': all_results[:10]  # 取样前10个结果
        }
        
        # 打印并发测试报告
        print(f"\n📊 并发测试结果:")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   请求速率: {concurrency_stats['requests_per_second']:.1f} 请求/秒")
        print(f"   成功率: {concurrency_stats['success_rate']:.1f}%")
        print(f"   平均响应时间: {concurrency_stats['avg_processing_time']*1000:.1f}毫秒")
        print(f"   最大响应时间: {concurrency_stats['max_processing_time']*1000:.1f}毫秒")
        print(f"   P95响应时间: {concurrency_stats['p95_processing_time']*1000:.1f}毫秒")
        
        return concurrency_stats
    
    def run_cache_test(self) -> Dict[str, Any]:
        """运行缓存效果测试"""
        print(f"\n💾 开始缓存效果测试")
        print("=" * 60)
        
        # 选择几个测试用例
        test_cases = [
            {'name': '重复查询1', 'command': '/mao concepts 矛盾'},
            {'name': '重复查询2', 'command': '/mao help'},
            {'name': '重复查询3', 'command': '/mao 分析团队协作'}
        ]
        
        cache_results = {}
        
        for test_case in test_cases:
            name = test_case['name']
            command = test_case['command']
            
            print(f"\n测试: {name} ({command})")
            
            # 第一次查询（冷缓存）
            start_time = time.time()
            response1 = self.integration.process_command(command)
            time1 = time.time() - start_time
            
            # 第二次查询（热缓存）
            start_time = time.time()
            response2 = self.integration.process_command(command)
            time2 = time.time() - start_time
            
            # 检查缓存命中
            cache_hit = time2 < time1 * 0.8  # 如果第二次快20%以上，认为缓存命中
            
            improvement = ((time1 - time2) / time1 * 100) if time1 > 0 else 0
            
            cache_results[name] = {
                'first_query_time': time1,
                'second_query_time': time2,
                'cache_hit': cache_hit,
                'improvement_percent': improvement,
                'response_same': response1 == response2
            }
            
            print(f"  第一次: {time1:.3f}s")
            print(f"  第二次: {time2:.3f}s")
            print(f"  提升: {improvement:.1f}% {'(缓存命中)' if cache_hit else '(缓存未命中或效果不明显)'}")
        
        # 计算平均缓存效果
        improvements = [r['improvement_percent'] for r in cache_results.values()]
        avg_improvement = statistics.mean(improvements) if improvements else 0
        
        cache_stats = {
            'cache_results': cache_results,
            'avg_improvement': avg_improvement,
            'cache_effective': avg_improvement > 20  # 平均提升20%以上认为缓存有效
        }
        
        print(f"\n📊 缓存效果总结:")
        print(f"   平均提升: {avg_improvement:.1f}%")
        print(f"   缓存效果: {'良好' if cache_stats['cache_effective'] else '一般'}")
        
        return cache_stats
    
    def _calculate_overall_stats(self, all_results: List[List[Dict]], category_stats: Dict) -> Dict[str, Any]:
        """计算总体统计"""
        # 扁平化所有结果
        flat_results = []
        for iteration_results in all_results:
            flat_results.extend(iteration_results)
        
        if not flat_results:
            return {}
        
        # 处理时间统计
        processing_times = [r['processing_time'] for r in flat_results]
        
        # 成功率统计
        success_count = sum(1 for r in flat_results if r['success'])
        total_count = len(flat_results)
        
        # 按类别成功率
        category_success_rates = {}
        for category, stats in category_stats.items():
            if stats['total_count'] > 0:
                success_rate = stats['success_count'] / stats['total_count'] * 100
                avg_time = statistics.mean(stats['times']) if stats['times'] else 0
                category_success_rates[category] = {
                    'success_rate': success_rate,
                    'avg_time': avg_time,
                    'count': stats['total_count']
                }
        
        return {
            'total_tests': total_count,
            'success_count': success_count,
            'success_rate': success_count / total_count * 100,
            'avg_processing_time': statistics.mean(processing_times),
            'min_processing_time': min(processing_times),
            'max_processing_time': max(processing_times),
            'p95_processing_time': self._percentile(processing_times, 95),
            'p99_processing_time': self._percentile(processing_times, 99),
            'category_success_rates': category_success_rates,
            'timestamp': datetime.now().isoformat()
        }
    
    def _print_report(self, overall_stats: Dict[str, Any]):
        """打印测试报告"""
        print("\n" + "=" * 60)
        print("📈 性能基准测试报告")
        print("=" * 60)
        
        print(f"\n📊 总体统计:")
        print(f"   测试总数: {overall_stats['total_tests']}")
        print(f"   成功率: {overall_stats['success_rate']:.1f}%")
        print(f"   平均响应时间: {overall_stats['avg_processing_time']*1000:.1f}ms")
        print(f"   最小响应时间: {overall_stats['min_processing_time']*1000:.1f}ms")
        print(f"   最大响应时间: {overall_stats['max_processing_time']*1000:.1f}ms")
        print(f"   P95响应时间: {overall_stats['p95_processing_time']*1000:.1f}ms")
        print(f"   P99响应时间: {overall_stats['p99_processing_time']*1000:.1f}ms")
        
        print(f"\n📋 按类别统计:")
        for category, rates in overall_stats.get('category_success_rates', {}).items():
            print(f"   {category}: {rates['success_rate']:.1f}% ({rates['avg_time']*1000:.1f}ms)")
        
        # 性能评估
        avg_time_ms = overall_stats['avg_processing_time'] * 1000
        if avg_time_ms < 500:
            performance_grade = "优秀 🏆"
        elif avg_time_ms < 1000:
            performance_grade = "良好 👍"
        elif avg_time_ms < 2000:
            performance_grade = "一般 ⚠️"
        else:
            performance_grade = "待改进 🐌"
        
        print(f"\n🎯 性能评估: {performance_grade}")
        print(f"   标准: <500ms优秀, <1000ms良好, <2000ms一般")
        
        print("\n" + "=" * 60)
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """计算百分位数"""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = (len(sorted_data) - 1) * percentile / 100
        lower = int(index)
        upper = lower + 1
        
        if upper >= len(sorted_data):
            return sorted_data[lower]
        
        weight = index - lower
        return sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
    
    def save_results(self, filename: str = None):
        """保存测试结果"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_benchmark_{timestamp}.json"
        
        results_with_data = {
            'benchmark_results': self.results,
            'integration_stats': self.integration.get_stats() if hasattr(self.integration, 'get_stats') else {}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_with_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 测试结果已保存到: {filename}")
        return filename


# 主测试程序
if __name__ == "__main__":
    print("🚀 毛泽东.skill 六层架构性能基准测试")
    print("版本: 1.2.0 (六层架构版)")
    print("=" * 60)
    
    try:
        # 创建性能测试器
        benchmark = PerformanceBenchmark(enable_cache=True, enable_monitoring=True)
        
        # 1. 运行批量测试
        print("\n阶段1: 批量功能测试")
        batch_results = benchmark.run_batch_tests(iterations=5, warmup_iterations=2)
        
        # 2. 运行并发测试
        print("\n阶段2: 并发压力测试")
        concurrency_results = benchmark.run_concurrency_test(concurrent_users=5, requests_per_user=3)
        
        # 3. 运行缓存测试
        print("\n阶段3: 缓存效果测试")
        cache_results = benchmark.run_cache_test()
        
        # 4. 获取系统统计
        print("\n阶段4: 系统统计收集")
        system_stats = benchmark.integration.get_stats() if hasattr(benchmark.integration, 'get_stats') else {}
        
        # 整合所有结果
        comprehensive_results = {
            'batch_results': batch_results,
            'concurrency_results': concurrency_results,
            'cache_results': cache_results,
            'system_stats': system_stats,
            'test_timestamp': datetime.now().isoformat(),
            'test_version': '1.0'
        }
        
        # 保存完整结果
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"performance_comprehensive_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 所有测试完成!")
        print(f"📁 完整结果已保存到: {output_file}")
        
        # 生成简要报告
        print("\n" + "=" * 60)
        print("📋 测试总结报告")
        print("=" * 60)
        
        avg_time = batch_results['overall_stats']['avg_processing_time'] * 1000
        success_rate = batch_results['overall_stats']['success_rate']
        rps = concurrency_results['requests_per_second']
        cache_improvement = cache_results['avg_improvement']
        
        print(f"📊 核心指标:")
        print(f"   平均响应时间: {avg_time:.1f}ms")
        print(f"   功能成功率: {success_rate:.1f}%")
        print(f"   并发处理能力: {rps:.1f} 请求/秒")
        print(f"   缓存提升效果: {cache_improvement:.1f}%")
        
        # 总体评估
        print(f"\n🎯 总体评估:")
        
        if avg_time < 1000 and success_rate > 95 and rps > 5:
            print("   ✅ 性能优秀 - 六层架构运行良好")
        elif avg_time < 2000 and success_rate > 90 and rps > 2:
            print("   ⚠️  性能良好 - 可满足基本使用需求")
        else:
            print("   ❌ 性能待优化 - 需要进一步调优")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试执行异常: {e}")
        import traceback
        traceback.print_exc()