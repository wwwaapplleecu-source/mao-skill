#!/usr/bin/env python3
"""
毛泽东.skill 入口点脚本

作为OpenClaw Skill的主入口，处理用户命令并调用六层架构集成系统。
"""

import sys
import os

# 尝试设置标准输出编码为UTF-8
try:
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass  # 如果失败，继续使用默认编码

def safe_print(text: str):
    """安全打印文本，处理编码问题"""
    try:
        print(text)
    except UnicodeEncodeError:
        # 尝试使用当前控制台编码，如果失败则使用GBK替换无法编码的字符
        encoding = sys.stdout.encoding or 'gbk'
        try:
            encoded = text.encode(encoding, errors='replace').decode(encoding, errors='replace')
            print(encoded)
        except Exception:
            # 最后尝试使用ASCII替换
            encoded = text.encode('ascii', errors='replace').decode('ascii', errors='replace')
            print(encoded)

# 添加tools目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

def main():
    """主函数：处理用户输入"""
    if len(sys.argv) < 2:
        safe_print("[错误] 请提供命令参数")
        safe_print("用法: python mao_skill.py <命令>")
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
        
        # 创建集成实例（禁用缓存和监控以加速）
        integration = MaoSkillIntegrationV2(
            enable_cache=False,
            enable_monitoring=False
        )
        
        # 处理命令
        response = integration.process_command(full_command)
        
        # 输出响应
        safe_print(response)
        
        # 返回成功
        sys.exit(0)
        
    except ImportError as e:
        safe_print(f"[错误] 导入错误: {e}")
        safe_print("请确保已安装依赖：pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        safe_print(f"[错误] 处理错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()