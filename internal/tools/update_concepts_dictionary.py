#!/usr/bin/env python3
"""
更新毛泽东概念词典脚本

从批量处理结果中提取新概念，更新text_processor.py中的MAO_CONCEPTS集合
"""

import json
import re
import sys
from pathlib import Path

def load_batch_results(batch_file):
    """加载批量处理结果文件"""
    with open(batch_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_concepts_from_batch(batch_data):
    """从批量处理结果中提取所有概念"""
    concepts = set()
    
    # 从top_concepts提取
    if "top_concepts" in batch_data:
        for concept in batch_data["top_concepts"].keys():
            concepts.add(concept)
    
    # 从每个文件的top_concepts提取
    if "file_stats" in batch_data:
        for file_stat in batch_data["file_stats"]:
            if "top_concepts" in file_stat:
                for concept in file_stat["top_concepts"].keys():
                    concepts.add(concept)
    
    return concepts

def load_existing_concepts(text_processor_path):
    """从text_processor.py中加载现有的MAO_CONCEPTS"""
    with open(text_processor_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找MAO_CONCEPTS定义
    pattern = r'MAO_CONCEPTS\s*=\s*{([^}]+)}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("未找到MAO_CONCEPTS定义")
        return set()
    
    concepts_text = match.group(1)
    # 提取概念（每行可能有多个，用逗号分隔，可能跨行）
    concept_pattern = r'"([^"]+)"'
    concepts = set(re.findall(concept_pattern, concepts_text))
    
    return concepts

def update_concepts_dictionary():
    """主函数：更新概念词典"""
    # 路径配置
    project_root = Path(__file__).parent.parent
    batch_file = project_root / "processed" / "batch_processing_summary_20260409_151951.json"
    text_processor_file = project_root / "tools" / "text_processor.py"
    
    if not batch_file.exists():
        print(f"批量处理结果文件不存在: {batch_file}")
        # 查找最新的批量处理文件
        processed_dir = project_root / "processed"
        batch_files = list(processed_dir.glob("batch_processing_summary_*.json"))
        if batch_files:
            batch_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            batch_file = batch_files[0]
            print(f"使用最新文件: {batch_file}")
        else:
            print("未找到批量处理结果文件")
            return
    
    print(f"加载批量处理结果: {batch_file}")
    batch_data = load_batch_results(batch_file)
    
    print(f"提取批量处理中的概念...")
    batch_concepts = extract_concepts_from_batch(batch_data)
    print(f"从批量处理中提取了 {len(batch_concepts)} 个概念")
    
    print(f"加载现有概念词典...")
    existing_concepts = load_existing_concepts(text_processor_file)
    print(f"现有概念词典有 {len(existing_concepts)} 个概念")
    
    # 找出新概念
    new_concepts = batch_concepts - existing_concepts
    print(f"发现 {len(new_concepts)} 个新概念")
    
    if not new_concepts:
        print("没有新概念需要添加")
        return
    
    # 显示部分新概念
    print("\n部分新概念示例:")
    for i, concept in enumerate(sorted(new_concepts)[:20]):
        print(f"  {i+1}. {concept}")
    if len(new_concepts) > 20:
        print(f"  ... 还有 {len(new_concepts) - 20} 个概念")
    
    # 更新text_processor.py
    print(f"\n更新概念词典文件...")
    with open(text_processor_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按概念类别分类新概念（简单分类）
    categorized_concepts = categorize_concepts(new_concepts)
    
    # 生成新的MAO_CONCEPTS定义
    new_mao_concepts = generate_mao_concepts_content(categorized_concepts, existing_concepts)
    
    # 替换MAO_CONCEPTS部分
    pattern = r'(MAO_CONCEPTS\s*=\s*{)[^}]*(})'
    replacement = r'\1' + new_mao_concepts + r'\2'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 写回文件
    with open(text_processor_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"概念词典已更新！")
    print(f"总概念数: {len(existing_concepts) + len(new_concepts)}")
    print(f"新增概念: {len(new_concepts)}")

def categorize_concepts(concepts):
    """简单分类概念"""
    categories = {
        "哲学概念": set(),
        "政治概念": set(),
        "工作方法": set(),
        "军事概念": set(),
        "领导艺术": set(),
        "经济思想": set(),
        "文化教育": set(),
        "高频词": set()
    }
    
    # 简单关键词分类
    for concept in concepts:
        # 军事概念
        if any(keyword in concept for keyword in ["战", "军", "兵", "敌", "攻", "防", "战略", "战术", "战争"]):
            categories["军事概念"].add(concept)
        # 哲学概念
        elif any(keyword in concept for keyword in ["论", "主义", "思想", "观", "辩证法", "唯物主义"]):
            categories["哲学概念"].add(concept)
        # 政治概念
        elif any(keyword in concept for keyword in ["主义", "阶级", "民主", "专政", "革命", "建设"]):
            categories["政治概念"].add(concept)
        # 工作方法
        elif any(keyword in concept for keyword in ["方法", "工作", "调查", "研究", "路线", "指导"]):
            categories["工作方法"].add(concept)
        # 经济思想
        elif any(keyword in concept for keyword in ["经济", "生产", "发展", "建设", "计划", "市场"]):
            categories["经济思想"].add(concept)
        # 文化教育
        elif any(keyword in concept for keyword in ["文化", "教育", "文艺", "学习", "知识"]):
            categories["文化教育"].add(concept)
        # 领导艺术
        elif any(keyword in concept for keyword in ["领导", "干部", "群众", "服务", "民主集中"]):
            categories["领导艺术"].add(concept)
        else:
            categories["高频词"].add(concept)
    
    return categories

def generate_mao_concepts_content(categorized_concepts, existing_concepts):
    """生成MAO_CONCEPTS内容"""
    lines = []
    
    # 现有概念按类别重新组织（简化处理，这里假设现有概念已在正确类别）
    # 这里只添加新概念到对应类别
    
    for category, concepts in categorized_concepts.items():
        if concepts:
            lines.append(f"    # {category}")
            # 每行放5个概念
            concept_list = sorted(concepts)
            for i in range(0, len(concept_list), 5):
                chunk = concept_list[i:i+5]
                concepts_str = ", ".join(f'"{c}"' for c in chunk)
                lines.append(f"    {concepts_str},")
            lines.append("")  # 空行分隔
    
    # 移除最后一个空行
    if lines and lines[-1] == "":
        lines.pop()
    
    return "\n".join(lines)

if __name__ == "__main__":
    update_concepts_dictionary()