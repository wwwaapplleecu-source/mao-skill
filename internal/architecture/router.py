#!/usr/bin/env python3
"""
六层认知架构路由器

实现毛泽东.skill的六层认知架构路由机制，统一处理所有请求，
支持智能路由、性能监控、缓存和错误处理。
"""

import time
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import threading

class SixLayerRouter:
    """六层架构路由器"""
    
    def __init__(self, enable_cache=True, enable_monitoring=True):
        """初始化路由器"""
        # 初始化各层实例
        self.layers = {
            'gateway': GatewayLayer(),
            'analytics': AnalyticsLayer(),
            'method': MethodLayer(),
            'knowledge': KnowledgeLayer()
        }
        
        # 初始化中间件
        self.middlewares = []
        if enable_monitoring:
            self.middlewares.append(PerformanceMonitoringMiddleware())
        
        if enable_cache:
            self.middlewares.append(CachingMiddleware())
        
        self.middlewares.append(ErrorHandlingMiddleware())
        self.middlewares.append(LoggingMiddleware())
        
        # 请求统计
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0,
            'requests_by_layer': defaultdict(int)
        }
        
        # 性能监控
        self.performance_monitor = PerformanceMonitor() if enable_monitoring else None
        
        # 缓存
        self.cache = SmartCache() if enable_cache else None
        
        # 线程安全锁
        self.lock = threading.Lock()
    
    def process_request(self, raw_input: str, user_id: str = "default_user", **kwargs) -> Dict[str, Any]:
        """
        处理请求的完整流程
        
        Args:
            raw_input: 用户原始输入
            user_id: 用户ID
            **kwargs: 其他参数
            
        Returns:
            处理结果字典
        """
        # 生成请求ID
        request_id = self._generate_request_id()
        
        # 构建标准请求格式
        request = {
            'request_id': request_id,
            'raw_input': raw_input,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'metadata': kwargs
        }
        
        # 记录开始时间
        start_time = time.time()
        
        # 更新统计
        with self.lock:
            self.stats['total_requests'] += 1
        
        # 应用中间件（预处理）
        processed_request = request
        for middleware in self.middlewares:
            processed_request = middleware.pre_process(processed_request)
        
        try:
            # 1. 网关层处理 - 请求验证和预处理
            with self.performance_monitor.measure_time('gateway_layer') if self.performance_monitor else nullcontext():
                gateway_result = self.layers['gateway'].process(processed_request)
            
            # 更新层统计
            with self.lock:
                self.stats['requests_by_layer']['gateway'] += 1
            
            # 2. 路由决策 - 确定目标处理层
            target_layer = self._route_to_layer(gateway_result)
            
            # 3. 目标层处理
            if target_layer == 'analytics':
                with self.performance_monitor.measure_time('analytics_layer') if self.performance_monitor else nullcontext():
                    result = self.layers['analytics'].process(gateway_result)
                with self.lock:
                    self.stats['requests_by_layer']['analytics'] += 1
                    
            elif target_layer == 'method':
                with self.performance_monitor.measure_time('method_layer') if self.performance_monitor else nullcontext():
                    result = self.layers['method'].process(gateway_result)
                with self.lock:
                    self.stats['requests_by_layer']['method'] += 1
                    
            elif target_layer == 'knowledge':
                with self.performance_monitor.measure_time('knowledge_layer') if self.performance_monitor else nullcontext():
                    result = self.layers['knowledge'].process(gateway_result)
                with self.lock:
                    self.stats['requests_by_layer']['knowledge'] += 1
                    
            else:
                # 默认路由到分析层
                with self.performance_monitor.measure_time('analytics_layer') if self.performance_monitor else nullcontext():
                    result = self.layers['analytics'].process(gateway_result)
                with self.lock:
                    self.stats['requests_by_layer']['analytics'] += 1
            
            # 4. 结果格式化
            formatted_result = self._format_result(result, request)
            
            # 添加性能信息
            elapsed_time = time.time() - start_time
            formatted_result['performance'] = {
                'total_processing_time': elapsed_time,
                'gateway_time': gateway_result.get('processing_time', 0),
                'target_layer_time': result.get('processing_time', 0),
                'cache_hit': processed_request.get('cache_hit', False)
            }
            
            # 应用中间件（后处理）
            final_result = formatted_result
            for middleware in self.middlewares:
                final_result = middleware.post_process(final_result)
            
            # 更新成功统计
            with self.lock:
                self.stats['successful_requests'] += 1
                # 更新平均响应时间（移动平均）
                old_avg = self.stats['average_response_time']
                total_success = self.stats['successful_requests']
                self.stats['average_response_time'] = (old_avg * (total_success - 1) + elapsed_time) / total_success
            
            return final_result
            
        except Exception as e:
            # 错误处理
            with self.lock:
                self.stats['failed_requests'] += 1
            
            error_result = self._handle_error(e, request)
            return error_result
    
    def _route_to_layer(self, gateway_result: Dict[str, Any]) -> str:
        """
        路由决策逻辑
        
        Args:
            gateway_result: 网关层处理结果
            
        Returns:
            目标层名称
        """
        command = gateway_result.get('command', '')
        
        # 基于命令的路由决策
        if command == 'analyze':
            # 如果有指定方法，路由到方法层
            if gateway_result.get('method'):
                return 'method'
            else:
                # 需要智能推荐，路由到分析层
                return 'analytics'
                
        elif command in ['learn', 'concepts', 'compare']:
            return 'knowledge'
            
        elif command == 'settings':
            return 'gateway'  # 设置由网关层直接处理
            
        elif command == 'help':
            # 帮助信息由知识层提供
            if gateway_result.get('topic'):
                return 'knowledge'
            else:
                return 'gateway'
                
        else:
            # 快捷命令或未知命令，默认路由到分析层
            return 'analytics'
    
    def _format_result(self, result: Dict[str, Any], original_request: Dict[str, Any]) -> Dict[str, Any]:
        """格式化最终结果"""
        formatted = {
            'request_id': original_request['request_id'],
            'success': True,
            'response': result.get('response', ''),
            'metadata': {
                'user_id': original_request['user_id'],
                'timestamp': original_request['timestamp'],
                'processing_steps': result.get('processing_steps', []),
                'command': result.get('command', ''),
                'method_used': result.get('method_used', ''),
                'confidence': result.get('confidence', 1.0)
            },
            'errors': []
        }
        
        # 添加额外信息
        if 'concepts_used' in result:
            formatted['metadata']['concepts_used'] = result['concepts_used']
        
        if 'learning_progress' in result:
            formatted['metadata']['learning_progress'] = result['learning_progress']
        
        return formatted
    
    def _handle_error(self, error: Exception, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理错误"""
        error_type = type(error).__name__
        error_message = str(error)
        
        # 构建错误响应
        error_response = {
            'request_id': request['request_id'],
            'success': False,
            'response': f"❌ 处理请求时发生错误: {error_type}\n\n{error_message}",
            'metadata': {
                'user_id': request['user_id'],
                'timestamp': request['timestamp'],
                'error_type': error_type,
                'error_message': error_message
            },
            'errors': [{
                'error_code': 'ROUTER_001',
                'error_type': error_type,
                'error_message': error_message,
                'suggested_fix': '请检查输入格式或稍后重试'
            }]
        }
        
        return error_response
    
    def _generate_request_id(self) -> str:
        """生成请求ID"""
        timestamp = int(time.time() * 1000)
        random_part = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        return f"req_{timestamp}_{random_part}"
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取路由器统计信息"""
        with self.lock:
            stats_copy = self.stats.copy()
            
            # 计算成功率
            total = stats_copy['total_requests']
            successful = stats_copy['successful_requests']
            stats_copy['success_rate'] = successful / total if total > 0 else 0
            
            # 添加缓存命中率
            if self.cache:
                stats_copy['cache_hit_rate'] = self.cache.hit_rate()
            
            return stats_copy
    
    def reset_statistics(self):
        """重置统计信息"""
        with self.lock:
            self.stats = {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'average_response_time': 0.0,
                'requests_by_layer': defaultdict(int)
            }
            
            if self.cache:
                self.cache.reset_stats()
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'components': {}
        }
        
        # 检查各层健康状态
        for layer_name, layer_instance in self.layers.items():
            try:
                layer_health = layer_instance.health_check()
                health_status['components'][layer_name] = layer_health
            except Exception as e:
                health_status['components'][layer_name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        # 检查中间件健康状态
        for i, middleware in enumerate(self.middlewares):
            try:
                middleware_health = middleware.health_check()
                health_status['components'][f'middleware_{i}'] = middleware_health
            except Exception as e:
                health_status['components'][f'middleware_{i}'] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        # 如果有不健康的组件，整体状态为不健康
        unhealthy_components = [
            name for name, status in health_status['components'].items()
            if status.get('status') == 'unhealthy'
        ]
        
        if unhealthy_components:
            health_status['status'] = 'unhealthy'
            health_status['unhealthy_components'] = unhealthy_components
        
        return health_status

# ============================================================================
# 各层实现（简化版本，实际应用中应该单独文件）
# ============================================================================

class GatewayLayer:
    """网关层"""
    
    def __init__(self):
        pass
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        start_time = time.time()
        
        raw_input = request['raw_input']
        
        # 简单的命令解析（实际应该使用完整的命令解析器）
        if raw_input.startswith('/'):
            parts = raw_input.lstrip('/').split(maxsplit=1)
            if len(parts) > 0:
                if parts[0] == 'mao' and len(parts) > 1:
                    # 解析 /mao 命令
                    subparts = parts[1].split(maxsplit=1)
                    if len(subparts) > 0:
                        command = subparts[0]
                        question = subparts[1] if len(subparts) > 1 else ''
                    else:
                        command = 'help'
                        question = ''
                else:
                    command = parts[0]
                    question = parts[1] if len(parts) > 1 else ''
            else:
                command = 'help'
                question = ''
        else:
            # 快捷方式：直接输入问题
            command = 'analyze'
            question = raw_input
        
        result = {
            'command': command,
            'question': question,
            'user_id': request['user_id'],
            'processing_time': time.time() - start_time
        }
        
        # 解析选项（简化）
        if '--method=' in raw_input:
            import re
            match = re.search(r'--method=([^\s]+)', raw_input)
            if match:
                result['method'] = match.group(1)
        
        if '--path=' in raw_input:
            import re
            match = re.search(r'--path=([^\s]+)', raw_input)
            if match:
                result['path'] = match.group(1)
        
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            'status': 'healthy',
            'component': 'GatewayLayer',
            'timestamp': datetime.now().isoformat()
        }

class AnalyticsLayer:
    """分析决策层"""
    
    def __init__(self):
        # 尝试导入智能推荐器
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))
            from smart_recommender import SmartRecommender
            self.recommender = SmartRecommender()
            self.has_recommender = True
        except Exception:
            self.has_recommender = False
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理分析请求"""
        start_time = time.time()
        
        question = request.get('question', '')
        
        if self.has_recommender:
            # 使用智能推荐器
            method, confidence, keywords = self.recommender.recommend(question)
            
            result = {
                'method_used': method,
                'confidence': confidence,
                'keywords': keywords,
                'processing_steps': ['analytics', 'recommendation'],
                'response': f"🎯 **智能推荐方法**: {method} (置信度: {confidence:.0%})"
            }
        else:
            # 简化版本
            result = {
                'method_used': '综合',
                'confidence': 0.3,
                'keywords': [],
                'processing_steps': ['analytics', 'fallback'],
                'response': "🎯 **智能推荐方法**: 综合分析 (置信度: 30%)"
            }
        
        result['processing_time'] = time.time() - start_time
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            'status': 'healthy' if self.has_recommender else 'degraded',
            'component': 'AnalyticsLayer',
            'has_recommender': self.has_recommender,
            'timestamp': datetime.now().isoformat()
        }

class MethodLayer:
    """方法执行层"""
    
    def __init__(self):
        # 方法知识库
        self.methods = {
            '矛盾': {
                'title': '矛盾分析法',
                'steps': [
                    '1. 识别矛盾：找出问题中的各种矛盾',
                    '2. 区分主次：确定主要矛盾和次要矛盾',
                    '3. 分析关系：分析矛盾双方的对立统一关系',
                    '4. 制定对策：针对主要矛盾制定解决方案'
                ],
                'quote': '事物发展的根本原因，不是在事物的外部而是在事物的内部，在于事物内部的矛盾性。'
            },
            '实践': {
                'title': '实践论方法',
                'steps': [
                    '1. 实践探索：进行小范围实践，获取感性认识',
                    '2. 总结提升：总结经验，形成理性认识',
                    '3. 指导实践：用理性认识指导更大范围的实践',
                    '4. 循环验证：实践-认识-再实践循环，逐步完善'
                ],
                'quote': '实践、认识、再实践、再认识，这种形式，循环往复以至无穷。'
            }
        }
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """执行分析方法"""
        start_time = time.time()
        
        method = request.get('method', '综合')
        question = request.get('question', '')
        
        if method in self.methods:
            method_info = self.methods[method]
            
            response = f"## 🔍 问题分析: {question}\n\n"
            response += f"🎯 **指定分析方法**: {method_info['title']}\n\n"
            response += f"## 📋 {method_info['title']}步骤\n"
            for step in method_info['steps']:
                response += f"{step}\n"
            
            response += f"\n**核心概念**: 根据方法确定\n\n"
            response += f"> *{method_info['quote']}*\n\n"
            
            result = {
                'method_used': method,
                'response': response,
                'concepts_used': ['方法论', method],
                'processing_steps': ['method', 'execution']
            }
        else:
            # 默认综合方法
            response = f"## 🔍 问题分析: {question}\n\n"
            response += "🎯 **智能推荐方法**: 综合分析\n\n"
            response += "## 📋 综合分析步骤\n"
            response += "1. 全面分析：从多个角度分析问题\n"
            response += "2. 方法组合：结合多种分析方法\n"
            response += "3. 综合判断：综合考虑各种因素\n"
            response += "4. 整体解决：制定整体解决方案\n\n"
            response += "**核心概念**: 全面分析, 方法组合, 综合判断, 整体解决\n\n"
            response += "> *我们需要的是热烈而镇定的情绪，紧张而有秩序的工作。*\n"
            
            result = {
                'method_used': '综合',
                'response': response,
                'concepts_used': ['综合', '分析'],
                'processing_steps': ['method', 'fallback']
            }
        
        result['processing_time'] = time.time() - start_time
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            'status': 'healthy',
            'component': 'MethodLayer',
            'methods_available': len(self.methods),
            'timestamp': datetime.now().isoformat()
        }

class KnowledgeLayer:
    """知识检索层"""
    
    def __init__(self):
        pass
    
    def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理知识检索请求"""
        start_time = time.time()
        
        command = request.get('command', '')
        
        if command == 'learn':
            response = "## 🎓 毛泽东方法论学习系统\n\n"
            response += "欢迎使用渐进式毛泽东方法论学习系统！\n\n"
            response += "### 📚 学习路径概览\n\n"
            response += "**入门路径** (15分钟) - 零基础友好\n"
            response += "**基础路径** (1小时) - 系统学习\n"
            response += "**进阶路径** (3小时) - 深度应用\n"
            response += "**专业路径** (10小时) - 理论研究\n\n"
            response += "### 🚀 快速开始\n"
            response += "使用命令: `/mao learn --path=入门`\n"
            
            result = {
                'response': response,
                'learning_progress': 'not_started',
                'processing_steps': ['knowledge', 'learning']
            }
            
        elif command == 'concepts':
            concept = request.get('question', '')
            if concept:
                response = f"## 📚 概念解释: {concept}\n\n"
                response += f"正在完善 {concept} 概念的解释...\n\n"
                response += "💡 您可以查看其他核心概念:\n"
                response += "- `/mao concepts 矛盾`\n"
                response += "- `/mao concepts 实践`\n"
                response += "- `/mao concepts 群众`\n"
            else:
                response = "## 📚 毛泽东核心概念库\n\n"
                response += "**核心概念列表**:\n"
                response += "- 矛盾: 对立统一规律\n"
                response += "- 实践: 实践-认识循环\n"
                response += "- 群众: 从群众中来，到群众中去\n"
                response += "- 战略: 持久战和战略规划\n\n"
                response += "使用命令: `/mao concepts [概念名]` 查看详细解释\n"
            
            result = {
                'response': response,
                'processing_steps': ['knowledge', 'concepts']
            }
            
        else:
            response = "## 📖 知识检索系统\n\n"
            response += "毛泽东.skill 知识检索系统\n\n"
            response += "**可用功能**:\n"
            response += "- 概念查询: `/mao concepts [概念名]`\n"
            response += "- 学习系统: `/mao learn [选项]`\n"
            response += "- 方法比较: `/mao compare [主题1] [主题2]`\n"
            
            result = {
                'response': response,
                'processing_steps': ['knowledge', 'general']
            }
        
        result['processing_time'] = time.time() - start_time
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            'status': 'healthy',
            'component': 'KnowledgeLayer',
            'timestamp': datetime.now().isoformat()
        }

# ============================================================================
# 中间件实现
# ============================================================================

class Middleware:
    """中间件基类"""
    
    def pre_process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """预处理请求"""
        return request
    
    def post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """后处理结果"""
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            'status': 'healthy',
            'component': self.__class__.__name__,
            'timestamp': datetime.now().isoformat()
        }

class PerformanceMonitoringMiddleware(Middleware):
    """性能监控中间件"""
    
    def __init__(self):
        self.request_times = []
    
    def pre_process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """记录请求开始时间"""
        request['_performance_start'] = time.time()
        return request
    
    def post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """记录处理时间"""
        if '_performance_start' in result.get('metadata', {}).get('_original_request', {}):
            start_time = result['metadata']['_original_request']['_performance_start']
            elapsed = time.time() - start_time
            self.request_times.append(elapsed)
            
            # 添加性能信息
            if 'performance' not in result:
                result['performance'] = {}
            result['performance']['middleware_monitored'] = True
            result['performance']['total_time'] = elapsed
        
        return result

class CachingMiddleware(Middleware):
    """缓存中间件"""
    
    def __init__(self, cache_size=100):
        self.cache = {}
        self.cache_size = cache_size
        self.hits = 0
        self.misses = 0
    
    def pre_process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """检查缓存"""
        cache_key = self._generate_cache_key(request)
        
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            # 检查是否过期（简单实现：5分钟有效期）
            if time.time() - cache_entry['timestamp'] < 300:
                self.hits += 1
                request['_cache_hit'] = True
                request['_cached_result'] = cache_entry['result']
            else:
                # 过期删除
                del self.cache[cache_key]
                self.misses += 1
                request['_cache_hit'] = False
        else:
            self.misses += 1
            request['_cache_hit'] = False
        
        return request
    
    def post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """缓存结果"""
        # 获取原始请求
        original_request = result.get('metadata', {}).get('_original_request', {})
        
        if not original_request.get('_cache_hit', False) and result.get('success', False):
            # 只缓存成功的请求
            cache_key = self._generate_cache_key(original_request)
            
            # 如果缓存满了，删除最老的项
            if len(self.cache) >= self.cache_size:
                oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
                del self.cache[oldest_key]
            
            self.cache[cache_key] = {
                'result': result,
                'timestamp': time.time()
            }
        
        # 添加缓存信息
        result['cache_info'] = {
            'hit': original_request.get('_cache_hit', False),
            'hit_rate': self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0,
            'cache_size': len(self.cache)
        }
        
        return result
    
    def _generate_cache_key(self, request: Dict[str, Any]) -> str:
        """生成缓存键"""
        # 基于用户ID和输入内容生成键
        key_data = f"{request.get('user_id', '')}:{request.get('raw_input', '')}"
        return hashlib.md5(key_data.encode()).hexdigest()

class ErrorHandlingMiddleware(Middleware):
    """错误处理中间件"""
    
    def pre_process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """请求验证"""
        # 检查必要字段
        required_fields = ['raw_input', 'user_id']
        for field in required_fields:
            if field not in request:
                raise ValueError(f"缺少必要字段: {field}")
        
        # 验证输入长度
        if len(request['raw_input']) > 1000:
            raise ValueError("输入过长，请控制在1000字符以内")
        
        return request
    
    def post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """结果验证"""
        # 检查结果格式
        if 'success' not in result:
            result['success'] = False
            result['errors'] = [{'error_code': 'MIDDLEWARE_001', 'error_message': '结果格式错误'}]
        
        # 确保有响应内容
        if not result.get('response'):
            result['response'] = "系统处理完成，但未生成响应内容。"
        
        return result

class LoggingMiddleware(Middleware):
    """日志记录中间件"""
    
    def __init__(self, log_file=None):
        self.log_file = log_file
    
    def pre_process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """记录请求日志"""
        log_entry = {
            'type': 'request',
            'request_id': request.get('request_id', 'unknown'),
            'user_id': request.get('user_id', 'unknown'),
            'raw_input': request.get('raw_input', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        self._write_log(log_entry)
        
        # 保存原始请求供后处理使用
        if 'metadata' not in request:
            request['metadata'] = {}
        request['metadata']['_original_request'] = request.copy()
        
        return request
    
    def post_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """记录结果日志"""
        log_entry = {
            'type': 'response',
            'request_id': result.get('request_id', 'unknown'),
            'success': result.get('success', False),
            'processing_time': result.get('performance', {}).get('total_time', 0),
            'timestamp': datetime.now().isoformat()
        }
        
        self._write_log(log_entry)
        
        # 将原始请求添加到结果中
        if 'metadata' not in result:
            result['metadata'] = {}
        
        # 从缓存中恢复原始请求
        original_request = result.get('metadata', {}).get('_original_request', {})
        if original_request:
            result['metadata']['_original_request'] = original_request
        
        return result
    
    def _write_log(self, log_entry: Dict[str, Any]):
        """写入日志"""
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        else:
            # 控制台输出
            print(f"[LOG] {json.dumps(log_entry, ensure_ascii=False)}")

# ============================================================================
# 辅助类
# ============================================================================

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def measure_time(self, operation_name: str):
        """测量操作时间的上下文管理器"""
        class TimerContext:
            def __init__(self, monitor, name):
                self.monitor = monitor
                self.name = name
                self.start_time = None
            
            def __enter__(self):
                self.start_time = time.time()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                elapsed = time.time() - self.start_time
                self.monitor.metrics[f"{self.name}_time"].append(elapsed)
        
        return TimerContext(self, operation_name)
    
    def get_metrics(self) -> Dict[str, Any]:
        """获取性能指标"""
        metrics = {}
        for key, values in self.metrics.items():
            if values:
                metrics[f"{key}_avg"] = sum(values) / len(values)
                metrics[f"{key}_max"] = max(values)
                metrics[f"{key}_min"] = min(values)
                metrics[f"{key}_count"] = len(values)
        
        return metrics

class SmartCache:
    """智能缓存"""
    
    def __init__(self, max_size=100, ttl=300):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl  # 生存时间（秒）
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str):
        """获取缓存值"""
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                self.hits += 1
                return entry['value']
            else:
                # 过期删除
                del self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, key: str, value):
        """设置缓存值"""
        # 如果缓存满了，删除最老的项
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['timestamp'])
            del self.cache[oldest_key]
        
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
    
    def hit_rate(self) -> float:
        """计算命中率"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def reset_stats(self):
        """重置统计"""
        self.hits = 0
        self.misses = 0

class nullcontext:
    """空上下文管理器（用于性能监控可选）"""
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# ============================================================================
# 测试和示例
# ============================================================================

def test_router():
    """测试路由器"""
    print("🔍 测试六层认知架构路由器\n")
    print("=" * 70)
    
    router = SixLayerRouter(enable_cache=True, enable_monitoring=True)
    
    test_cases = [
        "/mao 分析公司部门协作问题",
        "/mao analyze --method=矛盾 分析团队冲突",
        "/mao learn",
        "/mao concepts 矛盾",
        "/mao help",
        "直接输入问题测试",
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📋 测试 {i}: `{test_input}`")
        print("-" * 40)
        
        result = router.process_request(test_input)
        
        # 显示关键信息
        print(f"成功: {result.get('success', False)}")
        print(f"响应长度: {len(result.get('response', ''))} 字符")
        
        if 'performance' in result:
            perf = result['performance']
            print(f"处理时间: {perf.get('total_processing_time', 0):.3f} 秒")
        
        if 'cache_info' in result:
            cache = result['cache_info']
            print(f"缓存命中: {cache.get('hit', False)}")
        
        # 显示响应前几行
        response = result.get('response', '')
        lines = response.split('\n')
        for line in lines[:3]:
            print(line)
        
        if len(lines) > 3:
            print("...")
        
        print("-" * 40)
    
    # 显示统计信息
    print("\n📊 路由器统计信息:")
    stats = router.get_statistics()
    for key, value in stats.items():
        if isinstance(value, (int, float)):
            if 'time' in key:
                print(f"  {key}: {value:.3f}")
            elif 'rate' in key:
                print(f"  {key}: {value:.2%}")
            else:
                print(f"  {key}: {value}")
    
    # 健康检查
    print("\n🩺 健康检查:")
    health = router.health_check()
    print(f"  状态: {health['status']}")
    for comp_name, comp_status in health['components'].items():
        print(f"  {comp_name}: {comp_status.get('status', 'unknown')}")
    
    print("\n" + "=" * 70)
    print("✅ 路由器测试完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="六层认知架构路由器")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--command", help="处理单个命令")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--health", action="store_true", help="健康检查")
    parser.add_argument("--reset", action="store_true", help="重置统计")
    
    args = parser.parse_args()
    
    router = SixLayerRouter()
    
    if args.test:
        test_router()
    elif args.command:
        result = router.process_request(args.command)
        print(result.get('response', ''))
        print(f"\n[请求ID: {result.get('request_id', 'unknown')}]")
        print(f"[处理时间: {result.get('performance', {}).get('total_processing_time', 0):.3f}秒]")
    elif args.stats:
        stats = router.get_statistics()
        print("📊 路由器统计信息:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    elif args.health:
        health = router.health_check()
        print("🩺 路由器健康状态:")
        print(f"  整体状态: {health['status']}")
        for comp_name, comp_status in health['components'].items():
            print(f"  {comp_name}: {comp_status}")
    elif args.reset:
        router.reset_statistics()
        print("✅ 统计信息已重置")
    else:
        print("请提供参数或使用 --test 运行测试")
        print("示例: python router.py --command '/mao 分析问题'")

if __name__ == "__main__":
    main()