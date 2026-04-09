#!/usr/bin/env python3
"""
更新概念词典统计
"""

import json
import os
import glob

def update_concept_statistics():
    """更新概念词典统计信息"""
    
    print("=== 更新概念词典统计 ===")
    
    # 查找所有处理后的JSON文件
    processed_files = glob.glob("knowledge/**/*.json", recursive=True)
    processed_files = [f for f in processed_files if os.path.isfile(f)]
    
    print(f"找到 {len(processed_files)} 个处理后的文件")
    
    # 统计概念
    all_concepts = {}
    document_stats = []
    
    for file_path in processed_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 获取文档信息
            doc_title = data.get('title', os.path.basename(file_path))
            doc_type = os.path.dirname(file_path).split(os.sep)[-1] if len(os.path.dirname(file_path).split(os.sep)) > 1 else "unknown"
            
            # 统计概念
            concepts = data.get('concepts', [])
            concept_count = len(concepts)
            
            # 添加到总概念库
            for concept in concepts:
                concept_text = concept.get('concept', '')
                if concept_text:
                    if concept_text in all_concepts:
                        all_concepts[concept_text]['count'] += 1
                        all_concepts[concept_text]['documents'].append(doc_title)
                    else:
                        all_concepts[concept_text] = {
                            'count': 1,
                            'documents': [doc_title],
                            'type': concept.get('type', 'unknown')
                        }
            
            # 记录文档统计
            document_stats.append({
                'title': doc_title,
                'file': file_path,
                'type': doc_type,
                'concept_count': concept_count,
                'segment_count': len(data.get('segments', []))
            })
            
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            continue
    
    # 排序概念
    sorted_concepts = sorted(all_concepts.items(), key=lambda x: x[1]['count'], reverse=True)
    
    # 生成统计报告
    total_concepts = len(sorted_concepts)
    total_documents = len(document_stats)
    
    print(f"\n📊 统计结果:")
    print(f"总文档数: {total_documents}")
    print(f"总概念数: {total_concepts}")
    print(f"平均每个文档概念数: {total_concepts/total_documents if total_documents > 0 else 0:.1f}")
    
    # 按类别统计
    type_stats = {}
    for doc in document_stats:
        doc_type = doc['type']
        if doc_type not in type_stats:
            type_stats[doc_type] = {
                'count': 0,
                'total_concepts': 0,
                'documents': []
            }
        type_stats[doc_type]['count'] += 1
        type_stats[doc_type]['total_concepts'] += doc['concept_count']
        type_stats[doc_type]['documents'].append(doc['title'])
    
    print(f"\n📁 按类别统计:")
    for doc_type, stats in sorted(type_stats.items()):
        avg_concepts = stats['total_concepts'] / stats['count'] if stats['count'] > 0 else 0
        print(f"  {doc_type}: {stats['count']}篇文档, {stats['total_concepts']}个概念, 平均{avg_concepts:.1f}个/篇")
    
    # 最常见概念
    print(f"\n🏆 最常见概念 (Top 20):")
    for i, (concept, info) in enumerate(sorted_concepts[:20]):
        print(f"  {i+1}. {concept} (出现在{info['count']}篇文档中)")
    
    # 保存概念词典
    concepts_dict = {
        '统计时间': '2026-04-08',
        '总概念数': total_concepts,
        '总文档数': total_documents,
        '概念列表': [{
            '概念': concept,
            '出现次数': info['count'],
            '类型': info['type'],
            '出现文档': info['documents'][:5]  # 只显示前5个文档
        } for concept, info in sorted_concepts[:200]],  # 保存前200个概念
        '文档统计': document_stats,
        '类别统计': type_stats
    }
    
    # 保存到文件
    concepts_file = "processed/concepts.json"
    os.makedirs(os.path.dirname(concepts_file), exist_ok=True)
    
    with open(concepts_file, 'w', encoding='utf-8') as f:
        json.dump(concepts_dict, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 概念词典已保存到: {concepts_file}")
    
    # 生成简化的概念列表（用于Skill使用）
    simple_concepts = [concept for concept, _ in sorted_concepts[:150]]
    simple_file = "processed/simple_concepts.json"
    
    with open(simple_file, 'w', encoding='utf-8') as f:
        json.dump({
            '统计时间': '2026-04-08',
            '概念总数': len(simple_concepts),
            '概念列表': simple_concepts
        }, f, ensure_ascii=False, indent=2)
    
    print(f"简化概念列表已保存到: {simple_file}")
    
    # 更新PHASE2_PLAN.md中的统计信息
    try:
        plan_file = "PHASE2_PLAN.md"
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan_content = f.read()
        
        # 更新概念统计部分
        new_stats = f"**概念词典统计** (更新: 2026-04-08):\n"
        new_stats += f"- 总概念数: {total_concepts}个\n"
        new_stats += f"- 覆盖文档: {total_documents}篇\n"
        new_stats += f"- 最常见概念: {', '.join([concept for concept, _ in sorted_concepts[:10]])}\n"
        
        # 查找并更新统计部分
        import re
        pattern = r"\*\*概念词典统计\*\*.*?(?=\n\n|\Z)"
        if re.search(pattern, plan_content, re.DOTALL):
            plan_content = re.sub(pattern, new_stats, plan_content, flags=re.DOTALL)
        else:
            # 如果没有找到，在适当位置添加
            plan_content = plan_content.replace(
                "**当前统计** (更新:",
                f"{new_stats}\n\n**当前统计** (更新:"
            )
        
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(plan_content)
        
        print(f"📝 已更新 {plan_file} 中的概念统计信息")
        
    except Exception as e:
        print(f"更新计划文件时出错: {e}")
    
    return total_concepts, total_documents

if __name__ == "__main__":
    total_concepts, total_documents = update_concept_statistics()
    
    print(f"\n🎯 概念词典更新完成:")
    print(f"文档处理: {total_documents}篇")
    print(f"概念提取: {total_concepts}个核心概念")
    print(f"知识密度: {total_concepts/total_documents if total_documents > 0 else 0:.1f}概念/篇")