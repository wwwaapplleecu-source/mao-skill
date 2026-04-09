#!/usr/bin/env python3
"""
毛泽东.skill 命令解析器

实现主命令+子命令架构的解析逻辑，支持智能分析和向后兼容
"""

import re
from typing import Dict, List, Optional, Any
from collections import defaultdict

class MaoCommandParser:
    """毛泽东.skill命令解析器"""
    
    def __init__(self):
        """初始化命令解析器"""
        # 命令定义
        self.commands = {
            'help': {
                'description': '获取帮助和智能引导',
                'subcommands': {
                    '': '获取总体帮助',
                    'analyze': '分析方法帮助',
                    'learn': '学习系统帮助',
                    'concepts': '概念系统帮助',
                    'compare': '比较系统帮助',
                    'settings': '设置系统帮助',
                    'version': '版本信息'
                }
            },
            'analyze': {
                'description': '毛泽东方法论智能分析',
                'options': {
                    '--method': '指定分析方法（矛盾/实践/调查/战略/群众/综合）',
                    '--style': '指定风格（work/persona）'
                }
            },
            'learn': {
                'description': '毛泽东方法论渐进式学习',
                'subcommands': {
                    '': '开始学习（智能推荐路径）',
                    'progress': '查看学习进度',
                    'recommendations': '获取学习推荐',
                    'start': '开始新的学习路径',
                    'next': '继续下一个学习模块',
                    'complete': '完成当前学习模块',
                    '矛盾论': '学习矛盾论专题',
                    '实践论': '学习实践论专题',
                    '战略思维': '学习战略思维专题',
                    '群众路线': '学习群众路线专题'
                },
                'options': {
                    '--path': '指定学习路径（入门/基础/进阶/专业）'
                }
            },
            'concepts': {
                'description': '毛泽东概念查询和学习',
                'subcommands': {
                    '': '查看核心概念列表',
                    '[概念]': '查看概念详细解释'
                },
                'options': {
                    '--search': '搜索相关概念'
                }
            },
            'compare': {
                'description': '方法论比较和分析',
                'subcommands': {
                    '': '查看比较系统介绍',
                    '[主题1] [主题2]': '比较两个主题'
                }
            },
            'settings': {
                'description': '个性化设置',
                'subcommands': {
                    '': '查看当前设置',
                    '[选项]': '修改设置'
                }
            }
        }
        
        # 向后兼容映射
        self.legacy_commands = {
            'mao-work': {'new': 'analyze', 'options': {'style': 'work'}},
            'mao-persona': {'new': 'analyze', 'options': {'style': 'persona'}},
            'mao-analyze': {'new': 'analyze', 'special': True},  # 特殊处理
            'mao-concepts': {'new': 'concepts'},
            'mao-examples': {'new': 'learn', 'subcommand': 'examples'},
            'mao-help': {'new': 'help'},
            'mao-version': {'new': 'help', 'subcommand': 'version'}
        }
        
        # 支持的分析方法
        self.supported_methods = ['矛盾', '实践', '调查', '战略', '群众', '综合']
        
        # 支持的学习路径
        self.supported_paths = ['入门', '基础', '进阶', '专业']
        
        # 学习命令的特殊子命令
        self.learn_special_subcommands = ['progress', 'recommendations', 'start', 'next', 'complete']
        
    def parse(self, command_text: str) -> Dict[str, Any]:
        """
        解析命令文本
        
        Args:
            command_text: 完整的命令文本，如 "/mao analyze --method=矛盾 分析问题"
            
        Returns:
            解析后的命令结构字典
        """
        # 1. 清理和准备
        command_text = command_text.strip()
        
        # 2. 去除斜杠，分割命令
        parts = command_text.lstrip('/').split()
        if not parts:
            return self._error_result('空命令')
        
        # 3. 检查是否为老命令
        if parts[0] in self.legacy_commands:
            return self._parse_legacy_command(parts)
        
        # 4. 主命令必须是'mao'
        if parts[0] != 'mao':
            return self._error_result(f'无效主命令: {parts[0]}')
        
        # 5. 如果没有其他部分，默认显示帮助
        if len(parts) == 1:
            return {
                'command': 'help',
                'subcommand': '',
                'legacy': False
            }
        
        # 6. 检查第二个部分是否为已知子命令
        subcommand = parts[1]
        known_subcommands = ['help', 'analyze', 'learn', 'concepts', 'compare', 'settings']
        
        if subcommand in known_subcommands:
            # 是已知子命令，按子命令类型解析
            if subcommand == 'analyze':
                return self._parse_analyze(parts[2:])
            elif subcommand == 'help':
                return self._parse_help(parts[2:])
            elif subcommand == 'learn':
                return self._parse_learn(parts[2:])
            elif subcommand == 'concepts':
                return self._parse_concepts(parts[2:])
            elif subcommand == 'compare':
                return self._parse_compare(parts[2:])
            elif subcommand == 'settings':
                return self._parse_settings(parts[2:])
        else:
            # 不是已知子命令，视为快捷命令：/mao [问题]
            question = ' '.join(parts[1:])
            return {
                'command': 'analyze',
                'subcommand': '',
                'question': question,
                'method': 'auto',
                'is_shortcut': True,
                'legacy': False
            }
    
    def _parse_legacy_command(self, parts: List[str]) -> Dict[str, Any]:
        """解析老命令"""
        legacy_cmd = parts[0]
        legacy_info = self.legacy_commands[legacy_cmd]
        
        if legacy_cmd == 'mao-analyze':
            # 特殊处理mao-analyze
            if len(parts) < 3:
                return self._error_result('mao-analyze命令格式: /mao-analyze 方法 问题')
            
            method = parts[1]
            if method not in self.supported_methods:
                return self._error_result(f'不支持的分析方法: {method}')
            
            question = ' '.join(parts[2:])
            return {
                'command': 'analyze',
                'subcommand': '',
                'question': question,
                'method': method,
                'legacy': True,
                'legacy_command': legacy_cmd,
                'suggested_new': f'/mao analyze --method={method} {question}'
            }
        
        # 其他老命令
        result = {
            'command': legacy_info['new'],
            'legacy': True,
            'legacy_command': legacy_cmd
        }
        
        # 添加选项
        if 'options' in legacy_info:
            result.update(legacy_info['options'])
        
        # 添加子命令
        if 'subcommand' in legacy_info:
            result['subcommand'] = legacy_info['subcommand']
        else:
            result['subcommand'] = ''
        
        # 如果有问题参数
        if len(parts) > 1 and legacy_cmd in ['mao-work', 'mao-persona']:
            result['question'] = ' '.join(parts[1:])
        
        # 生成建议的新命令
        if legacy_cmd in ['mao-work', 'mao-persona'] and 'question' in result:
            style = 'work' if legacy_cmd == 'mao-work' else 'persona'
            result['suggested_new'] = f"/mao analyze --style={style} {result['question']}"
        
        return result
    
    def _parse_analyze(self, args: List[str]) -> Dict[str, Any]:
        """解析分析命令"""
        result = {
            'command': 'analyze',
            'subcommand': '',
            'method': 'auto',  # 默认智能选择
            'style': 'default',
            'question': None
        }
        
        # 解析参数
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg.startswith('--'):
                # 解析选项参数
                if '=' in arg:
                    key, value = arg[2:].split('=', 1)
                else:
                    if i + 1 < len(args) and not args[i + 1].startswith('--'):
                        key = arg[2:]
                        value = args[i + 1]
                        i += 1
                    else:
                        key = arg[2:]
                        value = True
                
                if key == 'method':
                    if value not in self.supported_methods:
                        return self._error_result(f'不支持的分析方法: {value}')
                    result['method'] = value
                elif key == 'style':
                    if value not in ['work', 'persona', 'default']:
                        return self._error_result(f'不支持的风格: {value}')
                    result['style'] = value
                else:
                    return self._error_result(f'未知选项: --{key}')
            else:
                # 问题文本
                result['question'] = ' '.join(args[i:])
                break
            
            i += 1
        
        if not result['question']:
            return self._error_result('分析命令需要问题参数')
        
        return result
    
    def _parse_help(self, args: List[str]) -> Dict[str, Any]:
        """解析帮助命令"""
        result = {
            'command': 'help',
            'subcommand': '',
            'topic': None
        }
        
        if args:
            result['subcommand'] = args[0]
            result['topic'] = ' '.join(args)
        
        return result
    
    def _parse_learn(self, args: List[str]) -> Dict[str, Any]:
        """解析学习命令"""
        result = {
            'command': 'learn',
            'subcommand': '',
            'path': 'auto',  # 默认智能推荐
            'topic': None,
            'special_action': None  # progress, recommendations, start, next, complete
        }
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg.startswith('--'):
                if '=' in arg:
                    key, value = arg[2:].split('=', 1)
                else:
                    if i + 1 < len(args) and not args[i + 1].startswith('--'):
                        key = arg[2:]
                        value = args[i + 1]
                        i += 1
                    else:
                        key = arg[2:]
                        value = True
                
                if key == 'path':
                    if value not in self.supported_paths:
                        return self._error_result(f'不支持的学习路径: {value}')
                    result['path'] = value
                else:
                    return self._error_result(f'未知选项: --{key}')
            else:
                # 学习子命令或主题
                result['subcommand'] = arg
                
                # 检查是否为特殊子命令
                if arg in self.learn_special_subcommands:
                    result['special_action'] = arg
                    result['topic'] = None
                else:
                    # 普通学习主题
                    result['topic'] = ' '.join(args[i:])
                
                break
            
            i += 1
        
        return result
    
    def _parse_concepts(self, args: List[str]) -> Dict[str, Any]:
        """解析概念命令"""
        result = {
            'command': 'concepts',
            'subcommand': '',
            'search': None,
            'concept': None
        }
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg.startswith('--'):
                if '=' in arg:
                    key, value = arg[2:].split('=', 1)
                else:
                    if i + 1 < len(args) and not args[i + 1].startswith('--'):
                        key = arg[2:]
                        value = args[i + 1]
                        i += 1
                    else:
                        key = arg[2:]
                        value = True
                
                if key == 'search':
                    result['search'] = value
                else:
                    return self._error_result(f'未知选项: --{key}')
            else:
                # 概念名称
                result['subcommand'] = arg
                result['concept'] = ' '.join(args[i:])
                break
            
            i += 1
        
        return result
    
    def _parse_compare(self, args: List[str]) -> Dict[str, Any]:
        """解析比较命令"""
        result = {
            'command': 'compare',
            'subcommand': '',
            'topic1': None,
            'topic2': None
        }
        
        if len(args) >= 2:
            result['subcommand'] = f'{args[0]} {args[1]}'
            result['topic1'] = args[0]
            result['topic2'] = args[1]
        elif args:
            result['subcommand'] = args[0]
            result['topic1'] = args[0]
        
        return result
    
    def _parse_settings(self, args: List[str]) -> Dict[str, Any]:
        """解析设置命令"""
        result = {
            'command': 'settings',
            'subcommand': '',
            'setting_key': None,
            'setting_value': None
        }
        
        if args:
            result['subcommand'] = args[0]
            if '=' in args[0]:
                key, value = args[0].split('=', 1)
                result['setting_key'] = key
                result['setting_value'] = value
            else:
                result['setting_key'] = args[0]
        
        return result
    
    def _error_result(self, error_message: str) -> Dict[str, Any]:
        """生成错误结果"""
        return {
            'error': True,
            'message': error_message,
            'suggestion': '使用 /mao help 获取帮助'
        }
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """格式化解析结果（用于调试）"""
        if result.get('error'):
            return f"❌ 错误: {result['message']}\n💡 建议: {result['suggestion']}"
        
        output = f"✅ 命令解析成功\n"
        output += f"📋 命令: {result['command']}\n"
        
        if 'subcommand' in result and result['subcommand']:
            output += f"📝 子命令: {result['subcommand']}\n"
        
        # 显示特定字段
        fields_to_show = ['question', 'method', 'style', 'path', 'search', 'topic', 
                         'topic1', 'topic2', 'setting_key', 'setting_value']
        
        for field in fields_to_show:
            if field in result and result[field]:
                output += f"🔧 {field}: {result[field]}\n"
        
        if result.get('legacy'):
            output += f"⚠️ 这是老命令: {result['legacy_command']}\n"
            if 'suggested_new' in result:
                output += f"🔄 建议使用新命令: {result['suggested_new']}\n"
        
        if result.get('is_shortcut'):
            output += f"⚡ 这是快捷命令\n"
        
        return output
    
    def get_help_text(self, command: str = None) -> str:
        """获取帮助文本"""
        if not command:
            # 总体帮助
            help_text = "## 🚀 毛泽东.skill 命令帮助\n\n"
            help_text += "### 核心命令架构\n\n"
            
            for cmd, info in self.commands.items():
                help_text += f"**/{cmd}** - {info['description']}\n"
            
            help_text += "\n### 快捷命令\n"
            help_text += "**/mao [问题]** - 智能分析快捷方式\n\n"
            
            help_text += "### 详细使用\n"
            help_text += "使用 `/mao help [主题]` 获取详细帮助，如：\n"
            help_text += "- `/mao help analyze` - 分析方法帮助\n"
            help_text += "- `/mao help learn` - 学习系统帮助\n"
            
            help_text += "\n### 向后兼容\n"
            help_text += "老命令继续支持，但建议使用新命令：\n"
            for legacy, info in self.legacy_commands.items():
                if 'suggested_new' not in info:
                    continue
                help_text += f"- `/{legacy}` → `/{info['suggested_new']}`\n"
            
            return help_text
        
        # 特定命令帮助
        if command not in self.commands:
            return f"❌ 未知命令: {command}"
        
        info = self.commands[command]
        help_text = f"## 📖 {command} 命令帮助\n\n"
        help_text += f"{info['description']}\n\n"
        
        if 'subcommands' in info:
            help_text += "### 子命令\n"
            for subcmd, desc in info['subcommands'].items():
                if subcmd:
                    help_text += f"- `{subcmd}` - {desc}\n"
                else:
                    help_text += f"- (默认) - {desc}\n"
        
        if 'options' in info:
            help_text += "\n### 选项\n"
            for opt, desc in info['options'].items():
                help_text += f"- `{opt}` - {desc}\n"
        
        # 添加示例
        help_text += "\n### 使用示例\n"
        if command == 'analyze':
            help_text += "- `/mao analyze 分析市场竞争格局` - 智能分析\n"
            help_text += "- `/mao analyze --method=矛盾 识别团队问题` - 指定方法\n"
            help_text += "- `/mao analyze --style=work 制定工作计划` - 纯方法论\n"
        elif command == 'learn':
            help_text += "- `/mao learn` - 开始学习\n"
            help_text += "- `/mao learn 矛盾论` - 学习矛盾论\n"
            help_text += "- `/mao learn --path=入门` - 入门学习路径\n"
        elif command == 'concepts':
            help_text += "- `/mao concepts` - 查看概念列表\n"
            help_text += "- `/mao concepts 矛盾` - 查看矛盾概念\n"
            help_text += "- `/mao concepts --search=群众` - 搜索相关概念\n"
        
        return help_text

def test_parser():
    """测试命令解析器"""
    parser = MaoCommandParser()
    
    test_commands = [
        # 新命令架构
        "/mao 分析公司部门协作问题",
        "/mao help",
        "/mao help analyze",
        "/mao analyze --method=矛盾 分析团队冲突",
        "/mao analyze --style=work 制定项目计划",
        "/mao learn",
        "/mao learn --path=入门",
        "/mao concepts",
        "/mao concepts 矛盾",
        "/mao concepts --search=群众",
        "/mao compare 毛泽东 邓小平",
        "/mao settings",
        "/mao settings 详细程度=高",
        
        # 老命令（向后兼容）
        "/mao-work 分析商业案例",
        "/mao-persona 写动员讲话",
        "/mao-analyze 矛盾 公司内部问题",
        "/mao-concepts",
        "/mao-help",
        
        # 错误命令
        "/mao unknown",
        "/mao analyze --method=错误方法 问题",
    ]
    
    print("🔍 命令解析器测试\n")
    print("=" * 60)
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n测试 {i}: {cmd}")
        print("-" * 40)
        
        result = parser.parse(cmd)
        print(parser.format_result(result))
        
        # 如果是help命令，显示帮助文本
        if not result.get('error') and result['command'] == 'help' and i <= 3:
            help_text = parser.get_help_text(result.get('subcommand', ''))
            print("\n帮助文本预览（前5行）:")
            for line in help_text.split('\n')[:5]:
                print(line)
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东.skill命令解析器")
    parser.add_argument("--command", help="需要解析的命令")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--help-cmd", help="获取命令帮助")
    
    args = parser.parse_args()
    
    cmd_parser = MaoCommandParser()
    
    if args.test:
        test_parser()
    elif args.help_cmd:
        help_text = cmd_parser.get_help_text(args.help_cmd)
        print(help_text)
    elif args.command:
        result = cmd_parser.parse(args.command)
        print(cmd_parser.format_result(result))
    else:
        print("请提供命令或使用 --test 运行测试")
        print("示例: python command_parser.py --command '/mao analyze 分析问题'")

if __name__ == "__main__":
    main()