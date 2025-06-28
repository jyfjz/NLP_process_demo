#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试案例和场景分析文档 - 核心场景测试脚本
专门针对文档中描述的关键测试场景的简化测试实现
"""

import sys
import os
import time
from datetime import datetime

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code_model.text_tools import TextProcessor

class DocumentScenarioTests:
    """文档场景测试类"""
    
    def __init__(self):
        self.processor = TextProcessor()
        self.results = []
        
    def log_result(self, test_name, status, details="", execution_time=0):
        """记录测试结果"""
        result = {
            'test_name': test_name,
            'status': status,
            'details': details,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        icon = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
        time_str = f" ({execution_time:.3f}s)" if execution_time > 0 else ""
        print(f"{icon} {test_name}{time_str}")
        if details:
            print(f"   {details}")
    
    def test_basic_functionality_tc001(self):
        """TC001: 基础文本处理功能测试"""
        print("\n=== TC001: 基础文本处理功能测试 ===")
        
        # 测试文本输入和统计
        test_text = "人工智能技术正在快速发展，深度学习、机器学习等技术在各个领域都有广泛应用。ChatGPT的出现标志着大语言模型技术的重大突破。未来，AI将在医疗、教育、金融等行业发挥更重要的作用。"
        
        start_time = time.time()
        try:
            self.processor.load_text(test_text)
            stats = self.processor.get_text_stats()
            execution_time = time.time() - start_time
            
            expected_char_count = len(test_text)
            actual_char_count = stats.get('字符数', 0)
            
            if actual_char_count == expected_char_count:
                self.log_result("文本输入和统计功能", "PASS", 
                              f"字符数: {actual_char_count}, 词数: {stats.get('词数', 0)}, 行数: {stats.get('行数', 0)}", 
                              execution_time)
            else:
                self.log_result("文本输入和统计功能", "FAIL", 
                              f"字符数不匹配: 期望{expected_char_count}, 实际{actual_char_count}")
        except Exception as e:
            self.log_result("文本输入和统计功能", "FAIL", f"异常: {str(e)}")
    
    def test_segmentation_tc002(self):
        """TC002: 中文分词算法对比测试"""
        print("\n=== TC002: 中文分词算法对比测试 ===")
        
        test_text = "北京大学的人工智能研究院在机器学习领域取得了重要突破。"
        self.processor.load_text(test_text)
        
        # 测试jieba分词
        start_time = time.time()
        try:
            jieba_words = self.processor.get_top_words(n=10, method='jieba')
            execution_time = time.time() - start_time
            
            if jieba_words:
                words_list = [word for word, freq in jieba_words]
                key_words_found = any(word in ['人工智能', '机器学习', '北京大学', '研究院'] 
                                    for word in words_list)
                
                if key_words_found:
                    self.log_result("jieba分词测试", "PASS", 
                                  f"找到关键词，分词结果: {words_list[:5]}", execution_time)
                else:
                    self.log_result("jieba分词测试", "WARNING", 
                                  f"未找到预期关键词，分词结果: {words_list[:5]}")
            else:
                self.log_result("jieba分词测试", "FAIL", "未返回分词结果")
        except Exception as e:
            self.log_result("jieba分词测试", "FAIL", f"异常: {str(e)}")
        
        # 测试pkuseg分词（如果可用）
        start_time = time.time()
        try:
            pkuseg_words = self.processor.get_top_words(n=10, method='pkuseg')
            execution_time = time.time() - start_time
            
            if pkuseg_words:
                self.log_result("pkuseg分词测试", "PASS", 
                              f"pkuseg分词成功，结果数量: {len(pkuseg_words)}", execution_time)
            else:
                self.log_result("pkuseg分词测试", "WARNING", "pkuseg不可用或无结果")
        except Exception as e:
            self.log_result("pkuseg分词测试", "WARNING", f"pkuseg不可用: {str(e)}")
    
    def test_sentiment_analysis_tc003(self):
        """TC003: 情感分析多模型融合测试"""
        print("\n=== TC003: 情感分析多模型融合测试 ===")
        
        sentiment_tests = [
            ("积极情感", "这个产品真的很棒！质量很好，服务也很周到，我非常满意，强烈推荐给大家！", "positive"),
            ("消极情感", "这个服务太差了，等了很久都没有回应，完全不推荐，浪费时间和金钱。", "negative"),
            ("中性情感", "今天天气不错，温度适中，适合外出活动。", "neutral")
        ]
        
        for test_name, text, expected_sentiment in sentiment_tests:
            start_time = time.time()
            try:
                self.processor.load_text(text)
                result = self.processor.analyze_sentiment()
                execution_time = time.time() - start_time
                
                if result['available']:
                    actual_sentiment = result['sentiment']
                    confidence = result.get('confidence', 0)
                    methods = result.get('methods_used', [])
                    
                    if actual_sentiment == expected_sentiment:
                        self.log_result(f"{test_name}分析", "PASS", 
                                      f"情感: {actual_sentiment}, 置信度: {confidence:.2f}, 方法: {methods}", 
                                      execution_time)
                    else:
                        self.log_result(f"{test_name}分析", "WARNING", 
                                      f"期望: {expected_sentiment}, 实际: {actual_sentiment}, 置信度: {confidence:.2f}")
                else:
                    self.log_result(f"{test_name}分析", "FAIL", "情感分析不可用")
            except Exception as e:
                self.log_result(f"{test_name}分析", "FAIL", f"异常: {str(e)}")
    
    def test_entity_recognition_tc004(self):
        """TC004: 实体识别混合策略测试"""
        print("\n=== TC004: 实体识别混合策略测试 ===")
        
        test_text = "张三在北京大学学习计算机科学，他来自上海市浦东新区。苹果公司的CEO蒂姆·库克访问了清华大学，讨论人工智能合作项目。中国科学院和微软公司将在深圳建立联合实验室。"
        
        start_time = time.time()
        try:
            self.processor.load_text(test_text)
            result = self.processor.recognize_entities()
            execution_time = time.time() - start_time
            
            if result['available']:
                entities = result['entities']
                
                # 统计实体类型
                entity_types = {}
                for entity in entities:
                    entity_type = entity.get('label', entity.get('type', 'UNKNOWN'))
                    if entity_type not in entity_types:
                        entity_types[entity_type] = []
                    entity_types[entity_type].append(entity['text'])
                
                # 检查是否找到关键实体
                expected_entities = ['张三', '北京大学', '上海市', '苹果公司', '清华大学']
                found_entities = [entity['text'] for entity in entities]
                found_expected = [e for e in expected_entities if any(e in f for f in found_entities)]
                
                accuracy = len(found_expected) / len(expected_entities)
                
                if accuracy >= 0.6:  # 60%准确率阈值
                    self.log_result("实体识别准确性", "PASS", 
                                  f"准确率: {accuracy:.1%}, 找到实体: {len(entities)}, 类型: {list(entity_types.keys())}", 
                                  execution_time)
                else:
                    self.log_result("实体识别准确性", "WARNING", 
                                  f"准确率: {accuracy:.1%}, 低于预期60%")
            else:
                self.log_result("实体识别准确性", "FAIL", "实体识别不可用")
        except Exception as e:
            self.log_result("实体识别准确性", "FAIL", f"异常: {str(e)}")
    
    def test_text_summarization_tc005(self):
        """TC005: 文本摘要算法对比测试"""
        print("\n=== TC005: 文本摘要算法对比测试 ===")
        
        # 使用长文本进行摘要测试
        long_text = """人工智能（Artificial Intelligence，简称AI）是计算机科学的一个重要分支，它致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。人工智能的概念最早可以追溯到1950年，当时英国数学家阿兰·图灵提出了著名的"图灵测试"，用来判断机器是否具有智能。

在20世纪50年代到60年代，人工智能经历了第一次发展高潮。研究者们开发了许多早期的AI程序，如逻辑理论机、通用问题求解器等。然而，由于计算能力的限制和对问题复杂性认识不足，人工智能在70年代遭遇了第一次"AI冬天"。

进入21世纪，随着计算能力的大幅提升、大数据的出现以及深度学习算法的突破，人工智能迎来了新的春天。深度学习技术在图像识别、语音识别、自然语言处理等领域取得了突破性进展，使得人工智能技术开始真正走向实用化。

今天，人工智能已经广泛应用于各个领域，包括医疗诊断、自动驾驶、金融分析、教育、娱乐等。机器学习、深度学习、自然语言处理、计算机视觉等技术不断发展，推动着人工智能技术的进步。"""
        
        self.processor.load_text(long_text)
        
        # 测试不同摘要方法
        summary_methods = [
            ("词频算法", "frequency"),
            ("混合方法", "hybrid"),
            ("TextTeaser", "textteaser")
        ]
        
        for method_name, method in summary_methods:
            start_time = time.time()
            try:
                if method == "textteaser":
                    summary = self.processor.generate_summary(
                        num_sentences=2, 
                        method=method, 
                        title="人工智能技术发展历程"
                    )
                else:
                    summary = self.processor.generate_summary(num_sentences=2, method=method)
                
                execution_time = time.time() - start_time
                
                if summary and len(summary.strip()) > 0:
                    compression_ratio = len(summary) / len(long_text)
                    
                    if 0.05 <= compression_ratio <= 0.4:  # 合理的压缩比
                        self.log_result(f"{method_name}摘要", "PASS", 
                                      f"摘要长度: {len(summary)}, 压缩比: {compression_ratio:.1%}", 
                                      execution_time)
                    else:
                        self.log_result(f"{method_name}摘要", "WARNING", 
                                      f"压缩比异常: {compression_ratio:.1%}")
                else:
                    self.log_result(f"{method_name}摘要", "FAIL", "摘要生成失败")
            except Exception as e:
                self.log_result(f"{method_name}摘要", "FAIL", f"异常: {str(e)}")
        
        # 测试Qwen3大模型摘要（如果可用）
        start_time = time.time()
        try:
            qwen3_summary = self.processor.generate_summary(
                num_sentences=2, 
                method="qwen3", 
                title="人工智能技术发展历程"
            )
            execution_time = time.time() - start_time
            
            if qwen3_summary and len(qwen3_summary.strip()) > 0:
                self.log_result("Qwen3大模型摘要", "PASS", 
                              f"摘要长度: {len(qwen3_summary)}", execution_time)
            else:
                self.log_result("Qwen3大模型摘要", "WARNING", "Qwen3服务不可用")
        except Exception as e:
            if "连接" in str(e) or "网络" in str(e):
                self.log_result("Qwen3大模型摘要", "WARNING", f"Qwen3服务不可用: {str(e)}")
            else:
                self.log_result("Qwen3大模型摘要", "FAIL", f"异常: {str(e)}")
    
    def test_boundary_conditions_tc006(self):
        """TC006: 边界条件和异常处理测试"""
        print("\n=== TC006: 边界条件和异常处理测试 ===")
        
        # 测试空输入
        start_time = time.time()
        try:
            self.processor.load_text("")
            stats = self.processor.get_text_stats()
            execution_time = time.time() - start_time
            
            if stats.get('字符数', -1) == 0:
                self.log_result("空输入处理", "PASS", "正确处理空文本", execution_time)
            else:
                self.log_result("空输入处理", "FAIL", f"空文本字符数应为0，实际为{stats.get('字符数')}")
        except Exception as e:
            self.log_result("空输入处理", "FAIL", f"异常: {str(e)}")
        
        # 测试特殊字符
        start_time = time.time()
        try:
            special_text = "😀🎉💻🚀 Hello World! 你好世界！@#$%^&*()_+-=[]{}|;':\",./<>?"
            self.processor.load_text(special_text)
            stats = self.processor.get_text_stats()
            sentiment = self.processor.analyze_sentiment()
            execution_time = time.time() - start_time
            
            if stats and sentiment['available']:
                self.log_result("特殊字符处理", "PASS", 
                              f"成功处理emoji和特殊符号，字符数: {stats.get('字符数')}", execution_time)
            else:
                self.log_result("特殊字符处理", "WARNING", "部分功能对特殊字符处理有限")
        except Exception as e:
            self.log_result("特殊字符处理", "FAIL", f"异常: {str(e)}")
    
    def test_performance_tc007(self):
        """TC007: 性能基准测试"""
        print("\n=== TC007: 性能基准测试 ===")
        
        # 准备测试文本
        medium_text = "人工智能技术正在快速发展，深度学习、机器学习等技术在各个领域都有广泛应用。" * 20
        
        performance_tests = [
            ("文本加载性能", lambda: self.processor.load_text(medium_text), 0.1),
            ("基础统计性能", lambda: self.processor.get_text_stats(), 0.2),
            ("分词性能", lambda: self.processor.get_top_words(n=10), 1.0),
            ("情感分析性能", lambda: self.processor.analyze_sentiment(), 5.0)
        ]
        
        # 先加载文本
        self.processor.load_text(medium_text)
        
        for test_name, operation, time_limit in performance_tests:
            start_time = time.time()
            try:
                operation()
                execution_time = time.time() - start_time
                
                if execution_time <= time_limit:
                    self.log_result(test_name, "PASS", 
                                  f"执行时间: {execution_time:.3f}s (限制: {time_limit}s)", execution_time)
                else:
                    self.log_result(test_name, "WARNING", 
                                  f"执行时间: {execution_time:.3f}s 超过限制 {time_limit}s")
            except Exception as e:
                self.log_result(test_name, "FAIL", f"异常: {str(e)}")
    
    def generate_summary_report(self):
        """生成测试总结报告"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r['status'] == 'PASS')
        failed_tests = sum(1 for r in self.results if r['status'] == 'FAIL')
        warning_tests = sum(1 for r in self.results if r['status'] == 'WARNING')
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n{'='*60}")
        print("测试案例和场景分析文档 - 测试总结报告")
        print(f"{'='*60}")
        print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ({pass_rate:.1f}%)")
        print(f"失败: {failed_tests}")
        print(f"警告: {warning_tests}")
        
        if pass_rate >= 80:
            print(f"\n✅ 测试结果: 优秀 - 系统功能基本完整")
        elif pass_rate >= 60:
            print(f"\n⚠️  测试结果: 良好 - 系统基本可用，部分功能需改进")
        else:
            print(f"\n❌ 测试结果: 需要改进 - 系统存在较多问题")
        
        # 保存详细报告
        try:
            report_filename = f"document_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(f"测试案例和场景分析文档 - 详细测试报告\n")
                f.write(f"{'='*60}\n")
                f.write(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for result in self.results:
                    status_icon = "✓" if result['status'] == "PASS" else "✗" if result['status'] == "FAIL" else "⚠"
                    f.write(f"{status_icon} {result['test_name']}")
                    if result['execution_time'] > 0:
                        f.write(f" ({result['execution_time']:.3f}s)")
                    f.write(f"\n")
                    if result['details']:
                        f.write(f"   {result['details']}\n")
                    f.write(f"\n")
                
                f.write(f"\n总结:\n")
                f.write(f"总测试数: {total_tests}\n")
                f.write(f"通过: {passed_tests} ({pass_rate:.1f}%)\n")
                f.write(f"失败: {failed_tests}\n")
                f.write(f"警告: {warning_tests}\n")
            
            print(f"\n📄 详细报告已保存到: {report_filename}")
        except Exception as e:
            print(f"\n⚠️  保存报告失败: {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始执行测试案例和场景分析文档核心测试")
        print("基于文档TC001-TC007的关键场景测试")
        print("="*60)
        
        try:
            self.test_basic_functionality_tc001()
            self.test_segmentation_tc002()
            self.test_sentiment_analysis_tc003()
            self.test_entity_recognition_tc004()
            self.test_text_summarization_tc005()
            self.test_boundary_conditions_tc006()
            self.test_performance_tc007()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  测试被用户中断")
        except Exception as e:
            print(f"\n\n❌ 测试执行过程中发生错误: {str(e)}")
        
        self.generate_summary_report()
        return self.results


def main():
    """主函数"""
    print("测试案例和场景分析文档 - 核心场景测试脚本")
    print("专门针对文档中关键测试场景的验证")
    print()
    
    # 创建并运行测试
    test_runner = DocumentScenarioTests()
    results = test_runner.run_all_tests()
    
    # 返回退出码
    failed_tests = sum(1 for r in results if r['status'] == 'FAIL')
    return 0 if failed_tests == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
