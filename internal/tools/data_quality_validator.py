#!/usr/bin/env python3
"""
数据质量验证器

检查著作文件的完整性，评估数据质量，生成报告
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import os

class DataQualityValidator:
    """数据质量验证器"""
    
    def __init__(self, knowledge_dir="knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.results = {}
        
    def scan_all_files(self):
        """扫描所有知识库文件"""
        files = []
        for ext in ["*.md", "*.txt"]:
            files.extend(self.knowledge_dir.rglob(ext))
        return files
    
    def evaluate_file_quality(self, file_path: Path) -> Dict[str, Any]:
        """评估单个文件的质量"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                "file_path": str(file_path),
                "error": str(e),
                "quality_score": 0,
                "status": "error"
            }
        
        # 计算质量指标
        metrics = self.calculate_metrics(content, file_path)
        
        # 计算质量分数（0-100）
        quality_score = self.calculate_quality_score(metrics)
        
        # 确定状态
        status = self.determine_status(quality_score, metrics)
        
        return {
            "file_path": str(file_path),
            "relative_path": str(file_path.relative_to(self.knowledge_dir)),
            "quality_score": quality_score,
            "status": status,
            "metrics": metrics,
            "recommendations": self.generate_recommendations(metrics)
        }
    
    def calculate_metrics(self, content: str, file_path: Path) -> Dict[str, Any]:
        """计算质量指标"""
        metrics = {}
        
        # 基础指标
        metrics["content_length"] = len(content)
        metrics["line_count"] = content.count('\n') + 1
        
        # 结构指标
        metrics["section_count"] = len(re.findall(r'^#{1,3}\s+', content, re.MULTILINE))
        metrics["has_author"] = "作者" in content and "毛泽东" in content
        metrics["has_date"] = bool(re.search(r'写作时间|时间.*\d{4}', content))
        metrics["has_content_intro"] = "内容简介" in content or "正文" in content
        
        # 内容指标
        metrics["has_body"] = "正文" in content or "###" in content
        metrics["has_conclusion"] = "总结" in content or "历史意义" in content or "核心观点" in content
        metrics["has_methodology"] = "方法论" in content or "方法" in content
        
        # 格式指标
        metrics["has_proper_headings"] = bool(re.search(r'^#\s+[^\n]+$', content, re.MULTILINE))
        metrics["has_separators"] = "---" in content or "***" in content or "====" in content
        
        # 概念密度（简单估算）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        metrics["chinese_char_count"] = chinese_chars
        metrics["concept_density"] = chinese_chars / max(1, len(content))
        
        # 文件类型判断
        file_name = file_path.name.lower()
        metrics["is_template"] = "模板" in content or "示例" in content or file_name.endswith("_template.md")
        metrics["is_backup"] = "backup" in file_name.lower() or "备份" in file_name
        
        return metrics
    
    def calculate_quality_score(self, metrics: Dict[str, Any]) -> float:
        """计算质量分数（0-100）"""
        score = 0
        max_score = 100
        
        # 1. 内容长度 (20分)
        if metrics["content_length"] > 10000:
            score += 20
        elif metrics["content_length"] > 5000:
            score += 15
        elif metrics["content_length"] > 1000:
            score += 10
        elif metrics["content_length"] > 500:
            score += 5
        
        # 2. 结构完整性 (30分)
        structure_score = 0
        if metrics["has_author"]:
            structure_score += 5
        if metrics["has_date"]:
            structure_score += 5
        if metrics["has_content_intro"]:
            structure_score += 5
        if metrics["has_body"]:
            structure_score += 10
        if metrics["has_conclusion"]:
            structure_score += 5
        
        score += min(structure_score, 30)
        
        # 3. 章节结构 (20分)
        if metrics["section_count"] >= 5:
            score += 20
        elif metrics["section_count"] >= 3:
            score += 15
        elif metrics["section_count"] >= 2:
            score += 10
        elif metrics["section_count"] >= 1:
            score += 5
        
        # 4. 格式规范 (15分)
        format_score = 0
        if metrics["has_proper_headings"]:
            format_score += 5
        if metrics["has_separators"]:
            format_score += 5
        if not metrics["is_template"] and not metrics["is_backup"]:
            format_score += 5
        
        score += min(format_score, 15)
        
        # 5. 方法论内容 (15分)
        if metrics["has_methodology"]:
            score += 15
        elif metrics["concept_density"] > 0.6:  # 中文内容密度高
            score += 10
        
        return min(score, 100)
    
    def determine_status(self, quality_score: float, metrics: Dict[str, Any]) -> str:
        """确定文件状态"""
        if metrics.get("is_template", False):
            return "template"
        if metrics.get("is_backup", False):
            return "backup"
        
        if quality_score >= 80:
            return "excellent"
        elif quality_score >= 60:
            return "good"
        elif quality_score >= 40:
            return "fair"
        elif quality_score >= 20:
            return "poor"
        else:
            return "incomplete"
    
    def generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        if metrics["content_length"] < 1000:
            recommendations.append("增加内容长度，补充更多原文或分析")
        
        if not metrics["has_author"]:
            recommendations.append("添加作者信息（毛泽东）")
        
        if not metrics["has_date"]:
            recommendations.append("添加写作时间或历史时期")
        
        if not metrics["has_content_intro"]:
            recommendations.append("添加内容简介或摘要")
        
        if not metrics["has_body"]:
            recommendations.append("添加正文内容，使用##或###标题组织章节")
        
        if not metrics["has_conclusion"]:
            recommendations.append("添加总结、历史意义或核心观点部分")
        
        if metrics["section_count"] < 3:
            recommendations.append("增加章节结构，使用更多标题层级")
        
        if not metrics["has_methodology"]:
            recommendations.append("补充方法论相关内容，如分析框架、核心观点等")
        
        if metrics["is_template"]:
            recommendations.append("将此模板文件替换为实际内容")
        
        return recommendations
    
    def validate_all(self) -> Dict[str, Any]:
        """验证所有文件"""
        files = self.scan_all_files()
        print(f"扫描到 {len(files)} 个文件")
        
        results = []
        for file_path in files:
            print(f"验证: {file_path.relative_to(self.knowledge_dir)}")
            result = self.evaluate_file_quality(file_path)
            results.append(result)
        
        # 分类统计
        self.results = results
        summary = self.generate_summary(results)
        
        return {
            "summary": summary,
            "results": results,
            "timestamp": self.get_timestamp()
        }
    
    def generate_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """生成摘要统计"""
        total_files = len(results)
        
        # 按状态统计
        status_counts = {}
        quality_scores = []
        
        for result in results:
            status = result["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
            if "quality_score" in result:
                quality_scores.append(result["quality_score"])
        
        # 按目录分类
        category_counts = {}
        for result in results:
            file_path = Path(result["file_path"])
            relative_path = file_path.relative_to(self.knowledge_dir)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else "root"
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # 平均质量分数
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            "total_files": total_files,
            "status_counts": status_counts,
            "category_counts": category_counts,
            "avg_quality_score": round(avg_quality, 2),
            "quality_score_distribution": {
                "excellent": len([s for s in quality_scores if s >= 80]),
                "good": len([s for s in quality_scores if 60 <= s < 80]),
                "fair": len([s for s in quality_scores if 40 <= s < 60]),
                "poor": len([s for s in quality_scores if 20 <= s < 40]),
                "incomplete": len([s for s in quality_scores if s < 20])
            }
        }
    
    def get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_report(self, report: Dict[str, Any], output_file: str = "data_quality_report.json"):
        """保存报告"""
        output_path = Path("reports") / "data_quality" / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"报告已保存: {output_path}")
        
        # 同时生成Markdown摘要
        self.generate_markdown_summary(report, output_path.with_suffix('.md'))
        
        return output_path
    
    def generate_markdown_summary(self, report: Dict[str, Any], output_file: Path):
        """生成Markdown摘要报告"""
        summary = report["summary"]
        results = report["results"]
        
        md_content = f"""# 数据质量验证报告

**生成时间**: {report["timestamp"]}
**总文件数**: {summary["total_files"]}
**平均质量分数**: {summary["avg_quality_score"]}/100

## 📊 总体统计

### 质量分布
| 等级 | 文件数 | 百分比 |
|------|--------|--------|
"""
        # 添加质量分布
        for level, count in summary["quality_score_distribution"].items():
            percentage = (count / summary["total_files"]) * 100
            md_content += f"| {level} | {count} | {percentage:.1f}% |\n"
        
        md_content += f"""
### 状态分布
| 状态 | 文件数 |
|------|--------|
"""
        for status, count in summary["status_counts"].items():
            md_content += f"| {status} | {count} |\n"
        
        md_content += f"""
### 目录分布
| 目录 | 文件数 |
|------|--------|
"""
        for category, count in sorted(summary["category_counts"].items()):
            md_content += f"| {category} | {count} |\n"
        
        # 高质量文件（得分>=80）
        excellent_files = [r for r in results if r.get("quality_score", 0) >= 80 and r.get("status") not in ["template", "backup"]]
        if excellent_files:
            md_content += f"""
## 🏆 高质量文件 (得分≥80)

| 文件 | 质量分 | 状态 | 长度 |
|------|--------|------|------|
"""
            for file in sorted(excellent_files, key=lambda x: x["quality_score"], reverse=True)[:10]:
                md_content += f"| {file['relative_path']} | {file['quality_score']} | {file['status']} | {file['metrics']['content_length']} |\n"
        
        # 需要改进的文件（得分<40）
        poor_files = [r for r in results if r.get("quality_score", 0) < 40 and r.get("status") not in ["template", "backup"]]
        if poor_files:
            md_content += f"""
## ⚠️ 需要改进的文件 (得分<40)

| 文件 | 质量分 | 主要问题 | 建议 |
|------|--------|----------|------|
"""
            for file in sorted(poor_files, key=lambda x: x["quality_score"])[:10]:
                # 提取主要问题（前2条建议）
                main_issues = ", ".join(file.get("recommendations", [])[:2])
                md_content += f"| {file['relative_path']} | {file['quality_score']} | {main_issues[:50]}... | 查看详细建议 |\n"
        
        # 详细文件列表
        md_content += f"""
## 📁 详细文件列表

| 文件 | 质量分 | 状态 | 长度 | 章节数 | 建议数 |
|------|--------|------|------|--------|--------|
"""
        for file in sorted(results, key=lambda x: x["relative_path"]):
            if file.get("status") in ["template", "backup"]:
                continue
            md_content += f"| {file['relative_path']} | {file['quality_score']} | {file['status']} | {file['metrics']['content_length']} | {file['metrics']['section_count']} | {len(file.get('recommendations', []))} |\n"
        
        md_content += f"""
## 🔧 改进建议汇总

### 常见问题及解决方案
1. **内容过短** - 补充原文内容，添加详细分析
2. **缺少结构** - 添加标准章节：作者、时间、内容简介、正文、总结
3. **缺少方法论** - 补充方法论分析，如矛盾分析、实践指导等
4. **格式不规范** - 使用标准Markdown格式，添加分隔线

### 优先改进顺序
建议优先改进质量分低于40的文件，特别是核心著作（selected_works目录下的文件）。

---

*报告由数据质量验证器自动生成*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Markdown报告已保存: {output_file}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="数据质量验证器")
    parser.add_argument("--knowledge-dir", default="knowledge", help="知识库目录路径")
    parser.add_argument("--output", default="data_quality_report.json", help="输出报告文件名")
    parser.add_argument("--quick", action="store_true", help="快速模式，只扫描主要文件")
    
    args = parser.parse_args()
    
    print("🔍 开始数据质量验证...")
    validator = DataQualityValidator(args.knowledge_dir)
    
    print("📂 扫描文件...")
    report = validator.validate_all()
    
    print("📊 生成报告...")
    output_path = validator.save_report(report, args.output)
    
    print(f"""
✅ 验证完成！
📈 总文件数: {report['summary']['total_files']}
⭐ 平均质量分: {report['summary']['avg_quality_score']}/100
📄 报告文件: {output_path}
""")
    
    # 显示简要统计
    summary = report["summary"]
    print("📋 质量分布:")
    for level, count in summary["quality_score_distribution"].items():
        print(f"  {level}: {count} 个文件")

if __name__ == "__main__":
    main()