#!/usr/bin/env python3
"""
提取《湖南农民运动考察报告》完整内容
从《毛泽东选集全卷.md》中提取并清理
"""

import re
from pathlib import Path

def extract_hunan_report():
    """提取湖南农民运动考察报告内容"""
    # 读取文件
    input_file = Path("knowledge/selected_works/毛泽东选集全卷.md")
    if not input_file.exists():
        print(f"错误: 文件不存在 {input_file}")
        return
    
    content = input_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    # 找到报告的开始和结束位置
    start_idx = None
    end_idx = None
    
    # 搜索"湖南农民运动考察报告"标题
    for i, line in enumerate(lines):
        if "湖南农民运动考察报告" in line and start_idx is None:
            start_idx = i
            print(f"找到标题在第 {i} 行: {line}")
            break
    
    if start_idx is None:
        print("错误: 未找到湖南农民运动考察报告标题")
        return
    
    # 搜索下一个著作的标题（中国的红色政权为什么能够存在）
    for i in range(start_idx + 1, len(lines)):
        if "中国的红色政权为什么能够存在" in lines[i]:
            end_idx = i - 1
            print(f"找到下一个标题在第 {i} 行，报告结束于第 {end_idx} 行")
            break
    
    if end_idx is None:
        end_idx = len(lines) - 1
        print(f"未找到下一个标题，使用文件结尾: {end_idx}")
    
    # 提取内容
    report_lines = lines[start_idx:end_idx + 1]
    
    # 清理HTML注释和多余空行
    cleaned_lines = []
    in_comment = False
    
    for line in report_lines:
        # 跳过HTML注释
        if "<!--" in line:
            in_comment = True
            continue
        if "-->" in line:
            in_comment = False
            continue
        if in_comment:
            continue
        
        # 跳过空行或只有空格的行
        if line.strip() == "":
            if cleaned_lines and cleaned_lines[-1].strip() != "":
                cleaned_lines.append("")
            continue
        
        # 添加清理后的行
        cleaned_lines.append(line)
    
    # 确保以空行结束
    if cleaned_lines and cleaned_lines[-1] != "":
        cleaned_lines.append("")
    
    print(f"提取了 {len(cleaned_lines)} 行内容")
    
    # 创建输出文件路径
    output_file = Path("knowledge/selected_works/湖南农民运动考察报告_extracted.md")
    output_file.write_text("\n".join(cleaned_lines), encoding='utf-8')
    print(f"已保存到: {output_file}")
    
    # 返回提取的行数
    return len(cleaned_lines)

if __name__ == "__main__":
    extract_hunan_report()