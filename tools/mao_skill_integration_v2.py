#!/usr/bin/env python3
"""
毛泽东.skill 集成系统 V2 - 六层架构版本

基于六层认知架构的现代集成系统，保持向后兼容。
"""

import sys
import os
import time
from typing import Dict, List, Any, Optional

# 添加路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入六层集成系统
from six_layer_integration import SixLayerIntegration
from performance_monitor import PerformanceMonitor

class MaoSkillIntegrationV2:
    """毛泽东.skill集成系统V2 - 六层架构版本"""
    
    def __init__(self, enable_cache=True, enable_monitoring=True):
        """初始化集成系统V2"""
        # 六层集成系统
        self.six_layer = SixLayerIntegration(
            enable_cache=enable_cache,
            enable_monitoring=enable_monitoring
        )
        
        # 性能监控器
        self.monitor = PerformanceMonitor() if enable_monitoring else None
        
        # 向后兼容性映射
        self.compatibility_map = {
            'mao-work': self._handle_mao_work,
            'mao-persona': self._handle_mao_persona,
            'mao-analyze': self._handle_mao_analyze,
            'mao-concepts': self._handle_mao_concepts,
            'mao-examples': self._handle_mao_examples,
            'mao-help': self._handle_mao_help,
            'mao-version': self._handle_mao_version
        }
        
        # 版本信息
        self.version = "1.2.0"
        self.architecture = "six-layer"
        self.release_date = "2026-04-09"
    
    def process_command(self, command_text: str, user_id: str = "default_user") -> str:
        """
        处理用户命令（主入口）
        
        Args:
            command_text: 用户输入的命令文本
            user_id: 用户ID
            
        Returns:
            系统响应文本
        """
        start_time = time.time()
        
        try:
            # 检查是否为老命令
            parsed = self._parse_legacy_command(command_text)
            
            if parsed['is_legacy']:
                # 处理老命令
                result = self._handle_legacy_command(parsed, user_id)
            else:
                # 使用六层架构处理新命令
                result = self.six_layer.process_command(command_text, user_id)
            
            # 记录性能监控
            if self.monitor:
                total_time = time.time() - start_time
                
                # 提取命令类型
                command_type = 'unknown'
                if parsed['is_legacy']:
                    command_type = parsed['legacy_type']
                elif 'parsed_command' in result:
                    command_type = result['parsed_command'].get('command', 'unknown')
                
                # 提取分析方法
                method = None
                if 'method_used' in result:
                    method = result.get('method_used')
                elif parsed['is_legacy'] and parsed['legacy_type'] == 'mao-analyze':
                    method = parsed.get('method')
                
                # 记录请求
                success = result.get('success', False)
                self.monitor.record_request(command_type, method, success, total_time)
            
            # 返回响应文本
            return result.get('response', '')
            
        except Exception as e:
            # 异常处理
            error_msg = str(e)
            
            # 记录失败请求
            if self.monitor:
                self.monitor.record_request('error', None, False, time.time() - start_time)
            
            return f"❌ 系统处理异常: {error_msg}\n\n💡 请重试或联系开发者"
    
    def get_performance_report(self) -> str:
        """获取性能报告"""
        if self.monitor:
            return self.monitor.get_performance_report()
        else:
            return "性能监控未启用"
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = {
            'version': self.version,
            'architecture': self.architecture,
            'release_date': self.release_date,
            'monitoring_enabled': self.monitor is not None
        }
        
        if self.monitor:
            stats.update(self.monitor.get_overall_stats())
        
        return stats
    
    def _parse_legacy_command(self, command_text: str) -> Dict[str, Any]:
        """解析老命令"""
        # 简单的老命令检测
        command_text_lower = command_text.lower().strip()
        
        result = {
            'is_legacy': False,
            'original': command_text,
            'legacy_type': None,
            'method': None,
            'topic': None
        }
        
        # 检查是否为老命令格式
        for legacy_type in self.compatibility_map.keys():
            if command_text_lower.startswith(f"/{legacy_type}"):
                result['is_legacy'] = True
                result['legacy_type'] = legacy_type
                
                # 提取参数
                parts = command_text.split(maxsplit=1)
                if len(parts) > 1:
                    result['topic'] = parts[1]
                    
                    # 对于mao-analyze，提取方法
                    if legacy_type == 'mao-analyze' and len(parts[1].split()) > 1:
                        subparts = parts[1].split(maxsplit=1)
                        result['method'] = subparts[0]
                        result['topic'] = subparts[1] if len(subparts) > 1 else ''
                
                break
        
        return result
    
    def _handle_legacy_command(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理老命令"""
        legacy_type = parsed['legacy_type']
        
        if legacy_type in self.compatibility_map:
            handler = self.compatibility_map[legacy_type]
            return handler(parsed, user_id)
        else:
            return {
                'success': False,
                'response': f"❌ 不支持的老命令: {legacy_type}\n\n💡 请使用新命令架构"
            }
    
    def _handle_mao_work(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理/mao-work命令"""
        topic = parsed.get('topic', '')
        
        if topic:
            # 转换为新命令格式
            new_command = f"/mao analyze {topic}"
            return self.six_layer.process_command(new_command, user_id)
        else:
            return {
                'success': True,
                'response': "## 🛠️ 毛泽东方法论系统\n\n使用 `/mao analyze [问题]` 进行智能分析"
            }
    
    def _handle_mao_persona(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理/mao-persona命令"""
        topic = parsed.get('topic', '')
        
        if topic:
            # 转换为新命令格式（添加persona风格）
            new_command = f"/mao analyze --method=综合 {topic}"
            result = self.six_layer.process_command(new_command, user_id)
            
            # 添加人格风格说明
            if result.get('success'):
                response = result.get('response', '')
                persona_note = "\n\n---\n*（使用毛泽东人格风格分析）*"
                result['response'] = response + persona_note
            
            return result
        else:
            return {
                'success': True,
                'response': "## 🎭 毛泽东人格风格\n\n使用 `/mao-persona [文本]` 获取毛式风格的分析或写作"
            }
    
    def _handle_mao_analyze(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理/mao-analyze命令"""
        method = parsed.get('method')
        topic = parsed.get('topic', '')
        
        if not topic:
            return {
                'success': False,
                'response': "❌ 请提供分析问题\n\n💡 格式: `/mao-analyze [方法] [问题]`"
            }
        
        if method:
            # 转换为新命令格式
            new_command = f"/mao analyze --method={method} {topic}"
        else:
            # 如果没有指定方法，使用智能分析
            new_command = f"/mao analyze {topic}"
        
        result = self.six_layer.process_command(new_command, user_id)
        
        # 添加老命令提示
        if result.get('success'):
            response = result.get('response', '')
            legacy_note = f"\n\n---\nℹ️ 您使用的是老命令 `/mao-analyze`，建议使用新命令 `/mao analyze`"
            result['response'] = response + legacy_note
        
        return result
    
    def _handle_mao_concepts(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理/mao-concepts命令"""
        topic = parsed.get('topic', '')
        
        if topic:
            new_command = f"/mao concepts {topic}"
        else:
            new_command = "/mao concepts"
        
        result = self.six_layer.process_command(new_command, user_id)
        
        # 添加老命令提示
        if result.get('success'):
            response = result.get('response', '')
            legacy_note = f"\n\n---\nℹ️ 您使用的是老命令 `/mao-concepts`，建议使用新命令 `/mao concepts`"
            result['response'] = response + legacy_note
        
        return result
    
    def _handle_mao_examples(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理/mao-examples命令"""
        # 转换为学习命令
        new_command = "/mao learn 示例"
        result = self.six_layer.process_command(new_command, user_id)
        
        # 添加示例内容
        if result.get('success'):
            examples = self._get_examples_content()
            result['response'] = examples
        
        return result
    
    def _handle_mao_help(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理/mao-help命令"""
        # 转换为帮助命令
        new_command = "/mao help"
        result = self.six_layer.process_command(new_command, user_id)
        
        # 添加版本信息
        if result.get('success'):
            response = result.get('response', '')
            version_info = f"\n\n---\n**版本**: {self.version} ({self.architecture})\n**发布日期**: {self.release_date}"
            result['response'] = response + version_info
        
        return result
    
    def _handle_mao_version(self, parsed: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """处理/mao-version命令"""
        return {
            'success': True,
            'response': f"## 📦 毛泽东.skill 版本信息\n\n"
                       f"**版本**: {self.version}\n"
                       f"**架构**: {self.architecture}\n"
                       f"**发布日期**: {self.release_date}\n\n"
                       f"**功能**:\n"
                       f"- ✅ 六层认知架构\n"
                       f"- ✅ 智能分析方法推荐\n"
                       f"- ✅ 四级渐进学习系统\n"
                       f"- ✅ 674+概念查询系统\n"
                       f"- ✅ 性能监控和缓存\n\n"
                       f"💡 使用 `/mao help` 获取详细帮助"
        }
    
    def _get_examples_content(self) -> str:
        """获取示例内容"""
        return """
# 📚 毛泽东.skill 使用示例

## 🎯 分析示例

### 1. 矛盾分析
```
用户: /mao 分析公司销售额下降的问题

响应: 首先要找出主要矛盾。销售额下降是现象，不是本质...
```

### 2. 实践指导
```
用户: /mao 如何改进产品设计流程

响应: 遵循"实践-认识-再实践"循环。首先进行小范围实践...
```

### 3. 战略制定
```
用户: /mao 制定新市场进入战略

响应: 市场进入如用兵，要讲究战略战术。第一阶段（防御）...
```

## 📖 学习示例

### 1. 开始学习
```
/mao learn --path=入门
```

### 2. 学习特定主题
```
/mao learn 矛盾论
```

### 3. 查看学习进度
```
/mao learn progress
```

## 🔍 概念查询示例

### 1. 查询概念
```
/mao concepts 矛盾
```

### 2. 搜索概念
```
/mao concepts --search=群众
```

### 3. 浏览概念
```
/mao concepts
```

---

💡 **提示**: 更多示例请使用 `/mao help` 查看详细文档
"""


# 测试代码
if __name__ == "__main__":
    print("=== 毛泽东.skill V2 测试 ===")
    
    # 创建集成系统
    integration = MaoSkillIntegrationV2(enable_cache=True, enable_monitoring=True)
    
    # 测试1：新命令
    print("\n1. 测试新命令:")
    result1 = integration.process_command("/mao help")
    print(f"命令: /mao help")
    print(f"响应长度: {len(result1)}")
    print(f"前100字符: {result1[:100]}...")
    
    # 测试2：老命令
    print("\n2. 测试老命令:")
    result2 = integration.process_command("/mao-analyze 矛盾 分析团队问题")
    print(f"命令: /mao-analyze 矛盾 分析团队问题")
    print(f"响应长度: {len(result2)}")
    print(f"前100字符: {result2[:100]}...")
    
    # 测试3：性能报告
    print("\n3. 测试性能报告:")
    report = integration.get_performance_report()
    print(f"报告长度: {len(report)}")
    print(f"前200字符:\n{report[:200]}...")
    
    # 测试4：统计信息
    print("\n4. 测试统计信息:")
    stats = integration.get_stats()
    print(f"版本: {stats.get('version')}")
    print(f"架构: {stats.get('architecture')}")
    print(f"总请求数: {stats.get('request_stats', {}).get('total', 0)}")
    
    print("\n=== 测试完成 ===")