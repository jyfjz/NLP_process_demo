#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能基准测试 - 测试系统在不同负载下的性能表现
"""

import sys
import os
import time
import psutil
import threading
from datetime import datetime
from typing import Dict, List, Tuple

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code_model.text_tools import TextProcessor

class PerformanceBenchmark:
    """性能基准测试类"""
    
    def __init__(self):
        self.processor = TextProcessor()
        self.results = []
        
    def monitor_resources(self, duration: float) -> Dict:
        """监控系统资源使用情况"""
        start_time = time.time()
        cpu_samples = []
        memory_samples = []
        
        while time.time() - start_time < duration:
            cpu_samples.append(psutil.cpu_percent(interval=0.1))
            memory_samples.append(psutil.virtual_memory().percent)
            time.sleep(0.1)
        
        return {
            'avg_cpu': sum(cpu_samples) / len(cpu_samples),
            'max_cpu': max(cpu_samples),
            'avg_memory': sum(memory_samples) / len(memory_samples),
            'max_memory': max(memory_samples)
        }
    
    def benchmark_function(self, func_name: str, func, *args, **kwargs) -> Dict:
        """基准测试单个功能"""
        print(f"测试 {func_name}...")
        
        # 预热
        try:
            func(*args, **kwargs)
        except:
            pass
        
        # 开始监控资源
        resource_monitor = None
        
        # 执行测试
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            # 启动资源监控
            def monitor():
                return self.monitor_resources(10)  # 监控10秒
            
            monitor_thread = threading.Thread(target=monitor)
            monitor_thread.daemon = True
            monitor_thread.start()
            
            # 执行功能
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            # 等待监控完成
            monitor_thread.join(timeout=1)
            
            execution_time = end_time - start_time
            memory_usage = end_memory - start_memory
            
            benchmark_result = {
                'function': func_name,
                'execution_time': execution_time,
                'memory_usage': memory_usage,
                'success': True,
                'result_size': len(str(result)) if result else 0,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"  ✓ 执行时间: {execution_time:.3f}s, 内存使用: {memory_usage:.1f}MB")
            
        except Exception as e:
            benchmark_result = {
                'function': func_name,
                'execution_time': 0,
                'memory_usage': 0,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"  ✗ 执行失败: {e}")
        
        self.results.append(benchmark_result)
        return benchmark_result
    
    def test_text_loading_performance(self):
        """测试文本加载性能"""
        print("\n=== 文本加载性能测试 ===")
        
        # 不同大小的文本
        test_sizes = [
            (100, "小文本"),
            (1000, "中等文本"),
            (10000, "大文本"),
            (50000, "超大文本")
        ]
        
        for size, description in test_sizes:
            test_text = "这是一个性能测试文本。" * (size // 10)
            
            self.benchmark_function(
                f"文本加载-{description}({len(test_text)}字符)",
                self.processor.load_text,
                test_text
            )
    
    def test_segmentation_performance(self):
        """测试分词性能"""
        print("\n=== 分词性能测试 ===")
        
        # 准备测试文本
        test_text = """
        人工智能技术正在快速发展，深度学习、机器学习、自然语言处理等技术在各个领域都有广泛应用。
        北京大学、清华大学、中科院等研究机构在人工智能领域取得了重要突破。
        苹果公司、谷歌公司、微软公司等科技巨头也在大力投资人工智能技术。
        """ * 50  # 重复50次，增加文本长度
        
        self.processor.load_text(test_text)
        
        # 测试不同分词方法
        methods = ['jieba', 'pkuseg_default', 'basic']
        
        for method in methods:
            try:
                self.benchmark_function(
                    f"分词-{method}",
                    self.processor.segment_text,
                    method=method
                )
            except Exception as e:
                print(f"  跳过 {method}: {e}")
    
    def test_word_frequency_performance(self):
        """测试词频统计性能"""
        print("\n=== 词频统计性能测试 ===")
        
        # 不同长度的文本
        text_lengths = [1000, 5000, 20000, 50000]
        
        for length in text_lengths:
            test_text = "人工智能机器学习深度学习自然语言处理计算机视觉语音识别。" * (length // 30)
            self.processor.load_text(test_text)
            
            self.benchmark_function(
                f"词频统计-{length}字符",
                self.processor.get_top_words,
                n=20
            )
    
    def test_sentiment_analysis_performance(self):
        """测试情感分析性能"""
        print("\n=== 情感分析性能测试 ===")
        
        # 不同情感的测试文本
        test_texts = [
            ("积极", "这个产品真的很棒！质量很好，服务也很周到，我非常满意！" * 20),
            ("消极", "这个服务太差了，等了很久都没有回应，完全不推荐！" * 20),
            ("中性", "今天天气不错，温度适中，适合外出活动。" * 20),
            ("长文本", "人工智能技术发展很快，在各个领域都有应用。" * 100)
        ]
        
        for text_type, text in test_texts:
            self.benchmark_function(
                f"情感分析-{text_type}({len(text)}字符)",
                self.processor.analyze_sentiment,
                text
            )
    
    def test_entity_recognition_performance(self):
        """测试实体识别性能"""
        print("\n=== 实体识别性能测试 ===")
        
        # 包含大量实体的文本
        entity_text = """
        张三在北京大学学习计算机科学，他来自上海市浦东新区。
        苹果公司的CEO蒂姆·库克访问了清华大学，讨论人工智能合作项目。
        中国科学院和微软公司将在深圳建立联合实验室。
        腾讯公司创始人马化腾在广州举办的AI大会上发表演讲。
        阿里巴巴集团在杭州总部宣布新的云计算战略。
        """ * 20  # 重复20次
        
        # 测试不同方法
        methods = ['hybrid', 'stanza', 'spacy', 'regex']
        
        for method in methods:
            try:
                self.benchmark_function(
                    f"实体识别-{method}",
                    self.processor.extract_entities,
                    entity_text,
                    method=method
                )
            except Exception as e:
                print(f"  跳过 {method}: {e}")
    
    def test_text_summarization_performance(self):
        """测试文本摘要性能"""
        print("\n=== 文本摘要性能测试 ===")
        
        # 长文本用于摘要
        long_text = """
        人工智能（Artificial Intelligence，简称AI）是计算机科学的一个重要分支。
        它致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。
        人工智能的发展可以追溯到20世纪50年代，经历了多次起伏。
        1950年，英国数学家阿兰·图灵发表了著名的论文《计算机器与智能》。
        进入21世纪，随着计算能力的大幅提升、大数据的出现以及深度学习算法的突破。
        今天，人工智能已经广泛应用于各个领域，包括医疗诊断、自动驾驶、金融分析等。
        """ * 50  # 重复50次，创建长文本
        
        self.processor.load_text(long_text)
        
        # 测试不同摘要方法
        methods = [
            ('frequency', '基于词频'),
            ('position', '基于位置'),
            ('hybrid', '混合方法'),
            ('textteaser', 'TextTeaser'),
            ('qwen3', 'Qwen3大模型')
        ]
        
        for method, description in methods:
            try:
                if method in ['textteaser', 'qwen3']:
                    self.benchmark_function(
                        f"文本摘要-{description}",
                        self.processor.generate_summary,
                        num_sentences=3,
                        method=method,
                        title="人工智能技术发展"
                    )
                else:
                    self.benchmark_function(
                        f"文本摘要-{description}",
                        self.processor.generate_summary,
                        num_sentences=3,
                        method=method
                    )
            except Exception as e:
                print(f"  跳过 {description}: {e}")
    
    def test_concurrent_performance(self):
        """测试并发性能"""
        print("\n=== 并发性能测试 ===")
        
        def worker_task():
            """工作线程任务"""
            processor = TextProcessor()
            test_text = "这是一个并发测试文本。" * 100
            processor.load_text(test_text)
            
            # 执行多个操作
            processor.get_text_stats()
            processor.get_top_words(n=10)
            processor.analyze_sentiment(test_text[:500])
            
            return "完成"
        
        # 测试不同并发数
        concurrent_levels = [1, 2, 5, 10]
        
        for level in concurrent_levels:
            start_time = time.time()
            
            threads = []
            for i in range(level):
                thread = threading.Thread(target=worker_task)
                threads.append(thread)
                thread.start()
            
            # 等待所有线程完成
            for thread in threads:
                thread.join()
            
            execution_time = time.time() - start_time
            
            result = {
                'function': f'并发测试-{level}线程',
                'execution_time': execution_time,
                'memory_usage': 0,
                'success': True,
                'concurrent_level': level,
                'timestamp': datetime.now().isoformat()
            }
            
            self.results.append(result)
            print(f"  ✓ {level}线程并发: {execution_time:.3f}s")
    
    def run_all_benchmarks(self):
        """运行所有性能测试"""
        print("=" * 80)
        print("中文文本处理和NLP分析工具 - 性能基准测试")
        print("=" * 80)
        
        start_time = time.time()
        
        # 运行各项性能测试
        self.test_text_loading_performance()
        self.test_segmentation_performance()
        self.test_word_frequency_performance()
        self.test_sentiment_analysis_performance()
        self.test_entity_recognition_performance()
        self.test_text_summarization_performance()
        self.test_concurrent_performance()
        
        total_time = time.time() - start_time
        
        # 生成性能报告
        self.generate_performance_report(total_time)
    
    def generate_performance_report(self, total_time: float):
        """生成性能测试报告"""
        print("\n" + "=" * 80)
        print("性能测试报告")
        print("=" * 80)
        
        # 统计成功和失败的测试
        successful_tests = [r for r in self.results if r.get('success', False)]
        failed_tests = [r for r in self.results if not r.get('success', False)]
        
        print(f"总测试数: {len(self.results)}")
        print(f"成功: {len(successful_tests)}")
        print(f"失败: {len(failed_tests)}")
        print(f"总执行时间: {total_time:.2f}秒")
        
        if successful_tests:
            # 性能统计
            execution_times = [r['execution_time'] for r in successful_tests]
            memory_usages = [r['memory_usage'] for r in successful_tests if r['memory_usage'] > 0]
            
            print(f"\n执行时间统计:")
            print(f"  平均: {sum(execution_times)/len(execution_times):.3f}s")
            print(f"  最快: {min(execution_times):.3f}s")
            print(f"  最慢: {max(execution_times):.3f}s")
            
            if memory_usages:
                print(f"\n内存使用统计:")
                print(f"  平均: {sum(memory_usages)/len(memory_usages):.1f}MB")
                print(f"  最少: {min(memory_usages):.1f}MB")
                print(f"  最多: {max(memory_usages):.1f}MB")
            
            # 性能排行榜（最快的功能）
            print(f"\n性能排行榜（前5名最快功能）:")
            sorted_results = sorted(successful_tests, key=lambda x: x['execution_time'])
            for i, result in enumerate(sorted_results[:5], 1):
                print(f"  {i}. {result['function']}: {result['execution_time']:.3f}s")
            
            # 性能瓶颈（最慢的功能）
            print(f"\n性能瓶颈（前5名最慢功能）:")
            sorted_results = sorted(successful_tests, key=lambda x: x['execution_time'], reverse=True)
            for i, result in enumerate(sorted_results[:5], 1):
                print(f"  {i}. {result['function']}: {result['execution_time']:.3f}s")
        
        # 保存详细报告
        import json
        report_file = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': len(self.results),
                    'successful': len(successful_tests),
                    'failed': len(failed_tests),
                    'total_time': total_time,
                    'timestamp': datetime.now().isoformat()
                },
                'results': self.results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细性能报告已保存到: {report_file}")
        
        # 性能建议
        print(f"\n性能优化建议:")
        if any(r['execution_time'] > 10 for r in successful_tests):
            print("  • 发现执行时间超过10秒的功能，建议优化算法或增加缓存")
        if any(r['memory_usage'] > 500 for r in successful_tests):
            print("  • 发现内存使用超过500MB的功能，建议优化内存管理")
        if len(failed_tests) > 0:
            print(f"  • 有{len(failed_tests)}个功能测试失败，建议检查相关模块")
        
        print("  • 建议在生产环境中定期运行性能测试")
        print("  • 可以考虑实现异步处理来提高用户体验")

if __name__ == "__main__":
    # 运行性能基准测试
    benchmark = PerformanceBenchmark()
    benchmark.run_all_benchmarks()
