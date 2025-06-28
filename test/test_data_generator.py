#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据生成器 - 为各种测试场景生成测试数据
"""

import random
import string
from typing import List, Dict, Tuple

class TestDataGenerator:
    """测试数据生成器"""
    
    def __init__(self):
        # 中文常用词汇
        self.chinese_words = [
            "人工智能", "机器学习", "深度学习", "神经网络", "自然语言处理",
            "计算机科学", "数据分析", "算法", "模型", "训练",
            "北京", "上海", "广州", "深圳", "杭州", "南京", "武汉",
            "清华大学", "北京大学", "复旦大学", "上海交通大学", "浙江大学",
            "苹果公司", "谷歌公司", "微软公司", "腾讯公司", "阿里巴巴",
            "张三", "李四", "王五", "赵六", "陈七", "刘八", "黄九"
        ]
        
        # 情感词汇
        self.positive_words = [
            "优秀", "出色", "完美", "满意", "喜欢", "推荐", "赞", "好评",
            "棒", "不错", "满分", "惊艳", "超赞", "给力", "点赞"
        ]
        
        self.negative_words = [
            "差劲", "失望", "糟糕", "不满", "讨厌", "垃圾", "差评", "坑",
            "烂", "无语", "崩溃", "恶心", "愤怒", "抱怨", "退货"
        ]
        
        self.neutral_words = [
            "一般", "普通", "正常", "还行", "凑合", "中等", "平常", "标准",
            "基本", "常规", "适中", "平均", "中性", "客观", "事实"
        ]
    
    def generate_basic_text_samples(self) -> List[Tuple[str, str]]:
        """生成基础文本测试样本"""
        samples = []
        
        # 1. 空文本
        samples.append(("空文本", ""))
        
        # 2. 单字符
        samples.append(("单字符", "测"))
        
        # 3. 短文本
        samples.append(("短文本", "这是一个简单的测试文本。"))
        
        # 4. 中等长度文本
        medium_text = "人工智能技术正在快速发展，深度学习和机器学习在各个领域都有广泛应用。" * 5
        samples.append(("中等文本", medium_text))
        
        # 5. 长文本
        long_text = "随着科技的不断进步，人工智能已经成为当今最热门的技术领域之一。" * 100
        samples.append(("长文本", long_text))
        
        # 6. 超长文本
        very_long_text = "这是一个用于测试系统处理能力的超长文本。" * 10000
        samples.append(("超长文本", very_long_text))
        
        # 7. 特殊字符文本
        special_text = "😀🎉💻🚀 Hello World! 你好世界！@#$%^&*()_+-=[]{}|;':\",./<>?"
        samples.append(("特殊字符", special_text))
        
        # 8. 混合语言文本
        mixed_text = "This is English text. 这是中文文本。これは日本語です。"
        samples.append(("混合语言", mixed_text))
        
        # 9. 数字和符号
        number_text = "2023年12月25日，温度-5°C，价格￥199.99，电话13800138000。"
        samples.append(("数字符号", number_text))
        
        # 10. 纯标点符号
        punctuation_text = "！@#￥%……&*（）——+{}|："《》？[]\\;',./"
        samples.append(("纯标点", punctuation_text))
        
        return samples
    
    def generate_sentiment_test_data(self) -> List[Tuple[str, str, str]]:
        """生成情感分析测试数据"""
        test_data = []
        
        # 积极情感样本
        positive_samples = [
            "这个产品真的很棒！质量很好，服务也很周到，我非常满意！",
            "太喜欢这个设计了，简直完美，强烈推荐给大家！",
            "体验超级好，功能强大，性价比很高，五星好评！",
            "客服态度很好，解决问题很及时，给个大大的赞！",
            "包装精美，物流快速，商品质量超出预期，非常满意！"
        ]
        
        for text in positive_samples:
            test_data.append(("积极情感", text, "positive"))
        
        # 消极情感样本
        negative_samples = [
            "这个服务太差了，等了很久都没有回应，完全不推荐！",
            "质量很差，用了几天就坏了，浪费钱，差评！",
            "客服态度恶劣，解决问题不积极，非常失望！",
            "物流太慢了，包装也很差，商品有损坏，要求退货！",
            "功能不好用，界面设计很糟糕，完全不符合描述！"
        ]
        
        for text in negative_samples:
            test_data.append(("消极情感", text, "negative"))
        
        # 中性情感样本
        neutral_samples = [
            "今天天气不错，温度适中，适合外出活动。",
            "这是一个普通的产品，功能基本满足需求。",
            "价格在合理范围内，质量一般，没有特别突出的地方。",
            "按照说明书操作，功能正常，符合基本要求。",
            "收到商品了，包装完整，正在试用中。"
        ]
        
        for text in neutral_samples:
            test_data.append(("中性情感", text, "neutral"))
        
        return test_data
    
    def generate_entity_test_data(self) -> List[Tuple[str, str, List[Dict]]]:
        """生成实体识别测试数据"""
        test_data = []
        
        # 人名、地名、机构名混合文本
        text1 = "张三在北京大学学习计算机科学，他来自上海市浦东新区。"
        entities1 = [
            {"text": "张三", "type": "PERSON"},
            {"text": "北京大学", "type": "ORG"},
            {"text": "上海市", "type": "GPE"},
            {"text": "浦东新区", "type": "GPE"}
        ]
        test_data.append(("基础实体", text1, entities1))
        
        # 公司和人名
        text2 = "苹果公司的CEO蒂姆·库克访问了清华大学，讨论人工智能合作项目。"
        entities2 = [
            {"text": "苹果公司", "type": "ORG"},
            {"text": "蒂姆·库克", "type": "PERSON"},
            {"text": "清华大学", "type": "ORG"}
        ]
        test_data.append(("公司人名", text2, entities2))
        
        # 多个机构
        text3 = "中国科学院和微软公司将在深圳建立联合实验室。"
        entities3 = [
            {"text": "中国科学院", "type": "ORG"},
            {"text": "微软公司", "type": "ORG"},
            {"text": "深圳", "type": "GPE"}
        ]
        test_data.append(("多机构", text3, entities3))
        
        # 复杂实体文本
        text4 = "腾讯公司创始人马化腾在广州举办的AI大会上表示，将与斯坦福大学合作开发新的机器学习算法。"
        entities4 = [
            {"text": "腾讯公司", "type": "ORG"},
            {"text": "马化腾", "type": "PERSON"},
            {"text": "广州", "type": "GPE"},
            {"text": "斯坦福大学", "type": "ORG"}
        ]
        test_data.append(("复杂实体", text4, entities4))
        
        return test_data
    
    def generate_segmentation_test_data(self) -> List[Tuple[str, str]]:
        """生成分词测试数据"""
        test_data = []
        
        # 基础分词
        test_data.append(("基础分词", "我爱北京天安门"))
        
        # 专业术语
        test_data.append(("专业术语", "机器学习和深度学习是人工智能的重要分支"))
        
        # 人名地名
        test_data.append(("人名地名", "张三在北京大学学习"))
        
        # 新词和网络用语
        test_data.append(("网络用语", "这个AI模型真的很牛逼，YYDS！"))
        
        # 数字和英文混合
        test_data.append(("数字英文", "iPhone15的价格是5999元"))
        
        # 长句子
        test_data.append(("长句子", "随着人工智能技术的快速发展，机器学习和深度学习在图像识别、自然语言处理、语音识别等领域都取得了重大突破"))
        
        return test_data
    
    def generate_summary_test_data(self) -> List[Tuple[str, str, str]]:
        """生成文本摘要测试数据"""
        test_data = []
        
        # 新闻类文本
        news_text = """
        苹果公司今日发布了最新的iPhone 15系列手机，搭载了全新的A17芯片。
        这款手机在摄影功能方面有显著提升，支持4K视频录制和专业级照片编辑。
        新的芯片采用3纳米工艺制造，性能比上一代提升了20%，同时功耗降低了15%。
        苹果公司CEO表示，这是迄今为止最先进的iPhone产品。
        预计这款手机将在下个月正式上市，起售价为999美元。
        分析师认为，新iPhone将帮助苹果在竞争激烈的智能手机市场中保持领先地位。
        """
        test_data.append(("新闻文本", news_text.strip(), "苹果iPhone新品发布"))
        
        # 技术文档
        tech_text = """
        深度学习是机器学习的一个子领域，它基于人工神经网络进行学习和决策。
        深度学习模型通常包含多个隐藏层，每一层都能学习数据的不同特征。
        卷积神经网络（CNN）特别适用于图像处理任务，而循环神经网络（RNN）则擅长处理序列数据。
        近年来，Transformer架构的出现革命性地改变了自然语言处理领域。
        深度学习在计算机视觉、语音识别、自然语言处理等领域都取得了突破性进展。
        然而，深度学习模型通常需要大量的训练数据和计算资源。
        """
        test_data.append(("技术文档", tech_text.strip(), "深度学习技术概述"))
        
        # 学术论文摘要
        academic_text = """
        本研究提出了一种新的注意力机制，用于改进Transformer模型在长序列处理中的性能。
        传统的自注意力机制在处理长序列时存在计算复杂度过高的问题。
        我们的方法通过引入稀疏注意力模式，将计算复杂度从O(n²)降低到O(n log n)。
        实验结果表明，在多个自然语言处理任务上，我们的方法都取得了显著的性能提升。
        特别是在文档级别的机器翻译任务中，BLEU分数提高了3.2个点。
        这种方法为处理长序列的Transformer模型提供了一个有效的解决方案。
        """
        test_data.append(("学术论文", academic_text.strip(), "改进的Transformer注意力机制"))
        
        return test_data
    
    def generate_performance_test_data(self) -> Dict[str, str]:
        """生成性能测试数据"""
        test_data = {}
        
        # 小文本 (< 1000字符)
        small_text = "人工智能技术正在改变我们的生活。" * 20
        test_data["小文本"] = small_text
        
        # 中等文本 (1000-10000字符)
        medium_text = "随着科技的发展，人工智能在各个领域都有广泛应用，包括医疗、教育、金融等。" * 100
        test_data["中等文本"] = medium_text
        
        # 大文本 (10000-50000字符)
        large_text = "深度学习是机器学习的一个重要分支，它模拟人脑神经网络的工作原理。" * 500
        test_data["大文本"] = large_text
        
        # 超大文本 (50000-200000字符)
        very_large_text = "自然语言处理是人工智能领域的一个重要研究方向。" * 2000
        test_data["超大文本"] = very_large_text
        
        return test_data
    
    def generate_edge_case_data(self) -> List[Tuple[str, str]]:
        """生成边界情况测试数据"""
        edge_cases = []
        
        # 1. 只有标点符号
        edge_cases.append(("纯标点", "！@#￥%……&*（）"))
        
        # 2. 只有数字
        edge_cases.append(("纯数字", "1234567890"))
        
        # 3. 只有英文
        edge_cases.append(("纯英文", "Hello World This is a test"))
        
        # 4. 只有空格
        edge_cases.append(("纯空格", "     "))
        
        # 5. 重复字符
        edge_cases.append(("重复字符", "测试测试测试测试测试"))
        
        # 6. 单个长词
        edge_cases.append(("超长词", "人工智能机器学习深度学习自然语言处理计算机视觉"))
        
        # 7. 换行符和制表符
        edge_cases.append(("控制字符", "第一行\n第二行\t制表符"))
        
        # 8. Unicode特殊字符
        edge_cases.append(("Unicode", "αβγδε中文🌟💫⭐"))
        
        # 9. HTML标签（应该被处理为普通文本）
        edge_cases.append(("HTML标签", "<div>这是一个测试</div>"))
        
        # 10. 极短文本
        edge_cases.append(("极短文本", "测"))
        
        return edge_cases
    
    def save_test_data_to_files(self):
        """将测试数据保存到文件"""
        import json
        
        # 保存各类测试数据
        all_data = {
            "basic_samples": self.generate_basic_text_samples(),
            "sentiment_data": self.generate_sentiment_test_data(),
            "entity_data": self.generate_entity_test_data(),
            "segmentation_data": self.generate_segmentation_test_data(),
            "summary_data": self.generate_summary_test_data(),
            "performance_data": self.generate_performance_test_data(),
            "edge_cases": self.generate_edge_case_data()
        }
        
        with open('test/test_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print("测试数据已保存到 test/test_data.json")

if __name__ == "__main__":
    generator = TestDataGenerator()
    
    print("=== 测试数据生成器 ===\n")
    
    # 生成并显示各类测试数据
    print("1. 基础文本样本:")
    for name, text in generator.generate_basic_text_samples()[:5]:
        print(f"   {name}: {text[:50]}{'...' if len(text) > 50 else ''}")
    
    print("\n2. 情感分析测试数据:")
    for category, text, sentiment in generator.generate_sentiment_test_data()[:3]:
        print(f"   {category} ({sentiment}): {text[:50]}...")
    
    print("\n3. 实体识别测试数据:")
    for name, text, entities in generator.generate_entity_test_data()[:2]:
        entity_names = [e['text'] for e in entities]
        print(f"   {name}: {text}")
        print(f"   实体: {entity_names}")
    
    print("\n4. 边界情况测试数据:")
    for name, text in generator.generate_edge_case_data()[:5]:
        print(f"   {name}: {repr(text)}")
    
    # 保存所有测试数据
    generator.save_test_data_to_files()
