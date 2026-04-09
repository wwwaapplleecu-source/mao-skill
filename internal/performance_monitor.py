#!/usr/bin/env python3
"""
性能监控模块

监控六层架构各层的性能指标，提供性能分析和优化建议。
"""

import time
import json
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
import threading

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self, history_size=1000):
        """初始化性能监控器"""
        # 各层性能数据
        self.layer_performance = {
            'ui': deque(maxlen=history_size),      # 用户界面层
            'gateway': deque(maxlen=history_size),  # 网关层
            'analytics': deque(maxlen=history_size), # 分析决策层
            'method': deque(maxlen=history_size),   # 方法执行层
            'knowledge': deque(maxlen=history_size), # 知识检索层
            'storage': deque(maxlen=history_size)   # 数据存储层
        }
        
        # 请求统计
        self.request_stats = {
            'total': 0,
            'success': 0,
            'failure': 0,
            'by_command': defaultdict(int),
            'by_method': defaultdict(int)
        }
        
        # 性能阈值
        self.thresholds = {
            'critical': 5.0,    # 5秒以上为严重
            'warning': 2.0,     # 2-5秒为警告
            'normal': 0.5       # 0.5秒以下为优秀
        }
        
        # 性能问题记录
        self.performance_issues = deque(maxlen=100)
        
        # 线程安全锁
        self.lock = threading.Lock()
        
        # 启动时间
        self.start_time = time.time()
    
    def record_layer_performance(self, layer_name: str, processing_time: float, success: bool = True):
        """
        记录层性能数据
        
        Args:
            layer_name: 层名称
            processing_time: 处理时间（秒）
            success: 是否成功
        """
        with self.lock:
            if layer_name in self.layer_performance:
                self.layer_performance[layer_name].append({
                    'timestamp': time.time(),
                    'processing_time': processing_time,
                    'success': success
                })
            
            # 检查性能问题
            if processing_time > self.thresholds['warning']:
                issue = {
                    'layer': layer_name,
                    'processing_time': processing_time,
                    'threshold': self.thresholds['warning'],
                    'timestamp': datetime.now().isoformat(),
                    'severity': 'critical' if processing_time > self.thresholds['critical'] else 'warning'
                }
                self.performance_issues.append(issue)
    
    def record_request(self, command: str, method: str = None, success: bool = True, total_time: float = 0.0):
        """
        记录请求统计
        
        Args:
            command: 命令类型
            method: 分析方法（如果有）
            success: 是否成功
            total_time: 总处理时间
        """
        with self.lock:
            self.request_stats['total'] += 1
            
            if success:
                self.request_stats['success'] += 1
            else:
                self.request_stats['failure'] += 1
            
            self.request_stats['by_command'][command] += 1
            
            if method:
                self.request_stats['by_method'][method] += 1
            
            # 记录总处理时间
            self.record_layer_performance('total', total_time, success)
    
    def get_layer_stats(self, layer_name: str, recent_n: int = 100) -> Dict[str, Any]:
        """
        获取层性能统计
        
        Args:
            layer_name: 层名称
            recent_n: 最近N条记录
            
        Returns:
            性能统计
        """
        if layer_name not in self.layer_performance:
            return {'error': f'未知的层: {layer_name}'}
        
        with self.lock:
            data = list(self.layer_performance[layer_name])[-recent_n:]
            
            if not data:
                return {
                    'layer': layer_name,
                    'count': 0,
                    'message': '暂无数据'
                }
            
            processing_times = [item['processing_time'] for item in data]
            success_count = sum(1 for item in data if item['success'])
            
            # 计算统计指标
            stats = {
                'layer': layer_name,
                'count': len(data),
                'success_rate': success_count / len(data) * 100,
                'avg_time': statistics.mean(processing_times),
                'min_time': min(processing_times),
                'max_time': max(processing_times),
                'p95_time': self._percentile(processing_times, 95),
                'p99_time': self._percentile(processing_times, 99),
                'recent_n': recent_n
            }
            
            # 性能评估
            stats['performance_grade'] = self._evaluate_performance(stats['avg_time'])
            
            return stats
    
    def get_overall_stats(self) -> Dict[str, Any]:
        """获取总体统计"""
        with self.lock:
            uptime = time.time() - self.start_time
            
            # 各层性能
            layer_stats = {}
            for layer_name in self.layer_performance.keys():
                stats = self.get_layer_stats(layer_name, 100)
                if 'error' not in stats:
                    layer_stats[layer_name] = stats
            
            # 请求统计
            success_rate = 0
            if self.request_stats['total'] > 0:
                success_rate = self.request_stats['success'] / self.request_stats['total'] * 100
            
            # 热门命令
            top_commands = sorted(
                self.request_stats['by_command'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # 热门方法
            top_methods = sorted(
                self.request_stats['by_method'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            # 性能问题统计
            critical_issues = [i for i in self.performance_issues if i['severity'] == 'critical']
            warning_issues = [i for i in self.performance_issues if i['severity'] == 'warning']
            
            return {
                'uptime_seconds': uptime,
                'uptime_human': str(timedelta(seconds=int(uptime))),
                'request_stats': {
                    'total': self.request_stats['total'],
                    'success': self.request_stats['success'],
                    'failure': self.request_stats['failure'],
                    'success_rate': success_rate,
                    'top_commands': top_commands,
                    'top_methods': top_methods
                },
                'layer_stats': layer_stats,
                'performance_issues': {
                    'critical': len(critical_issues),
                    'warning': len(warning_issues),
                    'total': len(self.performance_issues),
                    'recent_issues': list(self.performance_issues)[-5:]  # 最近5个问题
                },
                'thresholds': self.thresholds,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_performance_report(self) -> str:
        """获取性能报告（文本格式）"""
        stats = self.get_overall_stats()
        
        report = "=" * 60 + "\n"
        report += "          毛泽东.skill 性能监控报告\n"
        report += "=" * 60 + "\n\n"
        
        # 运行时间
        report += f"🏃 运行时间: {stats['uptime_human']}\n"
        report += f"📊 总请求数: {stats['request_stats']['total']}\n"
        report += f"✅ 成功请求: {stats['request_stats']['success']}\n"
        report += f"❌ 失败请求: {stats['request_stats']['failure']}\n"
        report += f"🎯 成功率: {stats['request_stats']['success_rate']:.1f}%\n\n"
        
        # 热门命令
        report += "🔥 热门命令:\n"
        for command, count in stats['request_stats']['top_commands']:
            report += f"  - {command}: {count}次\n"
        
        report += "\n"
        
        # 各层性能
        report += "📈 各层性能 (最近100次):\n"
        for layer_name, layer_stats in stats['layer_stats'].items():
            if 'count' in layer_stats and layer_stats['count'] > 0:
                grade = layer_stats.get('performance_grade', 'N/A')
                avg_time = layer_stats.get('avg_time', 0) * 1000  # 转换为毫秒
                report += f"  - {layer_name}: {avg_time:.1f}ms [{grade}]\n"
        
        report += "\n"
        
        # 性能问题
        issues = stats['performance_issues']
        if issues['total'] > 0:
            report += "⚠️  性能问题:\n"
            report += f"  - 严重问题: {issues['critical']}个\n"
            report += f"  - 警告问题: {issues['warning']}个\n"
            report += f"  - 总问题数: {issues['total']}个\n"
            
            if issues['recent_issues']:
                report += "\n  最近问题:\n"
                for issue in issues['recent_issues']:
                    report += f"  - {issue['layer']}: {issue['processing_time']:.2f}s ({issue['severity']})\n"
        
        report += "\n" + "=" * 60 + "\n"
        
        return report
    
    def get_optimization_suggestions(self) -> List[Dict[str, Any]]:
        """获取优化建议"""
        suggestions = []
        stats = self.get_overall_stats()
        
        # 检查各层性能
        for layer_name, layer_stats in stats['layer_stats'].items():
            if 'avg_time' in layer_stats:
                avg_time = layer_stats['avg_time']
                
                if avg_time > self.thresholds['critical']:
                    suggestions.append({
                        'layer': layer_name,
                        'issue': '响应时间过长',
                        'severity': 'critical',
                        'current': f"{avg_time:.3f}s",
                        'threshold': f"{self.thresholds['critical']}s",
                        'suggestion': f'优化{layer_name}层的处理逻辑，考虑添加缓存或并行处理',
                        'priority': '高'
                    })
                elif avg_time > self.thresholds['warning']:
                    suggestions.append({
                        'layer': layer_name,
                        'issue': '响应时间偏长',
                        'severity': 'warning',
                        'current': f"{avg_time:.3f}s",
                        'threshold': f"{self.thresholds['warning']}s",
                        'suggestion': f'监控{layer_name}层性能，考虑代码优化',
                        'priority': '中'
                    })
        
        # 检查成功率
        success_rate = stats['request_stats'].get('success_rate', 100)
        if success_rate < 90:
            suggestions.append({
                'layer': '整体',
                'issue': '成功率偏低',
                'severity': 'warning',
                'current': f"{success_rate:.1f}%",
                'threshold': '90%',
                'suggestion': '检查错误日志，优化错误处理机制',
                'priority': '高'
            })
        
        # 检查热门命令性能
        for layer_name, layer_stats in stats['layer_stats'].items():
            if 'p95_time' in layer_stats and layer_stats['p95_time'] > layer_stats['avg_time'] * 3:
                suggestions.append({
                    'layer': layer_name,
                    'issue': '性能波动较大',
                    'severity': 'warning',
                    'current': f"P95: {layer_stats['p95_time']:.3f}s, 平均: {layer_stats['avg_time']:.3f}s",
                    'threshold': 'P95 < 3倍平均时间',
                    'suggestion': f'检查{layer_name}层的异常情况处理',
                    'priority': '中'
                })
        
        return suggestions
    
    def clear_stats(self):
        """清空统计（谨慎使用）"""
        with self.lock:
            for layer in self.layer_performance.values():
                layer.clear()
            
            self.request_stats = {
                'total': 0,
                'success': 0,
                'failure': 0,
                'by_command': defaultdict(int),
                'by_method': defaultdict(int)
            }
            
            self.performance_issues.clear()
            self.start_time = time.time()
    
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
    
    def _evaluate_performance(self, avg_time: float) -> str:
        """评估性能等级"""
        if avg_time <= self.thresholds['normal']:
            return '优秀'
        elif avg_time <= self.thresholds['warning']:
            return '良好'
        elif avg_time <= self.thresholds['critical']:
            return '警告'
        else:
            return '严重'


# 测试代码
if __name__ == "__main__":
    monitor = PerformanceMonitor()
    
    # 模拟一些性能数据
    print("模拟性能数据...")
    
    # 记录各层性能
    monitor.record_layer_performance('ui', 0.1)
    monitor.record_layer_performance('analytics', 0.3)
    monitor.record_layer_performance('method', 0.2)
    monitor.record_layer_performance('knowledge', 0.15)
    
    # 记录一些较慢的请求
    monitor.record_layer_performance('method', 2.5)  # 警告级别
    monitor.record_layer_performance('knowledge', 6.0)  # 严重级别
    
    # 记录请求统计
    monitor.record_request('analyze', '矛盾', success=True, total_time=0.8)
    monitor.record_request('learn', None, success=True, total_time=0.3)
    monitor.record_request('analyze', '实践', success=False, total_time=0.4)
    
    # 获取统计报告
    print("\n" + monitor.get_performance_report())
    
    # 获取优化建议
    suggestions = monitor.get_optimization_suggestions()
    print("\n优化建议:")
    for suggestion in suggestions:
        print(f"- [{suggestion['priority']}] {suggestion['layer']}: {suggestion['issue']}")
        print(f"  建议: {suggestion['suggestion']}")
    
    # 获取JSON格式的详细统计
    print("\n详细统计 (JSON格式):")
    stats = monitor.get_overall_stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2)[:500] + "...")