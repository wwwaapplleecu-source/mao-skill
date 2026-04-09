#!/usr/bin/env python3
"""
分析决策层

负责智能推荐、问题分析、决策制定等分析功能。
属于六层架构中的分析决策层，包装现有的SmartRecommender。
"""

import sys
import os
from typing import Dict, List, Any, Optional, Tuple
import json

# 导入现有的智能推荐器
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from smart_recommender import SmartRecommender

class AnalyticsLayer:
    """分析决策层 - 六层架构的分析决策层"""
    
    def __init__(self, concepts_data_path=None):
        """初始化分析决策层"""
        # 使用现有的智能推荐器
        self.recommender = SmartRecommender(concepts_data_path)
        
        # 方法权重（可根据历史数据动态调整）
        self.method_weights = {
            '矛盾': 1.0,
            '实践': 0.9,
            '调查': 0.8,
            '战略': 0.85,
            '群众': 0.75,
            '综合': 0.95  # 综合方法默认权重较高
        }
        
        # 问题类型分类器（简单实现）
        self.problem_categories = {
            '矛盾问题': ['矛盾', '冲突', '对立', '问题', '分歧', '争执'],
            '实践问题': ['如何做', '怎样', '方法', '步骤', '操作', '实施'],
            '调查问题': ['调查', '研究', '了解', '数据', '信息', '调研'],
            '战略问题': ['战略', '规划', '长远', '目标', '方向', '计划'],
            '群众问题': ['团队', '管理', '群众', '员工', '组织', '协作'],
            '综合问题': ['分析', '解决', '处理', '评估', '判断', '考虑']
        }
        
        # 用户历史偏好（模拟）
        self.user_preferences = {}
    
    def analyze_problem(self, problem_text: str, user_id: str = "default_user") -> Dict[str, Any]:
        """
        分析问题并推荐方法
        
        Args:
            problem_text: 问题文本
            user_id: 用户ID
            
        Returns:
            分析结果
        """
        # 1. 提取关键词
        keywords = self.recommender.extract_keywords(problem_text)
        
        # 2. 推荐方法
        recommendations = self.recommender.recommend_methods(problem_text)
        
        # 3. 分析问题类型
        problem_category = self._categorize_problem(problem_text)
        
        # 4. 考虑用户历史偏好
        user_adjusted_recommendations = self._adjust_for_user_preferences(recommendations, user_id)
        
        # 5. 生成分析报告
        analysis_report = self._generate_analysis_report(
            problem_text, 
            keywords, 
            user_adjusted_recommendations, 
            problem_category
        )
        
        return {
            'success': True,
            'problem': problem_text,
            'keywords': keywords,
            'recommendations': user_adjusted_recommendations,
            'problem_category': problem_category,
            'analysis_report': analysis_report,
            'suggested_action': self._get_suggested_action(user_adjusted_recommendations)
        }
    
    def recommend_specific_method(self, problem_text: str, method_name: str) -> Dict[str, Any]:
        """
        推荐特定方法的分析
        
        Args:
            problem_text: 问题文本
            method_name: 指定的方法名称
            
        Returns:
            特定方法分析结果
        """
        # 验证方法名称
        valid_methods = ['矛盾', '实践', '调查', '战略', '群众', '综合']
        if method_name not in valid_methods:
            return {
                'success': False,
                'error': f"无效的方法名称: {method_name}",
                'valid_methods': valid_methods
            }
        
        # 即使指定了方法，也进行智能分析
        analysis = self.analyze_problem(problem_text)
        
        # 检查推荐是否匹配指定方法
        primary_recommendation = analysis['recommendations']['primary']
        confidence = analysis['recommendations']['confidence']
        
        if primary_recommendation['method'] == method_name:
            match_status = 'exact_match'
            match_confidence = confidence
        else:
            # 计算指定方法的推荐度
            method_recommendations = analysis['recommendations']['all_methods']
            specified_method_score = next(
                (m['score'] for m in method_recommendations if m['method'] == method_name), 
                0.0
            )
            match_status = 'specified_different'
            match_confidence = specified_method_score
        
        return {
            'success': True,
            'method': method_name,
            'problem': problem_text,
            'analysis': analysis,
            'match_status': match_status,
            'match_confidence': match_confidence,
            'recommendation': {
                'specified_method': method_name,
                'primary_recommendation': primary_recommendation['method'],
                'confidence_difference': abs(confidence - match_confidence)
            }
        }
    
    def compare_methods(self, problem_text: str, method_list: List[str] = None) -> Dict[str, Any]:
        """
        比较多个方法对同一问题的适用性
        
        Args:
            problem_text: 问题文本
            method_list: 要比较的方法列表
            
        Returns:
            方法比较结果
        """
        if method_list is None:
            method_list = ['矛盾', '实践', '调查', '战略', '群众', '综合']
        
        # 分析问题
        analysis = self.analyze_problem(problem_text)
        all_recommendations = analysis['recommendations']['all_methods']
        
        # 筛选指定方法
        specified_recommendations = [
            rec for rec in all_recommendations 
            if rec['method'] in method_list
        ]
        
        # 按推荐度排序
        specified_recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        # 生成对比分析
        comparison = self._generate_method_comparison(problem_text, specified_recommendations)
        
        return {
            'success': True,
            'problem': problem_text,
            'compared_methods': method_list,
            'recommendations': specified_recommendations,
            'comparison_analysis': comparison,
            'best_method': specified_recommendations[0] if specified_recommendations else None
        }
    
    def update_user_preference(self, user_id: str, method_name: str, feedback_score: float):
        """
        更新用户偏好
        
        Args:
            user_id: 用户ID
            method_name: 方法名称
            feedback_score: 反馈评分（0.0-1.0）
        """
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        
        user_prefs = self.user_preferences[user_id]
        
        if method_name not in user_prefs:
            user_prefs[method_name] = {
                'count': 0,
                'total_score': 0.0,
                'average_score': 0.0
            }
        
        pref_data = user_prefs[method_name]
        pref_data['count'] += 1
        pref_data['total_score'] += feedback_score
        pref_data['average_score'] = pref_data['total_score'] / pref_data['count']
    
    def _categorize_problem(self, problem_text: str) -> str:
        """分类问题类型"""
        problem_text_lower = problem_text.lower()
        
        max_matches = 0
        best_category = '综合问题'
        
        for category, keywords in self.problem_categories.items():
            matches = sum(1 for keyword in keywords if keyword in problem_text_lower)
            if matches > max_matches:
                max_matches = matches
                best_category = category
        
        return best_category
    
    def _adjust_for_user_preferences(self, recommendations: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """根据用户偏好调整推荐"""
        if user_id not in self.user_preferences:
            return recommendations
        
        user_prefs = self.user_preferences[user_id]
        
        # 复制推荐结果
        adjusted = recommendations.copy()
        
        # 调整主要推荐
        primary_method = adjusted['primary']['method']
        if primary_method in user_prefs:
            user_score = user_prefs[primary_method]['average_score']
            # 如果用户评分较低，考虑调整推荐
            if user_score < 0.5:
                # 寻找替代方法
                all_methods = adjusted['all_methods']
                alternative_methods = [
                    m for m in all_methods 
                    if m['method'] != primary_method and m['score'] > 0.3
                ]
                
                if alternative_methods:
                    # 选择用户评分较高的替代方法
                    alternative_methods.sort(
                        key=lambda x: user_prefs.get(x['method'], {}).get('average_score', 0.0), 
                        reverse=True
                    )
                    best_alternative = alternative_methods[0]
                    
                    # 调整主要推荐
                    adjusted['primary'] = best_alternative
                    adjusted['confidence'] = best_alternative['score']
                    adjusted['adjustment_reason'] = f"用户对'{primary_method}'评分较低({user_score:.2f})，调整为'{best_alternative['method']}'"
        
        return adjusted
    
    def _generate_analysis_report(self, problem_text: str, keywords: List[str], 
                                recommendations: Dict[str, Any], problem_category: str) -> str:
        """生成分析报告"""
        report = f"## 🔍 问题分析报告\n\n"
        report += f"**问题**: {problem_text}\n\n"
        report += f"**问题类型**: {problem_category}\n\n"
        report += f"**提取关键词**: {', '.join(keywords[:10])}\n\n"
        
        primary = recommendations['primary']
        confidence = recommendations.get('confidence', 0.0)
        
        report += f"## 🎯 智能推荐\n\n"
        report += f"**推荐方法**: {primary['method']} (置信度: {confidence*100:.1f}%)\n\n"
        report += f"**推荐理由**: {primary.get('reason', '基于问题内容分析')}\n\n"
        
        if 'adjustment_reason' in recommendations:
            report += f"**调整说明**: {recommendations['adjustment_reason']}\n\n"
        
        report += "## 📊 所有方法推荐度\n\n"
        for rec in recommendations['all_methods'][:5]:  # 显示前5个
            score_percent = rec['score'] * 100
            bar_length = int(score_percent / 5)  # 每5%一个字符
            bar = '█' * bar_length + '░' * (20 - bar_length)
            report += f"- **{rec['method']}**: {score_percent:.1f}% {bar}\n"
        
        return report
    
    def _get_suggested_action(self, recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """获取建议的下一步操作"""
        primary_method = recommendations['primary']['method']
        
        actions = {
            '矛盾': {
                'action': '进行矛盾分析',
                'command': f'/mao analyze --method=矛盾',
                'learn': '学习矛盾论专题'
            },
            '实践': {
                'action': '进行实践指导',
                'command': f'/mao analyze --method=实践',
                'learn': '学习实践论专题'
            },
            '调查': {
                'action': '进行调查研究',
                'command': f'/mao analyze --method=调查',
                'learn': '学习调查研究方法'
            },
            '战略': {
                'action': '进行战略分析',
                'command': f'/mao analyze --method=战略',
                'learn': '学习持久战战略'
            },
            '群众': {
                'action': '进行群众工作分析',
                'command': f'/mao analyze --method=群众',
                'learn': '学习群众路线专题'
            },
            '综合': {
                'action': '进行综合分析',
                'command': f'/mao analyze',
                'learn': '学习综合方法论'
            }
        }
        
        return actions.get(primary_method, actions['综合'])
    
    def _generate_method_comparison(self, problem_text: str, recommendations: List[Dict[str, Any]]) -> str:
        """生成方法对比分析"""
        if not recommendations:
            return "没有可对比的方法"
        
        comparison = f"## 🔄 方法对比分析\n\n"
        comparison += f"**问题**: {problem_text}\n\n"
        comparison += "### 📊 方法适用性对比\n\n"
        
        for rec in recommendations:
            score_percent = rec['score'] * 100
            comparison += f"#### {rec['method']}方法\n"
            comparison += f"- **推荐度**: {score_percent:.1f}%\n"
            comparison += f"- **适用场景**: {rec.get('reason', '基于关键词匹配')}\n"
            comparison += f"- **优势**: {self._get_method_advantages(rec['method'])}\n\n"
        
        # 给出建议
        best_method = recommendations[0]
        comparison += f"### 💡 使用建议\n\n"
        comparison += f"**推荐使用**: **{best_method['method']}方法**\n"
        comparison += f"**理由**: 推荐度最高({best_method['score']*100:.1f}%)，最适合当前问题\n"
        comparison += f"**使用命令**: `/mao analyze --method={best_method['method']}`\n"
        
        return comparison
    
    def _get_method_advantages(self, method_name: str) -> str:
        """获取方法优势"""
        advantages = {
            '矛盾': '擅长识别主要矛盾，解决复杂冲突问题',
            '实践': '注重实际操作性，指导具体工作实施',
            '调查': '强调事实依据，确保决策科学性',
            '战略': '着眼长远发展，制定系统性规划',
            '群众': '关注人的因素，促进团队协作',
            '综合': '多角度分析，提供全面解决方案'
        }
        return advantages.get(method_name, '通用问题分析')


# 测试代码
if __name__ == "__main__":
    analytics = AnalyticsLayer()
    
    # 测试问题分析
    print("问题分析测试:")
    result = analytics.analyze_problem("分析公司部门协作矛盾")
    print(f"问题: {result['problem']}")
    print(f"推荐方法: {result['recommendations']['primary']['method']}")
    print(f"置信度: {result['recommendations']['confidence']*100:.1f}%")
    
    # 测试方法比较
    print("\n\n方法比较测试:")
    comparison = analytics.compare_methods("分析公司部门协作矛盾", ['矛盾', '实践', '群众'])
    print(f"对比方法: {comparison['compared_methods']}")
    print(f"最佳方法: {comparison['best_method']['method']}")
    
    # 测试特定方法推荐
    print("\n\n特定方法测试:")
    specific = analytics.recommend_specific_method("分析公司部门协作矛盾", "群众")
    print(f"指定方法: {specific['method']}")
    print(f"匹配状态: {specific['match_status']}")
    print(f"匹配置信度: {specific['match_confidence']*100:.1f}%")