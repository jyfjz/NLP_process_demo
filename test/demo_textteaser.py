#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TextTeaser算法演示脚本
展示TextTeaser算法的特点和优势
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def demo_textteaser_vs_others():
    """演示TextTeaser与其他算法的对比"""
    print("=" * 80)
    print("TextTeaser算法演示 - 与其他摘要算法对比")
    print("=" * 80)
    
    # 测试文本：关于人工智能的新闻文章
    test_text = """
    苹果公司在最新的开发者大会上宣布了重大的人工智能突破。该公司推出了全新的AI芯片，专门为机器学习任务进行了优化。
    
    这款新芯片被命名为"Neural Engine Pro"，相比上一代产品，处理速度提升了300%，同时功耗降低了40%。
    苹果公司的首席执行官表示，这项技术将彻底改变移动设备上的人工智能应用。
    
    与此同时，谷歌公司也在人工智能领域取得了重要进展。该公司发布了新版本的TensorFlow框架，支持更高效的深度学习模型训练。
    谷歌的研究团队声称，新框架可以将模型训练时间缩短50%，这对于大规模AI项目具有重要意义。
    
    微软公司则专注于企业级AI解决方案的开发。该公司推出了Azure AI平台的升级版本，集成了更多自动化功能。
    微软的产品经理介绍说，新平台可以帮助企业更容易地部署和管理AI应用，降低了技术门槛。
    
    业界专家认为，这些技术进步标志着人工智能进入了一个新的发展阶段。
    随着硬件性能的提升和软件工具的完善，AI技术将在更多领域得到广泛应用。
    """
    
    processor = TextProcessor()
    processor.load_text(test_text)
    
    # 测试不同的标题，展示TextTeaser的标题敏感性
    test_cases = [
        ("苹果公司AI芯片突破", "重点关注苹果公司的技术突破"),
        ("谷歌TensorFlow更新", "重点关注谷歌的软件框架"),
        ("微软企业AI平台", "重点关注微软的企业解决方案"),
        ("人工智能技术发展", "通用的AI技术发展主题")
    ]
    
    for title, description in test_cases:
        print(f"\n【测试案例】{description}")
        print(f"标题: {title}")
        print("-" * 60)
        
        # 对比不同算法
        methods = [
            ('frequency', '基于词频'),
            ('hybrid', '混合方法'),
            ('textteaser', 'TextTeaser算法')
        ]
        
        for method, method_name in methods:
            try:
                if method == 'textteaser':
                    summary = processor.generate_summary(num_sentences=2, method=method, title=title)
                else:
                    summary = processor.generate_summary(num_sentences=2, method=method)
                
                print(f"\n{method_name}:")
                print(f"  {summary}")
                
            except Exception as e:
                print(f"{method_name}: 错误 - {e}")
        
        print("\n" + "=" * 60)

def demo_textteaser_features():
    """演示TextTeaser算法的特征评分"""
    print("\n" + "=" * 80)
    print("TextTeaser算法特征分析演示")
    print("=" * 80)
    
    processor = TextProcessor()
    
    # 简化的测试文本
    test_text = """
    人工智能技术正在快速发展，改变着我们的生活方式。
    机器学习是人工智能的核心技术之一，在各个领域都有广泛应用。
    深度学习作为机器学习的重要分支，在图像识别和自然语言处理方面表现出色。
    未来，人工智能将在医疗、教育、交通等更多领域发挥重要作用。
    我们需要关注人工智能发展带来的机遇和挑战。
    """
    
    processor.load_text(test_text)
    title = "人工智能技术发展"
    
    sentences = processor._split_sentences(test_text)
    print(f"标题: {title}")
    print(f"文本包含 {len(sentences)} 个句子\n")
    
    # 显示每个句子
    for i, sent in enumerate(sentences, 1):
        print(f"句子{i}: {sent}")
    
    print("\n" + "-" * 60)
    print("TextTeaser特征评分详细分析:")
    print("-" * 60)
    
    # 获取详细的评分信息
    word_freq = processor.word_frequency(ignore_case=True, exclude_punctuation=True)
    title_words = processor._extract_keywords(title.lower())
    
    print(f"标题关键词: {title_words}")
    print(f"高频词汇: {list(word_freq.keys())[:10]}")
    print()
    
    for i, sentence in enumerate(sentences, 1):
        print(f"句子{i}评分分析:")
        
        # 计算各项特征分数
        title_score = processor._calculate_title_similarity(sentence.lower(), title_words)
        position_score = processor._calculate_position_score(i-1, len(sentences))
        length_score = processor._calculate_length_score(sentence)
        keyword_score = processor._calculate_keyword_score(sentence, word_freq)
        
        # 综合分数
        final_score = (
            title_score * 0.40 +
            position_score * 0.20 +
            length_score * 0.15 +
            keyword_score * 0.25
        )
        
        print(f"  标题相似度: {title_score:.3f} (权重40%)")
        print(f"  位置评分:   {position_score:.3f} (权重20%)")
        print(f"  长度评分:   {length_score:.3f} (权重15%)")
        print(f"  关键词评分: {keyword_score:.3f} (权重25%)")
        print(f"  综合评分:   {final_score:.3f}")
        print()
    
    # 生成最终摘要
    summary = processor.generate_summary(num_sentences=2, method='textteaser', title=title)
    print("-" * 60)
    print("最终摘要结果:")
    print(f"  {summary}")

def demo_title_sensitivity():
    """演示TextTeaser对标题的敏感性"""
    print("\n" + "=" * 80)
    print("TextTeaser标题敏感性演示")
    print("=" * 80)
    
    processor = TextProcessor()
    
    # 包含多个主题的文本
    test_text = """
    苹果公司发布了最新的iPhone 15系列手机，搭载了全新的A17芯片。
    这款手机在摄影功能方面有显著提升，支持4K视频录制和专业级照片编辑。
    谷歌公司同时推出了Pixel 8手机，主打人工智能摄影功能。
    三星公司的Galaxy S24系列也即将上市，预计将配备更先进的显示屏技术。
    华为公司虽然面临挑战，但在5G技术和折叠屏设计方面仍保持创新。
    小米公司专注于性价比市场，推出了多款中端智能手机产品。
    """
    
    processor.load_text(test_text)
    
    # 测试不同焦点的标题
    titles = [
        "苹果iPhone新品发布",
        "谷歌Pixel摄影技术",
        "三星显示屏创新",
        "华为5G技术发展",
        "智能手机市场竞争"
    ]
    
    print("相同文本，不同标题的摘要结果对比:\n")
    
    for title in titles:
        print(f"标题: {title}")
        print("-" * 40)
        
        summary = processor.generate_summary(num_sentences=2, method='textteaser', title=title)
        print(f"摘要: {summary}")
        print()

if __name__ == "__main__":
    # 运行所有演示
    demo_textteaser_vs_others()
    demo_textteaser_features()
    demo_title_sensitivity()
    
    print("\n" + "=" * 80)
    print("✓ TextTeaser算法演示完成！")
    print("TextTeaser的主要特点:")
    print("1. 标题敏感性 - 根据标题选择最相关的句子")
    print("2. 位置权重 - 重视文章开头和结尾的句子")
    print("3. 长度优化 - 偏好适中长度的句子")
    print("4. 关键词密度 - 考虑高频词汇的分布")
    print("=" * 80)
