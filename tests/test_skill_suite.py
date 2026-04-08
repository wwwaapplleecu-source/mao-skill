#!/usr/bin/env python3
"""
毛泽东.skill测试套件执行脚本
基于test_suite.json中的测试用例，使用skill_simulator验证Skill功能
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.skill_simulator import MaoSkillSimulator
    print("✅ 成功导入MaoSkillSimulator")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保skill_simulator.py在tools目录中")
    sys.exit(1)

class SkillTestSuite:
    """Skill测试套件执行器"""
    
    def __init__(self):
        self.simulator = MaoSkillSimulator()
        self.test_suite_path = Path(__file__).parent / "test_suite.json"
        self.results = []
        
    def load_test_suite(self) -> List[Dict[str, Any]]:
        """加载测试套件"""
        if not self.test_suite_path.exists():
            print(f"❌ 测试套件文件不存在: {self.test_suite_path}")
            return []
        
        try:
            with open(self.test_suite_path, 'r', encoding='utf-8') as f:
                test_suite = json.load(f)
            return test_suite
        except Exception as e:
            print(f"❌ 加载测试套件失败: {e}")
            return []
    
    def run_test(self, test_case: Dict[str, Any], category: str) -> Dict[str, Any]:
        """运行单个测试用例"""
        test_name = test_case.get("name", "未命名测试")
        description = test_case.get("description", "")
        input_text = test_case.get("input", "")
        
        print(f"\n测试: {test_name}")
        print(f"描述: {description}")
        print(f"输入: {input_text}")
        
        try:
            # 生成响应
            response = self.simulator.generate_response(input_text)
            print(f"响应: {response[:100]}...")
            
            # 验证响应
            validation_result = self.validate_response(response, test_case)
            
            test_result = {
                "category": category,
                "name": test_name,
                "input": input_text,
                "response": response,
                "status": validation_result["status"],
                "message": validation_result["message"],
                "details": validation_result.get("details", {})
            }
            
            return test_result
            
        except Exception as e:
            print(f"❌ 测试执行出错: {e}")
            return {
                "category": category,
                "name": test_name,
                "input": input_text,
                "response": "",
                "status": "error",
                "message": f"测试执行出错: {str(e)}",
                "details": {}
            }
    
    def validate_response(self, response: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """验证响应是否符合预期"""
        response_lower = response.lower()
        validation_details = {}
        
        # 检查预期关键词
        expected_keywords = test_case.get("expected_keywords", [])
        if expected_keywords:
            found_keywords = []
            missing_keywords = []
            
            for keyword in expected_keywords:
                if keyword in response or keyword in response_lower:
                    found_keywords.append(keyword)
                else:
                    missing_keywords.append(keyword)
            
            validation_details["found_keywords"] = found_keywords
            validation_details["missing_keywords"] = missing_keywords
            
            if missing_keywords:
                return {
                    "status": "failed",
                    "message": f"响应缺少预期关键词: {', '.join(missing_keywords)}",
                    "details": validation_details
                }
        
        # 检查预期模式
        expected_patterns = test_case.get("expected_patterns", [])
        if expected_patterns:
            found_patterns = []
            missing_patterns = []
            
            for pattern in expected_patterns:
                if pattern in response:
                    found_patterns.append(pattern)
                else:
                    missing_patterns.append(pattern)
            
            validation_details["found_patterns"] = found_patterns
            validation_details["missing_patterns"] = missing_patterns
            
            if missing_patterns:
                return {
                    "status": "failed",
                    "message": f"响应缺少预期模式: {', '.join(missing_patterns)}",
                    "details": validation_details
                }
        
        # 检查预期指示器
        expected_indicators = test_case.get("expected_indicators", [])
        if expected_indicators:
            found_indicators = []
            missing_indicators = []
            
            for indicator in expected_indicators:
                if indicator in response:
                    found_indicators.append(indicator)
                else:
                    missing_indicators.append(indicator)
            
            validation_details["found_indicators"] = found_indicators
            validation_details["missing_indicators"] = missing_indicators
            
            if missing_indicators:
                return {
                    "status": "failed",
                    "message": f"响应缺少预期指示器: {', '.join(missing_indicators)}",
                    "details": validation_details
                }
        
        # 检查响应长度和质量
        if len(response.strip()) < 20:
            return {
                "status": "failed",
                "message": f"响应过短: {len(response)}字符",
                "details": validation_details
            }
        
        # 检查是否包含毛泽东方法论相关词汇
        mao_methodology_keywords = ["矛盾", "实践", "调查", "群众", "战略", "分析", "研究"]
        methodology_found = sum(1 for keyword in mao_methodology_keywords if keyword in response)
        
        if methodology_found < 2:
            return {
                "status": "failed",
                "message": f"响应中毛泽东方法论关键词不足，只找到{methodology_found}个",
                "details": validation_details
            }
        
        # 所有检查通过
        validation_details["response_length"] = len(response)
        validation_details["methodology_keywords_found"] = methodology_found
        
        return {
            "status": "passed",
            "message": "响应符合预期",
            "details": validation_details
        }
    
    def run_all_tests(self) -> bool:
        """运行所有测试"""
        test_suite = self.load_test_suite()
        
        if not test_suite:
            print("❌ 测试套件为空或加载失败")
            return False
        
        print("=" * 70)
        print("毛泽东.skill 测试套件执行")
        print("=" * 70)
        
        total_tests = 0
        passed_tests = 0
        
        for category_data in test_suite:
            category = category_data.get("category", "未分类")
            tests = category_data.get("tests", [])
            
            print(f"\n📁 测试类别: {category}")
            print("-" * 40)
            
            for test_case in tests:
                total_tests += 1
                test_result = self.run_test(test_case, category)
                self.results.append(test_result)
                
                status_symbol = {
                    "passed": "✅",
                    "failed": "❌",
                    "error": "⚠️"
                }.get(test_result["status"], "❓")
                
                print(f"{status_symbol} {test_result['name']}: {test_result['status']}")
                
                if test_result["status"] == "passed":
                    passed_tests += 1
        
        # 汇总结果
        print("\n" + "=" * 70)
        print("测试结果汇总")
        print("=" * 70)
        
        failed_tests = [r for r in self.results if r["status"] == "failed"]
        error_tests = [r for r in self.results if r["status"] == "error"]
        
        print(f"总计测试: {total_tests}")
        print(f"✅ 通过: {passed_tests}")
        print(f"❌ 失败: {len(failed_tests)}")
        print(f"⚠️ 错误: {len(error_tests)}")
        
        # 显示失败测试详情
        if failed_tests:
            print("\n❌ 失败测试详情:")
            for result in failed_tests:
                print(f"  - {result['category']}/{result['name']}: {result['message']}")
        
        if error_tests:
            print("\n⚠️ 错误测试详情:")
            for result in error_tests:
                print(f"  - {result['category']}/{result['name']}: {result['message']}")
        
        # 保存详细结果
        self.save_detailed_results()
        
        # 计算通过率
        if total_tests > 0:
            pass_rate = (passed_tests / total_tests) * 100
            print(f"\n📊 通过率: {pass_rate:.1f}%")
            
            if pass_rate >= 80:
                print("🎉 测试套件执行成功！")
            else:
                print("⚠️ 测试套件通过率未达标，需要改进。")
            
            return pass_rate >= 80
        else:
            print("⚠️ 没有执行任何测试")
            return False
    
    def save_detailed_results(self):
        """保存详细测试结果"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            results_dir = Path(__file__).parent / "test_results"
            results_dir.mkdir(exist_ok=True)
            
            results_file = results_dir / f"skill_test_results_{timestamp}.json"
            
            results_summary = {
                "timestamp": timestamp,
                "total_tests": len(self.results),
                "passed": sum(1 for r in self.results if r["status"] == "passed"),
                "failed": sum(1 for r in self.results if r["status"] == "failed"),
                "errors": sum(1 for r in self.results if r["status"] == "error"),
                "results": self.results
            }
            
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results_summary, f, ensure_ascii=False, indent=2)
            
            print(f"\n📁 详细测试结果已保存到: {results_file}")
            
        except Exception as e:
            print(f"\n⚠️ 保存测试结果失败: {e}")
    
    def generate_test_report(self):
        """生成测试报告"""
        if not self.results:
            print("没有测试结果可生成报告")
            return
        
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            report_dir = Path(__file__).parent / "test_reports"
            report_dir.mkdir(exist_ok=True)
            
            report_file = report_dir / f"test_report_{datetime.now().strftime('%Y%m%d')}.md"
            
            # 计算统计数据
            total = len(self.results)
            passed = sum(1 for r in self.results if r["status"] == "passed")
            failed = sum(1 for r in self.results if r["status"] == "failed")
            errors = sum(1 for r in self.results if r["status"] == "error")
            pass_rate = (passed / total * 100) if total > 0 else 0
            
            # 按类别统计
            category_stats = {}
            for result in self.results:
                category = result["category"]
                if category not in category_stats:
                    category_stats[category] = {"total": 0, "passed": 0, "failed": 0, "errors": 0}
                
                category_stats[category]["total"] += 1
                category_stats[category][result["status"]] += 1
            
            # 生成报告
            report_lines = [
                "# 毛泽东.skill 测试报告",
                "",
                f"**生成时间**: {timestamp}",
                f"**测试套件**: test_suite.json",
                f"**测试工具**: skill_simulator.py",
                "",
                "## 执行摘要",
                "",
                f"- **总计测试**: {total}",
                f"- **通过测试**: {passed}",
                f"- **失败测试**: {failed}",
                f"- **错误测试**: {errors}",
                f"- **通过率**: {pass_rate:.1f}%",
                "",
                "## 按类别统计",
                "",
                "| 类别 | 总计 | 通过 | 失败 | 错误 | 通过率 |",
                "|------|------|------|------|------|--------|"
            ]
            
            for category, stats in category_stats.items():
                cat_pass_rate = (stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0
                report_lines.append(f"| {category} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['errors']} | {cat_pass_rate:.1f}% |")
            
            report_lines.extend([
                "",
                "## 详细结果",
                ""
            ])
            
            # 添加每个测试的详细结果
            for result in self.results:
                status_emoji = {
                    "passed": "✅",
                    "failed": "❌", 
                    "error": "⚠️"
                }.get(result["status"], "❓")
                
                report_lines.append(f"### {status_emoji} {result['category']} - {result['name']}")
                report_lines.append("")
                report_lines.append(f"- **状态**: {result['status']}")
                report_lines.append(f"- **输入**: {result['input']}")
                report_lines.append(f"- **响应**: {result['response'][:200]}...")
                report_lines.append(f"- **消息**: {result['message']}")
                report_lines.append("")
            
            report_lines.extend([
                "## 结论与建议",
                "",
                "### 主要发现"
            ])
            
            if pass_rate >= 80:
                report_lines.append("✅ 测试套件通过率达标，Skill基本功能正常。")
            else:
                report_lines.append("⚠️ 测试套件通过率未达标，需要重点关注失败测试。")
            
            if failed_tests := [r for r in self.results if r["status"] == "failed"]:
                report_lines.append("")
                report_lines.append("### 需要改进的测试")
                for test in failed_tests:
                    report_lines.append(f"- **{test['category']}/{test['name']}**: {test['message']}")
            
            report_lines.extend([
                "",
                "### 建议",
                "",
                "1. **完善响应模板**: 针对失败测试，优化skill_simulator的响应模板",
                "2. **增强验证逻辑**: 添加更多维度的响应验证",
                "3. **扩展测试用例**: 添加更多边界情况和复杂场景测试",
                "4. **集成真实Skill**: 将测试套件与真实的毛泽东.skill集成",
                ""
            ])
            
            # 写入报告文件
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(report_lines))
            
            print(f"\n📄 测试报告已生成: {report_file}")
            
        except Exception as e:
            print(f"\n⚠️ 生成测试报告失败: {e}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东.skill测试套件执行器")
    parser.add_argument("--run", action="store_true", help="运行所有测试")
    parser.add_argument("--report", action="store_true", help="生成测试报告")
    parser.add_argument("--test", help="运行特定测试用例名称")
    
    args = parser.parse_args()
    
    test_suite = SkillTestSuite()
    
    if args.test:
        # 运行特定测试
        test_suite_data = test_suite.load_test_suite()
        found_test = None
        
        for category_data in test_suite_data:
            for test_case in category_data.get("tests", []):
                if test_case.get("name") == args.test:
                    found_test = (test_case, category_data.get("category", "未分类"))
                    break
            if found_test:
                break
        
        if found_test:
            test_case, category = found_test
            result = test_suite.run_test(test_case, category)
            
            status_emoji = {
                "passed": "✅",
                "failed": "❌",
                "error": "⚠️"
            }.get(result["status"], "❓")
            
            print(f"\n{status_emoji} 测试结果: {result['status']}")
            print(f"消息: {result['message']}")
            
            if "details" in result and result["details"]:
                print("详情:")
                for key, value in result["details"].items():
                    print(f"  {key}: {value}")
        else:
            print(f"❌ 未找到测试用例: {args.test}")
    
    elif args.run or (not args.test and not args.report):
        # 运行所有测试
        success = test_suite.run_all_tests()
        
        if args.report or success:
            test_suite.generate_test_report()
        
        sys.exit(0 if success else 1)
    
    elif args.report:
        # 需要先运行测试才能生成报告
        print("⚠️ 请先运行测试以生成报告（使用 --run 参数）")

if __name__ == "__main__":
    main()