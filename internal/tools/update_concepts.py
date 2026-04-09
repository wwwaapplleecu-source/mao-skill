#!/usr/bin/env python3
import json
import os
from collections import Counter

def update_concepts():
    """更新概念词典，统计所有已处理著作的概念"""
    processed_dir = "processed"
    
    # 读取所有处理后的著作文件
    all_concepts = Counter()
    document_stats = []
    category_stats = Counter()
    
    # 排除概念词典文件本身
    json_files = [f for f in os.listdir(processed_dir) 
                  if f.endswith('.json') and f != 'concepts.json' 
                  and f != 'summary.json' and f != 'simple_concepts.json']
    
    total_documents = len(json_files)
    
    for json_file in json_files:
        file_path = os.path.join(processed_dir, json_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取文件名和分类
            filename = json_file.replace('.json', '')
            
            # 确定分类
            category = "unknown"
            if "关于正确处理人民内部矛盾" in filename:
                category = "methodology"
            elif "中国革命战争的战略问题" in filename:
                category = "military"
            elif "新民主主义论" in filename:
                category = "selected_works"
            elif "纪念白求恩" in filename:
                category = "speeches"
            elif "关心群众生活" in filename:
                category = "work_methods"
            elif "论联合政府" in filename:
                category = "selected_works"
            elif "为人民服务" in filename:
                category = "speeches"
            elif "哲学批注摘录" in filename:
                category = "annotations"
            elif "关于自由与必然的思考" in filename:
                category = "philosophy"
            elif "实践论" in filename:
                category = "methodology"
            elif "矛盾论" in filename:
                category = "methodology"
            elif "论持久战" in filename:
                category = "military"
            elif "毛泽东选集全卷" in filename:
                category = "selected_works"
            elif "在延安文艺座谈会上的讲话" in filename:
                category = "speeches"
            elif "致徐特立同志的信" in filename:
                category = "letters"
            
            # 统计概念
            if 'concepts' in data:
                concepts = data['concepts']
                concept_count = len(concepts)
                
                # 更新概念计数
                for concept in concepts:
                    all_concepts[concept] += 1
                
                # 记录文档统计
                doc_stat = {
                    "title": filename,
                    "file": json_file,
                    "type": category,
                    "segment_count": data.get('segment_count', 0),
                    "concept_count": concept_count
                }
                document_stats.append(doc_stat)
                
                # 更新类别统计
                category_stats[category] += concept_count
            
        except Exception as e:
            print(f"处理文件 {json_file} 时出错: {e}")
    
    # 准备概念词典数据
    concepts_data = {
        "统计时间": "2026-04-08",
        "总概念数": len(all_concepts),
        "总文档数": total_documents,
        "概念列表": list(all_concepts.keys()),
        "文档统计": document_stats,
        "类别统计": dict(category_stats)
    }
    
    # 保存概念词典
    concepts_file = os.path.join(processed_dir, "concepts.json")
    with open(concepts_file, 'w', encoding='utf-8') as f:
        json.dump(concepts_data, f, ensure_ascii=False, indent=2)
    
    # 创建简化版概念词典（只包含概念名称）
    simple_concepts_file = os.path.join(processed_dir, "simple_concepts.json")
    with open(simple_concepts_file, 'w', encoding='utf-8') as f:
        json.dump(list(all_concepts.keys()), f, ensure_ascii=False, indent=2)
    
    print(f"概念词典更新完成:")
    print(f"总概念数: {len(all_concepts)}")
    print(f"总文档数: {total_documents}")
    print(f"类别统计: {dict(category_stats)}")
    
    # 创建摘要统计
    summary_data = {
        "update_time": "2026-04-08",
        "total_concepts": len(all_concepts),
        "total_documents": total_documents,
        "category_summary": dict(category_stats)
    }
    
    summary_file = os.path.join(processed_dir, "summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"摘要统计已保存到 {summary_file}")

if __name__ == "__main__":
    update_concepts()