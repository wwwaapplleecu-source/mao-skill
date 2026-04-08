#!/usr/bin/env python3
"""
毛泽东.skill模拟器
基于text_processor和知识库模拟Skill的响应
用于测试和验证目的
"""

import re
import random
from typing import Dict, List, Any, Optional
from pathlib import Path

# 导入文本处理器
try:
    from tools.text_processor import MaoTextProcessor
except ImportError:
    # 如果在独立运行，尝试相对导入
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from tools.text_processor import MaoTextProcessor

class MaoSkillSimulator:
    """毛泽东.skill模拟器"""
    
    def __init__(self):
        self.processor = MaoTextProcessor()
        self.responses = self._load_response_templates()
        
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """加载响应模板"""
        return {
            "矛盾分析": [
                "分析{subject}的矛盾，首先要抓住主要矛盾。{subject}的主要矛盾是{main_contradiction}，次要矛盾包括{secondary_contradictions}。要促进矛盾向有利方向转化。",
                "研究{subject}，就要分析其内部矛盾。主要矛盾决定事物的性质，次要矛盾影响事物的发展。抓住主要矛盾，问题就迎刃而解。",
                "{subject}的矛盾是复杂多样的。要区分主要矛盾和次要矛盾，分析矛盾双方的对立统一关系，找到解决矛盾的突破口。"
            ],
            "实践指导": [
                "开展{task}要遵循'实践-认识-再实践'的循环。先试点，获取感性认识；再总结经验，形成理性认识；最后扩大实践，验证认识。",
                "{task}要坚持实事求是的原则。从实际出发，理论联系实际，在实践中检验和发展认识。",
                "做好{task}，关键在实践。实践是认识的来源，是检验真理的标准。要通过实践认识规律，指导工作。"
            ],
            "调查研究": [
                "开展{task}，调查研究是基本功。没有调查就没有发言权。要深入实际，掌握第一手材料。",
                "{task}需要周密的调查研究。要亲自到一线，与群众面对面交流，掌握真实情况。没有调查就没有发言权，没有正确的调查同样没有发言权。",
                "调查研究是做好{task}的前提。材料要丰富，观点要准确，分析要客观，结论要可靠。首先要调查，然后才能研究。"
            ],
            "战略规划": [
                "制定{task}的战略，要有持久战思维。分三个阶段：防御、相持、反攻。战略上藐视困难，战术上重视困难。集中优势资源，稳步推进。",
                "{task}的战略规划要着眼长远。要有战略眼光，也要有战术安排。分步骤实施，逐步推进，打好持久战。",
                "规划{task}，要统筹全局，抓住重点。既要考虑当前，也要着眼长远；既要看到有利条件，也要看到困难因素。战略与战术要紧密结合。"
            ],
            "群众工作": [
                "开展{task}要坚持群众路线。从群众中来，到群众中去。相信群众，依靠群众，服务群众。",
                "{task}要密切联系群众。了解群众需求，集中群众智慧，解决群众困难。",
                "群众是{task}的力量源泉。要深入群众，宣传群众，组织群众，带领群众前进。"
            ],
            "动员讲话": [
                "同志们！我们要以饱满的革命热情投入{task}。前途是光明的，道路是曲折的。团结一致，坚持斗争，克服困难，争取胜利！",
                "在{task}的征程上，我们要发扬艰苦奋斗的精神。困难吓不倒我们，挫折压不垮我们。要坚持斗争，胜利一定属于我们！",
                "{task}是一场硬仗。我们要有必胜的信心，要有充分的准备，要有灵活的策略。坚持斗争，前进，向着胜利前进！"
            ],
            "工作重点": [
                "做好{task}，既要抓住主要矛盾，又要兼顾次要矛盾；既要看到有利条件，又要看到困难因素；既要立足当前，还要着眼长远。",
                "{task}的关键在于：一要调查研究，掌握实情；二要抓住重点，突破难点；三要依靠群众，发动群众；四要持之以恒，坚持不懈。",
                "开展{task}，必须坚持实事求是，必须坚持群众路线，必须坚持独立自主，必须坚持艰苦奋斗。",
                "分析{task}，我们既要看到成绩，又要看到缺点，还要看到潜力。既要发扬优势，又要弥补不足，还要开拓创新。"
            ],
            "历史边界": [
                "毛泽东同志生前未接触过{subject}。基于他的方法论，可能会从以下角度分析：{possible_analysis}。这是推断而非转述。",
                "对于{subject}，毛泽东没有直接论述。但我们可以运用他的矛盾分析法、实践论等方法来分析这个问题。这是基于方法论的推断。",
                "毛泽东的时代背景与今天不同，{subject}是新生事物。我们可以学习他的思维方法，而不是机械照搬具体结论。这是方法论的运用。"
            ],
            "价值观底线": [
                "毛泽东方法论反对{subject}。正确的群众工作方法是{correct_method}，要尊重群众，服务群众。",
                "{subject}不符合毛泽东的群众观点。要坚持为人民服务的宗旨，维护群众利益。",
                "毛泽东教导我们要{correct_teaching}，而不是{subject}。要树立正确的价值观和工作方法。"
            ]
        }
    
    def analyze_question(self, question: str) -> Dict[str, Any]:
        """分析问题类型和内容"""
        question_lower = question.lower()
        
        # 识别问题类型
        question_type = "其他"
        subject = self._extract_subject(question)
        
        if any(keyword in question_lower for keyword in ["矛盾", "主要矛盾", "次要矛盾"]):
            question_type = "矛盾分析"
        elif any(keyword in question_lower for keyword in ["实践", "怎么做", "如何做", "指导"]):
            question_type = "实践指导"
        elif any(keyword in question_lower for keyword in ["调查", "调研", "研究"]):
            question_type = "调查研究"
        elif any(keyword in question_lower for keyword in ["战略", "规划", "长期", "计划"]):
            question_type = "战略规划"
        elif any(keyword in question_lower for keyword in ["群众", "人民", "公众"]):
            question_type = "群众工作"
        elif any(keyword in question_lower for keyword in ["讲话", "动员", "发言"]):
            question_type = "动员讲话"
        elif any(keyword in question_lower for keyword in ["重点", "关键", "核心"]):
            question_type = "工作重点"
        elif any(keyword in question_lower for keyword in ["互联网", "技术", "现代", "当代"]):
            question_type = "历史边界"
        elif any(keyword in question_lower for keyword in ["操纵", "控制", "欺骗"]):
            question_type = "价值观底线"
        
        # 提取概念
        concepts = self.processor.extract_concepts(question)
        
        return {
            "type": question_type,
            "subject": subject,
            "concepts": concepts,
            "original_question": question
        }
    
    def _extract_subject(self, question: str) -> str:
        """从问题中提取主题"""
        # 简单的主题提取逻辑
        question = question.strip()
        
        # 移除常见的问题前缀
        prefixes = ["分析", "如何", "怎样", "怎么", "制定", "开展", "写一段", "毛泽东如何看待"]
        for prefix in prefixes:
            if question.startswith(prefix):
                question = question[len(prefix):].strip()
        
        # 如果问题以问号结尾，去掉问号
        if question.endswith("？") or question.endswith("?"):
            question = question[:-1].strip()
        
        # 如果还有"的"字结构，进一步处理
        if "的" in question:
            parts = question.split("的")
            if len(parts) > 1:
                # 返回最后一个部分之前的内容
                subject = "的".join(parts[:-1])
                return subject.strip()
        
        return question
    
    def generate_response(self, question: str, use_mao_style: bool = True) -> str:
        """生成模拟响应"""
        analysis = self.analyze_question(question)
        question_type = analysis["type"]
        subject = analysis["subject"] or "这个问题"
        
        # 根据问题类型选择响应模板
        if question_type in self.responses:
            templates = self.responses[question_type]
            template = random.choice(templates)
            
            # 填充模板
            response = self._fill_template(template, subject, question_type)
            
            # 添加毛泽东风格
            if use_mao_style:
                response = self._add_mao_style(response)
            
            return response
        else:
            # 默认响应
            return f"对于'{subject}'这个问题，我们需要运用毛泽东的方法论来分析。首先要调查研究，掌握实际情况；然后分析矛盾，抓住主要矛盾；最后制定切实可行的解决方案。"
    
    def _fill_template(self, template: str, subject: str, question_type: str) -> str:
        """填充响应模板"""
        # 根据问题类型生成特定的填充内容
        fillers = {
            "main_contradiction": "内部发展与外部环境的矛盾",
            "secondary_contradictions": "资源分配、人员协调、技术瓶颈等",
            "possible_analysis": "从矛盾分析的角度，研究其内部矛盾和外部联系；从实践论的角度，探讨其发展规律",
            "correct_method": "深入群众，了解需求，集中智慧，民主决策",
            "correct_teaching": "全心全意为人民服务，从群众中来，到群众中去"
        }
        
        # 替换主题
        response = template.replace("{subject}", subject)
        response = response.replace("{task}", subject)
        
        # 替换其他占位符
        for key, value in fillers.items():
            response = response.replace(f"{{{key}}}", value)
        
        return response
    
    def _add_mao_style(self, response: str) -> str:
        """添加毛泽东风格"""
        # 添加毛泽东常用表达
        mao_expressions = [
            "同志们，",
            "我们要认识到，",
            "实践证明，",
            "历史经验告诉我们，",
            "总而言之，",
            "综上所述，"
        ]
        
        # 随机决定是否添加毛泽东式开头
        if random.random() > 0.5:
            response = random.choice(mao_expressions) + " " + response
        
        # 添加毛泽东式结尾
        mao_endings = [
            "这是我们必须坚持的原则。",
            "胜利一定属于我们！",
            "让我们为此而努力奋斗！",
            "这是历史的必然选择。",
            "我们要有这个信心。"
        ]
        
        if random.random() > 0.5 and not response.endswith("！") and not response.endswith("。"):
            response = response + " " + random.choice(mao_endings)
        
        return response
    
    def simulate_skill_command(self, command: str, args: str = "") -> str:
        """模拟Skill命令响应"""
        command = command.lower().strip()
        
        if command == "/mao":
            return self.generate_response(args)
        elif command == "/mao-work":
            # 只使用方法论部分
            response = self.generate_response(args)
            return self._extract_methodology_part(response)
        elif command == "/mao-persona":
            # 只使用人格风格部分
            response = self.generate_response(args, use_mao_style=True)
            return self._emphasize_persona_style(response)
        elif command.startswith("/mao-analyze"):
            # 解析分析类型
            parts = command.split()
            if len(parts) >= 2:
                analysis_type = parts[1]
                question = " ".join(parts[2:]) if len(parts) > 2 else args
                
                analysis_map = {
                    "矛盾": "矛盾分析",
                    "实践": "实践指导", 
                    "调查": "调查研究",
                    "战略": "战略规划",
                    "群众": "群众工作"
                }
                
                if analysis_type in analysis_map:
                    question_type = analysis_map[analysis_type]
                    if question:
                        return self._generate_specific_response(question_type, question)
        
        # 默认响应
        return "命令格式不正确。请使用 /mao [问题] 或 /mao-analyze [类型] [问题]"
    
    def _extract_methodology_part(self, response: str) -> str:
        """从响应中提取方法论部分"""
        # 简单的实现：移除明显的风格化表达
        style_expressions = ["同志们，", "胜利一定属于我们！", "让我们为此而努力奋斗！"]
        for expr in style_expressions:
            response = response.replace(expr, "")
        
        return response.strip()
    
    def _emphasize_persona_style(self, response: str) -> str:
        """强调人格风格部分"""
        # 添加更多毛泽东风格元素
        style_elements = [
            "（毛泽东式分析）",
            "【毛式风格】",
            "*毛泽东可能会这样说：*"
        ]
        
        if not response.startswith("同志们，"):
            response = "同志们，" + response
        
        return response
    
    def _generate_specific_response(self, question_type: str, question: str) -> str:
        """生成特定类型的响应"""
        subject = self._extract_subject(question)
        
        if question_type in self.responses:
            templates = self.responses[question_type]
            template = random.choice(templates)
            response = self._fill_template(template, subject, question_type)
            response = self._add_mao_style(response)
            return response
        else:
            return self.generate_response(question)

def main():
    """主函数：测试模拟器"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东.skill模拟器")
    parser.add_argument("--question", help="测试问题")
    parser.add_argument("--command", help="模拟Skill命令")
    parser.add_argument("--test", action="store_true", help="运行测试")
    
    args = parser.parse_args()
    
    simulator = MaoSkillSimulator()
    
    if args.test:
        # 运行测试
        test_questions = [
            "分析当前项目的主要矛盾",
            "如何开展用户调研", 
            "制定长期战略规划",
            "写一段动员讲话",
            "毛泽东如何看待互联网技术"
        ]
        
        print("毛泽东.skill模拟器测试：")
        print("=" * 60)
        
        for question in test_questions:
            print(f"\n问题: {question}")
            response = simulator.generate_response(question)
            print(f"响应: {response}")
            print("-" * 40)
    
    elif args.question:
        response = simulator.generate_response(args.question)
        print(f"问题: {args.question}")
        print(f"响应: {response}")
    
    elif args.command:
        response = simulator.simulate_skill_command(args.command)
        print(f"命令: {args.command}")
        print(f"响应: {response}")
    
    else:
        # 交互模式
        print("毛泽东.skill模拟器（输入'退出'结束）")
        print("=" * 60)
        
        while True:
            user_input = input("\n请输入问题或命令: ").strip()
            
            if user_input.lower() in ["退出", "exit", "quit"]:
                break
            
            if user_input.startswith("/"):
                response = simulator.simulate_skill_command(user_input)
            else:
                response = simulator.generate_response(user_input)
            
            print(f"\n响应: {response}")

if __name__ == "__main__":
    main()