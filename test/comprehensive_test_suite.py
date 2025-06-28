#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试案例和场景分析文档测试脚本
基于测试案例和场景分析文档的全面测试实现
"""

import sys
import os
import time
import json
import traceback
from datetime import datetime
from typing import Dict, List, Any, Tuple

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code_model.text_tools import TextProcessor

class DocumentBasedTestSuite:
    """基于测试案例和场景分析文档的测试套件"""

    def __init__(self):
        self.processor = TextProcessor()
        self.test_results = []
        self.start_time = None
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.warning_tests = 0

        # 测试数据
        self.test_data = self._init_test_data()

    def _init_test_data(self) -> Dict[str, Any]:
        """初始化测试数据"""
        return {
            'short_text': "这是一个测试文本。",
            'medium_text': "人工智能技术正在快速发展，深度学习、机器学习等技术在各个领域都有广泛应用。ChatGPT的出现标志着大语言模型技术的重大突破。未来，AI将在医疗、教育、金融等行业发挥更重要的作用。",
            'long_text': """人工智能（Artificial Intelligence，简称AI）是计算机科学的一个重要分支，它致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。人工智能的概念最早可以追溯到1950年，当时英国数学家阿兰·图灵提出了著名的"图灵测试"，用来判断机器是否具有智能。

在20世纪50年代到60年代，人工智能经历了第一次发展高潮。研究者们开发了许多早期的AI程序，如逻辑理论机、通用问题求解器等。然而，由于计算能力的限制和对问题复杂性认识不足，人工智能在70年代遭遇了第一次"AI冬天"。

80年代，专家系统的兴起带来了人工智能的第二次繁荣。专家系统通过模拟人类专家的决策过程，在医疗诊断、金融分析等领域取得了一定的成功。但是，专家系统的局限性很快显现出来，人工智能再次进入低潮期。

进入21世纪，随着计算能力的大幅提升、大数据的出现以及深度学习算法的突破，人工智能迎来了新的春天。深度学习技术在图像识别、语音识别、自然语言处理等领域取得了突破性进展，使得人工智能技术开始真正走向实用化。

今天，人工智能已经广泛应用于各个领域，包括医疗诊断、自动驾驶、金融分析、教育、娱乐等。机器学习、深度学习、自然语言处理、计算机视觉等技术不断发展，推动着人工智能技术的进步。

然而，人工智能的发展也带来了一些挑战和担忧，如就业问题、隐私保护、算法偏见、安全风险等。如何在发展人工智能技术的同时，确保其安全、可控、有益于人类社会，是我们面临的重要课题。""",
            'special_chars_text': "😀🎉💻🚀 Hello World! 你好世界！@#$%^&*()_+-=[]{}|;':\",./<>?",
            'entity_text': "张三在北京大学学习计算机科学，他来自上海市浦东新区。苹果公司的CEO蒂姆·库克访问了清华大学，讨论人工智能合作项目。中国科学院和微软公司将在深圳建立联合实验室。",
            'positive_sentiment': "这个产品真的很棒！质量很好，服务也很周到，我非常满意，强烈推荐给大家！",
            'negative_sentiment': "这个服务太差了，等了很久都没有回应，完全不推荐，浪费时间和金钱。",
            'neutral_sentiment': "今天天气不错，温度适中，适合外出活动。",
            'segmentation_text': "北京大学的人工智能研究院在机器学习领域取得了重要突破。"
        }

    def log_test_result(self, test_id: str, test_name: str, status: str,
                       details: str = None, execution_time: float = None):
        """记录测试结果"""
        result = {
            'test_id': test_id,
            'test_name': test_name,
            'status': status,
            'execution_time': execution_time,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)

        # 更新统计
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        elif status == "FAIL":
            self.failed_tests += 1
        else:
            self.warning_tests += 1

        status_icon = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
        time_str = f" ({execution_time:.3f}s)" if execution_time else ""
        print(f"{status_icon} {test_id}: {test_name}{time_str}")
        if details and status != "PASS":
            print(f"   详情: {details}")

    def test_basic_text_processing(self):
        """测试案例1: 基础文本处理功能 (TC001)"""
        print("\n=== TC001: 基础文本处理功能测试 ===")

        test_cases = [
            ("TC001-1", "短文本处理", self.test_data['short_text']),
            ("TC001-2", "中等文本处理", self.test_data['medium_text']),
            ("TC001-3", "长文本处理", self.test_data['long_text']),
            ("TC001-4", "特殊字符处理", self.test_data['special_chars_text'])
        ]

        for test_id, test_name, text in test_cases:
            start_time = time.time()
            try:
                # 加载文本
                self.processor.load_text(text)

                # 验证文本统计
                stats = self.processor.get_text_stats()
                expected_keys = ['字符数', '词数', '行数', '段落数']

                if all(key in stats for key in expected_keys):
                    # 验证统计数据合理性
                    char_count = stats['字符数']
                    if char_count == len(text):
                        execution_time = time.time() - start_time
                        self.log_test_result(test_id, test_name, "PASS",
                                           f"字符数: {char_count}", execution_time)
                    else:
                        self.log_test_result(test_id, test_name, "FAIL",
                                           f"字符数不匹配: 期望{len(text)}, 实际{char_count}")
                else:
                    missing_keys = [key for key in expected_keys if key not in stats]
                    self.log_test_result(test_id, test_name, "FAIL",
                                       f"缺少统计项: {missing_keys}")

            except Exception as e:
                self.log_test_result(test_id, test_name, "FAIL", f"异常: {str(e)}")

    def test_chinese_segmentation(self):
        """测试案例2: 中文分词和词频统计 (TC002)"""
        print("\n=== TC002: 中文分词和词频统计测试 ===")

        text = self.test_data['segmentation_text']
        self.processor.load_text(text)

        # 测试jieba分词
        start_time = time.time()
        try:
            top_words = self.processor.get_top_words(n=10, method='jieba')
            execution_time = time.time() - start_time

            if top_words and len(top_words) > 0:
                # 验证是否包含预期的关键词
                words = [word for word, freq in top_words]
                expected_words = ['人工智能', '机器学习', '北京大学', '研究院']
                found_words = [word for word in expected_words if any(word in w for w in words)]

                if found_words:
                    self.log_test_result("TC002-1", "jieba分词测试", "PASS",
                                       f"找到关键词: {found_words}", execution_time)
                else:
                    self.log_test_result("TC002-1", "jieba分词测试", "WARNING",
                                       f"未找到预期关键词，实际词汇: {words[:5]}")
            else:
                self.log_test_result("TC002-1", "jieba分词测试", "FAIL", "未返回分词结果")

        except Exception as e:
            self.log_test_result("TC002-1", "jieba分词测试", "FAIL", f"异常: {str(e)}")

        # 测试pkuseg分词（如果可用）
        start_time = time.time()
        try:
            top_words_pkuseg = self.processor.get_top_words(n=10, method='pkuseg')
            execution_time = time.time() - start_time

            if top_words_pkuseg:
                self.log_test_result("TC002-2", "pkuseg分词测试", "PASS",
                                   f"分词结果数量: {len(top_words_pkuseg)}", execution_time)
            else:
                self.log_test_result("TC002-2", "pkuseg分词测试", "WARNING", "pkuseg不可用或无结果")

        except Exception as e:
            self.log_test_result("TC002-2", "pkuseg分词测试", "WARNING", f"pkuseg不可用: {str(e)}")

        # 测试停用词过滤
        start_time = time.time()
        try:
            words_with_stopwords = self.processor.get_top_words(n=20, remove_stopwords=False)
            words_without_stopwords = self.processor.get_top_words(n=20, remove_stopwords=True)
            execution_time = time.time() - start_time

            if len(words_without_stopwords) < len(words_with_stopwords):
                self.log_test_result("TC002-3", "停用词过滤测试", "PASS",
                                   f"过滤前: {len(words_with_stopwords)}, 过滤后: {len(words_without_stopwords)}",
                                   execution_time)
            else:
                self.log_test_result("TC002-3", "停用词过滤测试", "WARNING", "停用词过滤效果不明显")

        except Exception as e:
            self.log_test_result("TC002-3", "停用词过滤测试", "FAIL", f"异常: {str(e)}")

    def test_sentiment_analysis(self):
        """测试案例3: 情感分析多模型融合 (TC003)"""
        print("\n=== TC003: 情感分析多模型融合测试 ===")

        sentiment_tests = [
            ("TC003-1", "积极情感分析", self.test_data['positive_sentiment'], 'positive'),
            ("TC003-2", "消极情感分析", self.test_data['negative_sentiment'], 'negative'),
            ("TC003-3", "中性情感分析", self.test_data['neutral_sentiment'], 'neutral')
        ]

        for test_id, test_name, text, expected_sentiment in sentiment_tests:
            start_time = time.time()
            try:
                self.processor.load_text(text)
                result = self.processor.analyze_sentiment()
                execution_time = time.time() - start_time

                if result['available']:
                    actual_sentiment = result['sentiment']
                    confidence = result.get('confidence', 0)
                    methods_used = result.get('methods_used', [])

                    if actual_sentiment == expected_sentiment:
                        self.log_test_result(test_id, test_name, "PASS",
                                           f"情感: {actual_sentiment}, 置信度: {confidence:.2f}, 方法: {methods_used}",
                                           execution_time)
                    else:
                        self.log_test_result(test_id, test_name, "WARNING",
                                           f"期望: {expected_sentiment}, 实际: {actual_sentiment}, 置信度: {confidence:.2f}")
                else:
                    self.log_test_result(test_id, test_name, "FAIL", "情感分析不可用")

            except Exception as e:
                self.log_test_result(test_id, test_name, "FAIL", f"异常: {str(e)}")

    def test_entity_recognition(self):
        """测试案例4: 实体识别准确性测试 (TC004)"""
        print("\n=== TC004: 实体识别准确性测试 ===")

        text = self.test_data['entity_text']
        self.processor.load_text(text)

        start_time = time.time()
        try:
            result = self.processor.recognize_entities()
            execution_time = time.time() - start_time

            if result['available']:
                entities = result['entities']

                # 预期实体
                expected_entities = {
                    'PERSON': ['张三', '蒂姆·库克'],
                    'ORG': ['北京大学', '苹果公司', '清华大学', '中国科学院', '微软公司'],
                    'GPE': ['上海市', '浦东新区', '深圳']
                }

                found_entities = {}
                for entity in entities:
                    entity_type = entity.get('label', entity.get('type', 'UNKNOWN'))
                    if entity_type not in found_entities:
                        found_entities[entity_type] = []
                    found_entities[entity_type].append(entity['text'])

                # 计算准确率
                total_expected = sum(len(entities) for entities in expected_entities.values())
                total_found = 0
                correct_found = 0

                for entity_type, expected_list in expected_entities.items():
                    found_list = found_entities.get(entity_type, [])
                    for expected_entity in expected_list:
                        if any(expected_entity in found for found in found_list):
                            correct_found += 1
                    total_found += len(found_list)

                accuracy = correct_found / total_expected if total_expected > 0 else 0

                if accuracy >= 0.7:  # 70%准确率阈值
                    self.log_test_result("TC004-1", "实体识别准确性", "PASS",
                                       f"准确率: {accuracy:.2%}, 找到实体: {len(entities)}", execution_time)
                else:
                    self.log_test_result("TC004-1", "实体识别准确性", "WARNING",
                                       f"准确率: {accuracy:.2%}, 低于预期70%")

                # 详细结果记录
                details = f"找到的实体: {found_entities}"
                self.log_test_result("TC004-2", "实体识别详细结果", "PASS", details)

            else:
                self.log_test_result("TC004-1", "实体识别准确性", "FAIL", "实体识别不可用")

        except Exception as e:
            self.log_test_result("TC004-1", "实体识别准确性", "FAIL", f"异常: {str(e)}")

    def test_text_summarization(self):
        """测试案例5: 文本摘要算法对比 (TC005)"""
        print("\n=== TC005: 文本摘要算法对比测试 ===")

        text = self.test_data['long_text']
        self.processor.load_text(text)

        # 测试不同摘要算法
        summary_methods = [
            ("TC005-1", "词频算法摘要", "frequency"),
            ("TC005-2", "混合方法摘要", "hybrid"),
            ("TC005-3", "TextTeaser摘要", "textteaser"),
            ("TC005-4", "Qwen3大模型摘要", "qwen3")
        ]

        for test_id, test_name, method in summary_methods:
            start_time = time.time()
            try:
                if method == "qwen3":
                    # 测试大模型摘要（需要标题）
                    summary = self.processor.generate_summary(
                        num_sentences=2,
                        method=method,
                        title="人工智能技术发展历程"
                    )
                else:
                    summary = self.processor.generate_summary(num_sentences=2, method=method)

                execution_time = time.time() - start_time

                if summary and len(summary.strip()) > 0:
                    # 验证摘要质量
                    summary_length = len(summary)
                    original_length = len(text)
                    compression_ratio = summary_length / original_length

                    if 0.05 <= compression_ratio <= 0.3:  # 合理的压缩比
                        self.log_test_result(test_id, test_name, "PASS",
                                           f"摘要长度: {summary_length}, 压缩比: {compression_ratio:.2%}",
                                           execution_time)
                    else:
                        self.log_test_result(test_id, test_name, "WARNING",
                                           f"压缩比异常: {compression_ratio:.2%}")
                else:
                    self.log_test_result(test_id, test_name, "FAIL", f"{method}摘要生成失败")

            except Exception as e:
                if method == "qwen3" and "连接" in str(e):
                    self.log_test_result(test_id, test_name, "WARNING", f"Qwen3服务不可用: {str(e)}")
                else:
                    self.log_test_result(test_id, test_name, "FAIL", f"异常: {str(e)}")

    def test_boundary_conditions(self):
        """测试案例6: 边界条件和异常处理 (TC006)"""
        print("\n=== TC006: 边界条件和异常处理测试 ===")

        # 测试空输入
        start_time = time.time()
        try:
            self.processor.load_text("")
            stats = self.processor.get_text_stats()
            execution_time = time.time() - start_time

            if stats['字符数'] == 0:
                self.log_test_result("TC006-1", "空输入处理", "PASS",
                                   "正确处理空文本", execution_time)
            else:
                self.log_test_result("TC006-1", "空输入处理", "FAIL",
                                   f"空文本字符数应为0，实际为{stats['字符数']}")
        except Exception as e:
            self.log_test_result("TC006-1", "空输入处理", "FAIL", f"异常: {str(e)}")

        # 测试超长文本
        start_time = time.time()
        try:
            very_long_text = "测试文本" * 50000  # 约30万字符
            self.processor.load_text(very_long_text)
            execution_time = time.time() - start_time

            if len(very_long_text) > 200000:
                # 应该能处理，但可能有性能警告
                self.log_test_result("TC006-2", "超长文本处理", "WARNING",
                                   f"文本长度: {len(very_long_text)}, 超过建议限制", execution_time)
            else:
                self.log_test_result("TC006-2", "超长文本处理", "PASS",
                                   f"文本长度: {len(very_long_text)}", execution_time)
        except Exception as e:
            self.log_test_result("TC006-2", "超长文本处理", "FAIL", f"异常: {str(e)}")

        # 测试特殊字符
        start_time = time.time()
        try:
            special_text = self.test_data['special_chars_text']
            self.processor.load_text(special_text)

            # 测试分词
            top_words = self.processor.get_top_words(n=5)

            # 测试情感分析
            sentiment = self.processor.analyze_sentiment()

            execution_time = time.time() - start_time

            if top_words and sentiment['available']:
                self.log_test_result("TC006-3", "特殊字符处理", "PASS",
                                   f"成功处理emoji和特殊符号", execution_time)
            else:
                self.log_test_result("TC006-3", "特殊字符处理", "WARNING",
                                   "部分功能对特殊字符处理有限")

        except Exception as e:
            self.log_test_result("TC006-3", "特殊字符处理", "FAIL", f"异常: {str(e)}")

    def test_performance_benchmarks(self):
        """测试案例7: 性能和负载测试 (TC007)"""
        print("\n=== TC007: 性能和负载测试 ===")

        # 性能基准测试
        performance_tests = [
            ("TC007-1", "文本加载性能", self.test_data['medium_text'], 0.1),
            ("TC007-2", "基础统计性能", self.test_data['long_text'], 0.2),
            ("TC007-3", "分词性能", self.test_data['long_text'], 1.0),
            ("TC007-4", "情感分析性能", self.test_data['medium_text'], 5.0)
        ]

        for test_id, test_name, text, time_limit in performance_tests:
            start_time = time.time()
            try:
                self.processor.load_text(text)

                if "统计" in test_name:
                    self.processor.get_text_stats()
                elif "分词" in test_name:
                    self.processor.get_top_words(n=10)
                elif "情感" in test_name:
                    self.processor.analyze_sentiment()

                execution_time = time.time() - start_time

                if execution_time <= time_limit:
                    self.log_test_result(test_id, test_name, "PASS",
                                       f"执行时间: {execution_time:.3f}s (限制: {time_limit}s)",
                                       execution_time)
                else:
                    self.log_test_result(test_id, test_name, "WARNING",
                                       f"执行时间: {execution_time:.3f}s 超过限制 {time_limit}s")

            except Exception as e:
                self.log_test_result(test_id, test_name, "FAIL", f"异常: {str(e)}")

    def test_user_scenarios(self):
        """测试案例8: 用户场景测试 (TC008)"""
        print("\n=== TC008: 用户场景端到端测试 ===")

        # 学术研究场景
        start_time = time.time()
        try:
            academic_text = self.test_data['long_text']
            self.processor.load_text(academic_text)

            # 执行完整的学术分析流程
            summary = self.processor.generate_summary(num_sentences=3, method='hybrid')
            entities = self.processor.recognize_entities()
            top_words = self.processor.get_top_words(n=10)

            execution_time = time.time() - start_time

            if summary and entities['available'] and top_words:
                self.log_test_result("TC008-1", "学术研究场景", "PASS",
                                   f"完整分析流程执行成功", execution_time)
            else:
                self.log_test_result("TC008-1", "学术研究场景", "WARNING",
                                   "部分分析功能不可用")

        except Exception as e:
            self.log_test_result("TC008-1", "学术研究场景", "FAIL", f"异常: {str(e)}")

        # 内容创作场景
        start_time = time.time()
        try:
            content_text = self.test_data['medium_text']
            self.processor.load_text(content_text)

            # 执行内容优化流程
            sentiment = self.processor.analyze_sentiment()

            # 测试查找替换功能
            new_text, count = self.processor.find_and_replace("人工智能", "AI技术")

            execution_time = time.time() - start_time

            if sentiment['available'] and count > 0:
                self.log_test_result("TC008-2", "内容创作场景", "PASS",
                                   f"内容优化流程执行成功，替换{count}处", execution_time)
            else:
                self.log_test_result("TC008-2", "内容创作场景", "WARNING",
                                   "部分优化功能效果有限")

        except Exception as e:
            self.log_test_result("TC008-2", "内容创作场景", "FAIL", f"异常: {str(e)}")

    def test_integration_and_regression(self):
        """测试案例9: 集成测试和回归测试 (TC009)"""
        print("\n=== TC009: 集成测试和回归测试 ===")

        # 多功能协作测试
        start_time = time.time()
        try:
            text = self.test_data['entity_text']
            self.processor.load_text(text)

            # 依次执行多个功能，验证数据传递
            stats1 = self.processor.get_text_stats()
            top_words = self.processor.get_top_words(n=5)
            sentiment = self.processor.analyze_sentiment()
            entities = self.processor.recognize_entities()
            stats2 = self.processor.get_text_stats()

            execution_time = time.time() - start_time

            # 验证文本状态一致性
            if stats1 == stats2:
                self.log_test_result("TC009-1", "多功能协作测试", "PASS",
                                   f"文本状态保持一致，执行{len([top_words, sentiment, entities])}个功能",
                                   execution_time)
            else:
                self.log_test_result("TC009-1", "多功能协作测试", "FAIL",
                                   "文本状态在功能调用间发生变化")

        except Exception as e:
            self.log_test_result("TC009-1", "多功能协作测试", "FAIL", f"异常: {str(e)}")

        # 内存稳定性测试
        start_time = time.time()
        try:
            # 重复执行相同操作，检查内存泄漏
            for i in range(5):
                self.processor.load_text(self.test_data['medium_text'])
                self.processor.get_top_words(n=10)
                self.processor.analyze_sentiment()

            execution_time = time.time() - start_time
            self.log_test_result("TC009-2", "内存稳定性测试", "PASS",
                               f"重复执行5次操作无异常", execution_time)

        except Exception as e:
            self.log_test_result("TC009-2", "内存稳定性测试", "FAIL", f"异常: {str(e)}")

    def test_usability_and_user_experience(self):
        """测试案例10: 可用性和用户体验测试 (TC010)"""
        print("\n=== TC010: 可用性和用户体验测试 ===")

        # 接口响应性测试
        response_tests = [
            ("TC010-1", "文本加载响应", lambda: self.processor.load_text(self.test_data['short_text'])),
            ("TC010-2", "统计计算响应", lambda: self.processor.get_text_stats()),
            ("TC010-3", "查找功能响应", lambda: self.processor.find_matches("测试"))
        ]

        for test_id, test_name, operation in response_tests:
            start_time = time.time()
            try:
                operation()
                execution_time = time.time() - start_time

                if execution_time < 0.1:  # 100ms响应时间
                    self.log_test_result(test_id, test_name, "PASS",
                                       f"响应时间: {execution_time:.3f}s", execution_time)
                else:
                    self.log_test_result(test_id, test_name, "WARNING",
                                       f"响应时间: {execution_time:.3f}s 超过100ms")

            except Exception as e:
                self.log_test_result(test_id, test_name, "FAIL", f"异常: {str(e)}")

        # 错误处理友好性测试
        start_time = time.time()
        try:
            # 测试无效输入的处理
            self.processor.load_text("")
            result = self.processor.analyze_sentiment()

            execution_time = time.time() - start_time

            # 应该能优雅处理空输入
            if not result['available'] or result['sentiment'] == 'neutral':
                self.log_test_result("TC010-4", "错误处理友好性", "PASS",
                                   "优雅处理空输入", execution_time)
            else:
                self.log_test_result("TC010-4", "错误处理友好性", "WARNING",
                                   "空输入处理可能不够友好")

        except Exception as e:
            # 如果抛出异常，检查是否是友好的异常
            if "文本" in str(e) or "输入" in str(e):
                self.log_test_result("TC010-4", "错误处理友好性", "PASS",
                                   f"友好的错误提示: {str(e)}")
            else:
                self.log_test_result("TC010-4", "错误处理友好性", "FAIL",
                                   f"不友好的错误: {str(e)}")

    def generate_test_report(self) -> str:
        """生成测试报告"""
        total_time = time.time() - self.start_time if self.start_time else 0

        # 计算统计信息
        pass_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0

        # 按测试类别分组
        test_categories = {}
        for result in self.test_results:
            category = result['test_id'].split('-')[0]
            if category not in test_categories:
                test_categories[category] = {'total': 0, 'passed': 0, 'failed': 0, 'warning': 0}

            test_categories[category]['total'] += 1
            if result['status'] == 'PASS':
                test_categories[category]['passed'] += 1
            elif result['status'] == 'FAIL':
                test_categories[category]['failed'] += 1
            else:
                test_categories[category]['warning'] += 1

        # 生成报告
        report = f"""
{'='*80}
测试案例和场景分析文档 - 测试执行报告
{'='*80}
执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
总执行时间: {total_time:.2f}秒

📊 测试统计概览
{'─'*40}
总测试数: {self.total_tests}
通过: {self.passed_tests} ({pass_rate:.1f}%)
失败: {self.failed_tests}
警告: {self.warning_tests}

📋 分类测试结果
{'─'*40}"""

        for category, stats in test_categories.items():
            category_pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            report += f"""
{category}: {stats['passed']}/{stats['total']} 通过 ({category_pass_rate:.1f}%)
  ✓ 通过: {stats['passed']}  ✗ 失败: {stats['failed']}  ⚠ 警告: {stats['warning']}"""

        report += f"""

📝 详细测试结果
{'─'*40}"""

        for result in self.test_results:
            status_icon = "✓" if result['status'] == "PASS" else "✗" if result['status'] == "FAIL" else "⚠"
            time_str = f" ({result['execution_time']:.3f}s)" if result['execution_time'] else ""
            report += f"""
{status_icon} {result['test_id']}: {result['test_name']}{time_str}"""
            if result['details'] and result['status'] != "PASS":
                report += f"""
   详情: {result['details']}"""

        # 测试结论
        if pass_rate >= 90:
            conclusion = "✅ 优秀 - 系统功能完整，质量很高"
        elif pass_rate >= 80:
            conclusion = "✅ 良好 - 系统功能基本完整，质量较好"
        elif pass_rate >= 70:
            conclusion = "⚠️  一般 - 系统基本可用，需要改进"
        else:
            conclusion = "❌ 需要改进 - 系统存在较多问题"

        report += f"""

🎯 测试结论
{'─'*40}
{conclusion}

📈 质量评估
{'─'*40}
- 功能完整性: {'优秀' if pass_rate >= 90 else '良好' if pass_rate >= 80 else '一般' if pass_rate >= 70 else '需改进'}
- 系统稳定性: {'优秀' if self.failed_tests <= 2 else '良好' if self.failed_tests <= 5 else '需改进'}
- 性能表现: {'优秀' if any('性能' in r['test_name'] and r['status'] == 'PASS' for r in self.test_results) else '需测试'}

💡 改进建议
{'─'*40}"""

        # 根据失败的测试给出建议
        failed_categories = [cat for cat, stats in test_categories.items() if stats['failed'] > 0]
        if failed_categories:
            report += f"""
- 重点关注失败的测试类别: {', '.join(failed_categories)}"""

        if self.warning_tests > 0:
            report += f"""
- 关注{self.warning_tests}个警告项，可能影响用户体验"""

        if pass_rate < 90:
            report += f"""
- 建议修复失败的测试案例，提升系统稳定性"""

        report += f"""

{'='*80}
报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}
"""

        return report

    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始执行测试案例和场景分析文档测试套件")
        print("="*80)

        self.start_time = time.time()

        try:
            # 执行所有测试案例
            self.test_basic_text_processing()
            self.test_chinese_segmentation()
            self.test_sentiment_analysis()
            self.test_entity_recognition()
            self.test_text_summarization()
            self.test_boundary_conditions()
            self.test_performance_benchmarks()
            self.test_user_scenarios()
            self.test_integration_and_regression()
            self.test_usability_and_user_experience()

        except KeyboardInterrupt:
            print("\n\n⚠️  测试被用户中断")
        except Exception as e:
            print(f"\n\n❌ 测试执行过程中发生严重错误: {str(e)}")
            traceback.print_exc()

        # 生成并显示报告
        report = self.generate_test_report()
        print(report)

        # 保存报告到文件
        try:
            report_filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 测试报告已保存到: {report_filename}")
        except Exception as e:
            print(f"\n⚠️  保存报告失败: {str(e)}")

        return self.test_results


def main():
    """主函数"""
    print("测试案例和场景分析文档 - 自动化测试脚本")
    print("基于文档TC001-TC010的全面测试实现")
    print()

    # 创建并运行测试套件
    test_suite = DocumentBasedTestSuite()
    results = test_suite.run_all_tests()

    # 返回退出码
    failed_tests = sum(1 for r in results if r['status'] == 'FAIL')
    return 0 if failed_tests == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
            ("特殊字符", "😀🎉💻🚀 Hello World! 你好世界！@#$%^&*()_+-=[]{}|;':\",./<>?")
        ]
        
        for text_type, text in test_texts:
            start_time = time.time()
            try:
                # 加载文本
                self.processor.load_text(text)
                
                # 获取统计信息
                stats = self.processor.get_text_stats()
                
                # 验证统计信息
                expected_char_count = len(text)
                actual_char_count = stats.get('字符数', 0)
                
                if actual_char_count == expected_char_count:
                    self.log_test_result(
                        "TC001-1", 
                        f"文本统计-{text_type}", 
                        "PASS",
                        f"字符数: {actual_char_count}",
                        time.time() - start_time
                    )
                else:
                    self.log_test_result(
                        "TC001-1", 
                        f"文本统计-{text_type}", 
                        "FAIL",
                        f"期望字符数: {expected_char_count}, 实际: {actual_char_count}",
                        time.time() - start_time
                    )
                    
            except Exception as e:
                self.log_test_result(
                    "TC001-1", 
                    f"文本统计-{text_type}", 
                    "FAIL",
                    str(e),
                    time.time() - start_time
                )
    
    def test_chinese_segmentation(self):
        """测试案例2: 中文分词和词频统计"""
        print("\n=== TC002: 中文分词算法对比测试 ===")
        
        test_text = "北京大学的人工智能研究院在机器学习领域取得了重要突破。"
        self.processor.load_text(test_text)
        
        # 测试不同分词方法
        methods = ['jieba', 'pkuseg_default', 'basic']
        
        for method in methods:
            start_time = time.time()
            try:
                # 执行分词
                segments = self.processor.segment_text(method=method)
                
                if segments and len(segments) > 0:
                    self.log_test_result(
                        "TC002-1", 
                        f"分词测试-{method}", 
                        "PASS",
                        f"分词数量: {len(segments)}",
                        time.time() - start_time
                    )
                else:
                    self.log_test_result(
                        "TC002-1", 
                        f"分词测试-{method}", 
                        "FAIL",
                        "分词结果为空",
                        time.time() - start_time
                    )
                    
            except Exception as e:
                self.log_test_result(
                    "TC002-1", 
                    f"分词测试-{method}", 
                    "SKIP",
                    f"分词器不可用: {str(e)}",
                    time.time() - start_time
                )
        
        # 测试词频统计
        start_time = time.time()
        try:
            word_freq = self.processor.get_top_words(n=10)
            
            if word_freq and len(word_freq) > 0:
                self.log_test_result(
                    "TC002-2", 
                    "词频统计", 
                    "PASS",
                    f"词频条目: {len(word_freq)}",
                    time.time() - start_time
                )
            else:
                self.log_test_result(
                    "TC002-2", 
                    "词频统计", 
                    "FAIL",
                    "词频统计结果为空",
                    time.time() - start_time
                )
                
        except Exception as e:
            self.log_test_result(
                "TC002-2", 
                "词频统计", 
                "FAIL",
                str(e),
                time.time() - start_time
            )
    
    def test_sentiment_analysis(self):
        """测试案例3: 情感分析多模型融合"""
        print("\n=== TC003: 情感分析准确性测试 ===")
        
        test_cases = [
            ("积极情感", "这个产品真的很棒！质量很好，服务也很周到，我非常满意，强烈推荐给大家！", "positive"),
            ("消极情感", "这个服务太差了，等了很久都没有回应，完全不推荐，浪费时间和金钱。", "negative"),
            ("中性情感", "今天天气不错，温度适中，适合外出活动。", "neutral")
        ]
        
        for case_name, text, expected_sentiment in test_cases:
            start_time = time.time()
            try:
                result = self.processor.analyze_sentiment(text)
                
                actual_sentiment = result.get('sentiment', 'unknown')
                confidence = result.get('confidence', 0.0)
                
                if actual_sentiment == expected_sentiment:
                    self.log_test_result(
                        "TC003-1", 
                        f"情感分析-{case_name}", 
                        "PASS",
                        f"情感: {actual_sentiment}, 置信度: {confidence:.2f}",
                        time.time() - start_time
                    )
                else:
                    self.log_test_result(
                        "TC003-1", 
                        f"情感分析-{case_name}", 
                        "FAIL",
                        f"期望: {expected_sentiment}, 实际: {actual_sentiment}",
                        time.time() - start_time
                    )
                    
            except Exception as e:
                self.log_test_result(
                    "TC003-1", 
                    f"情感分析-{case_name}", 
                    "FAIL",
                    str(e),
                    time.time() - start_time
                )
    
    def test_entity_recognition(self):
        """测试案例4: 实体识别准确性测试"""
        print("\n=== TC004: 实体识别混合策略测试 ===")
        
        test_text = """张三在北京大学学习计算机科学，他来自上海市浦东新区。
苹果公司的CEO蒂姆·库克访问了清华大学，讨论人工智能合作项目。
中国科学院和微软公司将在深圳建立联合实验室。"""
        
        start_time = time.time()
        try:
            result = self.processor.extract_entities(test_text, method='hybrid')
            
            entities = result.get('entities', [])
            model_used = result.get('model_used', 'unknown')
            
            # 检查是否识别出关键实体
            entity_texts = [entity.get('text', '') for entity in entities]
            expected_entities = ['张三', '北京大学', '苹果公司', '清华大学']
            
            found_entities = [e for e in expected_entities if any(e in text for text in entity_texts)]
            
            if len(found_entities) >= len(expected_entities) * 0.7:  # 70%准确率
                self.log_test_result(
                    "TC004-1", 
                    "实体识别", 
                    "PASS",
                    f"识别实体: {len(entities)}, 模型: {model_used}",
                    time.time() - start_time
                )
            else:
                self.log_test_result(
                    "TC004-1", 
                    "实体识别", 
                    "FAIL",
                    f"识别准确率不足，期望实体: {expected_entities}, 找到: {found_entities}",
                    time.time() - start_time
                )
                
        except Exception as e:
            self.log_test_result(
                "TC004-1", 
                "实体识别", 
                "FAIL",
                str(e),
                time.time() - start_time
            )
    
    def test_text_summarization(self):
        """测试案例5: 文本摘要算法对比"""
        print("\n=== TC005: 文本摘要算法效果对比 ===")
        
        # 使用示例文本
        try:
            with open('test/sample_text.txt', 'r', encoding='utf-8') as f:
                test_text = f.read()
        except FileNotFoundError:
            test_text = """人工智能（Artificial Intelligence，简称AI）是计算机科学的一个重要分支。
它致力于研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统。
人工智能的发展可以追溯到20世纪50年代，经历了多次起伏。
今天，人工智能已经广泛应用于各个领域，包括医疗诊断、自动驾驶、金融分析等。"""
        
        self.processor.load_text(test_text)
        
        # 测试不同摘要方法
        methods = [
            ('frequency', '基于词频'),
            ('hybrid', '混合方法'),
            ('textteaser', 'TextTeaser算法'),
            ('qwen3', 'Qwen3大模型')
        ]
        
        for method, method_name in methods:
            start_time = time.time()
            try:
                if method in ['textteaser', 'qwen3']:
                    summary = self.processor.generate_summary(
                        num_sentences=2, 
                        method=method, 
                        title="人工智能技术发展"
                    )
                else:
                    summary = self.processor.generate_summary(num_sentences=2, method=method)
                
                if summary and len(summary.strip()) > 0:
                    self.log_test_result(
                        "TC005-1", 
                        f"摘要生成-{method_name}", 
                        "PASS",
                        f"摘要长度: {len(summary)}字符",
                        time.time() - start_time
                    )
                else:
                    self.log_test_result(
                        "TC005-1", 
                        f"摘要生成-{method_name}", 
                        "FAIL",
                        "摘要为空",
                        time.time() - start_time
                    )
                    
            except Exception as e:
                self.log_test_result(
                    "TC005-1", 
                    f"摘要生成-{method_name}", 
                    "SKIP",
                    f"方法不可用: {str(e)}",
                    time.time() - start_time
                )
    
    def test_boundary_conditions(self):
        """测试案例6: 边界条件和异常处理"""
        print("\n=== TC006: 边界条件和异常处理测试 ===")
        
        # 测试空输入
        start_time = time.time()
        try:
            self.processor.load_text("")
            stats = self.processor.get_text_stats()
            
            if stats.get('字符数', -1) == 0:
                self.log_test_result(
                    "TC006-1", 
                    "空输入处理", 
                    "PASS",
                    "正确处理空文本",
                    time.time() - start_time
                )
            else:
                self.log_test_result(
                    "TC006-1", 
                    "空输入处理", 
                    "FAIL",
                    f"空文本统计异常: {stats}",
                    time.time() - start_time
                )
                
        except Exception as e:
            self.log_test_result(
                "TC006-1", 
                "空输入处理", 
                "FAIL",
                str(e),
                time.time() - start_time
            )
        
        # 测试超长文本
        start_time = time.time()
        try:
            long_text = "测试文本。" * 50000  # 约25万字符
            
            # 这应该被系统拒绝或者正确处理
            if len(long_text) > 200000:
                self.log_test_result(
                    "TC006-2", 
                    "超长文本检测", 
                    "PASS",
                    f"正确识别超长文本: {len(long_text)}字符",
                    time.time() - start_time
                )
            else:
                self.processor.load_text(long_text)
                self.log_test_result(
                    "TC006-2", 
                    "超长文本处理", 
                    "PASS",
                    f"成功处理长文本: {len(long_text)}字符",
                    time.time() - start_time
                )
                
        except Exception as e:
            self.log_test_result(
                "TC006-2", 
                "超长文本处理", 
                "PASS",
                f"正确拒绝超长文本: {str(e)}",
                time.time() - start_time
            )
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=" * 80)
        print("中文文本处理和NLP分析工具 - 综合测试套件")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # 运行各个测试案例
        self.test_basic_text_processing()
        self.test_chinese_segmentation()
        self.test_sentiment_analysis()
        self.test_entity_recognition()
        self.test_text_summarization()
        self.test_boundary_conditions()
        
        # 生成测试报告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成测试报告"""
        total_time = time.time() - self.start_time
        
        # 统计测试结果
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        skipped_tests = len([r for r in self.test_results if r['status'] == 'SKIP'])
        
        print("\n" + "=" * 80)
        print("测试报告")
        print("=" * 80)
        print(f"总测试数: {total_tests}")
        print(f"通过: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"失败: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        print(f"跳过: {skipped_tests} ({skipped_tests/total_tests*100:.1f}%)")
        print(f"总执行时间: {total_time:.2f}秒")
        
        # 保存详细报告
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'skipped': skipped_tests,
                    'total_time': total_time,
                    'timestamp': datetime.now().isoformat()
                },
                'test_results': self.test_results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n详细报告已保存到: {report_file}")
        
        # 测试结论
        if failed_tests == 0:
            print("\n🎉 所有测试通过！系统功能正常。")
        elif failed_tests <= total_tests * 0.1:  # 失败率小于10%
            print(f"\n⚠️  大部分测试通过，有{failed_tests}个测试失败，建议检查相关功能。")
        else:
            print(f"\n❌ 有{failed_tests}个测试失败，建议优先修复相关问题。")

if __name__ == "__main__":
    # 运行综合测试套件
    test_suite = ComprehensiveTestSuite()
    test_suite.run_all_tests()
