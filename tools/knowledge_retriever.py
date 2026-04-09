#!/usr/bin/env python3
"""
知识检索层

负责概念查询、学习内容检索、案例搜索等知识检索功能。
属于六层架构中的知识检索层。
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

class KnowledgeRetriever:
    """知识检索器 - 六层架构的知识检索层"""
    
    def __init__(self, data_dir=None):
        """初始化知识检索器"""
        # 设置数据目录
        if data_dir is None:
            self.data_dir = Path(__file__).parent.parent / 'data'
        else:
            self.data_dir = Path(data_dir)
        
        # 确保数据目录存在
        self.data_dir.mkdir(exist_ok=True)
        
        # 加载学习路径数据
        self.learning_paths = self._load_learning_paths()
        
        # 加载概念词典
        self.concept_dictionary = self._load_concept_dictionary()
        
        # 用户学习进度（模拟，实际应持久化）
        self.user_progress = {}
    
    def _load_learning_paths(self) -> Dict[str, Any]:
        """加载学习路径数据"""
        learning_paths_file = self.data_dir / 'learning_paths.json'
        
        if learning_paths_file.exists():
            try:
                with open(learning_paths_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载学习路径失败: {e}")
        
        # 返回默认学习路径结构
        return {
            '入门': {
                'name': '入门路径',
                'description': '15分钟快速了解毛泽东方法论核心',
                'duration_minutes': 15,
                'target_audience': '完全新手，零基础用户',
                'modules': [
                    {'name': '毛泽东方法论概述', 'duration_minutes': 3},
                    {'name': '矛盾分析法基础', 'duration_minutes': 5},
                    {'name': '快速应用示例', 'duration_minutes': 7}
                ]
            },
            '基础': {
                'name': '基础路径',
                'description': '1小时系统学习毛泽东方法论体系',
                'duration_minutes': 60,
                'target_audience': '希望系统学习的新手用户',
                'modules': [
                    {'name': '实践论核心思想', 'duration_minutes': 15},
                    {'name': '矛盾论深度解析', 'duration_minutes': 20},
                    {'name': '调查研究方法', 'duration_minutes': 15},
                    {'name': '综合应用练习', 'duration_minutes': 10}
                ]
            }
        }
    
    def _load_concept_dictionary(self) -> Dict[str, Any]:
        """加载概念词典"""
        concept_file = Path(__file__).parent / 'concept_dictionary.json'
        
        if concept_file.exists():
            try:
                with open(concept_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载概念词典失败: {e}")
        
        # 返回默认概念结构
        return {
            'concepts': {},
            'categories': [],
            'total_count': 0
        }
    
    def get_learning_path(self, path_name: str = None) -> Dict[str, Any]:
        """
        获取学习路径信息
        
        Args:
            path_name: 路径名称（入门、基础、进阶、专业）
            
        Returns:
            学习路径信息
        """
        if path_name is None:
            # 返回所有路径
            return {
                'success': True,
                'paths': self.learning_paths,
                'recommended_path': self._recommend_learning_path()
            }
        
        if path_name not in self.learning_paths:
            return {
                'success': False,
                'error': f"未知的学习路径: {path_name}",
                'available_paths': list(self.learning_paths.keys())
            }
        
        path_info = self.learning_paths[path_name].copy()
        
        # 添加用户进度信息
        user_id = "default_user"
        if user_id in self.user_progress and path_name in self.user_progress[user_id]:
            path_info['user_progress'] = self.user_progress[user_id][path_name]
        
        return {
            'success': True,
            'path': path_info,
            'total_paths': len(self.learning_paths)
        }
    
    def get_concept_info(self, concept_name: str = None, search_term: str = None) -> Dict[str, Any]:
        """
        获取概念信息
        
        Args:
            concept_name: 概念名称（精确查询）
            search_term: 搜索关键词（模糊查询）
            
        Returns:
            概念信息
        """
        if concept_name:
            # 精确查询
            concept = self.concept_dictionary.get('concepts', {}).get(concept_name)
            if not concept:
                # 尝试模糊匹配
                matched_concepts = self._fuzzy_search_concept(concept_name)
                if matched_concepts:
                    return {
                        'success': True,
                        'matched_concepts': matched_concepts,
                        'exact_match': False
                    }
                
                return {
                    'success': False,
                    'error': f"未找到概念: {concept_name}",
                    'suggestions': self._get_similar_concepts(concept_name)
                }
            
            # 获取相关概念
            related_concepts = self._get_related_concepts(concept_name)
            
            return {
                'success': True,
                'concept': concept,
                'related_concepts': related_concepts,
                'exact_match': True
            }
        
        elif search_term:
            # 模糊查询
            matched_concepts = self._fuzzy_search_concept(search_term)
            
            return {
                'success': True,
                'search_term': search_term,
                'matched_concepts': matched_concepts,
                'match_count': len(matched_concepts)
            }
        
        else:
            # 返回所有概念
            concepts = self.concept_dictionary.get('concepts', {})
            categories = self.concept_dictionary.get('categories', [])
            
            return {
                'success': True,
                'total_concepts': len(concepts),
                'categories': categories,
                'concept_sample': dict(list(concepts.items())[:10])  # 前10个示例
            }
    
    def get_user_progress(self, user_id: str, path_name: str = None) -> Dict[str, Any]:
        """
        获取用户学习进度
        
        Args:
            user_id: 用户ID
            path_name: 学习路径名称
            
        Returns:
            学习进度信息
        """
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        
        if path_name:
            if path_name not in self.user_progress[user_id]:
                return {
                    'success': True,
                    'path': path_name,
                    'progress': 0,
                    'completed_modules': [],
                    'total_modules': len(self.learning_paths.get(path_name, {}).get('modules', []))
                }
            
            progress_data = self.user_progress[user_id][path_name]
            total_modules = len(self.learning_paths.get(path_name, {}).get('modules', []))
            progress_percentage = int((len(progress_data.get('completed_modules', [])) / max(total_modules, 1)) * 100)
            
            return {
                'success': True,
                'path': path_name,
                'progress': progress_percentage,
                'completed_modules': progress_data.get('completed_modules', []),
                'total_modules': total_modules,
                'last_accessed': progress_data.get('last_accessed')
            }
        else:
            # 返回所有路径的进度
            all_progress = {}
            for path in self.learning_paths.keys():
                progress = self.get_user_progress(user_id, path)
                if progress['success']:
                    all_progress[path] = progress
            
            return {
                'success': True,
                'user_id': user_id,
                'all_progress': all_progress,
                'overall_progress': self._calculate_overall_progress(user_id)
            }
    
    def update_user_progress(self, user_id: str, path_name: str, module_name: str) -> Dict[str, Any]:
        """
        更新用户学习进度
        
        Args:
            user_id: 用户ID
            path_name: 学习路径名称
            module_name: 完成的模块名称
            
        Returns:
            更新结果
        """
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        
        if path_name not in self.user_progress[user_id]:
            self.user_progress[user_id][path_name] = {
                'completed_modules': [],
                'started_at': None,
                'last_accessed': None
            }
        
        path_data = self.user_progress[user_id][path_name]
        
        # 添加完成的模块（如果尚未完成）
        if module_name not in path_data['completed_modules']:
            path_data['completed_modules'].append(module_name)
        
        # 更新时间戳
        from datetime import datetime
        path_data['last_accessed'] = datetime.now().isoformat()
        
        # 计算新进度
        total_modules = len(self.learning_paths.get(path_name, {}).get('modules', []))
        progress_percentage = int((len(path_data['completed_modules']) / max(total_modules, 1)) * 100)
        
        return {
            'success': True,
            'user_id': user_id,
            'path': path_name,
            'completed_module': module_name,
            'new_progress': progress_percentage,
            'total_completed': len(path_data['completed_modules']),
            'total_modules': total_modules
        }
    
    def _fuzzy_search_concept(self, search_term: str) -> List[Dict[str, Any]]:
        """模糊搜索概念"""
        matched_concepts = []
        concepts = self.concept_dictionary.get('concepts', {})
        
        for name, info in concepts.items():
            if search_term.lower() in name.lower():
                matched_concepts.append({
                    'name': name,
                    'description': info.get('description', ''),
                    'category': info.get('category', '其他')
                })
            elif 'description' in info and search_term.lower() in info['description'].lower():
                matched_concepts.append({
                    'name': name,
                    'description': info.get('description', ''),
                    'category': info.get('category', '其他'),
                    'matched_in_description': True
                })
        
        return matched_concepts
    
    def _get_similar_concepts(self, concept_name: str) -> List[str]:
        """获取相似概念（简单实现）"""
        # 这里可以使用更复杂的相似度算法
        # 目前返回所有包含相同字符的概念
        concepts = list(self.concept_dictionary.get('concepts', {}).keys())
        return [c for c in concepts if any(char in c for char in concept_name)][:5]
    
    def _get_related_concepts(self, concept_name: str) -> List[Dict[str, Any]]:
        """获取相关概念"""
        # 这里可以基于概念关系网络返回相关概念
        # 目前返回同类的其他概念
        concept_info = self.concept_dictionary.get('concepts', {}).get(concept_name, {})
        category = concept_info.get('category', '其他')
        
        related = []
        concepts = self.concept_dictionary.get('concepts', {})
        
        for name, info in concepts.items():
            if name != concept_name and info.get('category') == category:
                related.append({
                    'name': name,
                    'description': info.get('description', '')[:50] + '...',
                    'category': category
                })
        
        return related[:5]
    
    def _recommend_learning_path(self) -> Dict[str, Any]:
        """推荐学习路径"""
        # 简单推荐逻辑：根据用户历史推荐
        # 目前返回入门路径
        return {
            'path': '入门',
            'reason': '适合新手快速入门',
            'estimated_time': '15分钟'
        }
    
    def _calculate_overall_progress(self, user_id: str) -> int:
        """计算总体学习进度"""
        if user_id not in self.user_progress:
            return 0
        
        total_modules = 0
        completed_modules = 0
        
        for path_name, path_info in self.learning_paths.items():
            modules = path_info.get('modules', [])
            total_modules += len(modules)
            
            if path_name in self.user_progress[user_id]:
                completed = len(self.user_progress[user_id][path_name].get('completed_modules', []))
                completed_modules += completed
        
        if total_modules == 0:
            return 0
        
        return int((completed_modules / total_modules) * 100)


# 测试代码
if __name__ == "__main__":
    retriever = KnowledgeRetriever()
    
    # 测试学习路径
    print("学习路径测试:")
    paths = retriever.get_learning_path()
    print(f"可用路径: {list(paths.get('paths', {}).keys())}")
    
    # 测试概念查询
    print("\n概念查询测试:")
    concepts = retriever.get_concept_info()
    print(f"总概念数: {concepts.get('total_concepts', 0)}")
    
    # 测试用户进度
    print("\n用户进度测试:")
    progress = retriever.get_user_progress("test_user", "入门")
    print(f"入门路径进度: {progress.get('progress', 0)}%")
    
    # 测试进度更新
    print("\n进度更新测试:")
    update = retriever.update_user_progress("test_user", "入门", "毛泽东方法论概述")
    print(f"更新后进度: {update.get('new_progress', 0)}%")