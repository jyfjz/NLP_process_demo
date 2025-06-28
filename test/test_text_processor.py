#!/usr/bin/env python3
"""
文本处理工具测试脚本
"""

import sys
import os

# 添加父目录到路径，以便导入code_model模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code_model.text_tools import TextProcessor


def test_basic_functionality():
    """测试基本功能"""
    print("=" * 60)
    print("文本处理工具功能测试")
    print("=" * 60)
    
    # 创建处理器实例
    processor = TextProcessor()
    
    # 测试1: 加载文本
    print("\n1. 测试文本加载...")
    try:
        processor.load_from_file("test/sample_text.txt")
        print("✓ 文本加载成功")
        stats = processor.get_text_stats()
        print(f"  文本统计: {stats}")
    except Exception as e:
        print(f"✗ 文本加载失败: {e}")
        # 如果文件不存在，使用示例文本
        sample_text = """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。

在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
        """.strip()
        processor.load_text(sample_text)
        print("✓ 使用示例文本进行测试")
        stats = processor.get_text_stats()
        print(f"  文本统计: {stats}")
    
    # 测试2: 查找功能
    print("\n2. 测试查找功能...")
    matches = processor.find_matches("人工智能", use_regex=False, case_sensitive=True)
    print(f"✓ 找到 '人工智能' {len(matches)} 次")
    for i, (pos, match) in enumerate(matches[:5]):
        print(f"  {i+1}. 位置 {pos}: '{match}'")
    
    # 测试3: 正则表达式查找
    print("\n3. 测试正则表达式查找...")
    regex_matches = processor.find_matches(r"\d{4}", use_regex=True)
    print(f"✓ 找到年份格式 {len(regex_matches)} 次")
    for i, (pos, match) in enumerate(regex_matches):
        print(f"  {i+1}. 位置 {pos}: '{match}'")
    
    # 测试4: 替换功能
    print("\n4. 测试替换功能...")
    original_text = processor.text
    new_text, count = processor.find_and_replace("人工智能", "AI", use_regex=False)
    print(f"✓ 替换 '人工智能' -> 'AI' {count} 次")
    
    # 恢复原文本
    processor.text = original_text
    
    # 测试5: 词频统计
    print("\n5. 测试词频统计...")
    top_words = processor.get_top_words(n=10, ignore_case=True, min_word_length=2)
    print("✓ 词频统计结果 (前10个):")
    for i, (word, freq) in enumerate(top_words, 1):
        print(f"  {i:2d}. {word:<10} {freq:>3}")
    
    # 测试6: 摘要生成
    print("\n6. 测试摘要生成...")
    
    # 基于词频的摘要
    summary_freq = processor.generate_summary(num_sentences=3, method='frequency')
    print("✓ 基于词频的摘要:")
    print(f"  {summary_freq}")
    
    # 基于位置的摘要
    summary_pos = processor.generate_summary(num_sentences=3, method='position')
    print("\n✓ 基于位置的摘要:")
    print(f"  {summary_pos}")
    
    # 混合方法摘要
    summary_hybrid = processor.generate_summary(num_sentences=3, method='hybrid')
    print("\n✓ 混合方法摘要:")
    print(f"  {summary_hybrid}")
    
    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)


def test_edge_cases():
    """测试边界情况"""
    print("\n" + "=" * 60)
    print("边界情况测试")
    print("=" * 60)
    
    processor = TextProcessor()
    
    # 测试空文本
    print("\n1. 测试空文本...")
    processor.load_text("")
    word_freq = processor.word_frequency()
    print(f"✓ 空文本词频统计: {word_freq}")
    
    # 测试单句文本
    print("\n2. 测试单句文本...")
    processor.load_text("这是一个测试句子。")
    summary = processor.generate_summary(num_sentences=3)
    print(f"✓ 单句摘要: {summary}")
    
    # 测试正则表达式错误
    print("\n3. 测试正则表达式错误...")
    processor.load_text("测试文本")
    try:
        processor.find_matches("[", use_regex=True)
        print("✗ 应该抛出异常")
    except ValueError as e:
        print(f"✓ 正确捕获正则表达式错误: {e}")
    
    print("\n边界情况测试完成！")


def demo_advanced_features():
    """演示高级功能"""
    print("\n" + "=" * 60)
    print("高级功能演示")
    print("=" * 60)
    
    processor = TextProcessor()
    try:
        processor.load_from_file("test/sample_text.txt")
    except FileNotFoundError:
        # 使用示例文本
        sample_text = """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。

在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
        """.strip()
        processor.load_text(sample_text)
    
    # 演示复杂正则表达式
    print("\n1. 复杂正则表达式演示...")
    
    # 查找所有年份
    years = processor.find_matches(r"(19|20)\d{2}", use_regex=True)
    print(f"✓ 找到年份: {[match[1] for match in years]}")
    
    # 查找中文标点符号
    punctuation = processor.find_matches(r"[，。！？；：]", use_regex=True)
    print(f"✓ 找到中文标点符号 {len(punctuation)} 个")
    
    # 查找括号内容
    brackets = processor.find_matches(r"（[^）]*）", use_regex=True)
    print(f"✓ 找到括号内容: {[match[1] for match in brackets]}")
    
    # 演示不同词频统计选项
    print("\n2. 不同词频统计选项演示...")
    
    # 包含标点符号
    freq_with_punct = processor.get_top_words(n=5, exclude_punctuation=False)
    print("✓ 包含标点符号的词频:")
    for word, freq in freq_with_punct:
        print(f"  {word}: {freq}")
    
    # 最小词长过滤
    freq_long_words = processor.get_top_words(n=5, min_word_length=3)
    print("\n✓ 最小词长3的词频:")
    for word, freq in freq_long_words:
        print(f"  {word}: {freq}")
    
    print("\n高级功能演示完成！")


if __name__ == "__main__":
    test_basic_functionality()
    test_edge_cases()
    demo_advanced_features()
