#!/usr/bin/env python3
"""
六层架构集成系统

将六层认知架构的各层组件集成，提供统一的毛泽东.skill接口。
"""

import sys
import os
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# 添加路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入各层组件
from command_parser import MaoCommandParser
from analytics_layer import AnalyticsLayer
from method_executor import MethodExecutor
from knowledge_retriever import KnowledgeRetriever

class SixLayerIntegration:
    """六层架构集成系统"""
    
    def __init__(self, enable_cache=True, enable_monitoring=True):
        """初始化六层集成系统"""
        # 初始化各层实例
        self.ui_layer = MaoCommandParser()  # 用户界面层
        self.analytics_layer = AnalyticsLayer()  # 分析决策层
        self.method_layer = MethodExecutor()  # 方法执行层
        self.knowledge_layer = KnowledgeRetriever()  # 知识检索层
        
        # 配置
        self.enable_cache = enable_cache
        self.enable_monitoring = enable_monitoring
        
        # 简单缓存（生产环境应使用更复杂的缓存机制）
        self.cache = {}
        self.cache_ttl = 300  # 5分钟TTL
        
        # 性能监控
        self.monitoring_data = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0,
            'request_times': []
        }
        
        # 向后兼容性支持
        self.legacy_command_mapping = {
            'mao-work': {'new': 'analyze', 'options': {}},
            'mao-persona': {'new': 'analyze', 'options': {'style': 'persona'}},
            'mao-analyze': {'new': 'analyze', 'special': True},
            'mao-concepts': {'new': 'concepts'},
            'mao-examples': {'new': 'learn', 'subcommand': 'examples'},
            'mao-help': {'new': 'help'},
            'mao-version': {'new': 'help', 'subcommand': 'version'}
        }
    
    def process_command(self, command_text: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        处理用户命令（六层架构完整流程）
        
        Args:
            command_text: 用户输入的命令文本
            user_id: 用户ID
            
        Returns:
            处理结果
        """
        start_time = time.time()
        
        # 更新统计
        self.monitoring_data['total_requests'] += 1
        
        try:
            # 检查缓存
            cache_key = f"{user_id}:{command_text}"
            if self.enable_cache and cache_key in self.cache:
                cache_entry = self.cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                    # 使用缓存
                    response = cache_entry['response'].copy()
                    response['cached'] = True
                    response['cache_age'] = time.time() - cache_entry['timestamp']
                    
                    # 更新监控
                    processing_time = time.time() - start_time
                    self._update_monitoring(True, processing_time)
                    
                    return response
            
            # 1. UI层：解析命令
            ui_start = time.time()
            parsed_command = self.ui_layer.parse(command_text)
            ui_time = time.time() - ui_start
            
            # 处理错误
            if parsed_command.get('error'):
                response = self._format_error_response(parsed_command)
                self._update_monitoring(False, time.time() - start_time)
                return response
            
            # 2. 向后兼容处理
            legacy_notice = ""
            if parsed_command.get('legacy'):
                legacy_notice = self._handle_legacy_command(parsed_command)
                # 更新解析后的命令
                if parsed_command.get('suggested_new'):
                    # 可以选择重新解析或直接使用建议的新命令
                    pass
            
            # 3. 根据命令类型路由处理
            command_type = parsed_command.get('command', 'analyze')
            
            # 记录各层处理时间
            layer_times = {'ui': ui_time}
            
            # 路由到相应的处理流程
            if command_type == 'analyze':
                result = self._process_analyze(parsed_command, user_id, layer_times)
            elif command_type == 'learn':
                result = self._process_learn(parsed_command, user_id, layer_times)
            elif command_type == 'concepts':
                result = self._process_concepts(parsed_command, user_id, layer_times)
            elif command_type == 'help':
                result = self._process_help(parsed_command, user_id, layer_times)
            elif command_type == 'compare':
                result = self._process_compare(parsed_command, user_id, layer_times)
            elif command_type == 'settings':
                result = self._process_settings(parsed_command, user_id, layer_times)
            else:
                result = self._process_unknown_command(parsed_command, layer_times)
            
            # 4. 格式化响应
            response = self._format_response(result, parsed_command, legacy_notice, layer_times)
            
            # 5. 更新缓存
            if self.enable_cache and result.get('success', False):
                self.cache[cache_key] = {
                    'response': response,
                    'timestamp': time.time(),
                    'user_id': user_id
                }
                # 清理过期缓存（简单实现）
                self._cleanup_cache()
            
            # 6. 更新监控
            total_time = time.time() - start_time
            self._update_monitoring(result.get('success', False), total_time)
            
            # 添加性能数据
            if self.enable_monitoring:
                response['performance'] = {
                    'total_time': total_time,
                    'layer_times': layer_times,
                    'cache_hit': False  # 这次不是缓存命中
                }
            
            return response
            
        except Exception as e:
            # 异常处理
            error_response = self._format_exception_response(e, command_text)
            self._update_monitoring(False, time.time() - start_time)
            return error_response
    
    def _process_analyze(self, parsed_command: Dict[str, Any], user_id: str, layer_times: Dict[str, float]) -> Dict[str, Any]:
        """处理分析命令"""
        # 获取问题和方法
        problem = parsed_command.get('topic', '')
        specified_method = parsed_command.get('method')
        
        # 1. 分析决策层：智能推荐
        analytics_start = time.time()
        if specified_method:
            # 用户指定了方法
            analytics_result = self.analytics_layer.recommend_specific_method(problem, specified_method)
        else:
            # 智能推荐
            analytics_result = self.analytics_layer.analyze_problem(problem, user_id)
        layer_times['analytics'] = time.time() - analytics_start
        
        if not analytics_result.get('success', False):
            return analytics_result
        
        # 2. 方法执行层：执行分析
        method_start = time.time()
        if specified_method:
            method_to_use = specified_method
        else:
            method_to_use = analytics_result['recommendations']['primary']['method']
        
        method_result = self.method_layer.execute_method(method_to_use, problem)
        layer_times['method'] = time.time() - method_start
        
        if not method_result.get('success', False):
            return method_result
        
        # 3. 知识检索层：获取相关概念和学习建议
        knowledge_start = time.time()
        # 获取推荐的学习内容
        if specified_method:
            learn_recommendation = {'path': specified_method + '专题'}
        else:
            learn_recommendation = analytics_result.get('suggested_action', {}).get('learn', '入门')
        
        # 获取相关概念
        related_concepts = []
        if 'recommended_next_step' in method_result:
            next_step = method_result['recommended_next_step']
            if 'concepts' in next_step:
                for concept_name in next_step['concepts'][:3]:  # 取前3个
                    concept_info = self.knowledge_layer.get_concept_info(concept_name)
                    if concept_info.get('success'):
                        related_concepts.append(concept_info.get('concept', {}))
        
        layer_times['knowledge'] = time.time() - knowledge_start
        
        # 组合结果
        return {
            'success': True,
            'command': 'analyze',
            'problem': problem,
            'method_used': method_to_use,
            'analytics_result': analytics_result,
            'method_result': method_result,
            'related_concepts': related_concepts,
            'learn_recommendation': learn_recommendation,
            'confidence': analytics_result.get('recommendations', {}).get('confidence', 0.0)
        }
    
    def _process_learn(self, parsed_command: Dict[str, Any], user_id: str, layer_times: Dict[str, float]) -> Dict[str, Any]:
        """处理学习命令"""
        subcommand = parsed_command.get('subcommand', '')
        topic = parsed_command.get('topic', '')
        path = parsed_command.get('path', 'auto')
        
        knowledge_start = time.time()
        
        if subcommand == 'progress':
            # 获取学习进度
            result = self.knowledge_layer.get_user_progress(user_id, path if path != 'auto' else None)
        elif subcommand == 'recommendations':
            # 获取学习推荐
            result = self.knowledge_layer.get_learning_path()
        elif subcommand in ['start', 'next', 'complete']:
            # 开始/继续/完成学习
            if path == 'auto':
                # 自动推荐路径
                paths = self.knowledge_layer.get_learning_path()
                recommended = paths.get('recommended_path', {}).get('path', '入门')
                path = recommended
            
            if topic:
                # 学习特定主题
                result = {
                    'success': True,
                    'command': 'learn',
                    'subcommand': subcommand,
                    'topic': topic,
                    'path': path,
                    'message': f"开始学习{topic}主题"
                }
            else:
                # 获取学习路径信息
                result = self.knowledge_layer.get_learning_path(path)
                
                if result.get('success') and subcommand == 'start':
                    # 记录开始学习
                    self.knowledge_layer.update_user_progress(user_id, path, '开始学习')
        else:
            # 普通学习命令
            if topic:
                # 学习特定主题
                result = {
                    'success': True,
                    'command': 'learn',
                    'topic': topic,
                    'message': f"学习{topic}相关内容"
                }
            else:
                # 获取学习路径信息
                if path == 'auto':
                    result = self.knowledge_layer.get_learning_path()
                else:
                    result = self.knowledge_layer.get_learning_path(path)
        
        layer_times['knowledge'] = time.time() - knowledge_start
        
        return result
    
    def _process_concepts(self, parsed_command: Dict[str, Any], user_id: str, layer_times: Dict[str, float]) -> Dict[str, Any]:
        """处理概念查询命令"""
        topic = parsed_command.get('topic', '')
        search_term = parsed_command.get('search', '')
        
        knowledge_start = time.time()
        
        if topic:
            # 查询特定概念
            result = self.knowledge_layer.get_concept_info(topic)
        elif search_term:
            # 搜索概念
            result = self.knowledge_layer.get_concept_info(search_term=search_term)
        else:
            # 获取所有概念
            result = self.knowledge_layer.get_concept_info()
        
        layer_times['knowledge'] = time.time() - knowledge_start
        
        return result
    
    def _process_help(self, parsed_command: Dict[str, Any], user_id: str, layer_times: Dict[str, float]) -> Dict[str, Any]:
        """处理帮助命令"""
        subcommand = parsed_command.get('subcommand', '')
        topic = parsed_command.get('topic', '')
        
        help_content = self._generate_help_content(subcommand, topic)
        
        return {
            'success': True,
            'command': 'help',
            'subcommand': subcommand,
            'topic': topic,
            'content': help_content
        }
    
    def _process_compare(self, parsed_command: Dict[str, Any], user_id: str, layer_times: Dict[str, float]) -> Dict[str, Any]:
        """处理方法比较命令"""
        topic = parsed_command.get('topic', '')
        
        if not topic:
            return {
                'success': True,
                'command': 'compare',
                'content': self._generate_compare_help()
            }
        
        # 这里可以实现具体的比较逻辑
        # 目前返回简单响应
        return {
            'success': True,
            'command': 'compare',
            'topic': topic,
            'content': f"## 🔄 方法比较\n\n即将推出{topic}的比较分析功能..."
        }
    
    def _process_settings(self, parsed_command: Dict[str, Any], user_id: str, layer_times: Dict[str, float]) -> Dict[str, Any]:
        """处理设置命令"""
        # 设置功能待实现
        return {
            'success': True,
            'command': 'settings',
            'message': '设置功能开发中...'
        }
    
    def _process_unknown_command(self, parsed_command: Dict[str, Any], layer_times: Dict[str, float]) -> Dict[str, Any]:
        """处理未知命令"""
        return {
            'success': False,
            'error': '未知的命令类型',
            'parsed_command': parsed_command,
            'suggestion': '请使用 /mao help 查看可用命令'
        }
    
    def _handle_legacy_command(self, parsed_command: Dict[str, Any]) -> str:
        """处理向后兼容命令"""
        legacy_command = parsed_command.get('legacy_command', '')
        suggested_new = parsed_command.get('suggested_new', '')
        
        notice = f"⚠️ 您使用的是老命令 `{legacy_command}`\n"
        if suggested_new:
            notice += f"🔄 建议使用新命令: `{suggested_new}`\n\n"
        
        return notice
    
    def _format_response(self, result: Dict[str, Any], parsed_command: Dict[str, Any], 
                        legacy_notice: str, layer_times: Dict[str, float]) -> Dict[str, Any]:
        """格式化响应"""
        if not result.get('success', False):
            return result
        
        # 构建响应文本
        response_text = legacy_notice
        
        command_type = parsed_command.get('command', '')
        
        if command_type == 'analyze':
            response_text += self._format_analyze_response(result)
        elif command_type == 'learn':
            response_text += self._format_learn_response(result)
        elif command_type == 'concepts':
            response_text += self._format_concepts_response(result)
        elif command_type == 'help':
            response_text += result.get('content', '')
        elif command_type == 'compare':
            response_text += result.get('content', '')
        elif command_type == 'settings':
            response_text += result.get('message', '')
        else:
            response_text += json.dumps(result, ensure_ascii=False, indent=2)
        
        # 构建完整响应
        response = {
            'success': True,
            'response': response_text,
            'raw_result': result,
            'parsed_command': parsed_command,
            'legacy_notice': bool(legacy_notice),
            'layer_times': layer_times
        }
        
        return response
    
    def _format_analyze_response(self, result: Dict[str, Any]) -> str:
        """格式化分析响应"""
        method_result = result.get('method_result', {})
        analytics_result = result.get('analytics_result', {})
        
        if not method_result.get('success'):
            return f"❌ 分析失败: {method_result.get('error', '未知错误')}"
        
        # 获取分析内容
        analysis = method_result.get('analysis', '')
        
        # 添加智能推荐信息
        if analytics_result.get('success'):
            recommendations = analytics_result.get('recommendations', {})
            if 'primary' in recommendations:
                primary = recommendations['primary']
                confidence = recommendations.get('confidence', 0.0)
                
                # 在分析内容前添加推荐信息
                recommendation_header = f"## 🎯 智能推荐\n\n"
                recommendation_header += f"**推荐方法**: {primary['method']} (置信度: {confidence*100:.1f}%)\n\n"
                
                if primary.get('reason'):
                    recommendation_header += f"**推荐理由**: {primary['reason']}\n\n"
                
                analysis = recommendation_header + analysis
        
        # 添加相关概念
        related_concepts = result.get('related_concepts', [])
        if related_concepts:
            concepts_section = "\n\n## 📚 相关概念\n\n"
            for concept in related_concepts[:3]:  # 最多显示3个
                name = concept.get('name', '')
                description = concept.get('description', '')
                if name and description:
                    concepts_section += f"- **{name}**: {description[:100]}...\n"
            analysis += concepts_section
        
        # 添加学习建议
        learn_rec = result.get('learn_recommendation')
        if learn_rec:
            analysis += f"\n\n💡 **学习建议**: 使用 `/mao learn {learn_rec}` 深入学习相关知识"
        
        return analysis
    
    def _format_learn_response(self, result: Dict[str, Any]) -> str:
        """格式化学习响应"""
        if not result.get('success'):
            return f"❌ 学习系统错误: {result.get('error', '未知错误')}"
        
        # 这里可以根据result的具体内容生成响应
        # 目前返回简单响应
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _format_concepts_response(self, result: Dict[str, Any]) -> str:
        """格式化概念查询响应"""
        if not result.get('success'):
            return f"❌ 概念查询失败: {result.get('error', '未知错误')}"
        
        # 这里可以根据result的具体内容生成响应
        # 目前返回简单响应
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    def _format_error_response(self, error_result: Dict[str, Any]) -> Dict[str, Any]:
        """格式化错误响应"""
        return {
            'success': False,
            'response': f"❌ {error_result.get('message', '未知错误')}\n\n💡 {error_result.get('suggestion', '请重试')}",
            'error': error_result
        }
    
    def _format_exception_response(self, exception: Exception, command_text: str) -> Dict[str, Any]:
        """格式化异常响应"""
        error_msg = str(exception)
        return {
            'success': False,
            'response': f"❌ 系统处理异常: {error_msg}\n\n💡 请重试或联系开发者",
            'error': {
                'type': type(exception).__name__,
                'message': error_msg,
                'command': command_text
            }
        }
    
    def _generate_help_content(self, subcommand: str, topic: str) -> str:
        """生成帮助内容"""
        if subcommand == 'version':
            return "毛泽东.skill v1.2.0 - 六层架构版\n发布日期: 2026-04-09"
        
        if topic:
            # 特定主题帮助
            return f"## 📖 {topic}帮助\n\n正在完善{topic}的详细帮助文档..."
        
        # 通用帮助
        help_text = """
# 🆘 毛泽东.skill 帮助文档

## 🚀 核心命令

### 智能分析
```
/mao [问题]                     # 快捷方式：智能分析
/mao analyze [问题]            # 详细分析（支持--method参数）
```

### 学习系统
```
/mao learn                     # 开始学习（智能推荐路径）
/mao learn [主题]              # 学习特定主题
/mao learn --path=[路径]       # 选择学习路径
```

### 概念查询
```
/mao concepts                  # 查看核心概念列表
/mao concepts [概念]           # 查询特定概念
/mao concepts --search=[关键词] # 搜索相关概念
```

### 其他功能
```
/mao help                     # 查看帮助
/mao compare                  # 方法比较
/mao settings                 # 系统设置
```

## 📚 学习路径
- **入门路径** (15分钟)：快速掌握基础
- **基础路径** (1小时)：系统学习核心方法论
- **进阶路径** (3小时)：深度应用
- **专业路径** (10小时)：理论研究

## 🎯 分析方法
支持6种核心分析方法：矛盾、实践、调查、战略、群众、综合

---

💡 **提示**: 更多详细帮助请使用 `/mao help [主题]`
"""
        return help_text
    
    def _generate_compare_help(self) -> str:
        """生成比较帮助"""
        return """
# 🔄 方法比较系统

## 使用方法
```
/mao compare                  # 查看比较系统介绍
/mao compare [主题1] [主题2]  # 比较两个主题
```

## 支持比较的内容
1. **方法论比较**: 矛盾论 vs 实践论
2. **战略比较**: 持久战 vs 速决战
3. **工作方法比较**: 调查研究 vs 群众路线
4. **概念比较**: 任何毛泽东核心概念

## 示例
- `/mao compare 矛盾论 实践论`
- `/mao compare 毛泽东 邓小平`
- `/mao compare 调查研究 群众路线`

---
💡 **提示**: 比较功能正在完善中，即将推出更多详细分析
"""
    
    def _update_monitoring(self, success: bool, processing_time: float):
        """更新监控数据"""
        self.monitoring_data['request_times'].append(processing_time)
        
        if success:
            self.monitoring_data['successful_requests'] += 1
        else:
            self.monitoring_data['failed_requests'] += 1
        
        # 计算平均响应时间（保留最近100次）
        recent_times = self.monitoring_data['request_times'][-100:]
        self.monitoring_data['average_response_time'] = sum(recent_times) / len(recent_times)
    
    def _cleanup_cache(self):
        """清理过期缓存"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time - entry['timestamp'] > self.cache_ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """获取监控统计"""
        return {
            'monitoring_enabled': self.enable_monitoring,
            'cache_enabled': self.enable_cache,
            'cache_size': len(self.cache),
            'stats': self.monitoring_data.copy(),
            'timestamp': datetime.now().isoformat()
        }


# 测试代码
if __name__ == "__main__":
    # 创建集成系统
    integration = SixLayerIntegration(enable_cache=True, enable_monitoring=True)
    
    print("=== 六层架构集成系统测试 ===")
    print("=" * 50)
    
    # 测试1：智能分析
    print("\n1. 测试智能分析:")
    result1 = integration.process_command("/mao 分析公司部门协作矛盾")
    print(f"命令: /mao 分析公司部门协作矛盾")
    print(f"成功: {result1.get('success', False)}")
    if result1.get('success'):
        print("响应长度:", len(result1.get('response', '')))
    
    # 测试2：指定方法分析
    print("\n2. 测试指定方法分析:")
    result2 = integration.process_command("/mao analyze --method=矛盾 分析团队问题")
    print(f"命令: /mao analyze --method=矛盾 分析团队问题")
    print(f"成功: {result2.get('success', False)}")
    
    # 测试3：学习命令
    print("\n3. 测试学习命令:")
    result3 = integration.process_command("/mao learn --path=入门")
    print(f"命令: /mao learn --path=入门")
    print(f"成功: {result3.get('success', False)}")
    
    # 测试4：概念查询
    print("\n4. 测试概念查询:")
    result4 = integration.process_command("/mao concepts 矛盾")
    print(f"命令: /mao concepts 矛盾")
    print(f"成功: {result4.get('success', False)}")
    
    # 测试5：帮助命令
    print("\n5. 测试帮助命令:")
    result5 = integration.process_command("/mao help")
    print(f"命令: /mao help")
    print(f"成功: {result5.get('success', False)}")
    
    # 显示监控数据
    print("\n=== 监控统计数据 ===")
    stats = integration.get_monitoring_stats()
    print(f"总请求数: {stats['stats']['total_requests']}")
    print(f"成功请求: {stats['stats']['successful_requests']}")
    print(f"失败请求: {stats['stats']['failed_requests']}")
    print(f"平均响应时间: {stats['stats']['average_response_time']:.3f}秒")
    print(f"缓存大小: {stats['cache_size']}")