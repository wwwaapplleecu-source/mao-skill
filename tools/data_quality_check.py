#!/usr/bin/env python3
"""
毛泽东著作数据质量检查工具

功能：
1. 扫描knowledge目录中的所有著作文件
2. 评估每个文件的完整性指标
3. 生成数据质量报告
4. 提供改进建议

完整性指标：
- 字符数 (超过1000字符为基本完整)
- 章节数量 (至少3个章节为良好)
- 概念提取数量 (至少20个概念为良好)
- 是否存在内容完整度标记
- 文件格式规范度

使用方法：
    python3 data_quality_check.py --scan
    python3 data_quality_check.py --report
"""

import json
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import jieba
import jieba.analyse

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.text_processor import MaoTextProcessor
    TEXT_PROCESSOR_AVAILABLE = True
except ImportError:
    print("⚠️  文本处理器不可用，概念提取功能受限")
    TEXT_PROCESSOR_AVAILABLE = False

class DataQualityChecker:
    """数据质量检查器"""
    
    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.results = {}
        self.processor = MaoTextProcessor() if TEXT_PROCESSOR_AVAILABLE else None
        
    def scan_files(self) -> List[Path]:
        """扫描所有著作文件"""
        files = []
        # 排除备份文件和临时文件
        exclude_patterns = [
            "_backup_", "_extracted", "_complete", "_v\\d+",
            "著作索引.md", "README.md", "目录结构.md"
        ]
        
        for file_path in self.knowledge_dir.rglob("*.md"):
            if file_path.is_file():
                # 检查是否应该排除
                exclude = False
                for pattern in exclude_patterns:
                    if pattern in file_path.name:
                        exclude = True
                        break
                
                if not exclude:
                    files.append(file_path)
        
        return sorted(files)
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个文件的数据质量"""
        result = {
            "file_path": str(file_path.relative_to(self.knowledge_dir)),
            "file_size": file_path.stat().st_size,
            "character_count": 0,
            "line_count": 0,
            "section_count": 0,
            "concept_count": 0,
            "has_completeness_mark": False,
            "has_author_info": False,
            "has_category": False,
            "has_content_intro": False,
            "format_score": 0,
            "completeness_score": 0,
            "issues": [],
            "suggestions": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 基础统计
            result["character_count"] = len(content)
            result["line_count"] = len(content.splitlines())
            
            # 章节统计 (基于Markdown标题)
            section_pattern = r'^#{1,3}\s+.+$'
            sections = re.findall(section_pattern, content, re.MULTILINE)
            result["section_count"] = len(sections)
            
            # 检查关键元数据
            result["has_author_info"] = "**作者**:" in content or "作者:" in content
            result["has_category"] = "**分类**:" in content or "分类:" in content
            result["has_content_intro"] = "## 内容简介" in content or "内容简介" in content
            
            # 检查内容完整度标记
            completeness_patterns = [
                r"内容完整度.*[:：]\s*\d+%",
                r"内容完整度.*[:：]\s*待评估",
                r"**完整度**.*[:：]\s*\d+%"
            ]
            for pattern in completeness_patterns:
                if re.search(pattern, content):
                    result["has_completeness_mark"] = True
                    break
            
            # 概念提取
            if self.processor:
                try:
                    processed = self.processor.process_text(content)
                    result["concept_count"] = len(processed.get("top_concepts", []))
                except:
                    result["concept_count"] = 0
                    result["issues"].append("概念提取失败")
            else:
                # 简单概念计数
                words = jieba.lcut(content)
                unique_words = set(words)
                result["concept_count"] = len([w for w in unique_words if len(w) >= 2])
            
            # 格式评分 (0-10分)
            format_score = 0
            if result["has_author_info"]:
                format_score += 2
            if result["has_category"]:
                format_score += 2
            if result["has_content_intro"]:
                format_score += 2
            if result["section_count"] >= 3:
                format_score += 2
            if result["character_count"] > 1000:
                format_score += 2
            
            result["format_score"] = min(10, format_score)
            
            # 完整性评分 (0-100分)
            completeness_score = 0
            
            # 字符数贡献 (最多30分)
            char_score = min(30, result["character_count"] / 1000 * 10)
            completeness_score += char_score
            
            # 章节数贡献 (最多20分)
            section_score = min(20, result["section_count"] * 5)
            completeness_score += section_score
            
            # 概念数贡献 (最多20分)
            concept_score = min(20, result["concept_count"] / 10 * 5)
            completeness_score += concept_score
            
            # 格式分贡献 (最多30分)
            completeness_score += result["format_score"] * 3
            
            result["completeness_score"] = min(100, int(completeness_score))
            
            # 问题检测和建议
            if result["character_count"] < 500:
                result["issues"].append("内容过短")
                result["suggestions"].append("补充更多原文内容")
            
            if result["section_count"] < 2:
                result["issues"].append("结构简单")
                result["suggestions"].append("添加更多章节和结构")
            
            if not result["has_author_info"]:
                result["issues"].append("缺少作者信息")
                result["suggestions"].append("添加作者和写作时间")
            
            if not result["has_completeness_mark"]:
                result["suggestions"].append("添加内容完整度标记")
            
            if result["completeness_score"] < 50:
                result["suggestions"].append("需要大幅补充内容")
            elif result["completeness_score"] < 70:
                result["suggestions"].append("建议补充部分内容")
            elif result["completeness_score"] < 85:
                result["suggestions"].append("内容基本完整，可优化格式")
            else:
                result["suggestions"].append("内容完整度良好")
                
        except Exception as e:
            result["issues"].append(f"分析错误: {str(e)}")
            result["completeness_score"] = 0
        
        return result
    
    def run_scan(self, output_file: Optional[str] = None) -> Dict[str, Any]:
        """运行完整扫描"""
        print("🔍 开始扫描毛泽东著作数据质量...")
        files = self.scan_files()
        print(f"📁 找到 {len(files)} 个著作文件")
        
        results = {}
        total_score = 0
        file_count = 0
        
        for i, file_path in enumerate(files, 1):
            print(f"  [{i}/{len(files)}] 分析: {file_path.name}")
            rel_path = str(file_path.relative_to(self.knowledge_dir))
            result = self.analyze_file(file_path)
            results[rel_path] = result
            
            if result["completeness_score"] > 0:
                total_score += result["completeness_score"]
                file_count += 1
        
        # 生成汇总报告
        summary = {
            "scan_time": Path(".").resolve().name,
            "total_files": len(files),
            "files_analyzed": file_count,
            "average_completeness_score": round(total_score / max(1, file_count), 1),
            "files_by_score_range": {
                "excellent_90_100": len([r for r in results.values() if r["completeness_score"] >= 90]),
                "good_70_89": len([r for r in results.values() if 70 <= r["completeness_score"] < 90]),
                "fair_50_69": len([r for r in results.values() if 50 <= r["completeness_score"] < 70]),
                "poor_0_49": len([r for r in results.values() if r["completeness_score"] < 50]),
            },
            "common_issues": [],
            "recommendations": []
        }
        
        # 收集常见问题
        all_issues = []
        for result in results.values():
            all_issues.extend(result["issues"])
        
        from collections import Counter
        issue_counter = Counter(all_issues)
        summary["common_issues"] = issue_counter.most_common(10)
        
        # 生成总体建议
        if summary["average_completeness_score"] < 60:
            summary["recommendations"].append("整体数据质量较低，需要大幅补充著作内容")
        elif summary["average_completeness_score"] < 75:
            summary["recommendations"].append("数据质量中等，建议补充关键著作内容")
        else:
            summary["recommendations"].append("数据质量良好，可优化格式和元数据")
        
        report = {
            "summary": summary,
            "details": results
        }
        
        # 保存结果
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"📄 数据质量报告已保存到: {output_path}")
        
        # 控制台输出摘要
        print("\n📊 数据质量扫描完成")
        print(f"   平均完整度评分: {summary['average_completeness_score']}/100")
        print(f"   优秀文件 (90-100): {summary['files_by_score_range']['excellent_90_100']}个")
        print(f"   良好文件 (70-89): {summary['files_by_score_range']['good_70_89']}个")
        print(f"   一般文件 (50-69): {summary['files_by_score_range']['fair_50_69']}个")
        print(f"   较差文件 (0-49): {summary['files_by_score_range']['poor_0_49']}个")
        
        if summary["common_issues"]:
            print("\n⚠️  常见问题:")
            for issue, count in summary["common_issues"][:5]:
                print(f"   - {issue}: {count}个文件")
        
        if summary["recommendations"]:
            print("\n💡 建议:")
            for rec in summary["recommendations"]:
                print(f"   - {rec}")
        
        return report
    
    def generate_markdown_report(self, report: Dict[str, Any], output_file: str):
        """生成Markdown格式的报告"""
        summary = report["summary"]
        details = report["details"]
        
        lines = []
        lines.append("# 毛泽东著作数据质量检查报告")
        lines.append(f"**生成时间**: {summary['scan_time']}")
        lines.append(f"**扫描文件数**: {summary['total_files']}")
        lines.append(f"**平均完整度评分**: {summary['average_completeness_score']}/100")
        lines.append("")
        
        # 评分分布
        lines.append("## 评分分布")
        lines.append(f"- 优秀 (90-100分): {summary['files_by_score_range']['excellent_90_100']}个文件")
        lines.append(f"- 良好 (70-89分): {summary['files_by_score_range']['good_70_89']}个文件")
        lines.append(f"- 一般 (50-69分): {summary['files_by_score_range']['fair_50_69']}个文件")
        lines.append(f"- 较差 (0-49分): {summary['files_by_score_range']['poor_0_49']}个文件")
        lines.append("")
        
        # 详细文件列表
        lines.append("## 文件详细分析")
        lines.append("| 文件 | 字符数 | 章节数 | 概念数 | 格式分 | 完整度 | 状态 |")
        lines.append("|------|--------|--------|--------|--------|--------|------|")
        
        for file_path, result in sorted(details.items(), key=lambda x: x[1]["completeness_score"], reverse=True):
            status = "✅" if result["completeness_score"] >= 70 else "⚠️" if result["completeness_score"] >= 50 else "❌"
            lines.append(f"| {file_path} | {result['character_count']} | {result['section_count']} | {result['concept_count']} | {result['format_score']}/10 | {result['completeness_score']}/100 | {status} |")
        
        lines.append("")
        
        # 建议
        lines.append("## 改进建议")
        for rec in summary["recommendations"]:
            lines.append(f"- {rec}")
        
        # 写入文件
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        
        print(f"📄 Markdown报告已生成: {output_path}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东著作数据质量检查工具")
    parser.add_argument("--scan", action="store_true", help="运行数据质量扫描")
    parser.add_argument("--report", action="store_true", help="生成Markdown报告")
    parser.add_argument("--output", default="reports/data_quality/data_quality_report.json", help="输出JSON文件路径")
    parser.add_argument("--md-output", default="reports/data_quality/data_quality_report.md", help="输出Markdown文件路径")
    
    args = parser.parse_args()
    
    checker = DataQualityChecker()
    
    if args.scan or args.report:
        report = checker.run_scan(args.output if args.scan else None)
        
        if args.report:
            checker.generate_markdown_report(report, args.md_output)
    else:
        # 默认运行扫描和报告
        report = checker.run_scan(args.output)
        checker.generate_markdown_report(report, args.md_output)

if __name__ == "__main__":
    main()