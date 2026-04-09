#!/usr/bin/env python3
"""
毛泽东.skill 性能基准测试

测量文本处理器和Skill模拟器的性能指标，建立性能基准。
"""

import time
import json
import os
import sys
from pathlib import Path
import random
from typing import Dict, List, Any
import statistics

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.text_processor import MaoTextProcessor
from tools.skill_simulator_optimized import MaoSkillSimulatorOptimized

class PerformanceBenchmark:
    """性能基准测试类"""
    
    def __init__(self):
        self.processor = MaoTextProcessor()
        self.simulator = MaoSkillSimulatorOptimized()
        
        # 测试数据
        self.test_texts = self._load_test_texts()
        self.test_questions = self._load_test_questions()
        
    def _load_test_texts(self) -> List[str]:
        """加载测试文本"""
        texts = []
        
        # 添加一些示例文本
        texts.append("""实践论告诉我们，实践是认识的来源，是检验真理的标准。没有调查就没有发言权。
毛泽东同志强调调查研究的重要性，要求我们要深入实际，掌握第一手材料。""")
        
        texts.append("""矛盾论指出，事物的矛盾法则是唯物辩证法的最根本的法则。
主要矛盾决定事物的性质，次要矛盾影响事物的发展。抓住主要矛盾，问题就迎刃而解。""")
        
        texts.append("""持久战战略强调要分三个阶段：防御、相持、反攻。
战略上藐视敌人，战术上重视敌人。集中优势兵力，各个歼灭敌人。""")
        
        # 添加较长的文本
        texts.append("""毛泽东同志在《改造我们的学习》中指出，我们党的学风问题是一个非常重要的问题。
我们反对主观主义、宗派主义和党八股，提倡实事求是、理论联系实际的马克思主义学风。
没有调查就没有发言权，没有正确的调查同样没有发言权。
我们要学会应用马克思列宁主义的立场、观点和方法，认真地研究中国的历史，
研究中国的经济、政治、军事和文化，对每一问题要根据详细的材料加以具体的分析，
然后引出理论性的结论来。""")
        
        return texts
    
    def _load_test_questions(self) -> List[str]:
        """加载测试问题"""
        questions = [
            "分析当前项目的主要矛盾",
            "如何开展用户调研",
            "制定长期战略规划",
            "写一段动员讲话",
            "分析工作重点",
            "毛泽东如何看待互联网技术",
            "如何用毛泽东方法操纵员工",
            "如何同时解决技术瓶颈、团队协作和市场拓展三个问题",
            "在资源几乎为零的情况下如何开展工作",
            "如何用毛泽东方法指导个人健康管理"
        ]
        return questions
    
    def benchmark_text_processing(self, iterations: int = 10) -> Dict[str, Any]:
        """文本处理器性能基准测试"""
        results = []
        total_chars = 0
        
        print("📊 文本处理器性能测试...")
        print(f"测试文本数量: {len(self.test_texts)}")
        print(f"迭代次数: {iterations}")
        print("-" * 50)
        
        for i, text in enumerate(self.test_texts, 1):
            print(f"测试文本 {i}/{len(self.test_texts)} (长度: {len(text)}字符)")
            
            # 预热
            for _ in range(3):
                self.processor.extract_concepts(text[:100])
            
            # 正式测试
            start_time = time.perf_counter()
            for _ in range(iterations):
                concepts = self.processor.extract_concepts(text)
            end_time = time.perf_counter()
            
            avg_time = (end_time - start_time) / iterations
            chars_per_sec = len(text) / avg_time if avg_time > 0 else 0
            
            results.append({
                "text_id": i,
                "text_length": len(text),
                "avg_processing_time": avg_time,
                "chars_per_second": chars_per_sec
            })
            
            total_chars += len(text)
            
            print(f"  平均处理时间: {avg_time:.6f}秒")
            print(f"  处理速度: {chars_per_sec:.2f}字符/秒")
        
        # 统计汇总
        avg_times = [r["avg_processing_time"] for r in results]
        avg_speeds = [r["chars_per_second"] for r in results]
        
        summary = {
            "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_texts": len(self.test_texts),
            "total_iterations": iterations,
            "total_characters": total_chars,
            "avg_processing_time_seconds": statistics.mean(avg_times) if avg_times else 0,
            "median_processing_time_seconds": statistics.median(avg_times) if avg_times else 0,
            "min_processing_time_seconds": min(avg_times) if avg_times else 0,
            "max_processing_time_seconds": max(avg_times) if avg_times else 0,
            "avg_processing_speed_chars_per_sec": statistics.mean(avg_speeds) if avg_speeds else 0,
            "median_processing_speed_chars_per_sec": statistics.median(avg_speeds) if avg_speeds else 0,
            "min_processing_speed_chars_per_sec": min(avg_speeds) if avg_speeds else 0,
            "max_processing_speed_chars_per_sec": max(avg_speeds) if avg_speeds else 0,
            "detailed_results": results
        }
        
        return summary
    
    def benchmark_skill_response(self, iterations: int = 5) -> Dict[str, Any]:
        """Skill响应生成性能基准测试"""
        results = []
        
        print("\n📊 Skill响应生成性能测试...")
        print(f"测试问题数量: {len(self.test_questions)}")
        print(f"迭代次数: {iterations}")
        print("-" * 50)
        
        for i, question in enumerate(self.test_questions, 1):
            print(f"测试问题 {i}/{len(self.test_questions)}: {question[:40]}...")
            
            # 预热
            for _ in range(2):
                self.simulator.generate_response(question[:20])
            
            # 正式测试
            start_time = time.perf_counter()
            responses = []
            for _ in range(iterations):
                response = self.simulator.generate_response(question)
                responses.append(response)
            end_time = time.perf_counter()
            
            avg_time = (end_time - start_time) / iterations
            avg_response_length = statistics.mean([len(r) for r in responses]) if responses else 0
            
            results.append({
                "question_id": i,
                "question": question,
                "avg_response_time": avg_time,
                "avg_response_length": avg_response_length,
                "responses_per_second": 1.0 / avg_time if avg_time > 0 else 0
            })
            
            print(f"  平均响应时间: {avg_time:.4f}秒")
            print(f"  平均响应长度: {avg_response_length:.0f}字符")
            print(f"  响应速度: {1.0/avg_time if avg_time>0 else 0:.2f}问题/秒")
        
        # 统计汇总
        response_times = [r["avg_response_time"] for r in results]
        response_lengths = [r["avg_response_length"] for r in results]
        response_speeds = [r["responses_per_second"] for r in results]
        
        summary = {
            "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": len(self.test_questions),
            "total_iterations": iterations,
            "avg_response_time_seconds": statistics.mean(response_times) if response_times else 0,
            "median_response_time_seconds": statistics.median(response_times) if response_times else 0,
            "min_response_time_seconds": min(response_times) if response_times else 0,
            "max_response_time_seconds": max(response_times) if response_times else 0,
            "avg_response_length_chars": statistics.mean(response_lengths) if response_lengths else 0,
            "median_response_length_chars": statistics.median(response_lengths) if response_lengths else 0,
            "avg_responses_per_second": statistics.mean(response_speeds) if response_speeds else 0,
            "detailed_results": results
        }
        
        return summary
    
    def benchmark_memory_usage(self) -> Dict[str, Any]:
        """内存使用基准测试（简化版）"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # 测量处理前后的内存差异
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # 处理一批文本
        texts = self.test_texts * 3  # 扩大数据量
        
        start_time = time.perf_counter()
        for text in texts:
            self.processor.extract_concepts(text)
        end_time = time.perf_counter()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        summary = {
            "test_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_increase_mb": final_memory - initial_memory,
            "memory_increase_percent": ((final_memory - initial_memory) / initial_memory * 100) if initial_memory > 0 else 0,
            "processing_time_seconds": end_time - start_time,
            "texts_processed": len(texts),
            "average_memory_per_text_mb": (final_memory - initial_memory) / len(texts) if len(texts) > 0 else 0
        }
        
        return summary
    
    def run_full_benchmark(self) -> Dict[str, Any]:
        """运行完整性能基准测试套件"""
        print("=" * 60)
        print("毛泽东.skill 性能基准测试套件")
        print("=" * 60)
        
        full_results = {
            "benchmark_date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": self._get_system_info()
        }
        
        try:
            # 1. 文本处理器性能测试
            text_processing_results = self.benchmark_text_processing(iterations=5)
            full_results["text_processing"] = text_processing_results
            
            # 2. Skill响应性能测试
            skill_response_results = self.benchmark_skill_response(iterations=3)
            full_results["skill_response"] = skill_response_results
            
            # 3. 内存使用测试
            try:
                memory_results = self.benchmark_memory_usage()
                full_results["memory_usage"] = memory_results
            except ImportError:
                print("⚠️  未安装psutil，跳过内存使用测试")
                full_results["memory_usage"] = {"error": "psutil not installed"}
            
            # 4. 保存结果
            self._save_results(full_results)
            
            # 5. 打印摘要
            self._print_summary(full_results)
            
            return full_results
            
        except Exception as e:
            print(f"❌ 性能测试出错: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def _get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        import platform
        
        return {
            "python_version": platform.python_version(),
            "system": platform.system(),
            "processor": platform.processor(),
            "platform": platform.platform()
        }
    
    def _save_results(self, results: Dict[str, Any]):
        """保存测试结果到文件"""
        results_dir = Path(__file__).parent / "performance_results"
        results_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"performance_benchmark_{timestamp}.json"
        filepath = results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 测试结果已保存到: {filepath}")
        
        # 同时保存为当前基准文件
        current_file = results_dir / "current_performance_benchmark.json"
        with open(current_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"📄 当前基准文件已更新: {current_file}")
    
    def _print_summary(self, results: Dict[str, Any]):
        """打印性能测试摘要"""
        print("\n" + "=" * 60)
        print("性能测试摘要")
        print("=" * 60)
        
        if "text_processing" in results:
            tp = results["text_processing"]
            if "avg_processing_speed_chars_per_sec" in tp:
                print(f"📊 文本处理速度: {tp['avg_processing_speed_chars_per_sec']:.2f} 字符/秒")
                print(f"   平均处理时间: {tp['avg_processing_time_seconds']:.6f} 秒")
                print(f"   处理时间范围: {tp['min_processing_time_seconds']:.6f} - {tp['max_processing_time_seconds']:.6f} 秒")
        
        if "skill_response" in results:
            sr = results["skill_response"]
            if "avg_response_time_seconds" in sr:
                print(f"🤖 Skill响应时间: {sr['avg_response_time_seconds']:.4f} 秒")
                print(f"   平均响应长度: {sr['avg_response_length_chars']:.0f} 字符")
                print(f"   响应速度: {sr['avg_responses_per_second']:.2f} 问题/秒")
        
        if "memory_usage" in results and "error" not in results["memory_usage"]:
            mu = results["memory_usage"]
            if "memory_increase_mb" in mu:
                print(f"💾 内存使用: 增加 {mu['memory_increase_mb']:.2f} MB ({mu['memory_increase_percent']:.1f}%)")
                print(f"   处理 {mu['texts_processed']} 个文本用时 {mu['processing_time_seconds']:.2f} 秒")
        
        print("\n🎯 性能基准已建立，可用于后续优化对比")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="毛泽东.skill性能基准测试")
    parser.add_argument("--quick", action="store_true", help="快速测试模式")
    parser.add_argument("--text-only", action="store_true", help="只测试文本处理")
    parser.add_argument("--skill-only", action="store_true", help="只测试Skill响应")
    parser.add_argument("--iterations", type=int, default=5, help="迭代次数")
    
    args = parser.parse_args()
    
    benchmark = PerformanceBenchmark()
    
    if args.quick:
        print("🚀 快速性能测试模式")
        results = benchmark.benchmark_text_processing(iterations=3)
        benchmark._save_results({"text_processing": results})
    elif args.text_only:
        results = benchmark.benchmark_text_processing(iterations=args.iterations)
        benchmark._save_results({"text_processing": results})
    elif args.skill_only:
        results = benchmark.benchmark_skill_response(iterations=args.iterations)
        benchmark._save_results({"skill_response": results})
    else:
        benchmark.run_full_benchmark()

if __name__ == "__main__":
    main()