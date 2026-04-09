#!/usr/bin/env python3
"""
毛泽东.skill 集成系统原型

将命令解析器与智能推荐器集成，展示新命令架构的工作方式
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from command_parser import MaoCommandParser
from smart_recommender import SmartRecommender
from learning_system import LearningSystem

class MaoSkillIntegration:
    """毛泽东.skill集成系统"""
    
    def __init__(self):
        """初始化集成系统"""
        self.parser = MaoCommandParser()
        self.recommender = SmartRecommender()
        self.learning_system = LearningSystem()
        
        # 模拟的知识库响应
        self.knowledge_base = {
            '矛盾': {
                'title': '矛盾分析法',
                'description': '识别主要矛盾和次要矛盾，分析矛盾转化',
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
                'description': '遵循"实践-认识-再实践"循环，指导具体工作',
                'steps': [
                    '1. 实践探索：进行小范围实践，获取感性认识',
                    '2. 总结提升：总结经验，形成理性认识',
                    '3. 指导实践：用理性认识指导更大范围的实践',
                    '4. 循环验证：实践-认识-再实践循环，逐步完善'
                ],
                'quote': '实践、认识、再实践、再认识，这种形式，循环往复以至无穷。'
            },
            '综合': {
                'title': '综合分析法',
                'description': '多角度综合分析，智能选择合适方法',
                'steps': [
                    '1. 全面分析：从多个角度分析问题',
                    '2. 方法组合：结合多种分析方法',
                    '3. 综合判断：综合考虑各种因素',
                    '4. 整体解决：制定整体解决方案'
                ],
                'quote': '我们需要的是热烈而镇定的情绪，紧张而有秩序的工作。'
            }
        }
    
    def process_command(self, command_text: str) -> str:
        """
        处理命令
        
        Args:
            command_text: 用户输入的命令文本
            
        Returns:
            系统响应文本
        """
        # 1. 解析命令
        parsed = self.parser.parse(command_text)
        
        if parsed.get('error'):
            return f"❌ {parsed['message']}\n\n💡 {parsed['suggestion']}"
        
        # 2. 处理向后兼容提醒
        legacy_notice = ""
        if parsed.get('legacy'):
            legacy_notice = f"⚠️ 您使用的是老命令 `{parsed.get('legacy_command')}`\n"
            if parsed.get('suggested_new'):
                legacy_notice += f"🔄 建议使用新命令: `{parsed['suggested_new']}`\n\n"
        
        # 3. 根据命令类型处理
        command = parsed['command']
        
        if command == 'analyze':
            return legacy_notice + self._process_analyze(parsed)
        elif command == 'help':
            return legacy_notice + self._process_help(parsed)
        elif command == 'learn':
            return legacy_notice + self._process_learn(parsed)
        elif command == 'concepts':
            return legacy_notice + self._process_concepts(parsed)
        elif command == 'compare':
            return legacy_notice + self._process_compare(parsed)
        elif command == 'settings':
            return legacy_notice + self._process_settings(parsed)
        else:
            return f"❌ 未实现的命令: {command}"
    
    def _process_analyze(self, parsed: dict) -> str:
        """处理分析命令"""
        question = parsed.get('question', '')
        method = parsed.get('method', 'auto')
        style = parsed.get('style', 'default')
        
        if not question:
            return "❌ 分析命令需要问题参数\n\n💡 示例: `/mao analyze 分析公司部门协作问题`"
        
        # 智能推荐方法（如果是auto）
        if method == 'auto':
            recommendation = self.recommender.recommend_method(question)
            method = recommendation['recommended_method']
            method_info = f"🎯 **智能推荐方法**: {method}分析 (置信度: {recommendation['confidence']*100:.0f}%)\n\n"
            method_info += f"**推荐理由**: {recommendation['reason']}\n\n"
        else:
            method_info = f"🎯 **指定分析方法**: {method}分析\n\n"
        
        # 获取方法指导
        guidance = self.recommender.get_method_guidance(method)
        
        # 构建响应
        response = f"## 🔍 问题分析: {question}\n\n"
        response += method_info
        
        response += f"## 📋 {method}分析步骤\n\n"
        for step in guidance['steps']:
            response += f"{step}\n"
        
        response += f"\n**核心概念**: {', '.join(guidance['key_concepts'])}\n\n"
        response += f"> *{guidance['mao_quote']}*\n\n"
        
        # 添加风格说明
        if style == 'work':
            response += "📝 **响应风格**: 纯方法论（不包含毛泽东人格风格）\n"
        elif style == 'persona':
            response += "🎭 **响应风格**: 毛泽东人格风格\n"
        
        # 添加建议
        response += "\n---\n"
        response += "💡 **建议**: 如果需要更深入的分析，可以使用:\n"
        response += f"- `/mao analyze --method=实践 {question}` - 实践论角度\n"
        response += f"- `/mao analyze --method=调查 {question}` - 调查研究角度\n"
        response += f"- `/mao learn {method}` - 学习{method}分析方法\n"
        
        return response
    
    def _process_help(self, parsed: dict) -> str:
        """处理帮助命令"""
        topic = parsed.get('subcommand', '')
        return self.parser.get_help_text(topic)
    
    def _process_learn(self, parsed: dict) -> str:
        """处理学习命令"""
        special_action = parsed.get('special_action')
        topic = parsed.get('topic', '')
        path = parsed.get('path', 'auto')
        subcommand = parsed.get('subcommand', '')
        
        # 默认用户ID（实际应用中应该使用真实用户ID）
        user_id = "default_user"
        
        # 处理特殊动作
        if special_action:
            if special_action == 'progress':
                return self.learning_system.format_user_progress(user_id)
            
            elif special_action == 'recommendations':
                recommendations = self.learning_system.get_learning_recommendations(user_id)
                response = "## 💡 学习推荐\n\n"
                
                if not recommendations:
                    response += "暂时没有推荐。建议先开始一个学习路径！\n\n"
                    response += "**推荐命令**: `/mao learn --path=入门`\n"
                else:
                    for rec in recommendations:
                        priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                        response += f"{priority_icon} **{rec['reason']}**\n"
                        if rec['type'] == 'start_path':
                            response += f"   命令: `/mao learn --path={rec['path_id']}`\n"
                        elif rec['type'] == 'topic':
                            response += f"   命令: `/mao learn {rec['topic_id']}`\n"
                        response += "\n"
                
                return response
            
            elif special_action == 'start':
                # 开始学习路径
                if path == 'auto':
                    # 默认推荐入门路径
                    path = '入门'
                
                result = self.learning_system.start_learning_path(user_id, path)
                if 'error' in result:
                    return f"❌ 开始学习路径失败: {result['error']}"
                
                response = f"## 🚀 开始学习: {result['path_name']}\n\n"
                response += f"**总模块数**: {result['total_modules']}个\n\n"
                
                # 显示第一个模块内容
                module = result['module']
                response += self.learning_system.format_module_content(module)
                
                response += "\n\n### 📝 下一步\n"
                response += "完成此模块后，使用: `/mao learn next` 继续学习\n"
                
                return response
            
            elif special_action == 'next':
                # 继续下一个模块
                current_module = self.learning_system.get_current_module(user_id)
                if not current_module:
                    return "❌ 没有正在进行的学习路径。请先开始一个学习路径: `/mao learn --path=入门`"
                
                # 完成当前模块
                result = self.learning_system.complete_current_module(user_id, "")
                if 'error' in result:
                    return f"❌ 完成模块失败: {result['error']}"
                
                response = f"## ✅ 模块完成: {result.get('completed_module', '')}\n\n"
                
                if 'achievement' in result:
                    achievement = result['achievement']
                    response += f"🏆 **成就解锁**: {achievement['name']}\n"
                    response += f"   {achievement['description']}\n"
                    response += f"   🎁 奖励: {achievement['reward']}\n\n"
                
                if 'next_module' in result:
                    next_info = result['next_module']
                    response += f"**下一个模块**: {next_info['title']} ({next_info['index']}/{next_info['total']})\n"
                    response += f"**总体进度**: {result['progress_percentage']}%\n\n"
                    
                    # 获取下一个模块内容
                    next_module = self.learning_system.get_current_module(user_id)
                    if next_module:
                        response += self.learning_system.format_module_content(next_module['module'])
                else:
                    response += "🎉 恭喜！您已完成当前学习路径的所有模块！\n\n"
                    response += "### 🏆 学习成就\n"
                    progress = self.learning_system.get_user_progress(user_id)
                    response += f"**已完成路径**: {progress['achievements_count']}个\n"
                    response += f"**建议下一步**: `/mao learn recommendations`\n"
                
                return response
            
            elif special_action == 'complete':
                # 完成当前模块（带实践回答）
                current_module = self.learning_system.get_current_module(user_id)
                if not current_module:
                    return "❌ 没有正在进行的学习路径。"
                
                # 提取实践问题（如果有）
                practice_question = ""
                module = current_module['module']
                if 'practice_question' in module:
                    practice_question = module['practice_question']
                
                if practice_question:
                    response = "## 📝 完成当前模块\n\n"
                    response += f"**实践问题**: {practice_question}\n\n"
                    response += "💡 请提交您的实践回答，然后使用: `/mao learn next` 继续\n"
                else:
                    response = "✅ 当前模块没有实践问题。使用 `/mao learn next` 继续学习。\n"
                
                return response
        
        # 处理专题学习
        if topic:
            # 检查是否为已知专题
            topic_details = self.learning_system.get_topic_details(topic)
            if topic_details:
                response = f"## 📖 {topic_details['name']}\n\n"
                response += f"**描述**: {topic_details['description']}\n\n"
                
                if 'content' in topic_details:
                    content = topic_details['content']
                    if 'theory' in content:
                        response += "### 理论内容\n"
                        response += f"{content['theory']}\n\n"
                    if 'applications' in content:
                        response += "### 应用场景\n"
                        for app in content['applications']:
                            response += f"- {app}\n"
                        response += "\n"
                    if 'key_concepts' in content:
                        response += "### 核心概念\n"
                        for concept in content['key_concepts']:
                            response += f"- **{concept}**\n"
                
                response += "\n### 🚀 开始学习\n"
                response += f"**前置要求**: {', '.join(topic_details.get('prerequisites', ['无']))}\n"
                response += f"**相关命令**: `/mao learn --path={topic_details.get('prerequisites', ['基础'])[0]}`\n"
                
                return response
            else:
                # 未知专题，使用原来的简单响应
                response = f"## 📖 {topic} 专题学习\n\n"
                response += f"正在开发 {topic} 专题内容...\n\n"
                response += "💡 您可以先学习其他专题:\n"
                response += "- `/mao learn 矛盾论`\n"
                response += "- `/mao learn 实践论`\n"
                response += "- `/mao learn 战略思维`\n"
                return response
        
        # 默认情况：学习系统介绍
        if path != 'auto':
            # 显示学习路径详情
            return self.learning_system.format_path_details(path)
        else:
            # 显示学习系统总体介绍
            return self.learning_system.format_learning_introduction()
    
    def _process_concepts(self, parsed: dict) -> str:
        """处理概念命令"""
        concept = parsed.get('concept', '')
        search = parsed.get('search', '')
        
        if search:
            # 搜索概念
            response = f"## 🔍 概念搜索: {search}\n\n"
            response += "**相关概念**:\n"
            response += "- 群众路线: 从群众中来，到群众中去\n"
            response += "- 群众观点: 相信群众，依靠群众\n"
            response += "- 群众工作: 做好群众工作的具体方法\n"
            response += "- 为人民服务: 全心全意为人民服务\n"
            return response
        
        if concept:
            # 查看特定概念
            response = f"## 📚 概念解释: {concept}\n\n"
            
            if concept == '矛盾':
                response += "**定义**: 事物内部对立统一的双方关系\n\n"
                response += "**分类**:\n"
                response += "- 主要矛盾: 决定事物性质的矛盾\n"
                response += "- 次要矛盾: 处于从属地位的矛盾\n\n"
                response += "**应用**:\n"
                response += "1. 识别矛盾: 找出问题中的各种矛盾\n"
                response += "2. 区分主次: 确定主要矛盾和次要矛盾\n"
                response += "3. 分析转化: 分析矛盾双方如何转化\n"
            elif concept == '实践':
                response += "**定义**: 人们改造客观世界的物质活动\n\n"
                response += "**与实践论的关系**:\n"
                response += "- 实践是认识的来源\n"
                response += "- 实践是认识发展的动力\n"
                response += "- 实践是检验真理的标准\n\n"
                response += "**应用**:\n"
                response += "遵循'实践-认识-再实践'循环\n"
            else:
                response += f"正在完善 {concept} 概念的解释...\n\n"
                response += "💡 您可以查看其他核心概念:\n"
                response += "- `/mao concepts 矛盾`\n"
                response += "- `/mao concepts 实践`\n"
                response += "- `/mao concepts 群众`\n"
            
            return response
        
        # 默认：查看概念列表
        response = "## 📖 毛泽东核心概念库\n\n"
        response += "### 哲学概念\n"
        response += "- 矛盾: 对立统一规律\n"
        response += "- 实践: 改造客观世界的活动\n"
        response += "- 认识: 对客观世界的反映\n"
        response += "- 实事求是: 从实际出发\n\n"
        
        response += "### 工作方法概念\n"
        response += "- 调查研究: 深入实际了解情况\n"
        response += "- 群众路线: 从群众中来，到群众中去\n"
        response += "- 批评与自我批评: 改进工作的方法\n"
        response += "- 抓典型: 通过典型推动一般\n\n"
        
        response += "### 战略思维概念\n"
        response += "- 持久战: 长期斗争策略\n"
        response += "- 统一战线: 团结一切可以团结的力量\n"
        response += "- 集中优势兵力: 集中力量解决关键问题\n"
        response += "- 运动战: 灵活机动的作战方式\n\n"
        
        response += "💡 使用 `/mao concepts [概念名]` 查看详细解释"
        
        return response
    
    def _process_compare(self, parsed: dict) -> str:
        """处理比较命令"""
        topic1 = parsed.get('topic1', '')
        topic2 = parsed.get('topic2', '')
        
        if not topic1:
            # 默认比较介绍
            response = "## 🔄 方法论比较系统\n\n"
            response += "通过比较不同方法论，深化对毛泽东思想的理解。\n\n"
            response += "### 可比较的主题\n"
            response += "- 不同方法论: `/mao compare 矛盾论 实践论`\n"
            response += "- 不同时期思想: `/mao compare 毛泽东 邓小平`\n"
            response += "- 不同工作方法: `/mao compare 调查研究 群众路线`\n\n"
            
            response += "### 比较维度\n"
            response += "1. 核心思想\n"
            response += "2. 应用方法\n"
            response += "3. 适用场景\n"
            response += "4. 实践效果\n"
            
            return response
        
        if not topic2:
            response = f"## 📊 {topic1} 分析\n\n"
            response += f"需要另一个主题进行比较，例如:\n"
            response += f"- `/mao compare {topic1} 实践论`\n"
            response += f"- `/mao compare {topic1} 战略思维`\n"
            return response
        
        # 简单比较示例
        response = f"## 🔄 比较分析: {topic1} vs {topic2}\n\n"
        
        if topic1 == '矛盾论' and topic2 == '实践论':
            response += "### 核心思想比较\n"
            response += "**矛盾论**: 聚焦事物内部的对立统一关系\n"
            response += "**实践论**: 强调实践对认识的决定作用\n\n"
            
            response += "### 应用方法比较\n"
            response += "**矛盾论应用**:\n"
            response += "1. 识别主要矛盾和次要矛盾\n"
            response += "2. 分析矛盾双方的关系\n"
            response += "3. 促进矛盾转化\n\n"
            
            response += "**实践论应用**:\n"
            response += "1. 通过实践获取认识\n"
            response += "2. 用认识指导新的实践\n"
            response += "3. 循环往复，不断完善\n\n"
            
            response += "### 适用场景\n"
            response += "**矛盾论适用**: 问题诊断、冲突解决、决策分析\n"
            response += "**实践论适用**: 工作方法、学习计划、技能提升\n"
        
        else:
            response += f"正在开发 {topic1} 和 {topic2} 的比较分析...\n\n"
            response += "💡 您可以先尝试:\n"
            response += "- `/mao compare 矛盾论 实践论`\n"
            response += "- `/mao compare 调查研究 群众路线`\n"
        
        return response
    
    def _process_settings(self, parsed: dict) -> str:
        """处理设置命令"""
        setting_key = parsed.get('setting_key', '')
        setting_value = parsed.get('setting_value', '')
        
        if not setting_key:
            # 查看当前设置
            response = "## ⚙️ 个性化设置\n\n"
            response += "### 当前设置\n"
            response += "- **响应详细程度**: 中\n"
            response += "- **响应风格**: 毛泽东式（方法论+风格）\n"
            response += "- **分析方法权重**: 默认\n\n"
            
            response += "### 可设置的选项\n"
            response += "1. **详细程度**: 高/中/低\n"
            response += "   `/mao settings 详细程度=高`\n\n"
            response += "2. **响应风格**: 现代/传统/毛泽东式\n"
            response += "   `/mao settings 风格=现代`\n\n"
            response += "3. **分析方法权重**: 自定义不同方法的权重\n"
            response += "   `/mao settings 权重=矛盾:0.3,实践:0.2,调查:0.2,战略:0.2,群众:0.1`\n"
            
            return response
        
        if setting_value:
            # 修改设置
            response = f"## ✅ 设置已更新\n\n"
            response += f"**{setting_key}** = **{setting_value}**\n\n"
            response += "### 设置说明\n"
            
            if setting_key == '详细程度':
                response += f"设置为{setting_value}后，响应将包含{'更多细节和示例' if setting_value == '高' else '适中内容' if setting_value == '中' else '核心要点'}。\n"
            elif setting_key == '风格':
                response += f"响应风格已调整为{setting_value}。\n"
            
            response += "\n💡 使用 `/mao settings` 查看所有设置"
        else:
            # 查看特定设置
            response = f"## 🔧 设置详情: {setting_key}\n\n"
            response += f"**当前值**: 默认\n\n"
            response += f"**说明**: 此设置控制{setting_key}的行为。\n\n"
            response += f"**修改示例**: `/mao settings {setting_key}=新值`\n"
        
        return response

def test_integration():
    """测试集成系统"""
    integration = MaoSkillIntegration()
    
    test_commands = [
        # 新命令架构测试
        "/mao 分析公司部门协作问题",
        "/mao analyze --method=矛盾 分析团队冲突",
        "/mao analyze --style=work 制定项目计划",
        "/mao help",
        "/mao help analyze",
        "/mao learn",
        "/mao learn --path=入门",
        "/mao learn 矛盾论",
        "/mao concepts",
        "/mao concepts 矛盾",
        "/mao compare",
        "/mao compare 矛盾论 实践论",
        "/mao settings",
        "/mao settings 详细程度=高",
        
        # 老命令测试（向后兼容）
        "/mao-work 分析商业案例",
        "/mao-persona 写动员讲话",
        "/mao-analyze 矛盾 公司内部问题",
        
        # 错误命令测试
        "/mao unknown",
        "/mao analyze",
    ]
    
    print("🔍 毛泽东.skill集成系统测试\n")
    print("=" * 70)
    
    for i, cmd in enumerate(test_commands, 1):
        print(f"\n📋 测试 {i}: `{cmd}`")
        print("-" * 70)
        
        response = integration.process_command(cmd)
        
        # 限制输出长度
        lines = response.split('\n')
        if len(lines) > 20:
            print('\n'.join(lines[:20]))
            print("... (响应截断，显示前20行)")
        else:
            print(response)
        
        print("-" * 70)
    
    print("\n" + "=" * 70)
    print("✅ 集成测试完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东.skill集成系统")
    parser.add_argument("--command", help="需要处理的命令")
    parser.add_argument("--test", action="store_true", help="运行集成测试")
    
    args = parser.parse_args()
    
    integration = MaoSkillIntegration()
    
    if args.test:
        test_integration()
    elif args.command:
        response = integration.process_command(args.command)
        print(response)
    else:
        print("请提供命令或使用 --test 运行测试")
        print("示例: python mao_skill_integration.py --command '/mao analyze 分析问题'")

if __name__ == "__main__":
    main()