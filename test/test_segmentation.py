#!/usr/bin/env python3
"""
测试分词功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def test_segmentation():
    """测试分词功能"""
    print("=== 测试分词功能 ===")
    
    # 创建处理器
    processor = TextProcessor()
    
    # 测试文本
    test_texts = [
        "我爱北京天安门，天安门上太阳升。",
        "人工智能技术在医疗领域的应用越来越广泛。",
        "今天天气很好，我们去公园散步吧。",
        "苹果公司发布了新的iPhone手机。",
        "中国的经济发展取得了巨大成就。"
    ]
    
    # 测试不同的分词方法
    methods = ['auto', 'jieba', 'pkuseg_default', 'pkuseg_news', 'basic']
    
    for text in test_texts:
        print(f"\n原文: {text}")
        processor.load_text(text)
        
        for method in methods:
            try:
                segments = processor.segment_text(method=method, with_pos=False)
                words = [seg['word'] for seg in segments]
                print(f"{method:15}: {' / '.join(words)}")
            except Exception as e:
                print(f"{method:15}: 错误 - {e}")

def test_word_frequency():
    """测试词频统计"""
    print("\n=== 测试词频统计 ===")
    
    processor = TextProcessor()
    
    # 测试文本
    text = """
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    人工智能研究的一个主要目标是使机器能够胜任一些通常需要人类智能才能完成的复杂工作。
    在人工智能领域，机器学习是一个重要的研究方向。机器学习算法能够从数据中学习模式，并做出预测或决策。
    深度学习是机器学习的一个子领域，它使用神经网络来模拟人脑的学习过程。
    """
    
    processor.load_text(text)
    
    # 测试不同分词方法的词频统计
    methods = ['auto', 'jieba', 'basic']
    
    for method in methods:
        try:
            print(f"\n使用 {method} 分词的词频统计:")
            word_freq = processor.word_frequency(
                segmentation_method=method,
                min_word_length=2,
                exclude_punctuation=True
            )
            
            # 显示前10个高频词
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            for i, (word, freq) in enumerate(sorted_words[:10], 1):
                print(f"  {i:2d}. {word:<10} {freq}")
                
        except Exception as e:
            print(f"  {method} 分词失败: {e}")

def test_segmentation_capabilities():
    """测试分词器可用性"""
    print("\n=== 分词器可用性测试 ===")
    
    processor = TextProcessor()
    
    print("可用的分词器:")
    for name, segmenter in processor.segmenters.items():
        print(f"  ✓ {name}")
    
    if not processor.segmenters:
        print("  只有基础分词可用")

if __name__ == '__main__':
    test_segmentation_capabilities()
    test_segmentation()
    test_word_frequency()
