#!/usr/bin/env python3
"""
重命名毛泽东著作文件，使用正确的中文文件名
"""

import os
import shutil
from pathlib import Path

def rename_files():
    """重命名knowledge目录下的文件"""
    base_dir = Path(__file__).parent
    knowledge_dir = base_dir / 'knowledge'
    
    # 定义文件映射：目录 -> [(当前文件名模式, 新文件名), ...]
    # 由于文件名是乱码，我们通过文件大小来识别
    file_map = {
        'methodology': [
            (28859, '实践论.md'),    # 实践论大小
            (83661, '矛盾论.md'),    # 矛盾论大小
        ],
        'military': [
            (840812, '论持久战.md'),  # 论持久战大小
        ],
        'selected_works': [
            (2226542, '毛泽东选集全卷.md'),  # 选集大小
        ]
    }
    
    for subdir, mappings in file_map.items():
        dir_path = knowledge_dir / subdir
        if not dir_path.exists():
            print(f"目录不存在: {dir_path}")
            continue
            
        print(f"\n处理目录: {subdir}")
        
        # 收集目录中的文件
        files = list(dir_path.glob('*.md'))
        if not files:
            print("  没有找到.md文件")
            continue
            
        # 按文件大小匹配
        for file_path in files:
            file_size = file_path.stat().st_size
            current_name = file_path.name
            
            # 查找匹配的大小
            matched = False
            for size, new_name in mappings:
                if abs(file_size - size) < 100:  # 允许微小差异
                    # 检查是否已经是正确文件名
                    if current_name == new_name:
                        print(f"  ✓ {current_name} 已经是正确文件名")
                        matched = True
                        break
                    
                    # 重命名文件
                    new_path = file_path.parent / new_name
                    try:
                        # 如果目标文件已存在，先删除
                        if new_path.exists():
                            new_path.unlink()
                        
                        # 重命名
                        file_path.rename(new_path)
                        print(f"  ✓ {current_name} -> {new_name}")
                        matched = True
                        break
                    except Exception as e:
                        print(f"  ✗ 重命名失败: {current_name} -> {new_name}, 错误: {e}")
                        matched = True
                        break
            
            if not matched:
                print(f"  ? 未匹配: {current_name} (大小: {file_size})")
    
    print("\n重命名完成！")

if __name__ == '__main__':
    rename_files()