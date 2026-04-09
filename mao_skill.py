#!/usr/bin/env python3
"""
毛泽东.skill 入口点脚本

作为OpenClaw Skill的主入口，处理用户命令并调用六层架构集成系统。
"""

import sys
import os

# 添加tools目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

def main():
    """主函数：处理用户输入"""
    if len(sys.argv) < 2:
        print("❌ 错误：请提供命令参数")
        print("用法: python mao_skill.py <命令>")
        sys.exit(1)
    
    # 获取用户命令（去掉可能的斜杠）
    user_input = sys.argv[1].strip()
    if user_input.startswith('/'):
        user_input = user_input[1:]
    
    # 处理mao命令简写
    if user_input.startswith('mao '):
        user_input = user_input[4:]
    elif user_input == 'mao':
        user_input = 'help'
    
    # 构建完整命令
    full_command = f"/mao {user_input}" if user_input else "/mao help"
    
    try:
        # 导入并执行
        from mao_skill_integration_v2 import MaoSkillIntegrationV2
        
        # 创建集成实例（启用缓存和监控）
        integration = MaoSkillIntegrationV2(
            enable_cache=True,
            enable_monitoring=True
        )
        
        # 处理命令
        response = integration.process_command(full_command)
        
        # 输出响应
        print(response)
        
        # 返回成功
        sys.exit(0)
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装依赖：pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 处理错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()