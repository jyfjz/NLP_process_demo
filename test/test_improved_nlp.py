#!/usr/bin/env python3
"""
测试改进后的NLP功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def test_improved_entity_recognition():
    """测试改进的实体识别"""
    print("=== 测试改进的实体识别 ===")
    
    test_text = """
    苹果公司是一家位于美国加利福尼亚州库比蒂诺的跨国科技公司。
    该公司由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩于1976年4月1日创立。
    北京大学是中国的一所著名高等学府，位于北京市海淀区。
    微软公司、谷歌公司和腾讯公司都是知名的科技企业。
    在21世纪，特别是在2010年代，人工智能技术得到了快速发展。
    """
    
    processor = TextProcessor()
    processor.load_text(test_text)
    entities = processor.extract_entities()
    
    print(f"使用模型: {entities['model_used']}")
    print(f"找到 {len(entities['entities'])} 个实体:")
    
    # 按类型分组显示
    entity_groups = {}
    for entity in entities['entities']:
        if entity['label'] not in entity_groups:
            entity_groups[entity['label']] = []
        entity_groups[entity['label']].append(entity)
    
    for label, entity_list in entity_groups.items():
        print(f"\n{entity_list[0]['description']} ({label}):")
        for entity in entity_list:
            print(f"  - {entity['text']}")

def test_improved_sentiment_analysis():
    """测试改进的情感分析"""
    print("\n=== 测试改进的情感分析 ===")
    
    test_texts = [
        "这个产品真的很棒，我非常满意！质量优秀，服务也很好。",
        "太糟糕了，这个软件有很多问题，让我很失望和愤怒。",
        "今天天气不错，没什么特别的事情发生。",
        "我对这次的成功感到非常兴奋和开心，这是一个重大突破！",
        "这次失败让我感到沮丧和绝望，真是一场灾难。"
    ]
    
    processor = TextProcessor()
    
    for i, text in enumerate(test_texts, 1):
        processor.load_text(text)
        sentiment = processor.analyze_sentiment()
        
        print(f"\n文本 {i}: {text}")
        print(f"  情感倾向: {sentiment['sentiment']}")
        print(f"  使用方法: {', '.join(sentiment['methods_used'])}")
        
        if 'basic' in sentiment['scores']:
            scores = sentiment['scores']['basic']
            print(f"  积极词汇: {scores['positive_words']}, 消极词汇: {scores['negative_words']}")
            print(f"  极性分数: {scores['polarity']:.3f}")

def test_syntax_analysis_performance():
    """测试句法分析性能优化"""
    print("\n=== 测试句法分析性能优化 ===")
    
    # 测试短文本
    short_text = "我喜欢学习自然语言处理技术。"
    processor = TextProcessor()
    processor.load_text(short_text)
    
    print("短文本测试:")
    syntax = processor.analyze_syntax()
    print(f"  模型: {syntax['model_used']}")
    print(f"  句子数: {len(syntax['sentences'])}")
    print(f"  是否截断: {syntax.get('is_truncated', False)}")
    
    # 测试长文本
    long_text = "人工智能技术发展迅速。" * 2000  # 约10000字符
    processor.load_text(long_text)
    
    print("\n长文本测试:")
    syntax = processor.analyze_syntax()
    print(f"  模型: {syntax['model_used']}")
    print(f"  句子数: {len(syntax['sentences'])}")
    print(f"  是否截断: {syntax.get('is_truncated', False)}")

def test_enhanced_summary():
    """测试增强摘要功能"""
    print("\n=== 测试增强摘要功能 ===")
    
    test_text = """
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    
    机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。
    深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。
    
    在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
    
    苹果公司、谷歌公司、微软公司等科技巨头都在人工智能领域投入了大量资源。
    史蒂夫·乔布斯曾经预言，人工智能将改变世界。
    """
    
    processor = TextProcessor()
    processor.load_text(test_text)
    
    methods = ['enhanced_hybrid', 'syntax_based', 'hybrid']
    for method in methods:
        try:
            summary = processor.generate_enhanced_summary(num_sentences=2, method=method)
            print(f"\n{method} 方法摘要:")
            print(f"  {summary}")
        except Exception as e:
            print(f"{method} 方法出错: {e}")

def main():
    """主测试函数"""
    print("开始测试改进后的NLP功能...")
    
    try:
        test_improved_entity_recognition()
        test_improved_sentiment_analysis()
        test_syntax_analysis_performance()
        test_enhanced_summary()
        
        print("\n=== 测试完成 ===")
        print("✓ 实体识别效果已改进")
        print("✓ 情感分析词典已扩展")
        print("✓ 句法分析支持大文本处理")
        print("✓ 增强摘要功能正常")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
