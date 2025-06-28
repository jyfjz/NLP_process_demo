#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextTeaser算法测试脚本
测试我们实现的轻量级TextTeaser风格摘要算法
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def test_textteaser_summary():
    """测试TextTeaser摘要功能"""
    print("=== TextTeaser算法测试 ===\n")
    
    # 测试文本
    test_text = """
    人工智能技术的发展与应用前景
    
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    
    机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。
    深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。
    
    在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
    
    苹果公司、谷歌公司、微软公司等科技巨头都在人工智能领域投入了大量资源。
    史蒂夫·乔布斯曾经预言，人工智能将改变世界。
    
    目前，人工智能技术已经广泛应用于医疗诊断、金融分析、自动驾驶、智能家居等多个领域。
    未来，随着技术的不断进步，人工智能将在更多领域发挥重要作用，为人类社会带来更大的便利和效益。
    
    然而，人工智能的发展也带来了一些挑战，包括就业问题、隐私保护、算法偏见等。
    因此，我们需要在推进人工智能技术发展的同时，也要关注其可能带来的社会影响。
    """
    
    # 创建处理器
    processor = TextProcessor()
    processor.load_text(test_text)
    
    # 测试标题
    title = "人工智能技术的发展与应用前景"
    
    print(f"原文长度: {len(test_text)} 字符")
    print(f"标题: {title}")
    print("-" * 80)
    
    # 测试不同的摘要方法
    methods = [
        ('frequency', '基于词频'),
        ('position', '基于位置'),
        ('hybrid', '混合方法'),
        ('textteaser', 'TextTeaser算法')
    ]
    
    for method, method_name in methods:
        print(f"\n【{method_name}】")
        print("-" * 40)
        
        try:
            if method == 'textteaser':
                # TextTeaser需要标题参数
                summary = processor.generate_summary(num_sentences=3, method=method, title=title)
            else:
                summary = processor.generate_summary(num_sentences=3, method=method)
            
            print(f"摘要: {summary}")
            print(f"摘要长度: {len(summary)} 字符")
            
        except Exception as e:
            print(f"错误: {e}")
    
    print("\n" + "=" * 80)

def test_textteaser_features():
    """测试TextTeaser各个特征的评分"""
    print("\n=== TextTeaser特征评分测试 ===\n")
    
    processor = TextProcessor()
    
    # 简单测试文本
    test_text = """
    人工智能是未来科技发展的重要方向。
    机器学习技术在各个领域都有广泛应用。
    深度学习是机器学习的一个重要分支。
    人工智能将改变我们的生活方式。
    """
    
    processor.load_text(test_text)
    title = "人工智能技术发展"
    
    sentences = processor._split_sentences(test_text)
    print(f"句子列表:")
    for i, sent in enumerate(sentences):
        print(f"  {i+1}. {sent}")
    
    print(f"\n标题: {title}")
    print("-" * 60)
    
    # 计算TextTeaser评分
    scores = processor._calculate_textteaser_scores(sentences, title)
    
    print("\nTextTeaser评分结果:")
    for i, (score, sentence) in enumerate(scores):
        print(f"句子 {i+1}: {score:.3f} - {sentence}")
    
    # 排序后的结果
    scores.sort(reverse=True)
    print("\n按评分排序:")
    for i, (score, sentence) in enumerate(scores):
        print(f"第 {i+1} 名: {score:.3f} - {sentence}")

def test_different_titles():
    """测试不同标题对TextTeaser摘要的影响"""
    print("\n=== 不同标题影响测试 ===\n")
    
    processor = TextProcessor()
    
    test_text = """
    苹果公司发布了最新的iPhone手机，搭载了先进的人工智能芯片。
    这款手机在拍照、语音识别和自然语言处理方面都有显著提升。
    谷歌公司也在同期发布了新的Android系统，集成了更多AI功能。
    微软公司则专注于云计算和企业级AI解决方案的开发。
    三星公司在显示技术和移动处理器方面继续保持领先地位。
    华为公司虽然面临挑战，但在5G技术方面仍有重要贡献。
    """
    
    processor.load_text(test_text)
    
    # 测试不同的标题
    titles = [
        "苹果公司新产品发布",
        "人工智能技术发展",
        "科技公司竞争格局",
        "手机行业最新动态"
    ]
    
    for title in titles:
        print(f"标题: {title}")
        print("-" * 40)
        
        summary = processor.generate_summary(num_sentences=2, method='textteaser', title=title)
        print(f"摘要: {summary}")
        print()

if __name__ == "__main__":
    # 运行所有测试
    test_textteaser_summary()
    test_textteaser_features()
    test_different_titles()
    
    print("\n✓ TextTeaser算法测试完成！")
