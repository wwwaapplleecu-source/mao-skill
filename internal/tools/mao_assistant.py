#!/usr/bin/env python3
"""
毛泽东统一助理 - 模块三用户体验优化原型

功能：
1. 统一命令入口，智能路由用户请求
2. 基于概念关系网络提供深度分析
3. 交互式引导模式
4. 结构化响应生成
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import random

class MaoAssistant:
    """毛泽东统一助理"""

    def __init__(self, concept_network_path=None):
        self.concept_network = self.load_concept_network(concept_network_path)
        self.user_history = defaultdict(list)
        self.analysis_methods = {
            "矛盾": self.analyze_contradiction,
            "实践": self.analyze_practice,
            "调查": self.analyze_investigation,
            "战略": self.analyze_strategy,
            "群众": self.analyze_mass_line,
            "方法论": self.analyze_methodology,
            "综合分析": self.analyze_comprehensive
        }

        # 常见意图关键词
        self.intent_keywords = {
            "矛盾分析": ["矛盾", "冲突", "问题", "困难", "障碍", "挑战"],
            "实践指导": ["实践", "实施", "执行", "操作", "开展工作", "如何做"],
            "调查建议": ["调查", "调研", "研究", "了解", "探索", "数据"],
            "战略规划": ["战略", "规划", "计划", "目标", "方向", "发展"],
            "群众工作": ["群众", "团队", "员工", "管理", "领导", "服务"],
            "方法论指导": ["方法", "方法论", "框架", "理论", "原理", "思维"]
        }

        # 响应模板
        self.response_templates = self.load_response_templates()

    def load_concept_network(self, path=None):
        """加载概念网络"""
        if not path:
            # 查找最新的概念网络文件
            reports_dir = Path(__file__).parent.parent / "reports" / "concept_relations"
            if not reports_dir.exists():
                return {}

            json_files = list(reports_dir.glob("*.json"))
            if not json_files:
                return {}

            network = {}
            try:
                for json_file in json_files:
                    if "concept_cooccurrence" in json_file.name:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if "strong_relations" in data:
                                network = self.build_network_from_relations(data["strong_relations"])
                                break
            except Exception as e:
                print(f"加载概念网络失败: {e}")

            return network

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "strong_relations" in data:
                    return self.build_network_from_relations(data["strong_relations"])
        except Exception as e:
            print(f"加载概念网络失败: {e}")

        return {}

    def build_network_from_relations(self, relations):
        """从关系数据构建网络"""
        network = {}
        for relation in relations:
            if len(relation) >= 3:
                concept1, concept2, weight = relation[0], relation[1], relation[2]

                if concept1 not in network:
                    network[concept1] = {}
                if concept2 not in network:
                    network[concept2] = {}

                network[concept1][concept2] = weight
                network[concept2][concept1] = weight

        return network

    def load_response_templates(self):
        """加载响应模板"""
        return {
            "contradiction": {
                "title": "矛盾分析报告",
                "sections": [
                    "## 🔍 主要矛盾识别",
                    "## 🔗 次要矛盾分析",
                    "## ⚖️ 矛盾关系分析",
                    "## 💡 矛盾转化建议"
                ]
            },
            "practice": {
                "title": "实践指导方案",
                "sections": [
                    "## 🛠️ 当前实践状态分析",
                    "## 📈 实践改进方向",
                    "## 🔄 实践-认识循环设计",
                    "## ✅ 实践效果检验方法"
                ]
            },
            "investigation": {
                "title": "调查研究方案",
                "sections": [
                    "## 🔍 调查目标确定",
                    "## 📋 调查计划设计",
                    "## 🔧 调查方法选择",
                    "## 📊 数据分析与结论"
                ]
            },
            "strategy": {
                "title": "战略规划方案",
                "sections": [
                    "## 🎯 战略目标设定",
                    "## 📅 阶段划分与时间安排",
                    "## 💪 资源集中与优势发挥",
                    "## 🔄 灵活调整与风险应对"
                ]
            },
            "mass_line": {
                "title": "群众工作方案",
                "sections": [
                    "## 👥 深入了解群众需求",
                    "## 💬 集中群众智慧",
                    "## 🤝 团结与教育群众",
                    "## 🚀 发动群众共同行动"
                ]
            },
            "comprehensive": {
                "title": "综合问题分析报告",
                "sections": [
                    "## 问题概述与背景",
                    "## 多维角度分析", 
                    "## 核心洞见与发现",
                    "## 具体行动建议",
                    "## 方法论参考与学习"
                ]
            }
        }

    def recognize_intent(self, user_input: str) -> Dict[str, Any]:
        """识别用户意图"""
        intent = {
            "primary": "综合分析",  # 默认意图
            "confidence": 0.5,
            "keywords": [],
            "analysis_methods": ["矛盾", "实践", "战略"],
            "user_type": "普通用户",  # 新手、普通、专家
            "context": user_input
        }

        # 提取关键词
        keywords = []
        for category, word_list in self.intent_keywords.items():
            for word in word_list:
                if word in user_input:
                    keywords.append(word)
                    if category in ["矛盾分析", "实践指导", "调查建议", "战略规划", "群众工作", "方法论指导"]:
                        # 映射到分析方法
                        if category == "矛盾分析":
                            intent["primary"] = "矛盾分析"
                            intent["analysis_methods"] = ["矛盾"]
                        elif category == "实践指导":
                            intent["primary"] = "实践指导"
                            intent["analysis_methods"] = ["实践"]
                        elif category == "调查建议":
                            intent["primary"] = "调查建议"
                            intent["analysis_methods"] = ["调查"]
                        elif category == "战略规划":
                            intent["primary"] = "战略规划"
                            intent["analysis_methods"] = ["战略"]
                        elif category == "群众工作":
                            intent["primary"] = "群众工作"
                            intent["analysis_methods"] = ["群众"]
                        elif category == "方法论指导":
                            intent["primary"] = "方法论指导"
                            intent["analysis_methods"] = ["方法论"]

        intent["keywords"] = keywords

        # 基于输入长度判断用户类型
        if len(user_input) < 10:
            intent["user_type"] = "新手"
        elif len(user_input) < 50:
            intent["user_type"] = "普通用户"
        else:
            intent["user_type"] = "专家"

        # 计算置信度
        if keywords:
            intent["confidence"] = min(0.9, 0.5 + len(keywords) * 0.1)

        return intent

    def extract_concepts(self, text: str) -> List[str]:
        """从文本中提取相关概念"""
        if not self.concept_network:
            return []

        concepts = []
        for concept in self.concept_network.keys():
            if concept in text and len(concept) > 1:  # 避免单字匹配
                concepts.append(concept)

        return concepts[:10]  # 返回最多10个相关概念

    def find_related_concepts(self, concepts: List[str]) -> Dict[str, List[Tuple[str, int]]]:
        """查找相关概念"""
        if not self.concept_network:
            return {}

        related = {}
        for concept in concepts:
            if concept in self.concept_network:
                # 获取最强相关的5个概念
                related_concepts = list(self.concept_network[concept].items())
                related_concepts.sort(key=lambda x: x[1], reverse=True)
                related[concept] = related_concepts[:5]

        return related

    def analyze_contradiction(self, problem: str, concepts: List[str], related_concepts: Dict) -> str:
        """矛盾分析"""
        # 构建基于概念网络的深度分析
        analysis = "## 🎯 矛盾分析框架\n\n"

        # 主要矛盾识别
        if concepts:
            analysis += f"### 🔍 识别的主要概念\n"
            for concept in concepts[:5]:
                analysis += f"- **{concept}**"
                if concept in related_concepts:
                    related = [rc[0] for rc in related_concepts[concept][:3]]
                    analysis += f"（相关概念：{', '.join(related)}）"
                analysis += "\n"

        analysis += f"\n### ⚖️ 矛盾类型分析\n"

        # 基于概念网络的矛盾分析建议
        if "革命" in concepts or "斗争" in concepts:
            analysis += "**革命性矛盾**：具有根本性、对抗性的矛盾\n"
            analysis += "- 特点：对立双方利益根本冲突\n"
            analysis += "- 解决方法：通过斗争实现矛盾转化\n"
            analysis += "- 毛泽东方法：分清敌我，团结朋友，打击敌人\n"

        if "实践" in concepts or "认识" in concepts:
            analysis += "**实践认识矛盾**：认识与实践之间的矛盾\n"
            analysis += "- 特点：理论与实际的脱节\n"
            analysis += "- 解决方法：实践-认识-再实践循环\n"
            analysis += "- 毛泽东方法：调查研究，实事求是\n"

        if "群众" in concepts or "人民" in concepts:
            analysis += "**群众关系矛盾**：领导与群众之间的矛盾\n"
            analysis += "- 特点：脱离群众，官僚主义\n"
            analysis += "- 解决方法：群众路线，从群众中来，到群众中去\n"
            analysis += "- 毛泽东方法：关心群众生活，注意工作方法\n"

        # 添加毛泽东经典论述
        mao_quotes = [
            "一切事物中包含的矛盾方面的相互依赖和相互斗争，决定一切事物的生命，推动一切事物的发展。",
            "矛盾着的两方面中，必有一方面是主要的，他方面是次要的。",
            "捉住了这个主要矛盾，一切问题就迎刃而解了。",
            "事物的矛盾法则，即对立统一的法则，是唯物辩证法的最根本的法则。"
        ]

        analysis += f"\n### 💡 毛泽东矛盾论指导\n"
        analysis += f"> *{random.choice(mao_quotes)}*\n"

        return analysis

    def analyze_practice(self, problem: str, concepts: List[str], related_concepts: Dict) -> str:
        """实践分析"""
        analysis = "## 🛠️ 实践论指导框架\n\n"

        analysis += "### 🔄 实践-认识循环设计\n"
        analysis += "1. **初步实践**：从具体问题出发，开展初步实践活动\n"
        analysis += "2. **感性认识**：收集实践经验，形成感性认识\n"
        analysis += "3. **理性认识**：分析总结，上升为理性认识\n"
        analysis += "4. **再实践**：用理性认识指导新的实践\n"
        analysis += "5. **再认识**：在更高层次上形成新的认识\n"

        # 基于概念的具体建议
        if concepts:
            analysis += f"\n### 🎯 基于相关概念的具体实践建议\n"
            for concept in concepts[:3]:
                if concept in ["调查研究", "群众路线", "实事求是"]:
                    analysis += f"- **{concept}实践**：深入开展{concept}活动，掌握第一手材料\n"
                elif concept in ["矛盾", "问题", "困难"]:
                    analysis += f"- **{concept}解决实践**：通过具体实践活动解决{concept}\n"
                else:
                    analysis += f"- **{concept}相关实践**：围绕{concept}开展实践活动\n"

        # 毛泽东实践论指导
        mao_quotes = [
            "通过实践而发现真理，又通过实践而证实真理和发展真理。",
            "实践、认识、再实践、再认识，这种形式，循环往复以至无穷。",
            "你要有知识，你就得参加变革现实的实践。",
            "没有调查就没有发言权。"
        ]

        analysis += f"\n### 📚 毛泽东实践论指导\n"
        analysis += f"> *{random.choice(mao_quotes)}*\n"

        return analysis

    def analyze_investigation(self, problem: str, concepts: List[str], related_concepts: Dict) -> str:
        """调查研究分析"""
        analysis = "## 🔍 调查研究方法框架\n\n"

        analysis += "### 📋 调查研究四步法\n"
        analysis += "1. **制定调查计划**：明确调查目的、对象、方法和时间\n"
        analysis += "2. **深入实际调查**：到第一线获取第一手材料\n"
        analysis += "3. **周密分析研究**：对调查材料进行去粗取精、去伪存真\n"
        analysis += "4. **形成正确结论**：基于事实得出科学的结论\n"

        # 具体调查方法建议
        if "群众" in concepts or "人民" in concepts:
            analysis += "\n### 👥 群众路线调查方法\n"
            analysis += "- **蹲点调查**：深入一个基层单位，长期观察\n"
            analysis += "- **座谈会**：邀请群众代表座谈，听取意见\n"
            analysis += "- **个别访谈**：与群众个别交谈，了解真实想法\n"
            analysis += "- **参与观察**：与群众同吃同住同劳动\n"

        if "矛盾" in concepts or "问题" in concepts:
            analysis += "\n### ⚖️ 矛盾问题调查方法\n"
            analysis += "- **典型调查**：选择典型矛盾案例深入分析\n"
            analysis += "- **对比调查**：对比不同矛盾类型和解决方法\n"
            analysis += "- **历史调查**：调查矛盾的历史发展和演变\n"

        # 毛泽东调查研究指导
        mao_quotes = [
            "没有调查就没有发言权。",
            "调查就像'十月怀胎'，解决问题就像'一朝分娩'。",
            "一切结论产生于调查情况的末尾，而不是在它的先头。",
            "要了解情况，唯一的方法是向社会作调查。"
        ]

        analysis += f"\n### 📚 毛泽东调查研究指导\n"
        analysis += f"> *{random.choice(mao_quotes)}*\n"

        return analysis

    def analyze_strategy(self, problem: str, concepts: List[str], related_concepts: Dict) -> str:
        """战略分析"""
        analysis = "## 🎯 毛泽东战略思维框架\n\n"

        analysis += "### ⚔️ 战略三阶段思维\n"
        analysis += "1. **战略防御阶段**：积蓄力量，避免决战\n"
        analysis += "2. **战略相持阶段**：逐步消耗敌人，壮大自己\n"
        analysis += "3. **战略反攻阶段**：集中优势，决战决胜\n"

        # 基于概念的战略建议
        if "革命" in concepts or "斗争" in concepts:
            analysis += "\n### 🔥 革命战略原则\n"
            analysis += "- **战略上藐视敌人**：树立必胜信心\n"
            analysis += "- **战术上重视敌人**：认真对待每一个具体问题\n"
            analysis += "- **集中优势兵力**：在关键点上形成绝对优势\n"
            analysis += "- **各个歼灭敌人**：分化瓦解，逐个击破\n"

        if "群众" in concepts or "人民" in concepts:
            analysis += "\n### 🤝 群众战略原则\n"
            analysis += "- **依靠群众力量**：发动群众参与战略实施\n"
            analysis += "- **建立群众基础**：获得群众的广泛支持\n"
            analysis += "- **从群众中汲取智慧**：集中群众智慧完善战略\n"

        # 毛泽东战略指导
        mao_quotes = [
            "战略上要藐视敌人，战术上要重视敌人。",
            "集中优势兵力，各个歼灭敌人。",
            "你打你的，我打我的；打得赢就打，打不赢就走。",
            "以消灭敌人的有生力量为主要目标，不以保守或夺取地方为主要目标。"
        ]

        analysis += f"\n### 📚 毛泽东战略指导\n"
        analysis += f"> *{random.choice(mao_quotes)}*\n"

        return analysis

    def analyze_mass_line(self, problem: str, concepts: List[str], related_concepts: Dict) -> str:
        """群众路线分析"""
        analysis = "## 👥 群众路线工作框架\n\n"

        analysis += "### 🔄 群众路线循环\n"
        analysis += "1. **从群众中来**：深入群众，了解情况，集中意见\n"
        analysis += "2. **形成决策**：将群众意见集中起来，形成决策\n"
        analysis += "3. **到群众中去**：将决策贯彻到群众中去\n"
        analysis += "4. **检验修正**：在群众实践中检验决策，修正完善\n"

        # 具体工作方法
        analysis += "\n### 🛠️ 群众工作方法\n"
        analysis += "- **关心群众生活**：了解群众疾苦，解决实际困难\n"
        analysis += "- **听取群众意见**：虚心听取群众批评和建议\n"
        analysis += "- **发动群众参与**：让群众参与决策和执行\n"
        analysis += "- **教育引导群众**：提高群众觉悟，引导群众前进\n"

        # 毛泽东群众路线指导
        mao_quotes = [
            "从群众中来，到群众中去。",
            "群众是真正的英雄，而我们自己则往往是幼稚可笑的。",
            "全心全意为人民服务。",
            "关心群众生活，注意工作方法。"
        ]

        analysis += f"\n### 📚 毛泽东群众路线指导\n"
        analysis += f"> *{random.choice(mao_quotes)}*\n"

        return analysis

    def analyze_methodology(self, problem: str, concepts: List[str], related_concepts: Dict) -> str:
        """方法论分析"""
        analysis = "## 📚 毛泽东方法论体系\n\n"

        analysis += "### 🔧 五大核心方法论\n"
        analysis += "1. **矛盾分析法**：分析事物内部的矛盾运动\n"
        analysis += "2. **实践论方法**：实践-认识-再实践循环\n"
        analysis += "3. **调查研究法**：没有调查就没有发言权\n"
        analysis += "4. **群众路线法**：从群众中来，到群众中去\n"
        analysis += "5. **战略思维法**：战略上藐视，战术上重视\n"

        # 基于概念的方法选择
        if concepts:
            analysis += "\n### 🎯 推荐方法选择\n"
            for concept in concepts[:3]:
                if concept in ["矛盾", "冲突", "问题"]:
                    analysis += f"- **针对{concept}**：推荐使用矛盾分析法\n"
                elif concept in ["实践", "实施", "行动"]:
                    analysis += f"- **针对{concept}**：推荐使用实践论方法\n"
                elif concept in ["调查", "研究", "数据"]:
                    analysis += f"- **针对{concept}**：推荐使用调查研究法\n"
                elif concept in ["群众", "团队", "组织"]:
                    analysis += f"- **针对{concept}**：推荐使用群众路线法\n"
                elif concept in ["战略", "规划", "目标"]:
                    analysis += f"- **针对{concept}**：推荐使用战略思维法\n"

        # 毛泽东方法论指导
        mao_quotes = [
            "我们要把辩证法逐步推广，要求大家逐步地学会使用辩证法这个科学方法。",
            "分析的方法就是辩证的方法。",
            "马克思主义者看问题，不但要看到部分，而且要看到全体。",
            "研究问题，忌带主观性、片面性和表面性。"
        ]

        analysis += f"\n### 💡 毛泽东方法论指导\n"
        analysis += f"> *{random.choice(mao_quotes)}*\n"

        return analysis

    def analyze_comprehensive(self, problem: str, concepts: List[str], related_concepts: Dict) -> str:
        """综合分析"""
        analysis = "## 🎯 综合问题分析框架\n\n"

        # 使用多种方法综合分析
        analysis += "### 🔍 多角度分析方法\n"

        methods_used = []
        if concepts:
            for concept in concepts:
                if concept in ["矛盾", "冲突", "问题"] and "矛盾" not in methods_used:
                    analysis += self.analyze_contradiction(problem, concepts, related_concepts)
                    methods_used.append("矛盾")
                elif concept in ["实践", "实施", "行动"] and "实践" not in methods_used:
                    analysis += self.analyze_practice(problem, concepts, related_concepts)
                    methods_used.append("实践")
                elif concept in ["调查", "研究", "数据"] and "调查" not in methods_used:
                    analysis += self.analyze_investigation(problem, concepts, related_concepts)
                    methods_used.append("调查")
                elif concept in ["战略", "规划", "目标"] and "战略" not in methods_used:
                    analysis += self.analyze_strategy(problem, concepts, related_concepts)
                    methods_used.append("战略")
                elif concept in ["群众", "团队", "组织"] and "群众" not in methods_used:
                    analysis += self.analyze_mass_line(problem, concepts, related_concepts)
                    methods_used.append("群众")

                if len(methods_used) >= 3:  # 最多使用3种方法
                    break

        # 如果没找到合适的方法，使用默认方法
        if not methods_used:
            analysis += self.analyze_contradiction(problem, concepts, related_concepts)
            analysis += self.analyze_practice(problem, concepts, related_concepts)

        return analysis

    def generate_response(self, intent: Dict[str, Any], problem: str) -> str:
        """生成响应"""
        # 提取概念
        concepts = self.extract_concepts(problem)
        related_concepts = self.find_related_concepts(concepts)

        # 确定分析方法
        if intent["analysis_methods"]:
            primary_method = intent["analysis_methods"][0]
        else:
            primary_method = "综合分析"

        # 生成分析内容
        if primary_method in self.analysis_methods:
            analysis_content = self.analysis_methods[primary_method](problem, concepts, related_concepts)
        else:
            analysis_content = self.analyze_comprehensive(problem, concepts, related_concepts)

        # 构建响应
        response = f"# 毛泽东方法分析报告\n\n"
        response += f"**分析问题**: {problem}\n\n"
        response += f"**识别意图**: {intent['primary']} (置信度: {intent['confidence']:.1%})\n\n"

        if concepts:
            response += f"**提取概念**: {', '.join(concepts[:5])}\n\n"

        response += "---\n\n"
        response += analysis_content

        # 添加结构化建议
        response += "\n\n## 具体行动建议\n"
        response += "1. **明确主要矛盾**：抓住问题的关键\n"
        response += "2. **制定实施计划**：分步骤具体实施\n"
        response += "3. **深入调查研究**：获取第一手材料\n"
        response += "4. **依靠群众力量**：发动群众共同参与\n"
        response += "5. **实践检验修正**：在实践中不断改进\n"

        # 添加相关概念网络
        if concepts and related_concepts:
            response += "\n\n## 🔗 相关概念网络\n"
            for concept in concepts[:3]:
                if concept in related_concepts:
                    related = [f"{rc[0]}({rc[1]})" for rc in related_concepts[concept][:3]]
                    response += f"- **{concept}** → {', '.join(related)}\n"

        # 添加毛泽东语录总结
        mao_conclusion = [
            "我们要有'愚公移山'的毅力，不怕困难，坚持斗争，直到胜利。",
            "前途是光明的，道路是曲折的。",
            "下定决心，不怕牺牲，排除万难，去争取胜利。",
            "我们需要的是热烈而镇定的情绪，紧张而有秩序的工作。"
        ]

        response += f"\n\n## 💫 毛泽东思想指导\n"
        response += f"> *{random.choice(mao_conclusion)}*\n"

        return response

    def process_command(self, user_input: str, user_id: str = "default") -> str:
        """处理用户命令"""
        # 记录用户历史
        self.user_history[user_id].append(user_input)
        if len(self.user_history[user_id]) > 10:
            self.user_history[user_id] = self.user_history[user_id][-10:]

        # 识别意图
        intent = self.recognize_intent(user_input)

        # 生成响应
        response = self.generate_response(intent, user_input)

        return response

    def interactive_guide(self, user_input: str) -> List[str]:
        """交互式引导"""
        steps = []

        # 第一步：问题澄清
        steps.append("## 🔍 第一步：问题澄清")
        steps.append("请更具体地描述您的问题，包括：")
        steps.append("- 问题的具体表现")
        steps.append("- 已经尝试过的解决方法")
        steps.append("- 期望达到的目标")
        steps.append("- 面临的困难和障碍")

        # 第二步：方法选择
        steps.append("\n## 🛠️ 第二步：方法选择")
        steps.append("基于您的问题，推荐以下毛泽东方法：")

        intent = self.recognize_intent(user_input)
        for method in intent.get("analysis_methods", ["矛盾分析", "实践指导"]):
            if method == "矛盾":
                steps.append("- **矛盾分析法**：识别主要矛盾，分清主次")
            elif method == "实践":
                steps.append("- **实践论方法**：设计实践-认识循环")
            elif method == "调查":
                steps.append("- **调查研究法**：制定调查计划，获取第一手材料")
            elif method == "战略":
                steps.append("- **战略思维法**：制定分阶段实施战略")
            elif method == "群众":
                steps.append("- **群众路线法**：发动群众，依靠群众")

        # 第三步：实施步骤
        steps.append("\n## 🚀 第三步：实施步骤")
        steps.append("建议按照以下步骤实施：")
        steps.append("1. 明确目标和任务")
        steps.append("2. 制定详细计划")
        steps.append("3. 开展调查研究")
        steps.append("4. 实施具体行动")
        steps.append("5. 总结经验教训")
        steps.append("6. 调整改进方案")

        return steps

def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="毛泽东统一助理")
    parser.add_argument("--problem", type=str, help="要分析的问题")
    parser.add_argument("--interactive", action="store_true", help="交互式引导模式")
    parser.add_argument("--concept-network", type=str, help="概念网络文件路径")

    args = parser.parse_args()

    assistant = MaoAssistant(args.concept_network)

    if args.interactive:
        if not args.problem:
            print("请输入要分析的问题：")
            args.problem = input().strip()

        print("\n" + "="*60)
        print("毛泽东方法交互式引导")
        print("="*60)

        steps = assistant.interactive_guide(args.problem)
        for step in steps:
            print(step)

        print("\n" + "="*60)
        print("基于您的输入，以下是详细分析：")
        print("="*60)

    if args.problem:
        response = assistant.process_command(args.problem)
        print(response)
    else:
        print("请提供要分析的问题，使用 --problem 参数")

if __name__ == "__main__":
    main()