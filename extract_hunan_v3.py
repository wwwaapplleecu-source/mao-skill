#!/usr/bin/env python3
"""
提取《湖南农民运动考察报告》完整内容 - 版本3
基于具体的章节标题查找
"""

import re
from pathlib import Path

def extract_hunan_report_v3():
    """提取湖南农民运动考察报告内容 - 版本3"""
    # 读取文件
    input_file = Path("knowledge/selected_works/毛泽东选集全卷.md")
    if not input_file.exists():
        print(f"错误: 文件不存在 {input_file}")
        return
    
    content = input_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    print(f"文件总行数: {len(lines)}")
    
    # 查找报告的开始位置 - 查找"### 第一件 组织农民到农会里"
    start_idx = None
    for i, line in enumerate(lines):
        if "###" in line and "第一件" in line and "组织农民到农会里" in line:
            start_idx = i
            print(f"找到报告开始在第 {i} 行: {line}")
            break
    
    if start_idx is None:
        # 如果没有找到，尝试查找"第一件"的其他变体
        for i, line in enumerate(lines):
            if "第一件" in line and ("组织农民" in line or "农会" in line):
                start_idx = i
                print(f"找到报告开始（变体）在第 {i} 行: {line}")
                break
    
    if start_idx is None:
        print("错误: 未找到湖南农民运动考察报告内容开始")
        return
    
    # 查找报告结束位置 - 查找下一个著作的开始
    end_idx = None
    next_titles = [
        "中国的红色政权为什么能够存在",
        "井冈山的斗争", 
        "关于纠正党内的错误思想",
        "星星之火，可以燎原"
    ]
    
    # 先查找"第十四件 修道路，修塘坝"作为参考点
    fourteen_idx = None
    for i in range(start_idx, len(lines)):
        if "第十四件" in lines[i] or "修道路" in lines[i]:
            fourteen_idx = i
            print(f"找到'第十四件'在第 {i} 行: {lines[i]}")
            break
    
    if fourteen_idx:
        # 从第十四件之后开始查找下一个著作
        search_start = fourteen_idx + 100
    else:
        search_start = start_idx + 500
    
    # 查找下一个著作的开始
    for i in range(search_start, min(search_start + 1000, len(lines))):
        line = lines[i]
        # 查找下一个著作的标题（通常以###或##开头，且包含特定关键词）
        if (("###" in line or "##" in line) and 
            any(title in line for title in next_titles)):
            end_idx = i - 1
            print(f"找到下一个著作标题在第 {i} 行: {line}")
            print(f"报告结束于第 {end_idx} 行")
            break
    
    if end_idx is None and fourteen_idx:
        # 如果没有找到下一个著作，但找到了第十四件，则使用第十四件后300行作为结束
        end_idx = min(fourteen_idx + 300, len(lines) - 1)
        print(f"未找到下一个著作标题，使用第十四件后300行: {end_idx}")
    
    if end_idx is None:
        # 最后的手段：使用start_idx + 800行
        end_idx = min(start_idx + 800, len(lines) - 1)
        print(f"未找到结束位置，使用开始后800行: {end_idx}")
    
    # 提取内容
    report_lines = lines[start_idx:end_idx + 1]
    
    print(f"提取了 {len(report_lines)} 行原始内容 (从{start_idx}到{end_idx})")
    
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
    
    # 检查关键章节
    chapters_to_check = [
        ("第一件", "组织农民到农会里"),
        ("第二件", "政治上打击地主"),
        ("第三件", "经济上打击地主"),
        ("第四件", "推翻土豪劣绅的封建统治"),
        ("第五件", "推翻地主武装，建立农民武装"),
        ("第六件", "推翻县官老爷衙门差役的政权"),
        ("第七件", "推翻祠堂族长的族权和城隍土地菩萨的神权以至丈夫的男权"),
        ("第八件", "普及政治宣传"),
        ("第九件", "农民诸禁"),
        ("第十件", "清匪"),
        ("第十一件", "废苛捐"),
        ("第十二件", "文化运动"),
        ("第十三件", "合作社运动"),
        ("第十四件", "修道路，修塘坝")
    ]
    
    found_chapters = []
    missing_chapters = []
    
    for chapter_num, chapter_desc in chapters_to_check:
        if chapter_num in content_text:
            found_chapters.append((chapter_num, chapter_desc))
        else:
            missing_chapters.append((chapter_num, chapter_desc))
    
    print(f"\n章节检查结果:")
    print(f"✅ 找到 {len(found_chapters)} 个章节:")
    for chap, desc in found_chapters[:5]:  # 只显示前5个
        print(f"  - {chap}: {desc}")
    if len(found_chapters) > 5:
        print(f"  - ... 共{len(found_chapters)}个章节")
    
    if missing_chapters:
        print(f"⚠️ 缺失 {len(missing_chapters)} 个章节:")
        for chap, desc in missing_chapters[:5]:  # 只显示前5个
            print(f"  - {chap}: {desc}")
        if len(missing_chapters) > 5:
            print(f"  - ... 共{len(missing_chapters)}个章节")
    
    # 创建输出文件路径
    output_file = Path("knowledge/selected_works/湖南农民运动考察报告_extracted_v3.md")
    output_file.write_text("\n".join(cleaned_lines), encoding='utf-8')
    print(f"\n已保存到: {output_file}")
    
    # 显示前500个字符作为预览
    if content_text:
        preview = content_text[:500] + "..." if len(content_text) > 500 else content_text
        print(f"\n内容预览:\n{preview}")
    else:
        print("\n警告: 提取的内容为空!")
    
    return len(cleaned_lines)

if __name__ == "__main__":
    extract_hunan_report_v3()