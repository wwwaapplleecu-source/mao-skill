#!/usr/bin/env python3
"""
毛泽东著作文本处理器

功能：
1. 文本清洗和格式化
2. 分段和章节识别
3. 概念提取和术语统计
4. 文体分类（理论/讲话/书信/批注）
5. 输出结构化数据，供分析使用

用法：
    python3 text_processor.py --input-dir ./knowledge --output-dir ./processed
    python3 text_processor.py --file ./knowledge/shijianlun.txt --output ./processed/shijianlun.json
"""

import json
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from collections import Counter
import jieba
import jieba.analyse

# 毛泽东著作特有概念词典
MAO_CONCEPTS = {
    # 哲学概念
    "实践论", "矛盾论", "实事求是", "群众路线", "阶级斗争",
    "主要矛盾", "次要矛盾", "矛盾转化", "对立统一", "辩证唯物主义",
    "历史唯物主义", "主观主义", "客观主义", "教条主义", "经验主义",
    
    # 政治概念
    "新民主主义", "社会主义", "共产主义", "统一战线", "人民民主专政",
    "无产阶级", "资产阶级", "小资产阶级", "工农联盟", "人民战争",
    
    # 工作方法
    "调查研究", "批评与自我批评", "惩前毖后", "治病救人", "从群众中来",
    "到群众中去", "集中起来", "坚持下去", "试点推广", "典型试验",
    
    # 军事概念
    "持久战", "运动战", "阵地战", "游击战", "人民战争",
    "战略防御", "战略相持", "战略反攻", "集中优势兵力", "各个歼灭",
    "战略上藐视", "战术上重视", "不打无准备之仗", "保存自己", "消灭敌人",
    
    # 高频词
    "革命", "建设", "斗争", "团结", "胜利", "失败", "困难", "光明",
    "我们", "你们", "他们", "同志", "人民", "群众", "党", "国家",
}

@dataclass
class TextSegment:
    """文本片段"""
    text: str
    segment_type: str  # "paragraph", "title", "quote", "list"
    metadata: Dict[str, Any]
    
@dataclass
class ProcessedDocument:
    """处理后的文档"""
    title: str
    original_file: str
    segments: List[TextSegment]
    concepts: Dict[str, int]  # 概念 -> 出现次数
    stats: Dict[str, Any]
    metadata: Dict[str, Any]

class MaoTextProcessor:
    """毛泽东著作文本处理器"""
    
    def __init__(self):
        # 初始化分词工具
        jieba.initialize()
        
        # 添加自定义词典
        for concept in MAO_CONCEPTS:
            jieba.add_word(concept)
        
        # 正则模式
        self.title_pattern = re.compile(r'^第[一二三四五六七八九十]+[章节卷篇]')
        self.section_pattern = re.compile(r'^[一二三四五六七八九十]+、')
        self.quote_pattern = re.compile(r'^["\'「」『』"“”]')
        
    def clean_text(self, text: str) -> str:
        """清理文本"""
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 统一引号
        text = text.replace('"', '“').replace("'", "‘")
        # 处理特殊字符
        text = text.replace('□', ' ').replace('■', ' ')
        return text.strip()
    
    def segment_text(self, text: str, filename: str) -> List[TextSegment]:
        """分段处理文本"""
        segments = []
        lines = text.split('\n')
        
        current_paragraph = []
        current_type = "paragraph"
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_paragraph:
                    segments.append(TextSegment(
                        text=' '.join(current_paragraph),
                        segment_type=current_type,
                        metadata={"source": filename}
                    ))
                    current_paragraph = []
                    current_type = "paragraph"
                continue
            
            # 判断行类型
            if self.title_pattern.match(line):
                # 标题行
                if current_paragraph:
                    segments.append(TextSegment(
                        text=' '.join(current_paragraph),
                        segment_type=current_type,
                        metadata={"source": filename}
                    ))
                    current_paragraph = []
                
                segments.append(TextSegment(
                    text=line,
                    segment_type="title",
                    metadata={"source": filename, "level": 1}
                ))
                current_type = "paragraph"
            
            elif self.section_pattern.match(line):
                # 小标题
                if current_paragraph:
                    segments.append(TextSegment(
                        text=' '.join(current_paragraph),
                        segment_type=current_type,
                        metadata={"source": filename}
                    ))
                    current_paragraph = []
                
                segments.append(TextSegment(
                    text=line,
                    segment_type="title",
                    metadata={"source": filename, "level": 2}
                ))
                current_type = "paragraph"
            
            elif line.startswith('注：') or line.startswith('注释：'):
                # 注释
                segments.append(TextSegment(
                    text=line,
                    segment_type="note",
                    metadata={"source": filename}
                ))
            
            elif self.quote_pattern.match(line):
                # 引用
                segments.append(TextSegment(
                    text=line,
                    segment_type="quote",
                    metadata={"source": filename}
                ))
            
            else:
                # 普通段落
                current_paragraph.append(line)
        
        # 处理最后一段
        if current_paragraph:
            segments.append(TextSegment(
                text=' '.join(current_paragraph),
                segment_type=current_type,
                metadata={"source": filename}
            ))
        
        return segments
    
    def extract_concepts(self, text: str) -> Dict[str, int]:
        """提取概念和术语"""
        # 使用jieba提取关键词
        keywords = jieba.analyse.extract_tags(
            text, 
            topK=50, 
            allowPOS=('n', 'ns', 'nt', 'nz', 'v', 'a')
        )
        
        # 统计概念出现次数
        concept_counts = Counter()
        words = jieba.lcut(text)
        
        for word in words:
            if word in MAO_CONCEPTS:
                concept_counts[word] += 1
        
        # 添加关键词
        for kw in keywords:
            if kw not in concept_counts:
                concept_counts[kw] = 1
        
        return dict(concept_counts)
    
    def analyze_style(self, text: str) -> Dict[str, Any]:
        """分析文本风格"""
        # 句子长度分析
        sentences = re.split(r'[。！？；]', text)
        sentence_lengths = [len(s) for s in sentences if s.strip()]
        
        # 修辞手法检测
        rhetorical_patterns = {
            "排比": r'[，；]?既要[^，；]*又要[^，；]*(?:[，；]还要[^，；]*)?',
            "设问": r'[。！？][^。！？]*怎么办[？\?]|[^。！？]*为什么[？\?]',
            "对比": r'[^。！？]*不是[^。！？]*而是[^。！？]*[。！？]',
            "比喻": r'[^。！？]*像[^。！？]*一样[^。！？]*[。！？]|[^。！？]*是[^。！？]*的[^。！？]*[。！？]',
        }
        
        rhetoric_counts = {}
        for name, pattern in rhetorical_patterns.items():
            matches = re.findall(pattern, text)
            rhetoric_counts[name] = len(matches)
        
        # 高频词分析
        words = jieba.lcut(text)
        word_freq = Counter(words)
        top_words = dict(word_freq.most_common(20))
        
        return {
            "avg_sentence_length": sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
            "sentence_count": len(sentence_lengths),
            "word_count": len(words),
            "rhetoric_counts": rhetoric_counts,
            "top_words": top_words,
        }
    
    def classify_document(self, filename: str, content: str) -> str:
        """文档分类"""
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # 根据文件名分类
        if any(kw in filename_lower for kw in ["实践论", "矛盾论", "论持久战"]):
            return "philosophy"
        elif any(kw in filename_lower for kw in ["选集", "文集"]):
            return "selected_works"
        elif any(kw in filename_lower for kw in ["书信", "信件"]):
            return "letters"
        elif any(kw in filename_lower for kw in ["批注", "笔记"]):
            return "annotations"
        elif any(kw in filename_lower for kw in ["讲话", "发言", "报告"]):
            return "speeches"
        elif any(kw in filename_lower for kw in ["军事", "战争", "战略"]):
            return "military"
        
        # 根据内容分类
        philosophy_keywords = ["实践论", "矛盾论", "辩证法", "唯物主义"]
        military_keywords = ["战争", "战略", "战术", "军队", "军事"]
        
        if any(kw in content_lower for kw in philosophy_keywords):
            return "philosophy"
        elif any(kw in content_lower for kw in military_keywords):
            return "military"
        
        return "other"
    
    def process_file(self, filepath: Path) -> Optional[ProcessedDocument]:
        """处理单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='gbk') as f:
                    content = f.read()
            except:
                print(f"无法读取文件: {filepath}")
                return None
        
        # 清理文本
        cleaned_content = self.clean_text(content)
        
        # 分段
        segments = self.segment_text(cleaned_content, filepath.name)
        
        # 提取概念
        full_text = ' '.join([seg.text for seg in segments])
        concepts = self.extract_concepts(full_text)
        
        # 分析风格
        stats = self.analyze_style(full_text)
        
        # 文档分类
        doc_type = self.classify_document(filepath.name, full_text)
        
        # 提取标题（假设第一行是标题）
        title = filepath.stem
        if segments and segments[0].segment_type == "title":
            title = segments[0].text
        
        return ProcessedDocument(
            title=title,
            original_file=str(filepath),
            segments=[{"text": seg.text, "type": seg.segment_type, "metadata": seg.metadata} 
                     for seg in segments],
            concepts=concepts,
            stats=stats,
            metadata={
                "filename": filepath.name,
                "filepath": str(filepath),
                "doc_type": doc_type,
                "segment_count": len(segments),
                "processing_time": "2025-04-08",  # 实际应该用datetime.now()
            }
        )
    
    def process_directory(self, input_dir: Path, output_dir: Path):
        """处理整个目录"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 支持的文本文件扩展名
        text_extensions = {'.txt', '.md', '.json', '.xml'}
        
        all_docs = []
        
        for filepath in input_dir.rglob('*'):
            if filepath.is_file() and filepath.suffix.lower() in text_extensions:
                print(f"处理文件: {filepath}")
                
                doc = self.process_file(filepath)
                if doc:
                    # 保存单个文档
                    output_file = output_dir / f"{filepath.stem}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump({
                            "title": doc.title,
                            "original_file": doc.original_file,
                            "segments": doc.segments,
                            "concepts": doc.concepts,
                            "stats": doc.stats,
                            "metadata": doc.metadata
                        }, f, ensure_ascii=False, indent=2)
                    
                    all_docs.append({
                        "title": doc.title,
                        "file": str(output_file),
                        "type": doc.metadata["doc_type"],
                        "segment_count": doc.metadata["segment_count"],
                        "concept_count": len(doc.concepts),
                    })
        
        # 保存汇总信息
        if all_docs:
            summary_file = output_dir / "summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_documents": len(all_docs),
                    "documents": all_docs,
                    "processing_date": "2025-04-08",
                    "concept_library": list(MAO_CONCEPTS),
                }, f, ensure_ascii=False, indent=2)
            
            print(f"处理完成！共处理 {len(all_docs)} 个文档")
            print(f"汇总信息: {summary_file}")
        
        return all_docs

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东著作文本处理器")
    parser.add_argument("--input-dir", help="输入目录路径")
    parser.add_argument("--output-dir", help="输出目录路径")
    parser.add_argument("--file", help="处理单个文件")
    parser.add_argument("--output", help="单个文件输出路径")
    
    args = parser.parse_args()
    
    processor = MaoTextProcessor()
    
    if args.file:
        # 处理单个文件
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"文件不存在: {args.file}")
            sys.exit(1)
        
        doc = processor.process_file(filepath)
        if doc:
            output_path = Path(args.output) if args.output else filepath.with_suffix('.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "title": doc.title,
                    "original_file": doc.original_file,
                    "segments": doc.segments,
                    "concepts": doc.concepts,
                    "stats": doc.stats,
                    "metadata": doc.metadata
                }, f, ensure_ascii=False, indent=2)
            
            print(f"文件处理完成: {output_path}")
    
    elif args.input_dir and args.output_dir:
        # 处理目录
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        
        if not input_dir.exists():
            print(f"输入目录不存在: {args.input_dir}")
            sys.exit(1)
        
        processor.process_directory(input_dir, output_dir)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    # 测试代码
    if len(sys.argv) == 1:
        # 显示帮助信息
        main()
    else:
        main()
