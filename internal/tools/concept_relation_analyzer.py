#!/usr/bin/env python3
"""
概念关系分析器

分析毛泽东著作中概念之间的关系，建立概念网络，为知识图谱构建奠定基础
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict, Counter
import networkx as nx
# matplotlib导入移到visualize_concept_network函数内部

class ConceptRelationAnalyzer:
    """概念关系分析器"""
    
    def __init__(self, batch_file=None):
        self.batch_file = batch_file
        self.batch_data = None
        self.concepts = set()
        self.concept_freq = {}
        self.concept_cooccurrence = defaultdict(Counter)
        self.concept_by_category = defaultdict(set)
        self.graph = nx.Graph()
        
    def load_batch_data(self, batch_file=None):
        """加载批量处理数据"""
        if batch_file:
            self.batch_file = batch_file
        
        if not self.batch_file:
            # 查找最新的批量处理文件
            processed_dir = Path(__file__).parent.parent / "processed"
            batch_files = list(processed_dir.glob("batch_processing_summary_*.json"))
            if not batch_files:
                raise FileNotFoundError("未找到批量处理结果文件")
            batch_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            self.batch_file = batch_files[0]
        
        print(f"加载批量处理结果: {self.batch_file}")
        with open(self.batch_file, 'r', encoding='utf-8') as f:
            self.batch_data = json.load(f)
        
        return self.batch_data
    
    def extract_concepts(self):
        """从批量处理数据中提取概念"""
        if not self.batch_data:
            raise ValueError("请先加载批量处理数据")
        
        # 提取所有概念
        self.concepts = set()
        
        # 从top_concepts提取
        if "top_concepts" in self.batch_data:
            for concept, freq in self.batch_data["top_concepts"].items():
                self.concepts.add(concept)
                self.concept_freq[concept] = freq
        
        # 从每个文件的top_concepts提取
        if "file_stats" in self.batch_data:
            for file_stat in self.batch_data["file_stats"]:
                category = file_stat.get("category", "unknown")
                if "top_concepts" in file_stat:
                    file_concepts = set(file_stat["top_concepts"].keys())
                    self.concepts.update(file_concepts)
                    self.concept_by_category[category].update(file_concepts)
        
        print(f"提取了 {len(self.concepts)} 个概念")
        print(f"概念分布在 {len(self.concept_by_category)} 个分类中")
        
        return self.concepts
    
    def analyze_cooccurrence(self):
        """分析概念共现关系"""
        if not self.batch_data or "file_stats" not in self.batch_data:
            return
        
        print("分析概念共现关系...")
        
        for file_stat in self.batch_data["file_stats"]:
            if "top_concepts" not in file_stat:
                continue
            
            file_concepts = list(file_stat["top_concepts"].keys())
            
            # 计算文件中概念的两两共现
            for i in range(len(file_concepts)):
                for j in range(i + 1, len(file_concepts)):
                    concept1 = file_concepts[i]
                    concept2 = file_concepts[j]
                    
                    # 增加共现计数
                    self.concept_cooccurrence[concept1][concept2] += 1
                    self.concept_cooccurrence[concept2][concept1] += 1
        
        print(f"分析了 {len(self.concept_cooccurrence)} 个概念的共现关系")
        
        # 计算最强的共现关系
        strong_relations = []
        for concept1, cooccurrences in self.concept_cooccurrence.items():
            for concept2, count in cooccurrences.items():
                if count >= 3:  # 至少共现3次
                    strong_relations.append((concept1, concept2, count))
        
        strong_relations.sort(key=lambda x: x[2], reverse=True)
        
        return strong_relations
    
    def build_concept_graph(self, min_cooccurrence=2):
        """构建概念图"""
        print(f"构建概念图 (最小共现次数: {min_cooccurrence})...")
        
        # 创建图
        self.graph = nx.Graph()
        
        # 添加节点（概念）
        for concept in self.concepts:
            self.graph.add_node(concept, frequency=self.concept_freq.get(concept, 1))
        
        # 添加边（共现关系）
        edge_count = 0
        for concept1, cooccurrences in self.concept_cooccurrence.items():
            for concept2, count in cooccurrences.items():
                if count >= min_cooccurrence and concept1 != concept2:
                    # 添加边，权重为共现次数
                    self.graph.add_edge(concept1, concept2, weight=count)
                    edge_count += 1
        
        print(f"概念图构建完成: {self.graph.number_of_nodes()} 个节点, {edge_count} 条边")
        
        # 计算图的基本统计
        stats = self.calculate_graph_stats()
        
        return stats
    
    def calculate_graph_stats(self):
        """计算图统计信息"""
        stats = {}
        
        if self.graph.number_of_nodes() == 0:
            return stats
        
        stats["node_count"] = self.graph.number_of_nodes()
        stats["edge_count"] = self.graph.number_of_edges()
        
        # 度中心性（节点的连接数）
        degrees = dict(self.graph.degree())
        stats["avg_degree"] = sum(degrees.values()) / len(degrees)
        
        # 找到最重要的节点（高度中心性）
        degree_centrality = nx.degree_centrality(self.graph)
        top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        stats["top_nodes_by_degree"] = top_nodes
        
        # 介数中心性（节点在最短路径中的重要性）
        try:
            betweenness = nx.betweenness_centrality(self.graph, weight='weight')
            top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
            stats["top_nodes_by_betweenness"] = top_betweenness
        except:
            stats["top_nodes_by_betweenness"] = "计算失败"
        
        # 连通分量
        components = list(nx.connected_components(self.graph))
        stats["component_count"] = len(components)
        stats["largest_component_size"] = max(len(c) for c in components) if components else 0
        
        # 聚类系数（网络的聚集程度）
        clustering = nx.average_clustering(self.graph)
        stats["average_clustering"] = clustering
        
        return stats
    
    def categorize_concepts(self):
        """对概念进行分类"""
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
        
        # 关键词分类
        for concept in self.concepts:
            # 军事概念
            if any(keyword in concept for keyword in ["战", "军", "兵", "敌", "攻", "防", "战略", "战术", "战争"]):
                categories["军事概念"].add(concept)
            # 哲学概念
            elif any(keyword in concept for keyword in ["论", "主义", "思想", "观", "辩证法", "唯物主义", "矛盾", "实践"]):
                categories["哲学概念"].add(concept)
            # 政治概念
            elif any(keyword in concept for keyword in ["主义", "阶级", "民主", "专政", "革命", "建设", "社会主义", "共产主义"]):
                categories["政治概念"].add(concept)
            # 工作方法
            elif any(keyword in concept for keyword in ["方法", "工作", "调查", "研究", "路线", "指导", "批评", "自我批评"]):
                categories["工作方法"].add(concept)
            # 经济思想
            elif any(keyword in concept for keyword in ["经济", "生产", "发展", "建设", "计划", "市场", "合作化", "工业化"]):
                categories["经济思想"].add(concept)
            # 文化教育
            elif any(keyword in concept for keyword in ["文化", "教育", "文艺", "学习", "知识", "普及", "提高"]):
                categories["文化教育"].add(concept)
            # 领导艺术
            elif any(keyword in concept for keyword in ["领导", "干部", "群众", "服务", "民主集中", "团结", "统一战线"]):
                categories["领导艺术"].add(concept)
            else:
                categories["高频词"].add(concept)
        
        # 统计每个分类的大小
        category_stats = {cat: len(concepts) for cat, concepts in categories.items()}
        
        return categories, category_stats
    
    def generate_relationship_report(self, output_dir="reports/concept_relations"):
        """生成关系报告"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 基本概念统计
        basic_stats = {
            "total_concepts": len(self.concepts),
            "concept_frequency_distribution": dict(sorted(self.concept_freq.items(), key=lambda x: x[1], reverse=True)[:50]),
            "concept_by_category": {cat: list(concepts)[:20] for cat, concepts in self.concept_by_category.items()}
        }
        
        with open(output_dir / "basic_concept_stats.json", 'w', encoding='utf-8') as f:
            json.dump(basic_stats, f, ensure_ascii=False, indent=2)
        
        # 2. 共现关系
        strong_relations = self.analyze_cooccurrence()
        if strong_relations:
            relations_data = {
                "strong_relations": strong_relations[:100],  # 前100个最强关系
                "total_relations": len(strong_relations)
            }
            
            with open(output_dir / "concept_cooccurrence.json", 'w', encoding='utf-8') as f:
                json.dump(relations_data, f, ensure_ascii=False, indent=2)
        
        # 3. 图统计
        if self.graph.number_of_nodes() > 0:
            graph_stats = self.calculate_graph_stats()
            
            with open(output_dir / "concept_graph_stats.json", 'w', encoding='utf-8') as f:
                json.dump(graph_stats, f, ensure_ascii=False, indent=2)
            
            # 保存图数据（GEXF格式，可用于Gephi等工具）
            nx.write_gexf(self.graph, output_dir / "concept_graph.gexf")
        
        # 4. 概念分类
        categories, category_stats = self.categorize_concepts()
        
        category_data = {
            "category_stats": category_stats,
            "categories": {cat: list(concepts)[:50] for cat, concepts in categories.items()}
        }
        
        with open(output_dir / "concept_categories.json", 'w', encoding='utf-8') as f:
            json.dump(category_data, f, ensure_ascii=False, indent=2)
        
        # 5. 生成Markdown报告
        self.generate_markdown_report(output_dir)
        
        print(f"关系报告已生成到: {output_dir}")
        
        return output_dir
    
    def generate_markdown_report(self, output_dir):
        """生成Markdown报告"""
        md_content = f"""# 毛泽东著作概念关系分析报告

## 📊 总体统计

### 概念体系
- **总概念数**: {len(self.concepts)}
- **高频概念** (前20):
"""

        # 添加高频概念
        top_concepts = sorted(self.concept_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        for i, (concept, freq) in enumerate(top_concepts, 1):
            md_content += f"{i}. **{concept}** - {freq}次\n"
        
        # 概念分类
        categories, category_stats = self.categorize_concepts()
        md_content += f"""
### 概念分类统计
| 分类 | 概念数 | 比例 |
|------|--------|------|
"""
        total_concepts = len(self.concepts)
        for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_concepts) * 100
            md_content += f"| {category} | {count} | {percentage:.1f}% |\n"
        
        # 图统计
        if self.graph.number_of_nodes() > 0:
            graph_stats = self.calculate_graph_stats()
            md_content += f"""
## 🕸️ 概念网络分析

### 网络基本属性
- **节点数**: {graph_stats.get('node_count', 0)}
- **边数**: {graph_stats.get('edge_count', 0)}
- **平均度**: {graph_stats.get('avg_degree', 0):.2f}
- **连通分量数**: {graph_stats.get('component_count', 0)}
- **最大连通分量大小**: {graph_stats.get('largest_component_size', 0)}
- **平均聚类系数**: {graph_stats.get('average_clustering', 0):.3f}

### 核心概念 (度中心性)
| 概念 | 度中心性 |
|------|----------|
"""
            for concept, centrality in graph_stats.get("top_nodes_by_degree", [])[:10]:
                md_content += f"| {concept} | {centrality:.4f} |\n"
        
        # 强关系
        strong_relations = self.analyze_cooccurrence()
        if strong_relations:
            md_content += f"""
## 🔗 强共现关系 (共现≥3次)

| 概念1 | 概念2 | 共现次数 |
|-------|-------|----------|
"""
            for concept1, concept2, count in strong_relations[:20]:
                md_content += f"| {concept1} | {concept2} | {count} |\n"
        
        # 文件分类分布
        md_content += f"""
## 📂 概念的文件分类分布

| 分类 | 概念数 | 示例概念 |
|------|--------|----------|
"""
        for category, concepts in self.concept_by_category.items():
            example_concepts = ", ".join(list(concepts)[:5])
            md_content += f"| {category} | {len(concepts)} | {example_concepts} |\n"
        
        md_content += f"""
## 🎯 知识图谱构建建议

### 1. 核心概念群识别
基于度中心性和介数中心性分析，识别以下核心概念群：
- **革命相关概念群**: 革命、斗争、人民、群众、党
- **方法论概念群**: 实践、矛盾、调查研究、群众路线
- **军事概念群**: 战争、战略、战术、军队、敌人

### 2. 关系挖掘重点
建议重点挖掘以下概念关系：
1. **阶级关系**: 无产阶级、资产阶级、小资产阶级之间的关系
2. **方法关系**: 调查研究、群众路线、批评与自我批评之间的关系
3. **战略关系**: 战略防御、持久战、运动战、游击战之间的关系

### 3. 知识图谱应用方向
1. **智能问答**: 基于概念关系回答毛泽东方法论相关问题
2. **内容推荐**: 根据用户兴趣推荐相关著作和概念
3. **学习路径**: 构建毛泽东方法论学习路径图
4. **比较分析**: 分析不同著作的概念分布和关系差异

---

**报告生成时间**: {self.get_timestamp()}
**数据源**: {self.batch_file.name if self.batch_file else "未知"}
**分析方法**: 共现分析 + 网络分析 + 分类分析

*注：此报告为初步分析结果，可用于指导知识图谱的深度构建*
"""
        
        report_file = output_dir / "concept_relation_analysis_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Markdown报告已生成: {report_file}")
    
    def get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def visualize_concept_network(self, output_file="concept_network.png"):
        """可视化概念网络（简单版本）"""
        if self.graph.number_of_nodes() == 0:
            print("图为空，无法可视化")
            return
        
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(15, 15))
            
            # 使用spring布局
            pos = nx.spring_layout(self.graph, k=0.5, iterations=50)
            
            # 节点大小基于度
            node_sizes = [self.graph.degree(n) * 50 for n in self.graph.nodes()]
            
            # 节点颜色基于概念类别
            node_colors = []
            categories, _ = self.categorize_concepts()
            for node in self.graph.nodes():
                for color_idx, (category, concepts) in enumerate(categories.items()):
                    if node in concepts:
                        node_colors.append(color_idx)
                        break
                else:
                    node_colors.append(len(categories))  # 默认颜色
            
            # 绘制图
            nx.draw_networkx_nodes(self.graph, pos, node_size=node_sizes, 
                                  node_color=node_colors, cmap=plt.cm.tab20, alpha=0.8)
            
            # 只绘制权重较高的边
            edges = [(u, v) for (u, v, d) in self.graph.edges(data=True) if d['weight'] >= 3]
            nx.draw_networkx_edges(self.graph, pos, edgelist=edges, alpha=0.2)
            
            # 只标注重要的节点
            important_nodes = [n for n in self.graph.nodes() if self.graph.degree(n) >= 10]
            labels = {n: n for n in important_nodes}
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=10)
            
            plt.title(f"毛泽东著作概念关系网络 ({self.graph.number_of_nodes()}个节点, {self.graph.number_of_edges()}条边)")
            plt.axis('off')
            plt.tight_layout()
            
            output_path = Path("reports/concept_relations") / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"概念网络图已保存: {output_path}")
            
        except Exception as e:
            print(f"可视化失败: {e}")
            print("请确保已安装matplotlib: pip install matplotlib")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="概念关系分析器")
    parser.add_argument("--batch-file", help="批量处理结果文件路径")
    parser.add_argument("--min-cooccurrence", type=int, default=2, help="最小共现次数阈值")
    parser.add_argument("--visualize", action="store_true", help="生成可视化图")
    parser.add_argument("--quick", action="store_true", help="快速模式，只进行基本分析")
    
    args = parser.parse_args()
    
    print("🔍 开始概念关系分析...")
    
    analyzer = ConceptRelationAnalyzer(args.batch_file)
    
    try:
        # 1. 加载数据
        analyzer.load_batch_data()
        
        # 2. 提取概念
        analyzer.extract_concepts()
        
        # 3. 分析共现关系
        strong_relations = analyzer.analyze_cooccurrence()
        if strong_relations:
            print(f"发现 {len(strong_relations)} 个强共现关系 (共现≥3次)")
            print("前5个最强关系:")
            for i, (c1, c2, count) in enumerate(strong_relations[:5], 1):
                print(f"  {i}. {c1} ↔ {c2}: {count}次")
        
        # 4. 构建概念图
        stats = analyzer.build_concept_graph(min_cooccurrence=args.min_cooccurrence)
        if stats:
            print(f"概念图统计: {stats['node_count']}节点, {stats['edge_count']}边, 平均度{stats['avg_degree']:.2f}")
        
        # 5. 生成报告
        output_dir = analyzer.generate_relationship_report()
        
        # 6. 可视化（如果请求）
        if args.visualize:
            analyzer.visualize_concept_network()
        
        print(f"""
✅ 概念关系分析完成！
📈 总概念数: {len(analyzer.concepts)}
🔗 强关系数: {len(strong_relations) if strong_relations else 0}
🕸️ 概念网络: {analyzer.graph.number_of_nodes()}节点, {analyzer.graph.number_of_edges()}边
📄 报告目录: {output_dir}
""")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())