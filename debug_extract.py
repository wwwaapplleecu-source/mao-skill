#!/usr/bin/env python3
"""
调试提取过程 - 查看原始内容
"""

from pathlib import Path

def debug_extract():
    # 读取文件
    input_file = Path("knowledge/selected_works/毛泽东选集全卷.md")
    content = input_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    # 提取第818-850行看看
    start = 818
    end = 850
    
    print(f"查看第{start}到{end}行原始内容:\n")
    for i in range(start, min(end, len(lines))):
        print(f"{i:4d}: {lines[i]}")
    
    print("\n" + "="*80 + "\n")
    
    # 查看第1070-1100行
    start2 = 1070
    end2 = 1100
    
    print(f"查看第{start2}到{end2}行原始内容:\n")
    for i in range(start2, min(end2, len(lines))):
        print(f"{i:4d}: {lines[i]}")
    
    print("\n" + "="*80 + "\n")
    
    # 统计HTML注释
    html_comments = 0
    for i in range(start, min(start+500, len(lines))):
        if "<!--" in lines[i] or "-->" in lines[i]:
            html_comments += 1
    
    print(f"在前500行中，有{html_comments}行包含HTML注释")
    
    # 查看一行示例
    print("\n示例行分析:")
    sample_line = lines[825]
    print(f"行825: {repr(sample_line)}")
    print(f"长度: {len(sample_line)}")
    print(f"包含'<!--': {'<!--' in sample_line}")
    print(f"包含'-->': {'-->' in sample_line}")

if __name__ == "__main__":
    debug_extract()