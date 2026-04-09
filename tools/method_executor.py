#!/usr/bin/env python3
"""
方法执行层

负责执行具体的分析方法，包括矛盾分析、实践论方法、调查研究法等。
属于六层架构中的方法执行层。
"""

import sys
import os
from typing import Dict, List, Any, Optional
import json

class MethodExecutor:
    """方法执行器 - 六层架构的方法执行层"""
    
    def __init__(self, knowledge_base_path=None):
        """初始化方法执行器"""
        # 加载知识库
        self.knowledge_base = self._load_knowledge_base(knowledge_base_path)
        
        # 分析方法定义
        self.methods = {
            '矛盾': {
                'name': '矛盾分析法',
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
                'name': '实践论方法',
                'description': '遵循"实践-认识-再实践"循环，指导具体工作',
                'steps': [
                    '1. 实践探索：进行小范围实践，获取感性认识',
                    '2. 总结提升：总结经验，形成理性认识',
                    '3. 指导实践：用理性认识指导更大范围的实践',
                    '4. 循环验证：实践-认识-再实践循环，逐步完善'
                ],
                'quote': '实践、认识、再实践、再认识，这种形式，循环往复以至无穷。'
            },
            '调查': {
                'name': '调查研究法',
                'description': '没有调查就没有发言权，典型与普遍结合',
                'steps': [
                    '1. 制定计划：明确调查目的和范围',
                    '2. 深入实际：亲自到一线，与群众面对面交流',
                    '3. 典型调查：选择典型单位进行深入调查',
                    '4. 普遍调查：扩大调查范围，了解普遍情况',
                    '5. 分析综合：材料要丰富，观点要准确'
                ],
                'quote': '没有调查，就没有发言权；没有正确的调查，同样没有发言权。'
            },
            '战略': {
                'name': '战略思维法',
                'description': '持久战思维，战略藐视战术重视',
                'steps': [
                    '1. 战略分析：分析敌我力量对比',
                    '2. 阶段划分：防御 → 相持 → 反攻',
                    '3. 战术运用：集中优势兵力，各个歼灭敌人',
                    '4. 根据地建设：建立巩固的根据地，逐步发展'
                ],
                'quote': '在战略上要藐视敌人，在战术上要重视敌人。'
            },
            '群众': {
                'name': '群众路线法',
                'description': '从群众中来，到群众中去',
                'steps': [
                    '1. 深入群众：了解群众的真实想法和需求',
                    '2. 集中智慧：集中群众的智慧和意见',
                    '3. 形成决策：将群众意见转化为科学决策',
                    '4. 发动群众：将决策变为群众的自觉行动'
                ],
                'quote': '从群众中来，到群众中去。'
            },
            '综合': {
                'name': '综合分析法',
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
    
    def _load_knowledge_base(self, path):
        """加载知识库"""
        # 简单的内置知识库
        return {}
    
    def execute_method(self, method_name: str, problem: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行分析方法
        
        Args:
            method_name: 方法名称（矛盾、实践、调查等）
            problem: 问题描述
            context: 执行上下文
            
        Returns:
            执行结果
        """
        if method_name not in self.methods:
            return {
                'success': False,
                'error': f"未知的分析方法: {method_name}",
                'available_methods': list(self.methods.keys())
            }
        
        method_info = self.methods[method_name]
        
        # 构建响应
        result = {
            'success': True,
            'method': method_name,
            'method_info': method_info,
            'problem': problem,
            'analysis': self._generate_analysis(method_name, problem, method_info),
            'recommended_next_step': self._get_recommended_next_step(method_name)
        }
        
        return result
    
    def _generate_analysis(self, method_name: str, problem: str, method_info: Dict[str, Any]) -> str:
        """生成分析内容"""
        # 这里可以更复杂地根据问题生成具体的分析
        # 目前使用模板方法
        
        analysis = f"## 🔍 {method_info['name']}分析\n\n"
        analysis += f"**问题**: {problem}\n\n"
        analysis += f"**方法描述**: {method_info['description']}\n\n"
        analysis += "### 📋 分析步骤\n\n"
        
        for step in method_info['steps']:
            analysis += f"{step}\n"
        
        analysis += f"\n**核心原则**: {method_info['quote']}\n"
        
        return analysis
    
    def _get_recommended_next_step(self, method_name: str) -> Dict[str, Any]:
        """获取推荐下一步"""
        recommendations = {
            '矛盾': {
                'learn': '矛盾论专题',
                'concepts': ['主要矛盾', '次要矛盾', '矛盾转化', '对立统一'],
                'compare_with': '实践论'
            },
            '实践': {
                'learn': '实践论专题',
                'concepts': ['实践论', '认识论', '循环提升', '理论联系实际'],
                'compare_with': '矛盾论'
            },
            '调查': {
                'learn': '调查研究方法',
                'concepts': ['调查研究', '典型调查', '普遍调查', '没有调查就没有发言权'],
                'compare_with': '群众路线'
            },
            '战略': {
                'learn': '持久战战略',
                'concepts': ['持久战', '战略藐视战术重视', '集中优势兵力', '根据地'],
                'compare_with': '战术方法'
            },
            '群众': {
                'learn': '群众路线专题',
                'concepts': ['群众路线', '从群众中来', '到群众中去', '民主集中制'],
                'compare_with': '调查研究'
            },
            '综合': {
                'learn': '综合方法论',
                'concepts': ['综合分析', '多角度分析', '方法组合', '整体解决'],
                'compare_with': '所有单一方法'
            }
        }
        
        return recommendations.get(method_name, {})
    
    def execute_multiple_methods(self, method_names: List[str], problem: str) -> Dict[str, Any]:
        """执行多个方法，进行对比分析"""
        results = {}
        comparisons = []
        
        for method_name in method_names:
            if method_name in self.methods:
                result = self.execute_method(method_name, problem)
                results[method_name] = result
        
        # 生成对比分析
        if len(results) > 1:
            comparisons = self._generate_comparison(results, problem)
        
        return {
            'success': True,
            'results': results,
            'comparisons': comparisons,
            'recommended_method': self._recommend_best_method(results)
        }
    
    def _generate_comparison(self, results: Dict[str, Any], problem: str) -> List[str]:
        """生成方法对比"""
        comparisons = []
        comparisons.append(f"## 🔄 方法对比分析: {problem}")
        comparisons.append("")
        
        for method_name, result in results.items():
            method_info = self.methods.get(method_name, {})
            comparisons.append(f"### 📊 {method_info.get('name', method_name)}")
            comparisons.append(f"**特点**: {method_info.get('description', '')}")
            comparisons.append(f"**适用场景**: {self._get_application_scenarios(method_name)}")
            comparisons.append("")
        
        return comparisons
    
    def _get_application_scenarios(self, method_name: str) -> str:
        """获取方法适用场景"""
        scenarios = {
            '矛盾': '识别复杂问题中的主要矛盾、分析对立统一关系、解决冲突',
            '实践': '指导具体工作、改进工作流程、理论与实践结合',
            '调查': '收集信息、了解实际情况、制定调研方案',
            '战略': '制定长期计划、应对竞争、资源配置决策',
            '群众': '群众工作、团队建设、民主决策',
            '综合': '复杂问题分析、多角度决策、整体解决方案'
        }
        return scenarios.get(method_name, '通用问题分析')
    
    def _recommend_best_method(self, results: Dict[str, Any]) -> str:
        """推荐最佳方法（简单实现，后续可优化）"""
        if not results:
            return '综合'
        
        # 简单规则：如果有矛盾分析，优先推荐矛盾方法
        if '矛盾' in results:
            return '矛盾'
        
        # 否则返回第一个方法
        return list(results.keys())[0]


# 测试代码
if __name__ == "__main__":
    executor = MethodExecutor()
    
    # 测试单一方法
    result = executor.execute_method('矛盾', '分析公司部门协作问题')
    print("单一方法测试:")
    print(json.dumps(result, ensure_ascii=False, indent=2)[:500] + "...")
    
    # 测试多方法
    print("\n\n多方法测试:")
    multi_result = executor.execute_multiple_methods(['矛盾', '实践'], '分析项目进度问题')
    print(json.dumps(multi_result, ensure_ascii=False, indent=2)[:500] + "...")