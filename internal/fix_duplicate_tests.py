#!/usr/bin/env python3
import json

def fix_duplicate_tests():
    """修复测试套件中的重复测试项"""
    with open('tests/test_suite.json', 'r', encoding='utf-8') as f:
        test_suite = json.load(f)
    
    # 找到边界测试类别
    boundary_tests = None
    for category in test_suite:
        if category['category'] == '边界测试':
            boundary_tests = category
            break
    
    if boundary_tests:
        # 去重：基于测试名称
        unique_tests = []
        seen_names = set()
        
        for test in boundary_tests['tests']:
            if test['name'] not in seen_names:
                seen_names.add(test['name'])
                unique_tests.append(test)
            else:
                print(f"删除重复测试: {test['name']}")
        
        # 更新测试列表
        boundary_tests['tests'] = unique_tests
        
        # 写回文件
        with open('tests/test_suite.json', 'w', encoding='utf-8') as f:
            json.dump(test_suite, f, ensure_ascii=False, indent=2)
        
        print(f"修复完成，剩余 {len(unique_tests)} 个边界测试")
        
        # 显示当前边界测试
        print("\n当前边界测试:")
        for test in unique_tests:
            print(f"  - {test['name']}: {test['input']}")
    else:
        print("未找到边界测试类别")

if __name__ == "__main__":
    fix_duplicate_tests()