#!/usr/bin/env python3
"""
文本处理工具演示脚本
展示主要功能的使用方法
"""

import sys
import os

# 添加父目录到路径，以便导入code_model模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code_model.text_tools import TextProcessor


def demo_basic_features():
    """演示基本功能"""
    print("=" * 60)
    print("文本处理工具功能演示")
    print("=" * 60)
    
    # 创建处理器
    processor = TextProcessor()
    
    # 加载示例文本
    print("\n1. 加载文本文件...")
    try:
        processor.load_from_file("test/sample_text.txt")
        print("✓ 成功加载 sample_text.txt")
    except FileNotFoundError:
        # 使用示例文本
        sample_text = """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。

在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
        """.strip()
        processor.load_text(sample_text)
        print("✓ 使用示例文本进行演示")
    
    # 显示文本统计
    stats = processor.get_text_stats()
    print(f"文本统计: {stats}")
    
    # 查找功能演示
    print("\n2. 查找功能演示...")
    matches = processor.find_matches("人工智能")
    print(f"找到 '人工智能' {len(matches)} 次")
    
    # 正则表达式查找
    year_matches = processor.find_matches(r"\d{4}", use_regex=True)
    print(f"找到年份 {len(year_matches)} 次: {[m[1] for m in year_matches]}")
    
    # 词频统计演示
    print("\n3. 词频统计演示...")
    top_words = processor.get_top_words(n=10)
    print("前10个高频词:")
    for i, (word, freq) in enumerate(top_words, 1):
        print(f"  {i:2d}. {word:<15} {freq:>3}")
    
    # 摘要生成演示
    print("\n4. 摘要生成演示...")
    summary = processor.generate_summary(num_sentences=2, method='hybrid')
    print("摘要 (2句话):")
    print(f"  {summary}")
    
    # 替换功能演示
    print("\n5. 替换功能演示...")
    original_text = processor.text
    new_text, count = processor.find_and_replace("人工智能", "AI")
    print(f"替换 '人工智能' -> 'AI' {count} 次")
    
    # 保存结果
    processor.save_to_file("demo_output.txt")
    print("✓ 替换后的文本已保存到 demo_output.txt")
    
    # 重置文本
    processor.reset_text()
    print("✓ 文本已重置到原始状态")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


def demo_advanced_regex():
    """演示高级正则表达式功能"""
    print("\n" + "=" * 60)
    print("高级正则表达式功能演示")
    print("=" * 60)
    
    processor = TextProcessor()
    # 使用示例文本
    sample_text = """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。

在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
    """.strip()
    processor.load_text(sample_text)
    
    # 各种正则表达式示例
    regex_examples = [
        (r"\d{4}", "四位数字（年份）"),
        (r"[，。！？]", "中文标点符号"),
        (r"（[^）]*）", "括号内容"),
        (r"[a-zA-Z]+", "英文单词"),
        (r"人工智能|机器学习|深度学习", "AI相关术语"),
        (r"\d+世纪", "世纪表达"),
    ]
    
    for pattern, description in regex_examples:
        matches = processor.find_matches(pattern, use_regex=True)
        print(f"\n{description}: {len(matches)} 个匹配")
        if matches:
            # 显示前5个匹配项
            for i, (pos, match) in enumerate(matches[:5]):
                print(f"  {i+1}. 位置 {pos}: '{match}'")
            if len(matches) > 5:
                print(f"  ... 还有 {len(matches)-5} 个")


def demo_different_summary_methods():
    """演示不同的摘要方法"""
    print("\n" + "=" * 60)
    print("不同摘要方法对比")
    print("=" * 60)
    
    processor = TextProcessor()
    # 使用示例文本
    sample_text = """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。

在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
    """.strip()
    processor.load_text(sample_text)
    
    methods = [
        ('frequency', '基于词频'),
        ('position', '基于位置'),
        ('hybrid', '混合方法')
    ]
    
    for method, description in methods:
        print(f"\n{description}摘要:")
        print("-" * 40)
        summary = processor.generate_summary(num_sentences=2, method=method)
        print(summary)


def demo_word_frequency_options():
    """演示词频统计的不同选项"""
    print("\n" + "=" * 60)
    print("词频统计选项对比")
    print("=" * 60)
    
    processor = TextProcessor()
    # 使用示例文本
    sample_text = """
人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。

人工智能从诞生以来，理论和技术日益成熟，应用领域也不断扩大。可以设想，未来人工智能带来的科技产品，将会是人类智慧的"容器"。人工智能可以对人的意识、思维的信息过程的模拟。人工智能不是人的智能，但能像人那样思考、也可能超过人的智能。

机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。

在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
    """.strip()
    processor.load_text(sample_text)
    
    options = [
        {'ignore_case': True, 'min_word_length': 1, 'exclude_punctuation': True},
        {'ignore_case': False, 'min_word_length': 1, 'exclude_punctuation': True},
        {'ignore_case': True, 'min_word_length': 3, 'exclude_punctuation': True},
        {'ignore_case': True, 'min_word_length': 1, 'exclude_punctuation': False},
    ]
    
    descriptions = [
        "默认设置（忽略大小写，包含所有词，排除标点）",
        "区分大小写",
        "最小词长为3",
        "包含标点符号"
    ]
    
    for i, (opts, desc) in enumerate(zip(options, descriptions)):
        print(f"\n{i+1}. {desc}:")
        top_words = processor.get_top_words(n=5, **opts)
        for j, (word, freq) in enumerate(top_words, 1):
            print(f"  {j}. {word:<20} {freq}")


if __name__ == "__main__":
    demo_basic_features()
    demo_advanced_regex()
    demo_different_summary_methods()
    demo_word_frequency_options()
    
    print("\n" + "=" * 60)
    print("所有演示完成！")
    print("要使用交互式界面，请运行: python text_processor.py")
    print("=" * 60)
