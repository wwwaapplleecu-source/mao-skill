#!/usr/bin/env python3
"""
提取《中国革命战争的战略问题》完整内容 - 最终版
基于《湖南农民运动考察报告》提取脚本修改
"""

import re
from pathlib import Path

def clean_html_comments(text):
    """清理HTML注释"""
    # 移除完整的HTML注释块 <!-- ... -->
    lines = text.splitlines()
    cleaned_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检查是否是完整的注释行
        stripped = line.strip()
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            # 完整注释行，跳过
            i += 1
            continue
        
        # 检查是否包含注释开始
        if "<!--" in line:
            # 查找注释结束
            end_idx = line.find("-->")
            if end_idx != -1:
                # 注释在同一行结束
                # 移除注释部分
                comment_start = line.find("<!--")
                before = line[:comment_start]
                after = line[end_idx+3:]  # 跳过"-->"的3个字符
                line = before + after
                if line.strip():  # 如果还有内容
                    cleaned_lines.append(line)
                i += 1
                continue
            else:
                # 多行注释，跳过直到找到-->
                i += 1
                while i < len(lines) and "-->" not in lines[i]:
                    i += 1
                if i < len(lines):
                    # 跳过包含-->的行
                    i += 1
                continue
        
        # 正常行，添加到结果
        if line.strip():  # 跳过空行
            cleaned_lines.append(line)
        i += 1
    
    return "\n".join(cleaned_lines)

def extract_military_strategy_final():
    """提取《中国革命战争的战略问题》内容 - 最终版"""
    # 读取文件
    input_file = Path("knowledge/selected_works/毛泽东选集全卷.md")
    if not input_file.exists():
        print(f"错误: 文件不存在 {input_file}")
        return
    
    content = input_file.read_text(encoding='utf-8')
    lines = content.splitlines()
    
    print(f"文件总行数: {len(lines)}")
    
    # 查找著作的开始位置 - 查找"### 中国革命战争的战略问题"或"第一章"
    start_idx = None
    
    # 先找"### 中国革命战争的战略问题"
    for i, line in enumerate(lines):
        if "###" in line and "中国革命战争的战略问题" in line:
            start_idx = i
            print(f"找到著作标题在第 {i} 行: {line}")
            break
    
    # 如果没找到，找"### 第一章"
    if start_idx is None:
        for i, line in enumerate(lines):
            if "###" in line and "第一章" in line and "如何研究战争" in line:
                start_idx = i
                print(f"找到著作开始（第一章）在第 {i} 行: {line}")
                break
    
    if start_idx is None:
        # 再尝试找"如何研究战争"
        for i, line in enumerate(lines):
            if "如何研究战争" in line and "###" in line:
                start_idx = i
                print(f"找到著作开始（如何研究战争）在第 {i} 行: {line}")
                break
    
    if start_idx is None:
        print("错误: 未找到《中国革命战争的战略问题》内容开始")
        return
    
    # 查找著作结束位置 - 查找下一个著作的开始
    end_idx = None
    
    # 查找下一个著作"关于蒋介石声明的声明"
    next_title_idx = None
    for i in range(start_idx + 500, len(lines)):
        if "关于蒋介石声明的声明" in lines[i]:
            next_title_idx = i
            print(f"找到下一个著作在第 {i} 行: {lines[i]}")
            break
    
    # 如果没找到，找"中国的红色政权为什么能够存在"
    if next_title_idx is None:
        for i in range(start_idx + 500, len(lines)):
            if "中国的红色政权为什么能够存在" in lines[i]:
                next_title_idx = i
                print(f"找到下一个著作在第 {i} 行: {lines[i]}")
                break
    
    if next_title_idx:
        end_idx = next_title_idx - 1
    else:
        # 使用开始后1500行作为安全范围
        end_idx = min(start_idx + 1500, len(lines) - 1)
        print(f"未找到下一个著作，使用开始后1500行: 第 {end_idx} 行")
    
    print(f"著作结束于第 {end_idx} 行")
    
    # 提取原始内容
    report_lines = lines[start_idx:end_idx + 1]
    raw_content = "\n".join(report_lines)
    
    print(f"提取了 {len(report_lines)} 行原始内容")
    
    # 清理HTML注释
    cleaned_content = clean_html_comments(raw_content)
    
    # 进一步清理：移除页码标记等
    # 移除**第X/1258页**这样的标记
    cleaned_content = re.sub(r'\*\*第\d+/\d+页\*\*', '', cleaned_content)
    
    # 移除多余的空白行
    lines_cleaned = [line.strip() for line in cleaned_content.splitlines() if line.strip()]
    final_content = "\n".join(lines_cleaned)
    
    print(f"清理后得到 {len(lines_cleaned)} 行内容")
    
    # 检查关键章节
    chapters_to_check = [
        ("第一章", "如何研究战争"),
        ("第二章", "中国共产党和中国革命战争"),
        ("第三章", "中国革命战争的特点"),
        ("第四章", "围剿和反围剿"),
        ("第五章", "战略防御"),
        ("第六章", "战略退却"),
        ("第七章", "战略反攻"),
        ("第八章", "集中兵力问题"),
        ("第九章", "歼灭战"),
        ("第十章", "决战问题")
    ]
    
    found = []
    missing = []
    
    for chap_num, chap_desc in chapters_to_check:
        if chap_num in final_content:
            found.append((chap_num, chap_desc))
        else:
            missing.append((chap_num, chap_desc))
    
    print(f"\n章节检查结果:")
    print(f"✅ 找到 {len(found)} 个章节:")
    for chap, desc in found:
        print(f"  - {chap}: {desc}")
    
    if missing:
        print(f"⚠️ 缺失 {len(missing)} 个章节:")
        for chap, desc in missing[:5]:
            print(f"  - {chap}: {desc}")
        if len(missing) > 5:
            print(f"  - ... 共{len(missing)}个章节")
    
    # 创建输出文件
    output_file = Path("knowledge/military/中国革命战争的战略问题_complete.md")
    
    # 读取现有文件的前面部分（头部信息）
    existing_file = Path("knowledge/military/中国革命战争的战略问题.md")
    existing_text = ""
    if existing_file.exists():
        existing_text = existing_file.read_text(encoding='utf-8')
    
    # 提取现有文件中的各部分
    header_content = ""
    history_section = ""
    core_viewpoints = ""
    methodology_value = ""
    
    # 提取头部信息（直到"## 正文"之前）
    if "## 正文" in existing_text:
        header_parts = existing_text.split("## 正文")
        if len(header_parts) > 0:
            header_content = header_parts[0] + "## 正文\n\n"
    
    if not header_content:
        # 创建默认头部
        header_content = """# 中国革命战争的战略问题

**作者**: 毛泽东  
**写作时间**: 1936年12月  
**来源**: 《毛泽东选集第一卷》  
**分类**: military

---

## 内容简介

毛泽东总结中国革命战争经验的重要军事著作，系统阐述了人民战争的战略战术原则。

---

## 正文

"""
    
    # 提取历史意义等部分
    if "## 历史意义" in existing_text:
        history_start = existing_text.find("## 历史意义")
        history_end = existing_text.find("##", history_start + 1)
        if history_end == -1:
            history_end = len(existing_text)
        history_section = existing_text[history_start:history_end].strip()
    
    if "## 核心观点" in existing_text:
        core_start = existing_text.find("## 核心观点")
        core_end = existing_text.find("##", core_start + 1)
        if core_end == -1:
            core_end = len(existing_text)
        core_viewpoints = existing_text[core_start:core_end].strip()
    
    if "## 方法论价值" in existing_text:
        method_start = existing_text.find("## 方法论价值")
        method_end = existing_text.find("---", method_start)
        if method_end == -1:
            method_end = len(existing_text)
        methodology_value = existing_text[method_start:method_end].strip()
    
    # 构建完整内容
    full_content = header_content + final_content + "\n\n---\n\n"
    
    if history_section:
        full_content += history_section + "\n\n"
    
    if core_viewpoints:
        full_content += core_viewpoints + "\n\n"
    
    if methodology_value:
        full_content += methodology_value + "\n\n"
    
    # 添加补充信息
    full_content += f"""
---

**收集时间**: 2026-04-09  
**补充时间**: 2026-04-09  
**状态**: ✅ 完整内容已补充  
**验证状态**: 需校对细节  
**内容完整度**: 待评估 (已提取完整正文，章节完整性: {len(found)}/{len(chapters_to_check)})

**关键词**: 战争, 战略, 人民战争, 军事, 革命, 围剿, 反围剿, 积极防御, 集中优势兵力, 歼灭战, 诱敌深入, 运动战, 游击战
"""
    
    output_file.write_text(full_content, encoding='utf-8')
    print(f"\n✅ 已保存完整著作到: {output_file}")
    
    # 预览
    if final_content:
        preview = final_content[:500] + "..." if len(final_content) > 500 else final_content
        print(f"\n内容预览:\n{preview}")
    
    return len(lines_cleaned)

if __name__ == "__main__":
    extract_military_strategy_final()