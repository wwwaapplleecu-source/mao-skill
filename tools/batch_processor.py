#!/usr/bin/env python3
"""
毛泽东著作批量处理器
用于批量处理knowledge目录下的所有著作文件，提取概念，更新概念词典

功能：
1. 扫描knowledge目录下的所有.md文件
2. 使用text_processor处理每个文件
3. 提取概念并合并到全局概念词典
4. 生成处理报告
5. 更新概念词典文件

用法：
    python3 batch_processor.py --input-dir ./knowledge --output-dir ./processed
    python3 batch_processor.py --stats  # 生成统计报告
    python3 batch_processor.py --update-concepts  # 更新概念词典
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict
import argparse
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.text_processor import MaoTextProcessor
    print("✅ 成功导入MaoTextProcessor")
except ImportError as e:
    print(f"❌ 导入MaoTextProcessor失败: {e}")
    sys.exit(1)

class MaoBatchProcessor:
    """毛泽东著作批量处理器"""
    
    def __init__(self, input_dir: str = "knowledge", output_dir: str = "processed"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.processor = MaoTextProcessor()
        self.concepts_counter = Counter()  # 全局概念计数器
        self.files_processed = 0
        self.total_files = 0
        self.file_stats = []  # 文件处理统计
        self.errors = []
        
    def scan_files(self) -> List[Path]:
        """扫描输入目录下的所有.md文件"""
        md_files = []
        for ext in [".md", ".txt"]:
            md_files.extend(self.input_dir.rglob(f"*{ext}"))
        
        # 过滤掉README.md和目录说明文件
        filtered_files = []
        for file_path in md_files:
            file_name = file_path.name.lower()
            if "readme" in file_name or "目录" in file_name or "指南" in file_name:
                continue
            filtered_files.append(file_path)
        
        self.total_files = len(filtered_files)
        print(f"📁 找到 {self.total_files} 个著作文件")
        return filtered_files
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """处理单个文件"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取文件名和分类信息
            relative_path = file_path.relative_to(self.input_dir)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "unknown"
            
            # 提取概念
            concepts = self.processor.extract_concepts(content)
            
            # 添加到全局计数器
            self.concepts_counter.update(concepts)
            
            # 统计文件信息
            stats = {
                "file_path": str(file_path),
                "relative_path": str(relative_path),
                "category": category,
                "content_length": len(content),
                "concepts_count": len(concepts),
                "top_concepts": dict(sorted(concepts.items(), key=lambda x: x[1], reverse=True)[:10]),
                "success": True
            }
            
            self.files_processed += 1
            print(f"  ✅ 处理: {relative_path} ({len(content)}字符, {len(concepts)}概念)")
            
            return stats
            
        except Exception as e:
            error_msg = f"处理文件 {file_path} 失败: {e}"
            print(f"  ❌ {error_msg}")
            self.errors.append(error_msg)
            
            return {
                "file_path": str(file_path),
                "category": "error",
                "success": False,
                "error": str(e)
            }
    
    def process_all(self) -> Dict[str, Any]:
        """处理所有文件"""
        print("🚀 开始批量处理毛泽东著作...")
        print("=" * 70)
        
        files = self.scan_files()
        
        if not files:
            print("⚠️ 未找到任何著作文件")
            return {"status": "error", "message": "未找到文件"}
        
        for file_path in files:
            stats = self.process_file(file_path)
            self.file_stats.append(stats)
        
        # 生成汇总报告
        summary = self.generate_summary()
        
        print("=" * 70)
        print(f"🎉 批量处理完成!")
        print(f"  已处理: {self.files_processed}/{self.total_files} 个文件")
        print(f"  提取概念: {len(self.concepts_counter)} 个唯一概念")
        print(f"  总概念出现次数: {sum(self.concepts_counter.values())}")
        
        if self.errors:
            print(f"⚠️ 错误: {len(self.errors)} 个")
            for error in self.errors[:5]:  # 显示前5个错误
                print(f"  - {error}")
        
        return summary
    
    def generate_summary(self) -> Dict[str, Any]:
        """生成处理摘要"""
        # 按分类统计
        category_stats = defaultdict(lambda: {"files": 0, "concepts": 0, "content_length": 0})
        
        for stats in self.file_stats:
            if stats.get("success"):
                category = stats["category"]
                category_stats[category]["files"] += 1
                category_stats[category]["concepts"] += stats.get("concepts_count", 0)
                category_stats[category]["content_length"] += stats.get("content_length", 0)
        
        # 最常见的概念
        top_concepts = self.concepts_counter.most_common(50)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "total_files": self.total_files,
            "files_processed": self.files_processed,
            "errors_count": len(self.errors),
            "total_concepts": len(self.concepts_counter),
            "total_concept_occurrences": sum(self.concepts_counter.values()),
            "category_stats": dict(category_stats),
            "top_concepts": dict(top_concepts),
            "file_stats": self.file_stats,
            "errors": self.errors
        }
        
        return summary
    
    def save_summary(self, summary: Dict[str, Any], output_file: str = None):
        """保存处理摘要"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"batch_processing_summary_{timestamp}.json"
        else:
            output_file = Path(output_file)
        
        # 确保输出目录存在
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"📁 处理摘要已保存到: {output_file}")
        return output_file
    
    def update_concept_dictionary(self, min_count: int = 2):
        """更新概念词典文件"""
        print("🔄 更新概念词典...")
        
        # 加载现有的概念词典
        concept_dict_path = project_root / "tools" / "concept_dictionary.json"
        existing_concepts = {}
        
        if concept_dict_path.exists():
            try:
                with open(concept_dict_path, 'r', encoding='utf-8') as f:
                    existing_concepts = json.load(f)
                print(f"  已加载现有概念词典: {len(existing_concepts)} 个概念")
            except Exception as e:
                print(f"  ⚠️ 加载现有概念词典失败: {e}")
        
        # 合并概念
        merged_concepts = dict(existing_concepts)
        
        # 添加新概念或更新计数
        for concept, count in self.concepts_counter.items():
            if count >= min_count:  # 只保留出现次数足够多的概念
                if concept in merged_concepts:
                    # 更新计数（取最大值）
                    merged_concepts[concept] = max(merged_concepts[concept], count)
                else:
                    merged_concepts[concept] = count
        
        # 排序并保存
        sorted_concepts = dict(sorted(merged_concepts.items(), key=lambda x: x[1], reverse=True))
        
        with open(concept_dict_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_concepts, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 概念词典已更新: {len(sorted_concepts)} 个概念")
        print(f"  新增/更新概念: {len(sorted_concepts) - len(existing_concepts)} 个")
        
        return sorted_concepts
    
    def generate_statistics_report(self):
        """生成统计报告"""
        print("📊 生成统计报告...")
        
        summary = self.generate_summary()
        
        # 创建Markdown报告
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_lines = [
            "# 毛泽东著作批量处理统计报告",
            "",
            f"**生成时间**: {timestamp}",
            f"**处理目录**: {self.input_dir}",
            "",
            "## 处理摘要",
            "",
            f"- **总文件数**: {summary['total_files']}",
            f"- **已处理文件**: {summary['files_processed']}",
            f"- **处理错误**: {summary['errors_count']}",
            f"- **提取概念数**: {summary['total_concepts']}",
            f"- **概念出现总次数**: {summary['total_concept_occurrences']}",
            ""
        ]
        
        # 分类统计
        report_lines.extend([
            "## 分类统计",
            "",
            "| 分类 | 文件数 | 总字符数 | 概念数 |",
            "|------|--------|----------|--------|"
        ])
        
        for category, stats in summary["category_stats"].items():
            report_lines.append(f"| {category} | {stats['files']} | {stats['content_length']} | {stats['concepts']} |")
        
        report_lines.extend(["", ""])
        
        # 最常见概念
        report_lines.extend([
            "## 最常见概念 (前20)",
            "",
            "| 概念 | 出现次数 |",
            "|------|----------|"
        ])
        
        for concept, count in list(summary["top_concepts"].items())[:20]:
            report_lines.append(f"| {concept} | {count} |")
        
        report_lines.extend(["", ""])
        
        # 文件详情
        report_lines.extend([
            "## 文件处理详情",
            "",
            "| 文件路径 | 分类 | 字符数 | 概念数 | 状态 |",
            "|----------|------|--------|--------|------|"
        ])
        
        for stats in summary["file_stats"]:
            if stats.get("success"):
                status = "✅"
                concepts = stats.get("concepts_count", 0)
                length = stats.get("content_length", 0)
            else:
                status = "❌"
                concepts = 0
                length = 0
            
            file_path = stats.get("relative_path", stats.get("file_path", "unknown"))
            category = stats.get("category", "unknown")
            
            report_lines.append(f"| {file_path} | {category} | {length} | {concepts} | {status} |")
        
        # 如果有错误，添加错误部分
        if summary["errors"]:
            report_lines.extend([
                "",
                "## 处理错误",
                ""
            ])
            
            for error in summary["errors"]:
                report_lines.append(f"- {error}")
        
        report_lines.extend([
            "",
            "## 后续步骤建议",
            "",
            "1. **补充缺失内容**: 根据概念提取结果，识别内容不完整的著作",
            "2. **扩展概念词典**: 基于新提取的概念，完善毛泽东方法论概念体系",
            "3. **质量验证**: 检查提取概念的质量和准确性",
            "4. **知识图谱构建**: 基于概念关系，开始知识图谱构建工作",
            ""
        ])
        
        # 保存报告
        report_dir = project_root / "reports" / "batch_processing"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"batch_processing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        
        print(f"📄 统计报告已生成: {report_file}")
        
        return report_file

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="毛泽东著作批量处理器")
    parser.add_argument("--input-dir", default="knowledge", help="输入目录 (默认: knowledge)")
    parser.add_argument("--output-dir", default="processed", help="输出目录 (默认: processed)")
    parser.add_argument("--process", action="store_true", help="批量处理所有文件")
    parser.add_argument("--stats", action="store_true", help="生成统计报告")
    parser.add_argument("--update-concepts", action="store_true", help="更新概念词典")
    parser.add_argument("--all", action="store_true", help="执行所有操作 (处理 + 统计 + 更新)")
    
    args = parser.parse_args()
    
    processor = MaoBatchProcessor(
        input_dir=args.input_dir,
        output_dir=args.output_dir
    )
    
    # 确保输出目录存在
    processor.output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.process or args.all:
        # 批量处理
        summary = processor.process_all()
        
        # 保存摘要
        summary_file = processor.save_summary(summary)
        print(f"📁 处理摘要: {summary_file}")
    
    if args.stats or args.all:
        # 生成统计报告
        if not processor.file_stats and args.stats and not args.process:
            # 如果没有处理数据，先处理文件
            print("⚠️ 未找到处理数据，先执行批量处理...")
            summary = processor.process_all()
            processor.save_summary(summary)
        
        report_file = processor.generate_statistics_report()
        print(f"📄 统计报告: {report_file}")
    
    if args.update_concepts or args.all:
        # 更新概念词典
        if not processor.concepts_counter and args.update_concepts and not args.process:
            # 如果没有概念数据，先处理文件
            print("⚠️ 未找到概念数据，先执行批量处理...")
            summary = processor.process_all()
            processor.save_summary(summary)
        
        updated_concepts = processor.update_concept_dictionary()
        print(f"📚 概念词典已更新: {len(updated_concepts)} 个概念")
    
    if not any([args.process, args.stats, args.update_concepts, args.all]):
        print("ℹ️ 请指定操作参数:")
        print("  --process        批量处理所有文件")
        print("  --stats          生成统计报告")
        print("  --update-concepts 更新概念词典")
        print("  --all            执行所有操作")
        print("\n示例:")
        print("  python batch_processor.py --all")
        print("  python batch_processor.py --process --update-concepts")

if __name__ == "__main__":
    main()