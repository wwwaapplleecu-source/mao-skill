#!/usr/bin/env python3
"""
智能推荐器

基于用户问题内容推荐最佳分析方法，支持毛泽东.skill的智能引导功能
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class SmartRecommender:
    """智能分析方法推荐器"""
    
    def __init__(self, concepts_data_path=None):
        """初始化推荐器"""
        # 分析方法到关键词的映射
        self.method_keywords = {
            '矛盾': ['矛盾', '冲突', '问题', '对立', '主要矛盾', '次要矛盾', '矛盾分析', '矛盾转化', '对立统一', 
                    '矛盾双方', '矛盾关系', '矛盾运动', '矛盾斗争', '矛盾解决', '矛盾处理'],
            '实践': ['如何做', '实施', '方法', '步骤', '操作', '执行', '实践', '认识', '循环', '改进',
                    '如何', '怎样', '做法', '工作方法', '实践论', '实践检验', '实践过程', '实践经验'],
            '调查': ['调查', '研究', '了解', '数据', '信息', '收集', '调研', '实地', '第一手', '材料',
                    '调查研究', '调查工作', '调查方法', '调查结果', '实地调查', '周密调查'],
            '战略': ['战略', '规划', '长远', '目标', '方向', '计划', '竞争', '发展', '未来', '布局',
                    '战略规划', '战略目标', '战略方向', '战略思维', '战略部署', '战略决策', '战略管理'],
            '群众': ['团队', '管理', '群众', '员工', '人员', '组织', '协作', '沟通', '领导', '服务',
                    '群众路线', '群众工作', '群众观点', '群众基础', '群众运动', '群众组织', '群众管理']
        }
        
        # 停用词（不提取为关键词）
        self.stop_words = {'的', '了', '在', '是', '和', '与', '及', '或', '等', '这', '那', '哪', '什么',
                          '如何', '怎样', '为什么', '因为', '所以', '但是', '然而', '而且', '如果', '那么'}
        
        # 方法描述
        self.method_descriptions = {
            '矛盾': '矛盾分析法 - 识别主要矛盾和次要矛盾，分析矛盾转化',
            '实践': '实践论方法 - 遵循"实践-认识-再实践"循环，指导具体工作',
            '调查': '调查研究法 - 没有调查就没有发言权，深入实际了解情况',
            '战略': '战略思维法 - 战略上藐视，战术上重视，制定长远规划',
            '群众': '群众路线法 - 从群众中来，到群众中去，做好群众工作',
            '综合': '综合分析法 - 多角度综合分析，智能选择合适方法'
        }
        
        # 方法适用场景
        self.method_scenarios = {
            '矛盾': ['问题诊断', '冲突解决', '决策分析', '根本原因分析'],
            '实践': ['工作方法', '学习计划', '技能提升', '流程改进'],
            '调查': ['市场调研', '用户研究', '数据收集', '情况了解'],
            '战略': ['规划制定', '竞争分析', '发展方向', '资源配置'],
            '群众': ['团队管理', '人员协作', '群众工作', '组织建设'],
            '综合': ['综合问题', '复杂分析', '多角度思考', '全面考虑']
        }
        
        # 加载概念数据（如果提供）
        self.concepts_data = None
        if concepts_data_path:
            self.load_concepts_data(concepts_data_path)
    
    def load_concepts_data(self, filepath: str):
        """加载概念关系数据"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.concepts_data = json.load(f)
            print(f"已加载概念数据: {filepath}")
        except Exception as e:
            print(f"加载概念数据失败: {e}")
            self.concepts_data = None
    
    def extract_keywords(self, question: str) -> List[str]:
        """从问题中提取关键词"""
        keywords = []
        
        # 1. 首先提取已知的方法关键词（直接搜索）
        all_method_keywords = []
        for method_keys in self.method_keywords.values():
            all_method_keywords.extend(method_keys)
        
        # 去重并排序（长的关键词优先，避免短关键词优先匹配）
        all_method_keywords = sorted(set(all_method_keywords), key=len, reverse=True)
        
        question_remaining = question
        matched_keywords = []
        
        # 在问题中搜索所有方法关键词
        for keyword in all_method_keywords:
            if keyword in question_remaining:
                matched_keywords.append(keyword)
                # 标记已匹配的部分（简单处理）
                question_remaining = question_remaining.replace(keyword, ' ', 1)
        
        keywords.extend(matched_keywords)
        
        # 2. 提取其他有意义的词汇（2-4个中文字符）
        # 去除标点符号和非中文字符
        question_clean = re.sub(r'[^\u4e00-\u9fff]+', ' ', question)
        
        # 按空白分割，提取2-4字的词汇，过滤停用词
        for word in question_clean.split():
            word = word.strip()
            if 2 <= len(word) <= 4:
                # 过滤停用词
                if word in self.stop_words:
                    continue
                # 检查是否已经作为方法关键词匹配过
                if word not in keywords:
                    keywords.append(word)
        
        # 3. 如果没有提取到关键词，尝试提取所有2字符以上的词汇
        if not keywords:
            for word in question_clean.split():
                word = word.strip()
                if len(word) >= 2 and word not in self.stop_words:
                    keywords.append(word)
        
        return keywords
    
    def match_methods(self, keywords: List[str]) -> Dict[str, int]:
        """匹配关键词到分析方法"""
        method_scores = defaultdict(int)
        
        # 构建关键词到方法的反向映射
        keyword_to_methods = defaultdict(list)
        for method, method_keys in self.method_keywords.items():
            for method_key in method_keys:
                keyword_to_methods[method_key].append(method)
        
        # 为每个关键词分配分数
        for keyword in keywords:
            # 检查是否直接是方法关键词
            if keyword in keyword_to_methods:
                for method in keyword_to_methods[keyword]:
                    method_scores[method] += 3  # 直接匹配得分最高
            
            # 检查部分匹配
            for method_key in keyword_to_methods.keys():
                if len(keyword) >= 2 and len(method_key) >= 2:
                    # 检查互相包含关系
                    if keyword in method_key or method_key in keyword:
                        for method in keyword_to_methods[method_key]:
                            method_scores[method] += 1
        
        return dict(method_scores)
    
    def recommend_method(self, question: str) -> Dict[str, any]:
        """推荐分析方法"""
        # 1. 提取关键词
        keywords = self.extract_keywords(question)
        
        # 2. 匹配方法
        method_scores = self.match_methods(keywords)
        
        # 3. 如果没有匹配到，使用默认方法
        if not method_scores:
            return {
                'recommended_method': '综合',
                'confidence': 0.3,
                'alternative_methods': ['矛盾', '实践', '调查', '战略', '群众'],
                'keywords': keywords,
                'method_scores': method_scores,
                'reason': '未检测到明确关键词，推荐综合分析法',
                'description': self.method_descriptions.get('综合', '综合分析法 - 多角度综合分析，智能选择合适方法'),
                'scenarios': self.method_scenarios.get('综合', ['综合问题', '复杂分析', '多角度思考'])
            }
        
        # 4. 排序并选择最佳方法
        sorted_methods = sorted(method_scores.items(), key=lambda x: x[1], reverse=True)
        best_method, best_score = sorted_methods[0]
        
        # 5. 计算置信度（0-1）
        total_score = sum(method_scores.values())
        confidence = best_score / max(total_score, 1)
        
        # 6. 获取备选方法
        alternative_methods = [m for m, _ in sorted_methods[1:4] if m != best_method]
        
        # 7. 生成推荐理由
        reason = self.generate_reason(best_method, keywords, confidence)
        
        return {
            'recommended_method': best_method,
            'confidence': round(confidence, 2),
            'alternative_methods': alternative_methods[:3],
            'keywords': keywords,
            'method_scores': method_scores,
            'reason': reason,
            'description': self.method_descriptions.get(best_method, '综合分析法 - 多角度综合分析，智能选择合适方法'),
            'scenarios': self.method_scenarios.get(best_method, ['综合问题', '复杂分析', '多角度思考'])
        }
    
    def generate_reason(self, method: str, keywords: List[str], confidence: float) -> str:
        """生成推荐理由"""
        if confidence > 0.7:
            confidence_text = "高度匹配"
        elif confidence > 0.4:
            confidence_text = "较为匹配"
        else:
            confidence_text = "基础匹配"
        
        keyword_text = "、".join(keywords[:5]) if keywords else "无明确关键词"
        
        reasons = {
            '矛盾': f"问题中包含'{keyword_text}'等关键词，涉及矛盾分析需求。{confidence_text}矛盾分析法。",
            '实践': f"问题中包含'{keyword_text}'等关键词，涉及实践方法需求。{confidence_text}实践论方法。",
            '调查': f"问题中包含'{keyword_text}'等关键词，涉及调查了解需求。{confidence_text}调查研究法。",
            '战略': f"问题中包含'{keyword_text}'等关键词，涉及战略规划需求。{confidence_text}战略思维法。",
            '群众': f"问题中包含'{keyword_text}'等关键词，涉及群众工作需求。{confidence_text}群众路线法。",
            '综合': f"问题关键词'{keyword_text}'匹配度一般，推荐综合分析法全面考虑。"
        }
        
        return reasons.get(method, f"推荐{method}方法，匹配关键词：{keyword_text}")
    
    def analyze_question_type(self, question: str) -> Dict[str, any]:
        """分析问题类型"""
        # 问题类型分类
        question_types = {
            'what': ['是什么', '什么是', '什么叫', '定义', '概念'],
            'why': ['为什么', '原因', '为何', '缘故', '理由'],
            'how': ['如何', '怎么', '怎样', '方法', '步骤', '操作'],
            'which': ['哪个', '哪些', '选择', '比较', '优劣'],
            'analysis': ['分析', '剖析', '解读', '理解', '看法'],
            'plan': ['计划', '规划', '方案', '策划', '设计'],
            'problem': ['问题', '困难', '挑战', '障碍', '麻烦'],
            'decision': ['决定', '决策', '选择', '取舍', '判断']
        }
        
        detected_types = []
        for q_type, keywords in question_types.items():
            for keyword in keywords:
                if keyword in question:
                    detected_types.append(q_type)
                    break
        
        return {
            'question': question,
            'detected_types': detected_types,
            'primary_type': detected_types[0] if detected_types else 'general',
            'type_count': len(detected_types)
        }
    
    def get_method_guidance(self, method: str) -> Dict[str, any]:
        """获取方法指导信息"""
        guidance_templates = {
            '矛盾': {
                'steps': [
                    "1. 识别矛盾：找出问题中的各种矛盾",
                    "2. 区分主次：确定主要矛盾和次要矛盾",
                    "3. 分析关系：分析矛盾双方的对立统一关系",
                    "4. 制定对策：针对主要矛盾制定解决方案"
                ],
                'key_concepts': ['主要矛盾', '次要矛盾', '矛盾转化', '对立统一'],
                'mao_quote': "事物发展的根本原因，不是在事物的外部而是在事物的内部，在于事物内部的矛盾性。"
            },
            '实践': {
                'steps': [
                    "1. 实践探索：进行小范围实践，获取感性认识",
                    "2. 总结提升：总结经验，形成理性认识",
                    "3. 指导实践：用理性认识指导更大范围的实践",
                    "4. 循环验证：实践-认识-再实践循环，逐步完善"
                ],
                'key_concepts': ['感性认识', '理性认识', '实践循环', '真理标准'],
                'mao_quote': "实践、认识、再实践、再认识，这种形式，循环往复以至无穷。"
            },
            '调查': {
                'steps': [
                    "1. 制定计划：明确调查目的和范围",
                    "2. 深入实际：到一线了解实际情况",
                    "3. 收集材料：收集全面、真实的第一手材料",
                    "4. 分析研究：对材料进行科学的分析研究"
                ],
                'key_concepts': ['第一手材料', '周密的调查', '正确的调查', '实事求是'],
                'mao_quote': "没有调查，就没有发言权。"
            },
            '战略': {
                'steps': [
                    "1. 全局分析：分析全局形势和趋势",
                    "2. 阶段划分：划分战略阶段（防御、相持、反攻）",
                    "3. 资源集中：集中优势资源解决关键问题",
                    "4. 灵活调整：根据形势变化灵活调整战略"
                ],
                'key_concepts': ['持久战', '三个阶段', '集中优势', '灵活机动'],
                'mao_quote': "战略上藐视敌人，战术上重视敌人。"
            },
            '群众': {
                'steps': [
                    "1. 深入群众：了解群众的真实想法和需求",
                    "2. 集中智慧：集中群众的智慧和意见",
                    "3. 形成决策：将群众意见转化为科学决策",
                    "4. 发动群众：将决策变为群众的自觉行动"
                ],
                'key_concepts': ['从群众中来', '到群众中去', '民主集中', '群众观点'],
                'mao_quote': "从群众中来，到群众中去。"
            },
            '综合': {
                'steps': [
                    "1. 全面分析：从多个角度分析问题",
                    "2. 方法组合：结合多种分析方法",
                    "3. 综合判断：综合考虑各种因素",
                    "4. 整体解决：制定整体解决方案"
                ],
                'key_concepts': ['全面分析', '方法组合', '综合判断', '整体解决'],
                'mao_quote': "我们需要的是热烈而镇定的情绪，紧张而有秩序的工作。"
            }
        }
        
        return guidance_templates.get(method, guidance_templates['综合'])
    
    def format_recommendation(self, recommendation: Dict[str, any]) -> str:
        """格式化推荐结果"""
        method = recommendation.get('recommended_method', '综合')
        confidence = recommendation.get('confidence', 0.3)
        reason = recommendation.get('reason', '未检测到明确关键词，推荐综合分析法')
        description = recommendation.get('description', self.method_descriptions.get(method, '综合分析法'))
        
        output = f"## 🎯 分析推荐\n\n"
        output += f"**推荐方法**: {method}分析\n"
        output += f"**置信度**: {confidence*100:.0f}%\n"
        output += f"**方法说明**: {description}\n\n"
        output += f"**推荐理由**: {reason}\n\n"
        
        # 添加适用场景
        if recommendation.get('scenarios'):
            output += f"**适用场景**: {', '.join(recommendation['scenarios'][:3])}\n\n"
        
        # 添加备选方法
        if recommendation.get('alternative_methods'):
            output += f"**备选方法**: {', '.join(recommendation['alternative_methods'])}\n\n"
        
        # 添加方法指导
        guidance = self.get_method_guidance(method)
        output += f"## 📋 {method}分析步骤\n\n"
        for step in guidance['steps']:
            output += f"{step}\n"
        
        output += f"\n**核心概念**: {', '.join(guidance['key_concepts'])}\n\n"
        output += f"> *{guidance['mao_quote']}*\n"
        
        return output

def test_recommender():
    """测试推荐器"""
    recommender = SmartRecommender()
    
    test_questions = [
        "分析公司部门之间的协作矛盾",
        "如何开展用户需求调研",
        "制定公司未来三年的发展战略",
        "如何改进团队管理工作",
        "实践论对工作方法有什么指导意义",
        "当前市场竞争激烈，我们应该采取什么策略",
        "群众路线在基层工作中如何应用"
    ]
    
    print("🔍 智能推荐器测试\n")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n测试 {i}: {question}")
        print("-" * 40)
        
        # 分析问题类型
        type_analysis = recommender.analyze_question_type(question)
        print(f"问题类型: {', '.join(type_analysis['detected_types'])}")
        
        # 推荐方法
        recommendation = recommender.recommend_method(question)
        print(f"推荐方法: {recommendation['recommended_method']} (置信度: {recommendation['confidence']})")
        print(f"关键词: {', '.join(recommendation['keywords'][:5]) if recommendation['keywords'] else '无'}")
        
        # 格式化输出示例
        if i <= 2:  # 只显示前2个的详细输出
            print("\n详细推荐:")
            print(recommender.format_recommendation(recommendation))
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="智能分析方法推荐器")
    parser.add_argument("--question", help="需要分析的问题")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--concepts", help="概念数据文件路径")
    
    args = parser.parse_args()
    
    recommender = SmartRecommender(args.concepts)
    
    if args.test:
        test_recommender()
    elif args.question:
        recommendation = recommender.recommend_method(args.question)
        print(recommender.format_recommendation(recommendation))
    else:
        print("请提供问题或使用 --test 运行测试")
        print("示例: python smart_recommender.py --question '分析公司内部矛盾'")

if __name__ == "__main__":
    main()