#!/usr/bin/env python3
"""
提取《湖南农民运动考察报告》完整内容 - 版本2
更精确地提取内容
"""

import re
from pathlib import Path

def extract_hunan_report_v2():
    """提取湖南农民运动考察报告内容 - 版本2"""
    # 读取文件
    input_file = Path("knowledge/selected_works/毛泽东选集全卷.md")
    if not input_file.exists():
        print(f"错误: 文件不存在 {input_file}")
        return
    
    content = input_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    print(f"文件总行数: {len(lines)}")
    
    # 查找报告的开始位置
    start_idx = None
    for i, line in enumerate(lines):
        if "湖南农民运动考察报告" in line and i > 100:  # 跳过目录部分
            print(f"找到报告标题在第 {i} 行: {line}")
            # 向后查找实际内容开始
            for j in range(i+1, min(i+50, len(lines))):
                if "###" in lines[j] and "第一件" in lines[j]:
                    start_idx = j
                    print(f"找到内容开始在第 {j} 行: {lines[j]}")
                    break
            if start_idx is None:
                start_idx = i
            break
    
    if start_idx is None:
        print("错误: 未找到湖南农民运动考察报告内容开始")
        return
    
    # 查找报告结束位置（下一个著作的开始）
    end_idx = None
    next_titles = ["中国的红色政权为什么能够存在", "井冈山的斗争", "关于纠正党内的错误思想"]
    
    for i in range(start_idx + 100, len(lines)):
        line = lines[i]
        # 查找下一个著作的标题（通常以###或##开头）
        if ("###" in line or "##" in line) and any(title in line for title in next_titles):
            end_idx = i - 1
            print(f"找到下一个著作标题在第 {i} 行: {line}")
            print(f"报告结束于第 {end_idx} 行")
            break
    
    if end_idx is None:
        # 如果没有找到，使用文件结尾
        end_idx = len(lines) - 1
        print(f"未找到下一个著作标题，使用文件结尾: {end_idx}")
    
    # 提取内容
    report_lines = lines[start_idx:end_idx + 1]
    
    print(f"提取了 {len(report_lines)} 行原始内容")
    
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
        
        # 跳过页码标记（如**第X/1258页**）
        if re.search(r'\*\*第\d+/\d+页\*\*', line):
            continue
        
        # 跳过纯注释行
        if line.strip().startswith("<!--") or line.strip().endswith("-->"):
            continue
        
        # 跳过空行或只有空格的行
        stripped = line.strip()
        if stripped == "":
            if cleaned_lines and cleaned_lines[-1].strip() != "":
                cleaned_lines.append("")
            continue
        
        # 清理行尾的特殊字符
        cleaned_line = line.rstrip('�?').strip()
        
        # 添加清理后的行
        cleaned_lines.append(cleaned_line)
    
    # 确保以空行结束
    if cleaned_lines and cleaned_lines[-1] != "":
        cleaned_lines.append("")
    
    print(f"清理后得到 {len(cleaned_lines)} 行内容")
    
    # 检查内容是否包含关键部分
    content_text = "\n".join(cleaned_lines)
    if "第一件" in content_text and "第十四件" in content_text:
        print("✅ 成功提取完整报告，包含第一件到第十四件")
    else:
        print("⚠️ 警告：可能未提取完整报告")
        if "第一件" not in content_text:
            print("  - 缺少'第一件'")
        if "第十四件" not in content_text:
            print("  - 缺少'第十四件'")
    
    # 创建输出文件路径
    output_file = Path("knowledge/selected_works/湖南农民运动考察报告_extracted_v2.md")
    output_file.write_text("\n".join(cleaned_lines), encoding='utf-8')
    print(f"已保存到: {output_file}")
    
    # 显示前100个字符作为预览
    preview = content_text[:500] + "..." if len(content_text) > 500 else content_text
    print(f"\n内容预览:\n{preview}")
    
    return len(cleaned_lines)

if __name__ == "__main__":
    extract_hunan_report_v2()