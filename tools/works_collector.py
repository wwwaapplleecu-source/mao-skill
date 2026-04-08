#!/usr/bin/env python3
"""
毛泽东著作收集工具
用于从可靠来源收集和整理毛泽东著作
"""

import os
import re
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class MaoWorksCollector:
    """毛泽东著作收集器"""
    
    def __init__(self, knowledge_base_path: str = "knowledge"):
        self.knowledge_base = Path(knowledge_base_path)
        self.sources = self._load_sources()
        
    def _load_sources(self) -> Dict[str, str]:
        """加载著作来源配置"""
        return {
            "新民主主义论": "毛泽东选集第二卷",
            "中国革命战争的战略问题": "毛泽东选集第一卷",
            "关于正确处理人民内部矛盾的问题": "毛泽东选集第五卷",
            "纪念白求恩": "毛泽东选集第二卷",
            "关心群众生活，注意工作方法": "毛泽东选集第一卷",
            "论联合政府": "毛泽东选集第三卷",
            "论人民民主专政": "毛泽东选集第四卷",
            "湖南农民运动考察报告": "毛泽东选集第一卷",
            "抗日游击战争的战略问题": "毛泽东选集第二卷",
            "集中优势兵力，各个歼灭敌人": "毛泽东选集第四卷",
            "战争和战略问题": "毛泽东选集第二卷",
            "人的正确思想是从哪里来的？": "毛泽东著作选读",
            "反对本本主义": "毛泽东选集第一卷",
            "改造我们的学习": "毛泽东选集第三卷",
            "愚公移山": "毛泽东选集第三卷",
            "关于重庆谈判": "毛泽东选集第四卷",
            "在扩大的中央工作会议上的讲话": "毛泽东文集第八卷",
            "给雷经天的信": "毛泽东书信选集",
            "致郭沫若": "毛泽东书信选集",
            "致宋庆龄": "毛泽东书信选集",
            "致李达": "毛泽东书信选集",
            "读《辩证法唯物论教程》批注": "毛泽东哲学批注集",
            "读《政治经济学教科书》批注": "毛泽东读社会主义政治经济学批注和谈话",
            "读史笔记摘录": "毛泽东读史笔记",
            "辩证法唯物论提纲": "毛泽东哲学思想研究资料",
            "关于哲学问题的谈话": "毛泽东哲学思想研究资料",
            "党委会的工作方法": "毛泽东选集第四卷",
            "关于健全党委制": "毛泽东选集第四卷",
            "工作方法六十条（草案）": "毛泽东文集第七卷"
        }
    
    def get_work_info(self, title: str) -> Dict[str, str]:
        """获取著作信息"""
        if title not in self.sources:
            return {
                "title": title,
                "source": "未知来源",
                "category": self._guess_category(title),
                "writing_time": "时间未知",
                "description": "暂无描述"
            }
        
        category = self._guess_category(title)
        
        # 估计写作时间（基于历史知识）
        writing_times = {
            "新民主主义论": "1940年1月",
            "中国革命战争的战略问题": "1936年12月",
            "关于正确处理人民内部矛盾的问题": "1957年2月",
            "纪念白求恩": "1939年12月",
            "关心群众生活，注意工作方法": "1934年1月",
            "论联合政府": "1945年4月",
            "论人民民主专政": "1949年6月",
            "湖南农民运动考察报告": "1927年3月",
            "抗日游击战争的战略问题": "1938年5月",
            "集中优势兵力，各个歼灭敌人": "1946年9月",
            "战争和战略问题": "1938年11月",
            "人的正确思想是从哪里来的？": "1963年5月",
            "反对本本主义": "1930年5月",
            "改造我们的学习": "1941年5月",
            "愚公移山": "1945年6月",
            "关于重庆谈判": "1945年10月",
            "在扩大的中央工作会议上的讲话": "1962年1月",
            "给雷经天的信": "1937年10月",
            "致郭沫若": "1944年11月",
            "致宋庆龄": "1936年9月",
            "致李达": "1951年3月",
            "读《辩证法唯物论教程》批注": "1936-1937年",
            "读《政治经济学教科书》批注": "1959-1960年",
            "读史笔记摘录": "多种时间",
            "辩证法唯物论提纲": "1937年",
            "关于哲学问题的谈话": "1964年8月",
            "党委会的工作方法": "1949年3月",
            "关于健全党委制": "1948年9月",
            "工作方法六十条（草案）": "1958年1月"
        }
        
        writing_time = writing_times.get(title, "时间未知")
        
        return {
            "title": title,
            "source": self.sources[title],
            "category": category,
            "writing_time": writing_time,
            "description": self._generate_description(title, category)
        }
    
    def _guess_category(self, title: str) -> str:
        """根据标题猜测分类"""
        title_lower = title.lower()
        
        # 分类关键词映射
        category_keywords = {
            "methodology": ["实践", "矛盾", "正确处理", "本本", "改造", "学习", "思想", "哲学"],
            "military": ["战争", "战略", "军事", "游击", "歼灭", "持久", "兵力"],
            "selected_works": ["新民主", "论联合", "论人民", "湖南农民", "考察报告"],
            "speeches": ["讲话", "纪念", "白求恩", "愚公", "移山", "重庆", "谈判"],
            "letters": ["信", "致", "给", "同志"],
            "annotations": ["批注", "笔记", "读", "摘录"],
            "philosophy": ["哲学", "唯物", "辩证", "提纲", "谈话"],
            "work_methods": ["关心", "群众", "工作方法", "党委", "领导", "方法"]
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    return category
        
        # 默认分类
        if any(word in title_lower for word in ["论", "报告", "问题"]):
            return "selected_works"
        elif any(word in title_lower for word in ["讲话", "纪念"]):
            return "speeches"
        else:
            return "selected_works"
    
    def _generate_description(self, title: str, category: str) -> str:
        """生成著作描述"""
        descriptions = {
            "新民主主义论": "毛泽东关于中国新民主主义革命理论的重要著作，系统阐述了新民主主义革命的性质、任务、动力和前途。",
            "中国革命战争的战略问题": "毛泽东总结中国革命战争经验的重要军事著作，系统阐述了人民战争的战略战术原则。",
            "关于正确处理人民内部矛盾的问题": "毛泽东关于社会主义社会矛盾问题的重要著作，提出了正确处理人民内部矛盾的理论。",
            "纪念白求恩": "毛泽东为纪念国际主义战士白求恩而写的文章，提倡毫不利己专门利人的精神。",
            "关心群众生活，注意工作方法": "毛泽东关于群众路线和工作方法的重要文章，强调要关心群众生活，改进工作方法。",
            "论联合政府": "毛泽东在中共七大上的政治报告，系统阐述了建立联合政府的主张。",
            "论人民民主专政": "毛泽东为纪念中国共产党成立28周年而写的文章，阐述了人民民主专政的理论。",
            "湖南农民运动考察报告": "毛泽东对湖南农民运动进行实地考察后写的报告，高度评价农民运动的伟大作用。",
            "抗日游击战争的战略问题": "毛泽东关于抗日游击战争战略问题的重要军事著作。",
            "集中优势兵力，各个歼灭敌人": "毛泽东提出的重要军事原则，强调在战役战术上要集中优势兵力。"
        }
        
        return descriptions.get(title, f"毛泽东的重要著作《{title}》，属于{category}类别。")
    
    def create_work_template(self, title: str, content: str = None) -> str:
        """创建著作模板文件"""
        work_info = self.get_work_info(title)
        
        # 构建Markdown内容
        template = f"""# {work_info['title']}

**作者**: 毛泽东  
**写作时间**: {work_info['writing_time']}  
**来源**: 《{work_info['source']}》  
**分类**: {work_info['category']}

---

## 内容简介

{work_info['description']}

---

## 正文

"""
        
        if content:
            template += f"{content}\n\n"
        else:
            template += f"*此处应放置《{title}》的完整正文内容*\n\n"
            template += "**说明**: 此文件为著作模板，需要补充完整著作内容。\n"
            template += "请从可靠来源获取完整文本，确保内容准确无误。\n\n"
        
        template += """---

## 历史意义

*（此处可简要说明该著作的历史意义和影响）*

## 核心观点

1. *核心观点一*
2. *核心观点二*
3. *核心观点三*

## 方法论价值

*（此处可说明该著作中包含的方法论价值）*

---

**收集时间**: {collection_time}  
**状态**: ⚠️ 需要补充完整内容  
**验证状态**: 待验证

**关键词**: {keywords}
""".format(
    collection_time=datetime.now().strftime("%Y-%m-%d"),
    keywords=self._extract_keywords(title)
)
        
        return template
    
    def _extract_keywords(self, title: str) -> str:
        """提取关键词"""
        # 简单的关键词提取
        keywords_map = {
            "新民主主义论": "新民主主义, 革命, 资产阶级, 无产阶级, 统一战线",
            "中国革命战争的战略问题": "战争, 战略, 人民战争, 军事, 革命",
            "关于正确处理人民内部矛盾的问题": "矛盾, 人民内部矛盾, 社会主义, 民主, 批评",
            "纪念白求恩": "白求恩, 国际主义, 共产主义, 牺牲, 精神",
            "关心群众生活，注意工作方法": "群众路线, 工作方法, 群众生活, 领导, 方法",
            "论联合政府": "联合政府, 民主, 政治, 国共合作, 抗战",
            "论人民民主专政": "人民民主专政, 国家, 阶级, 民主, 专政",
            "湖南农民运动考察报告": "农民运动, 农村, 革命, 考察, 报告",
            "抗日游击战争的战略问题": "游击战争, 抗日, 战略, 军事, 战争",
            "集中优势兵力，各个歼灭敌人": "军事原则, 兵力, 歼灭, 战术, 战争"
        }
        
        return keywords_map.get(title, "毛泽东, 著作, 方法论")
    
    def save_work(self, title: str, content: str = None, force: bool = False) -> bool:
        """保存著作文件"""
        work_info = self.get_work_info(title)
        category = work_info["category"]
        
        # 确定保存路径
        category_dir = self.knowledge_base / category
        category_dir.mkdir(exist_ok=True)
        
        file_path = category_dir / f"{title}.md"
        
        # 检查文件是否已存在
        if file_path.exists() and not force:
            print(f"⚠️ 文件已存在: {file_path}")
            return False
        
        # 创建内容
        template = self.create_work_template(title, content)
        
        # 保存文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template)
            print(f"✅ 已创建著作文件: {file_path}")
            print(f"   分类: {category}")
            print(f"   来源: {work_info['source']}")
            print(f"   时间: {work_info['writing_time']}")
            return True
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
            return False
    
    def create_works_index(self) -> bool:
        """创建著作索引文件"""
        index_file = self.knowledge_base / "著作索引.md"
        
        # 收集所有著作信息
        works = []
        for category_dir in self.knowledge_base.iterdir():
            if category_dir.is_dir():
                for work_file in category_dir.glob("*.md"):
                    if work_file.name != "README.md":
                        works.append({
                            "title": work_file.stem,
                            "category": category_dir.name,
                            "path": work_file.relative_to(self.knowledge_base.parent)
                        })
        
        # 按分类组织
        works_by_category = {}
        for work in works:
            category = work["category"]
            if category not in works_by_category:
                works_by_category[category] = []
            works_by_category[category].append(work)
        
        # 生成索引内容
        index_content = """# 毛泽东著作索引

本索引列出了毛泽东.skill知识库中收录的所有毛泽东著作。

## 著作统计

- **总著作数**: {total_works}
- **分类数**: {total_categories}
- **最后更新**: {update_time}

## 分类索引

""".format(
    total_works=len(works),
    total_categories=len(works_by_category),
    update_time=datetime.now().strftime("%Y年%m月%d日")
)
        
        # 添加各分类的著作列表
        for category, category_works in sorted(works_by_category.items()):
            index_content += f"\n### {self._get_category_name(category)}\n\n"
            
            for work in sorted(category_works, key=lambda x: x["title"]):
                index_content += f"- **{work['title']}**  \n"
                index_content += f"  路径: `{work['path']}`  \n"
            
            index_content += f"\n**共计**: {len(category_works)} 篇著作\n"
        
        # 添加使用说明
        index_content += """
---

## 使用说明

### 1. 阅读著作
所有著作均以Markdown格式保存，可直接阅读或使用Markdown阅读器打开。

### 2. 贡献著作
如需添加新的毛泽东著作，请遵循以下步骤：
1. 确保著作来源可靠，内容准确
2. 使用标准Markdown格式
3. 包含完整的元数据（作者、时间、来源等）
4. 提交前进行校对

### 3. 报告问题
如发现著作内容有误或需要更新，请通过GitHub Issues报告。

### 4. 学术引用
如需学术引用，请参考原始出版物或权威版本。

---

**维护者**: 毛泽东.skill项目组  
**版本**: 1.0  
**更新频率**: 每月更新一次
"""
        
        # 保存索引文件
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            print(f"✅ 已创建著作索引: {index_file}")
            print(f"   总计著作: {len(works)} 篇")
            print(f"   分类数量: {len(works_by_category)} 个")
            return True
        except Exception as e:
            print(f"❌ 创建索引失败: {e}")
            return False
    
    def _get_category_name(self, category_key: str) -> str:
        """获取分类中文名称"""
        category_names = {
            "methodology": "哲学方法论类",
            "military": "军事战略类", 
            "selected_works": "选集著作类",
            "speeches": "重要讲话类",
            "letters": "书信选集类",
            "annotations": "批注笔记类",
            "philosophy": "哲学思考类",
            "work_methods": "工作方法类"
        }
        return category_names.get(category_key, category_key)
    
    def batch_create_templates(self, titles: List[str]) -> Dict[str, bool]:
        """批量创建著作模板"""
        results = {}
        for title in titles:
            print(f"\n处理著作: 《{title}》")
            success = self.save_work(title)
            results[title] = success
        return results

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东著作收集工具")
    parser.add_argument("--title", help="单个著作标题")
    parser.add_argument("--batch", help="批量创建，传入JSON文件路径")
    parser.add_argument("--index", action="store_true", help="创建著作索引")
    parser.add_argument("--list-sources", action="store_true", help="列出支持的著作")
    parser.add_argument("--category", help="指定分类")
    
    args = parser.parse_args()
    
    collector = MaoWorksCollector()
    
    if args.list_sources:
        print("支持的毛泽东著作:")
        print("=" * 60)
        for i, (title, source) in enumerate(collector.sources.items(), 1):
            category = collector._guess_category(title)
            print(f"{i:2d}. 《{title}》")
            print(f"    来源: 《{source}》")
            print(f"    分类: {category} ({collector._get_category_name(category)})")
            print()
    
    elif args.index:
        collector.create_works_index()
    
    elif args.batch:
        # 批量创建
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                titles = json.load(f)
            
            if isinstance(titles, list):
                print(f"批量创建 {len(titles)} 个著作模板:")
                results = collector.batch_create_templates(titles)
                
                print("\n" + "=" * 60)
                print("批量创建结果:")
                success_count = sum(1 for success in results.values() if success)
                print(f"成功: {success_count}/{len(titles)}")
                
        except Exception as e:
            print(f"❌ 批量创建失败: {e}")
    
    elif args.title:
        # 单个创建
        collector.save_work(args.title)
    
    else:
        # 交互模式
        print("毛泽东著作收集工具")
        print("=" * 60)
        
        print("\n可选的毛泽东重要著作:")
        sample_titles = list(collector.sources.keys())[:10]
        for i, title in enumerate(sample_titles, 1):
            print(f"{i}. 《{title}》")
        
        print("\n输入著作标题（或输入'退出'结束）:")
        
        while True:
            user_input = input("\n请输入著作标题: ").strip()
            
            if user_input.lower() in ["退出", "exit", "quit"]:
                break
            
            if user_input:
                collector.save_work(user_input)
            else:
                print("请输入有效的著作标题")

if __name__ == "__main__":
    main()