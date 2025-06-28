#!/usr/bin/env python3
"""
测试高级自然语言处理功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def test_nlp_capabilities():
    """测试NLP功能可用性"""
    print("=== 测试NLP功能可用性 ===")
    
    processor = TextProcessor()
    capabilities = processor.get_nlp_capabilities()
    
    print("可用功能:")
    for feature, available in capabilities.items():
        status = "✓" if available else "✗"
        print(f"  {status} {feature}: {available}")
    
    return processor

def test_entity_recognition(processor):
    """测试实体识别"""
    print("\n=== 测试实体识别 ===")
    
    test_text = """
    苹果公司是一家位于美国加利福尼亚州库比蒂诺的跨国科技公司。
    该公司由史蒂夫·乔布斯、史蒂夫·沃兹尼亚克和罗纳德·韦恩于1976年4月1日创立。
    北京大学是中国的一所著名高等学府，位于北京市海淀区。
    """
    
    processor.load_text(test_text)
    entities = processor.extract_entities()
    
    if entities['available']:
        print(f"使用模型: {entities['model_used']}")
        print(f"找到 {len(entities['entities'])} 个实体:")
        for entity in entities['entities']:
            print(f"  - {entity['text']} ({entity['label']}) - {entity.get('description', '')}")
    else:
        print("实体识别功能不可用")

def test_sentiment_analysis(processor):
    """测试情感分析"""
    print("\n=== 测试情感分析 ===")
    
    test_texts = [
        "我今天心情很好，天气也很棒！",
        "这个产品质量太差了，我很失望。",
        "今天是普通的一天，没什么特别的。"
    ]
    
    for text in test_texts:
        processor.load_text(text)
        sentiment = processor.analyze_sentiment()
        
        if sentiment['available']:
            print(f"文本: {text}")
            print(f"  情感倾向: {sentiment['sentiment']}")
            print(f"  使用方法: {', '.join(sentiment['methods_used'])}")
            if 'vader' in sentiment['scores']:
                scores = sentiment['scores']['vader']
                print(f"  VADER分数: pos={scores['pos']:.3f}, neg={scores['neg']:.3f}, neu={scores['neu']:.3f}")
            if 'textblob' in sentiment['scores']:
                scores = sentiment['scores']['textblob']
                print(f"  TextBlob分数: polarity={scores['polarity']:.3f}, subjectivity={scores['subjectivity']:.3f}")
            print()
        else:
            print(f"情感分析不可用: {text}")

def test_syntax_analysis(processor):
    """测试句法分析"""
    print("\n=== 测试句法分析 ===")
    
    test_text = "我喜欢学习自然语言处理技术。"
    
    processor.load_text(test_text)
    syntax = processor.analyze_syntax()
    
    if syntax['available']:
        print(f"使用模型: {syntax['model_used']}")
        print(f"句法分析结果:")
        for i, sent in enumerate(syntax['sentences']):
            print(f"  句子 {i+1}: {sent['text']}")
            for word in sent['words']:
                print(f"    {word['text']} - 词性:{word['pos']}, 依存关系:{word['deprel']}")
    else:
        print("句法分析功能不可用")

def test_enhanced_summary(processor):
    """测试增强摘要功能"""
    print("\n=== 测试增强摘要功能 ===")
    
    test_text = """
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    
    机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。
    深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。
    
    在21世纪，人工智能技术得到了快速发展，特别是在2010年代以后，深度学习技术的突破使得人工智能在图像识别、语音识别、自然语言处理等领域取得了显著进展。
    """
    
    processor.load_text(test_text)
    
    methods = ['enhanced_hybrid', 'syntax_based', 'hybrid']
    for method in methods:
        try:
            summary = processor.generate_enhanced_summary(num_sentences=2, method=method)
            print(f"{method} 方法摘要:")
            print(f"  {summary}")
            print()
        except Exception as e:
            print(f"{method} 方法出错: {e}")

def main():
    """主测试函数"""
    print("开始测试高级自然语言处理功能...")
    
    try:
        processor = test_nlp_capabilities()
        test_entity_recognition(processor)
        test_sentiment_analysis(processor)
        test_syntax_analysis(processor)
        test_enhanced_summary(processor)
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
