#!/usr/bin/env python3
"""
综合修复所有文件名编码问题
1. 修复knowledge目录中的Markdown文件名
2. 修复processed目录中的JSON文件名
"""

import os
import json
import shutil
from pathlib import Path

def fix_knowledge_filenames():
    """修复knowledge目录中的文件名"""
    knowledge_dir = Path("knowledge")
    if not knowledge_dir.exists():
        print("knowledge目录不存在")
        return 0
    
    print("修复knowledge目录文件名...")
    
    # 已知的文件映射（基于之前创建的示例内容）
    file_mapping = {
        # methodology目录
        "methodology/ʵ����.md": "实践论.md",
        "methodology/ì����.md": "矛盾论.md",
        
        # military目录  
        "military/�۳־�ս.md": "论持久战.md",
        
        # selected_works目录
        "selected_works/ë��ѡ��ȫ��.md": "毛泽东选集全卷.md",
        
        # speeches目录
        "speeches/Ϊ�������.md": "为人民服务.md",
        "speeches/���Ӱ�������̸���ϵĽ�������ѡ��.md": "在延安文艺座谈会上的讲话（节选）.md",
        
        # letters目录
        "letters/��������ͬ־����.md": "致徐特立同志的信.md",
        
        # annotations目录
        "annotations/��ѧ��עժ¼.md": "哲学批注摘录.md",
        
        # philosophy目录
        "philosophy/�����������Ȼ��˼��.md": "关于自由与必然的思考.md",
        
        # work_methods目录
        "work_methods/�����쵼��������������.md": "关于领导方法的若干问题.md",
    }
    
    fixed_count = 0
    
    for old_path_str, new_name in file_mapping.items():
        old_path = knowledge_dir / old_path_str
        if old_path.exists():
            new_path = old_path.parent / new_name
            if new_path != old_path:
                try:
                    # 如果目标文件已存在，先删除
                    if new_path.exists():
                        new_path.unlink()
                    
                    # 重命名文件
                    old_path.rename(new_path)
                    print(f"  ✓ {old_path.name} -> {new_name}")
                    fixed_count += 1
                except Exception as e:
                    print(f"  ✗ 重命名失败: {old_path.name} -> {new_name}, 错误: {e}")
            else:
                print(f"  ✓ {old_path.name} 已是正确文件名")
                fixed_count += 1
        else:
            # 尝试直接使用新文件名检查
            parts = old_path_str.split('/')
            if len(parts) == 2:
                dir_name, old_file_name = parts
                check_path = knowledge_dir / dir_name / new_name
                if check_path.exists():
                    print(f"  ✓ {new_name} 已是正确文件名")
                    fixed_count += 1
                else:
                    print(f"  ? 文件不存在: {old_path_str}")
    
    print(f"knowledge目录修复完成，处理 {fixed_count} 个文件")
    return fixed_count

def fix_processed_filenames():
    """修复processed目录中的JSON文件名"""
    processed_dir = Path("processed")
    if not processed_dir.exists():
        print("processed目录不存在")
        return 0
    
    print("\n修复processed目录文件名...")
    
    fixed_count = 0
    
    # 首先读取summary.json获取正确的文件名映射
    summary_file = processed_dir / "summary.json"
    if not summary_file.exists():
        print("  summary.json不存在，无法修复")
        return 0
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        summary = json.load(f)
    
    # 收集title到文件的映射
    title_to_file = {}
    for doc in summary.get("documents", []):
        file_path = doc.get("file", "")
        title = doc.get("title", "")
        
        if file_path and title and title != "README":
            # 提取文件名
            filename = Path(file_path).name
            title_to_file[filename] = f"{title}.json"
    
    # 修复所有JSON文件
    json_files = list(processed_dir.glob("*.json"))
    
    for json_file in json_files:
        if json_file.name == "summary.json" or json_file.name == "README.json":
            continue
            
        # 尝试从文件内容读取title
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            title = content.get("title", "")
            if not title:
                # 尝试从文件名映射获取
                if json_file.name in title_to_file:
                    new_name = title_to_file[json_file.name]
                else:
                    continue
            else:
                new_name = f"{title}.json"
            
            # 重命名文件
            new_path = json_file.parent / new_name
            if new_path != json_file:
                try:
                    # 如果目标文件已存在，先删除
                    if new_path.exists():
                        new_path.unlink()
                    
                    json_file.rename(new_path)
                    print(f"  ✓ {json_file.name} -> {new_name}")
                    fixed_count += 1
                except Exception as e:
                    print(f"  ✗ 重命名失败: {json_file.name} -> {new_name}, 错误: {e}")
            else:
                print(f"  ✓ {json_file.name} 已是正确文件名")
                fixed_count += 1
                
        except Exception as e:
            print(f"  ? 处理失败: {json_file.name}, 错误: {e}")
    
    print(f"processed目录修复完成，处理 {fixed_count} 个文件")
    return fixed_count

def verify_fixes():
    """验证修复结果"""
    print("\n验证修复结果...")
    
    # 检查knowledge目录
    knowledge_dir = Path("knowledge")
    if knowledge_dir.exists():
        print("\nknowledge/ 目录内容:")
        subdirs = ["methodology", "military", "selected_works", "speeches", "letters", "annotations", "philosophy", "work_methods"]
        
        for subdir in subdirs:
            dir_path = knowledge_dir / subdir
            if dir_path.exists():
                print(f"\n{subdir}/:")
                files = list(dir_path.glob("*.md"))
                if files:
                    for file_path in sorted(files):
                        print(f"  - {file_path.name}")
                else:
                    print("  (空目录)")
    
    # 检查processed目录
    processed_dir = Path("processed")
    if processed_dir.exists():
        print("\nprocessed/ 目录内容:")
        files = list(processed_dir.glob("*.json"))
        if files:
            for file_path in sorted(files):
                print(f"  - {file_path.name}")
        else:
            print("  (空目录)")

def main():
    """主函数"""
    print("=" * 60)
    print("毛泽东.skill 文件名综合修复工具")
    print("=" * 60)
    
    total_fixed = 0
    total_fixed += fix_knowledge_filenames()
    total_fixed += fix_processed_filenames()
    
    verify_fixes()
    
    print(f"\n总计修复: {total_fixed} 个文件")
    print("修复完成！")

if __name__ == "__main__":
    main()