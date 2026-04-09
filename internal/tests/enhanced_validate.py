#!/usr/bin/env python3
"""
毛泽东.skill增强版验证测试脚本
实际测试text_processor.py的各项功能
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.text_processor import MaoTextProcessor, MAO_CONCEPTS
    print("✅ 成功导入MaoTextProcessor")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)

def load_test_text():
    """加载测试文本（使用实践论的前1000字符）"""
    test_file = project_root / "knowledge" / "methodology" / "实践论.md"
    if not test_file.exists():
        # 如果没有文件，使用示例文本
        sample_text = """实践论是毛泽东的重要哲学著作。它阐述了认识与实践的关系，提出了实践是认识的来源、动力、标准和目的的观点。认识从实践开始，经过实践得到理论的认识，还须再回到实践去。实践、认识、再实践、再认识，这种形式，循环往复以至无穷，而实践和认识之每一循环的内容，都比较地进到了高一级的程度。这就是辩证唯物论的全部认识论，这就是辩证唯物论的知行统一观。"""
        return sample_text
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 读取前2000字符作为测试文本
        return content
    except Exception as e:
        print(f"❌ 读取测试文件失败: {e}")
        return "实践论是毛泽东的重要哲学著作。"

def test_concept_extraction():
    """测试概念提取功能"""
    print("测试概念提取功能...")
    
    try:
        processor = MaoTextProcessor()
        test_text = load_test_text()
        
        # 提取概念
        concepts = processor.extract_concepts(test_text)
        
        # 验证概念提取结果
        if not concepts:
            return {
                "status": "failed",
                "message": "概念提取返回空结果"
            }
        
        # 检查是否包含毛泽东核心概念
        expected_concepts = ["实践论", "认识", "实践", "辩证唯物论"]
        found_concepts = []
        
        for concept in expected_concepts:
            if concept in concepts:
                found_concepts.append(concept)
        
        if len(found_concepts) >= 2:
            return {
                "status": "passed",
                "message": f"成功提取{len(concepts)}个概念，包含核心概念: {', '.join(found_concepts)}"
            }
        else:
            return {
                "status": "failed",
                "message": f"提取的概念中缺少核心毛泽东概念。提取了{len(concepts)}个概念"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"概念提取测试出错: {str(e)}"
        }

def test_argument_structure():
    """测试论证结构分析"""
    print("测试论证结构分析...")
    
    try:
        processor = MaoTextProcessor()
        test_text = load_test_text()
        
        # 分析论证结构
        argument_structure = processor.analyze_argument_structure(test_text)
        
        # 验证返回结构
        required_keys = ["structure_counts", "argument_steps", "total_steps"]
        missing_keys = [key for key in required_keys if key not in argument_structure]
        
        if missing_keys:
            return {
                "status": "failed",
                "message": f"论证结构分析缺少必要字段: {', '.join(missing_keys)}"
            }
        
        # 检查是否有分析结果
        structure_counts = argument_structure.get("structure_counts", {})
        total_steps = argument_structure.get("total_steps", 0)
        
        if total_steps > 0 or structure_counts:
            return {
                "status": "passed",
                "message": f"成功分析论证结构，识别到{total_steps}个论证步骤"
            }
        else:
            return {
                "status": "failed", 
                "message": "论证结构分析未识别到有效结构"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"论证结构测试出错: {str(e)}"
        }

def test_mao_analogies():
    """测试毛泽东比喻识别"""
    print("测试毛泽东比喻识别...")
    
    try:
        processor = MaoTextProcessor()
        
        # 使用包含毛泽东比喻的测试文本
        test_text = """星星之火可以燎原。帝国主义和一切反动派都是纸老虎。我们要解剖麻雀，深入分析问题。抓典型，以点带面推动工作。"""
        
        # 提取毛泽东比喻
        analogies = processor.extract_mao_analogies(test_text)
        
        # 验证返回结果
        if not isinstance(analogies, list):
            return {
                "status": "failed",
                "message": f"比喻识别返回类型错误: {type(analogies)}"
            }
        
        # 检查是否识别到毛泽东经典比喻
        mao_analogy_names = []
        for analogy in analogies:
            if isinstance(analogy, dict) and "name" in analogy:
                mao_analogy_names.append(analogy["name"])
        
        expected_analogies = ["星星之火可以燎原", "纸老虎", "解剖麻雀", "抓典型", "以点带面"]
        found_count = 0
        
        for expected in expected_analogies:
            for name in mao_analogy_names:
                if expected in name:
                    found_count += 1
                    break
        
        if found_count >= 2:
            return {
                "status": "passed",
                "message": f"成功识别{len(analogies)}个比喻，包含{found_count}个毛泽东经典比喻"
            }
        else:
            return {
                "status": "failed",
                "message": f"识别到{len(analogies)}个比喻，但毛泽东经典比喻识别不足"
            }
            
    except Exception as e:
        return {
            "status": "error", 
            "message": f"毛泽东比喻测试出错: {str(e)}"
        }

def test_rhetorical_patterns():
    """测试修辞模式识别"""
    print("测试修辞模式识别...")
    
    try:
        processor = MaoTextProcessor()
        
        # 使用包含修辞手法的测试文本
        test_text = """我们既要看到成绩，又要看到缺点，还要看到困难。为什么要革命？因为要解放人民。不是东风压倒西风，就是西风压倒东风。古人云：知己知彼，百战不殆。"""
        
        # 识别修辞模式
        rhetorical_patterns = processor.identify_rhetorical_patterns(test_text)
        
        # 验证返回结构
        required_keys = ["parallelism_counts", "rhetorical_questions_count", "contrasts_count"]
        missing_keys = [key for key in required_keys if key not in rhetorical_patterns]
        
        if missing_keys:
            return {
                "status": "failed",
                "message": f"修辞模式识别缺少必要字段: {', '.join(missing_keys)}"
            }
        
        # 检查是否识别到修辞手法
        parallelism_counts = rhetorical_patterns.get("parallelism_counts", {})
        rhetorical_questions = rhetorical_patterns.get("rhetorical_questions_count", 0)
        contrasts = rhetorical_patterns.get("contrasts_count", 0)
        
        total_patterns = sum(parallelism_counts.values()) + rhetorical_questions + contrasts
        
        if total_patterns > 0:
            return {
                "status": "passed",
                "message": f"成功识别修辞模式: {total_patterns}个修辞手法"
            }
        else:
            return {
                "status": "failed",
                "message": "修辞模式识别未发现有效修辞手法"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"修辞模式测试出错: {str(e)}"
        }

def test_style_analysis():
    """测试文本风格分析"""
    print("测试文本风格分析...")
    
    try:
        processor = MaoTextProcessor()
        test_text = load_test_text()
        
        # 分析文本风格
        style_stats = processor.analyze_style(test_text)
        
        # 验证返回结构
        required_keys = ["avg_sentence_length", "sentence_count", "word_count", "rhetoric_counts", "top_words"]
        missing_keys = [key for key in required_keys if key not in style_stats]
        
        if missing_keys:
            return {
                "status": "failed",
                "message": f"风格分析缺少必要字段: {', '.join(missing_keys)}"
            }
        
        # 检查分析结果是否合理
        sentence_count = style_stats.get("sentence_count", 0)
        word_count = style_stats.get("word_count", 0)
        
        if sentence_count > 0 and word_count > 0:
            return {
                "status": "passed",
                "message": f"成功分析文本风格: {sentence_count}个句子，{word_count}个词"
            }
        else:
            return {
                "status": "failed",
                "message": "风格分析结果不合理"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"风格分析测试出错: {str(e)}"
        }

def test_concept_library():
    """测试概念词典"""
    print("测试概念词典...")
    
    try:
        # 检查MAO_CONCEPTS是否正确定义
        if not MAO_CONCEPTS:
            return {
                "status": "failed",
                "message": "MAO_CONCEPTS为空"
            }
        
        # 检查概念数量
        concept_count = len(MAO_CONCEPTS)
        
        # 检查是否包含核心概念
        core_concepts = ["实践论", "矛盾论", "实事求是", "群众路线", "调查研究"]
        missing_core = []
        
        for concept in core_concepts:
            if concept not in MAO_CONCEPTS:
                missing_core.append(concept)
        
        if concept_count >= 100 and len(missing_core) <= 1:
            return {
                "status": "passed",
                "message": f"概念词典包含{concept_count}个概念，核心概念完整"
            }
        else:
            return {
                "status": "failed",
                "message": f"概念词典只有{concept_count}个概念，缺少核心概念: {', '.join(missing_core)}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"概念词典测试出错: {str(e)}"
        }

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("毛泽东.skill 增强版验证测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行各项测试
    test_functions = [
        ("概念词典", test_concept_library),
        ("概念提取", test_concept_extraction),
        ("风格分析", test_style_analysis),
        ("论证结构", test_argument_structure),
        ("毛泽东比喻", test_mao_analogies),
        ("修辞模式", test_rhetorical_patterns),
    ]
    
    for test_name, test_func in test_functions:
        print(f"\n[{test_name}]")
        try:
            result = test_func()
            test_results.append({
                "test": test_name,
                "status": result.get("status", "unknown"),
                "message": result.get("message", ""),
            })
            print(f"  状态: {result.get('status', 'unknown')}")
            if result.get("message"):
                print(f"  信息: {result.get('message')}")
        except Exception as e:
            test_results.append({
                "test": test_name,
                "status": "error",
                "message": str(e),
            })
            print(f"  错误: {e}")
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for r in test_results if r["status"] == "passed")
    failed = sum(1 for r in test_results if r["status"] == "failed")
    pending = sum(1 for r in test_results if r["status"] == "pending")
    errors = sum(1 for r in test_results if r["status"] == "error")
    
    for result in test_results:
        status_symbol = {
            "passed": "✅",
            "failed": "❌",
            "pending": "⏳",
            "error": "⚠️",
            "unknown": "❓"
        }.get(result["status"], "❓")
        
        print(f"{status_symbol} {result['test']}: {result['status']}")
        if result["message"]:
            print(f"    {result['message']}")
    
    print(f"\n总计: {len(test_results)} 项测试")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"⏳ 待定: {pending}")
    print(f"⚠️ 错误: {errors}")
    
    # 保存测试结果
    save_test_results(test_results)
    
    return all(r["status"] == "passed" for r in test_results)

def save_test_results(test_results):
    """保存测试结果到文件"""
    try:
        results_dir = Path(__file__).parent / "test_results"
        results_dir.mkdir(exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"test_results_{timestamp}.json"
        
        results_data = {
            "timestamp": timestamp,
            "total_tests": len(test_results),
            "passed": sum(1 for r in test_results if r["status"] == "passed"),
            "failed": sum(1 for r in test_results if r["status"] == "failed"),
            "errors": sum(1 for r in test_results if r["status"] == "error"),
            "tests": test_results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n测试结果已保存到: {results_file}")
        
    except Exception as e:
        print(f"\n保存测试结果失败: {e}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东.skill增强版验证测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--concept", action="store_true", help="只运行概念相关测试")
    parser.add_argument("--analysis", action="store_true", help="只运行分析功能测试")
    
    args = parser.parse_args()
    
    if args.concept:
        print("运行概念相关测试...")
        result1 = test_concept_library()
        result2 = test_concept_extraction()
        print(f"概念词典: {result1['status']} - {result1['message']}")
        print(f"概念提取: {result2['status']} - {result2['message']}")
    elif args.analysis:
        print("运行分析功能测试...")
        result1 = test_argument_structure()
        result2 = test_mao_analogies()
        result3 = test_rhetorical_patterns()
        print(f"论证结构: {result1['status']} - {result1['message']}")
        print(f"毛泽东比喻: {result2['status']} - {result2['message']}")
        print(f"修辞模式: {result3['status']} - {result3['message']}")
    else:
        # 默认运行所有测试
        success = run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()