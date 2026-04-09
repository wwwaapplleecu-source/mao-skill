#!/usr/bin/env python3
"""
毛泽东.skill 学习系统

提供渐进式学习路径，管理学习进度，提供个性化学习建议
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime

class LearningSystem:
    """学习系统管理器"""
    
    def __init__(self, config_path="data/learning_paths.json"):
        """初始化学习系统"""
        self.config_path = Path(config_path)
        self.learning_config = self.load_config()
        
        # 用户学习状态（模拟，实际应用中应该持久化存储）
        self.user_states = {}
        
        # 默认用户（模拟）
        self.default_user_id = "default_user"
        
    def load_config(self) -> Dict[str, Any]:
        """加载学习配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载学习配置失败: {e}")
            # 返回默认配置
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "learning_paths": {
                "入门": {
                    "name": "入门路径",
                    "description": "15分钟快速了解",
                    "modules": []
                }
            }
        }
    
    def get_user_state(self, user_id: str = None) -> Dict[str, Any]:
        """获取用户学习状态"""
        if user_id is None:
            user_id = self.default_user_id
        
        if user_id not in self.user_states:
            # 初始化用户状态
            self.user_states[user_id] = {
                "user_id": user_id,
                "current_path": None,
                "completed_modules": set(),
                "current_module_index": 0,
                "learning_history": [],
                "started_paths": {},
                "last_accessed": datetime.now().isoformat(),
                "achievements": []
            }
        
        return self.user_states[user_id]
    
    def update_user_state(self, user_id: str, updates: Dict[str, Any]):
        """更新用户学习状态"""
        state = self.get_user_state(user_id)
        state.update(updates)
        state["last_accessed"] = datetime.now().isoformat()
    
    def get_learning_paths(self) -> List[Dict[str, Any]]:
        """获取所有学习路径"""
        paths = []
        for path_id, path_info in self.learning_config.get("learning_paths", {}).items():
            path_data = {
                "id": path_id,
                "name": path_info.get("name", path_id),
                "description": path_info.get("description", ""),
                "duration_minutes": path_info.get("duration_minutes", 0),
                "target_audience": path_info.get("target_audience", ""),
                "module_count": len(path_info.get("modules", [])),
                "learning_goals": path_info.get("learning_goals", [])
            }
            paths.append(path_data)
        
        return sorted(paths, key=lambda x: ["入门", "基础", "进阶", "专业"].index(x["id"]) 
                     if x["id"] in ["入门", "基础", "进阶", "专业"] else 999)
    
    def get_path_details(self, path_id: str) -> Optional[Dict[str, Any]]:
        """获取学习路径详情"""
        return self.learning_config.get("learning_paths", {}).get(path_id)
    
    def start_learning_path(self, user_id: str, path_id: str) -> Dict[str, Any]:
        """开始学习路径"""
        path_details = self.get_path_details(path_id)
        if not path_details:
            return {"error": f"找不到学习路径: {path_id}"}
        
        state = self.get_user_state(user_id)
        
        # 记录开始学习
        if path_id not in state["started_paths"]:
            state["started_paths"][path_id] = {
                "started_at": datetime.now().isoformat(),
                "completed_modules": [],
                "current_module": 0,
                "progress_percentage": 0
            }
        
        self.update_user_state(user_id, {
            "current_path": path_id,
            "current_module_index": 0
        })
        
        # 获取第一个模块
        modules = path_details.get("modules", [])
        if modules:
            first_module = modules[0]
            return {
                "path_id": path_id,
                "path_name": path_details["name"],
                "module_index": 0,
                "module": first_module,
                "total_modules": len(modules),
                "message": f"已开始学习{path_details['name']}，第一个模块：{first_module.get('title', '')}"
            }
        else:
            return {"error": "该学习路径没有设置学习模块"}
    
    def get_current_module(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户当前学习模块"""
        state = self.get_user_state(user_id)
        current_path = state.get("current_path")
        
        if not current_path:
            return None
        
        path_details = self.get_path_details(current_path)
        if not path_details:
            return None
        
        modules = path_details.get("modules", [])
        current_index = state.get("current_module_index", 0)
        
        if current_index < len(modules):
            return {
                "path_id": current_path,
                "path_name": path_details["name"],
                "module_index": current_index,
                "module": modules[current_index],
                "total_modules": len(modules),
                "progress_percentage": int((current_index / len(modules)) * 100) if modules else 0
            }
        
        return None
    
    def complete_current_module(self, user_id: str, practice_answer: str = "") -> Dict[str, Any]:
        """完成当前学习模块"""
        state = self.get_user_state(user_id)
        current_path = state.get("current_path")
        
        if not current_path:
            return {"error": "用户没有正在进行的学习路径"}
        
        path_details = self.get_path_details(current_path)
        if not path_details:
            return {"error": f"找不到学习路径: {current_path}"}
        
        modules = path_details.get("modules", [])
        current_index = state.get("current_module_index", 0)
        
        if current_index >= len(modules):
            return {"error": "已经完成所有模块"}
        
        # 标记模块完成
        module_id = modules[current_index].get("id", f"module_{current_index}")
        module_completed = {
            "module_id": module_id,
            "module_title": modules[current_index].get("title", ""),
            "completed_at": datetime.now().isoformat(),
            "practice_answer": practice_answer
        }
        
        # 添加到完成列表
        state["completed_modules"].add(f"{current_path}:{module_id}")
        
        # 更新路径进度
        if current_path in state["started_paths"]:
            state["started_paths"][current_path]["completed_modules"].append(module_completed)
            state["started_paths"][current_path]["current_module"] = current_index + 1
            
            # 计算进度百分比
            progress = ((current_index + 1) / len(modules)) * 100
            state["started_paths"][current_path]["progress_percentage"] = int(progress)
        
        # 记录学习历史
        state["learning_history"].append({
            "timestamp": datetime.now().isoformat(),
            "action": "complete_module",
            "path_id": current_path,
            "module_id": module_id,
            "module_title": modules[current_index].get("title", "")
        })
        
        # 移动到下一个模块
        next_index = current_index + 1
        state["current_module_index"] = next_index
        
        self.update_user_state(user_id, state)
        
        # 检查是否完成整个路径
        if next_index >= len(modules):
            return self.complete_learning_path(user_id, current_path)
        
        # 返回下一个模块信息
        if next_index < len(modules):
            next_module = modules[next_index]
            return {
                "completed_module": modules[current_index].get("title", ""),
                "next_module": {
                    "title": next_module.get("title", ""),
                    "index": next_index,
                    "total": len(modules)
                },
                "progress_percentage": int((next_index / len(modules)) * 100),
                "message": f"恭喜完成模块！下一个：{next_module.get('title', '')}"
            }
        
        return {"message": "模块完成！"}
    
    def complete_learning_path(self, user_id: str, path_id: str) -> Dict[str, Any]:
        """完成整个学习路径"""
        path_details = self.get_path_details(path_id)
        if not path_details:
            return {"error": f"找不到学习路径: {path_id}"}
        
        state = self.get_user_state(user_id)
        
        # 记录成就
        achievement = {
            "achievement_id": f"complete_{path_id}",
            "name": f"完成{path_details['name']}",
            "description": f"成功完成{path_details['name']}学习路径",
            "earned_at": datetime.now().isoformat(),
            "reward": path_details.get("completion_reward", "")
        }
        
        state["achievements"].append(achievement)
        
        # 更新状态
        state["current_path"] = None
        state["current_module_index"] = 0
        
        self.update_user_state(user_id, state)
        
        return {
            "achievement": achievement,
            "message": f"🎉 恭喜完成{path_details['name']}！获得奖励：{achievement['reward']}"
        }
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """获取用户学习进度概览"""
        state = self.get_user_state(user_id)
        
        # 计算总体统计
        total_paths = len(self.learning_config.get("learning_paths", {}))
        started_paths = len(state.get("started_paths", {}))
        completed_modules = len(state.get("completed_modules", set()))
        
        # 计算每个路径的进度
        path_progress = []
        for path_id, path_info in self.learning_config.get("learning_paths", {}).items():
            path_data = {
                "path_id": path_id,
                "path_name": path_info.get("name", path_id),
                "started": path_id in state.get("started_paths", {}),
                "completed": False,
                "progress_percentage": 0
            }
            
            if path_id in state.get("started_paths", {}):
                path_data["progress_percentage"] = state["started_paths"][path_id].get("progress_percentage", 0)
                # 检查是否完成（进度100%）
                if path_data["progress_percentage"] >= 100:
                    path_data["completed"] = True
            
            path_progress.append(path_data)
        
        return {
            "user_id": user_id,
            "total_paths": total_paths,
            "started_paths": started_paths,
            "completed_modules": completed_modules,
            "achievements_count": len(state.get("achievements", [])),
            "path_progress": path_progress,
            "current_path": state.get("current_path"),
            "last_accessed": state.get("last_accessed"),
            "recommendations": self.get_learning_recommendations(user_id)
        }
    
    def get_learning_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """获取学习推荐"""
        state = self.get_user_state(user_id)
        recommendations = []
        
        # 如果没有开始任何路径，推荐入门路径
        if not state.get("started_paths"):
            entry_path = self.get_path_details("入门")
            if entry_path:
                recommendations.append({
                    "type": "start_path",
                    "path_id": "入门",
                    "path_name": entry_path.get("name", "入门"),
                    "reason": "建议从入门路径开始学习",
                    "priority": "high"
                })
        
        # 推荐下一个路径
        completed_paths = []
        for path_id, path_info in state.get("started_paths", {}).items():
            if path_info.get("progress_percentage", 0) >= 100:
                completed_paths.append(path_id)
        
        # 按顺序推荐路径
        path_order = ["入门", "基础", "进阶", "专业"]
        for path_id in path_order:
            if path_id not in state.get("started_paths", {}):
                path_details = self.get_path_details(path_id)
                if path_details:
                    recommendations.append({
                        "type": "start_path",
                        "path_id": path_id,
                        "path_name": path_details.get("name", path_id),
                        "reason": f"建议继续学习{path_details.get('name', path_id)}路径",
                        "priority": "medium"
                    })
                break
        
        # 推荐专题学习
        completed_modules = state.get("completed_modules", set())
        for topic_id, topic_info in self.learning_config.get("topics", {}).items():
            # 检查前置条件
            prerequisites = topic_info.get("prerequisites", [])
            prerequisites_met = all(
                any(f"{path}:module_" in str(completed_modules) for completed_modules in completed_modules)
                for path in prerequisites
            )
            
            if prerequisites_met:
                recommendations.append({
                    "type": "topic",
                    "topic_id": topic_id,
                    "topic_name": topic_info.get("name", topic_id),
                    "reason": f"符合前置条件，可以学习{topic_info.get('name', topic_id)}专题",
                    "priority": "low"
                })
        
        return recommendations[:5]  # 返回前5个推荐
    
    def get_topic_details(self, topic_id: str) -> Optional[Dict[str, Any]]:
        """获取专题学习详情"""
        return self.learning_config.get("topics", {}).get(topic_id)
    
    def format_learning_introduction(self) -> str:
        """格式化学习系统介绍"""
        paths = self.get_learning_paths()
        
        response = "## 🎓 毛泽东方法论学习系统\n\n"
        response += "欢迎使用渐进式毛泽东方法论学习系统！\n\n"
        
        response += "### 📚 学习路径概览\n\n"
        for path in paths:
            response += f"**{path['name']}** ({path['duration_minutes']}分钟)\n"
            response += f"- {path['description']}\n"
            response += f"- 目标人群: {path['target_audience']}\n"
            response += f"- 学习目标: {', '.join(path['learning_goals'][:2])}\n"
            response += f"- 使用命令: `/mao learn --path={path['id']}`\n\n"
        
        response += "### 🚀 快速开始\n"
        response += "1. **入门路径** (15分钟): `/mao learn --path=入门`\n"
        response += "2. **专题学习**: `/mao learn 矛盾论`\n"
        response += "3. **学习进度**: `/mao learn progress`\n"
        response += "4. **学习推荐**: `/mao learn recommendations`\n\n"
        
        response += "### 💡 学习建议\n"
        for tip in self.learning_config.get("learning_tips", {}).get("general", []):
            response += f"- {tip}\n"
        
        return response
    
    def format_path_details(self, path_id: str) -> str:
        """格式化学习路径详情"""
        path_details = self.get_path_details(path_id)
        if not path_details:
            return f"❌ 找不到学习路径: {path_id}"
        
        response = f"## 📚 {path_details['name']}\n\n"
        response += f"**描述**: {path_details.get('description', '')}\n\n"
        response += f"**时长**: {path_details.get('duration_minutes', 0)}分钟\n"
        response += f"**目标人群**: {path_details.get('target_audience', '')}\n\n"
        
        response += "### 🎯 学习目标\n"
        for goal in path_details.get("learning_goals", []):
            response += f"- {goal}\n"
        
        response += "\n### 📖 学习模块\n"
        modules = path_details.get("modules", [])
        for i, module in enumerate(modules, 1):
            response += f"{i}. **{module.get('title', '')}** ({module.get('duration_minutes', 0)}分钟)\n"
        
        response += "\n### 🚀 开始学习\n"
        response += f"使用命令: `/mao learn --path={path_id}` 开始学习\n"
        
        return response
    
    def format_module_content(self, module: Dict[str, Any]) -> str:
        """格式化模块内容"""
        response = f"## 📖 {module.get('title', '')}\n\n"
        
        content_type = module.get('content_type', 'text')
        content = module.get('content', '')
        
        if content_type == 'example':
            response += "### 📋 学习示例\n\n"
        elif content_type == 'case_study':
            response += "### 📊 案例分析\n\n"
        elif content_type == 'project':
            response += "### 🛠️ 实践项目\n\n"
        
        response += content
        
        if module.get('practice_question'):
            response += "\n\n### 💪 实践练习\n"
            response += f"**练习问题**: {module['practice_question']}\n"
            response += "**回答格式**: 完成模块后可以提交你的回答\n"
        
        return response
    
    def format_user_progress(self, user_id: str) -> str:
        """格式化用户学习进度"""
        progress = self.get_user_progress(user_id)
        
        response = "## 📊 学习进度概览\n\n"
        
        response += f"**已开始路径**: {progress['started_paths']}/{progress['total_paths']}\n"
        response += f"**已完成模块**: {progress['completed_modules']}个\n"
        response += f"**获得成就**: {progress['achievements_count']}个\n\n"
        
        if progress['current_path']:
            response += f"**当前学习路径**: {progress['current_path']}\n\n"
        
        response += "### 📈 路径进度\n"
        for path in progress['path_progress']:
            status_icon = "✅" if path['completed'] else "🔄" if path['started'] else "⏳"
            progress_bar = self._create_progress_bar(path['progress_percentage'])
            response += f"{status_icon} **{path['path_name']}**: {progress_bar} {path['progress_percentage']}%\n"
        
        if progress['achievements_count'] > 0:
            response += "\n### 🏆 已获成就\n"
            # 只显示最近3个成就
            state = self.get_user_state(user_id)
            recent_achievements = state.get('achievements', [])[-3:]
            for achievement in reversed(recent_achievements):
                response += f"🏅 **{achievement.get('name', '')}**\n"
                response += f"   {achievement.get('description', '')}\n"
        
        if progress['recommendations']:
            response += "\n### 💡 学习推荐\n"
            for rec in progress['recommendations']:
                priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                response += f"{priority_icon} **{rec.get('reason', '')}**\n"
                if rec['type'] == 'start_path':
                    response += f"   命令: `/mao learn --path={rec['path_id']}`\n"
                elif rec['type'] == 'topic':
                    response += f"   命令: `/mao learn {rec['topic_id']}`\n"
        
        return response
    
    def _create_progress_bar(self, percentage: int, width: int = 20) -> str:
        """创建进度条"""
        filled = int(width * percentage / 100)
        empty = width - filled
        return "█" * filled + "░" * empty

def test_learning_system():
    """测试学习系统"""
    print("🔍 测试毛泽东方法论学习系统\n")
    print("=" * 70)
    
    learning_system = LearningSystem()
    
    # 测试1：获取学习路径
    print("\n测试1：获取学习路径")
    print("-" * 40)
    paths = learning_system.get_learning_paths()
    for path in paths:
        print(f"{path['id']}: {path['name']} ({path['duration_minutes']}分钟)")
    
    # 测试2：开始学习路径
    print("\n\n测试2：开始学习路径")
    print("-" * 40)
    result = learning_system.start_learning_path("test_user", "入门")
    if "error" not in result:
        print(f"开始学习: {result['path_name']}")
        print(f"第一个模块: {result['module'].get('title', '')}")
    
    # 测试3：获取当前模块
    print("\n\n测试3：获取当前模块")
    print("-" * 40)
    current_module = learning_system.get_current_module("test_user")
    if current_module:
        print(f"当前模块: {current_module['module'].get('title', '')}")
        print(f"进度: {current_module['progress_percentage']}%")
    
    # 测试4：完成模块
    print("\n\n测试4：完成模块")
    print("-" * 40)
    result = learning_system.complete_current_module("test_user", "这是我的实践回答")
    if "error" not in result:
        print(f"完成模块: {result.get('completed_module', '')}")
        print(f"下一个模块: {result.get('next_module', {}).get('title', '')}")
    
    # 测试5：获取学习进度
    print("\n\n测试5：获取学习进度")
    print("-" * 40)
    progress = learning_system.get_user_progress("test_user")
    print(f"已开始路径: {progress['started_paths']}/{progress['total_paths']}")
    print(f"已完成模块: {progress['completed_modules']}")
    
    # 测试6：格式化输出
    print("\n\n测试6：格式化学习系统介绍")
    print("-" * 40)
    intro = learning_system.format_learning_introduction()
    print(intro[:500] + "..." if len(intro) > 500 else intro)
    
    print("\n" + "=" * 70)
    print("✅ 学习系统测试完成")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东方法论学习系统")
    parser.add_argument("--test", action="store_true", help="运行测试")
    parser.add_argument("--list-paths", action="store_true", help="列出学习路径")
    parser.add_argument("--path-details", help="查看路径详情")
    parser.add_argument("--user-progress", help="查看用户学习进度")
    
    args = parser.parse_args()
    
    learning_system = LearningSystem()
    
    if args.test:
        test_learning_system()
    elif args.list_paths:
        paths = learning_system.get_learning_paths()
        for path in paths:
            print(f"{path['id']}: {path['name']} ({path['duration_minutes']}分钟)")
            print(f"  描述: {path['description']}")
            print(f"  模块数: {path['module_count']}")
            print()
    elif args.path_details:
        details = learning_system.format_path_details(args.path_details)
        print(details)
    elif args.user_progress:
        progress = learning_system.format_user_progress(args.user_progress)
        print(progress)
    else:
        print("请提供参数或使用 --test 运行测试")
        print("示例: python learning_system.py --list-paths")

if __name__ == "__main__":
    main()