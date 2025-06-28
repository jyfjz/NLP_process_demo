#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的摘要方法演示脚本
展示所有可用的摘要算法效果对比
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def demo_comprehensive_comparison():
    """全面的摘要方法对比演示"""
    print("=" * 80)
    print("文本摘要算法全面对比演示")
    print("=" * 80)
    
    processor = TextProcessor()
    
    # 测试文本：科技新闻
    test_text = """
    OpenAI公司最新发布的GPT-4模型在多项基准测试中表现出色，展现了前所未有的语言理解和生成能力。
    该模型在数学推理、代码编写、创意写作等任务上都有显著提升，准确率比前一代模型提高了30%以上。
    
    与此同时，谷歌公司也推出了竞争性的Bard模型，该模型专注于对话交互和实时信息检索。
    Bard模型集成了谷歌搜索引擎的强大功能，能够提供最新的信息和数据支持。
    
    微软公司则将GPT技术深度集成到Office套件中，推出了Copilot助手功能。
    用户可以通过自然语言指令完成文档编辑、数据分析、演示制作等复杂任务。
    
    业界专家认为，这些技术进步标志着人工智能进入了一个新的发展阶段。
    大型语言模型的能力边界不断扩展，将在教育、医疗、法律等专业领域发挥重要作用。
    
    然而，随着AI能力的增强，数据安全、隐私保护、算法偏见等问题也日益突出。
    各国政府和国际组织正在制定相关法规，以确保AI技术的安全和负责任发展。
    """
    
    processor.load_text(test_text)
    title = "大型语言模型技术突破与挑战"
    
    print(f"测试文本: {len(test_text)} 字符")
    print(f"标题: {title}")
    print("\n" + "=" * 80)
    
    # 所有可用的摘要方法
    methods = [
        ('frequency', '基于词频算法', '统计词汇出现频率，选择包含高频词的句子'),
        ('position', '基于位置算法', '根据句子在文本中的位置进行评分'),
        ('hybrid', '混合方法算法', '结合词频和位置权重的传统方法'),
        ('textteaser', 'TextTeaser算法', '模拟TextTeaser的多特征评分方法'),
        ('qwen3', 'Qwen3大模型', '基于大型语言模型的智能摘要')
    ]
    
    for method, name, description in methods:
        print(f"\n【{name}】")
        print(f"算法描述: {description}")
        print("-" * 60)
        
        try:
            if method in ['textteaser', 'qwen3']:
                summary = processor.generate_summary(num_sentences=3, method=method, title=title)
            else:
                summary = processor.generate_summary(num_sentences=3, method=method)
            
            print(f"摘要结果: {summary}")
            print(f"摘要长度: {len(summary)} 字符")
            
            # 简单的质量评估
            sentences = summary.split('.')
            actual_sentences = len([s for s in sentences if s.strip()])
            print(f"实际句数: {actual_sentences}")
            
        except Exception as e:
            print(f"生成失败: {e}")
        
        print()

def demo_different_domains():
    """不同领域文本的摘要效果"""
    print("\n" + "=" * 80)
    print("不同领域文本摘要效果演示")
    print("=" * 80)
    
    processor = TextProcessor()
    
    # 测试不同领域的文本
    test_cases = [
        {
            "domain": "医疗健康",
            "title": "新冠疫苗研发进展",
            "text": """
            新冠疫苗的研发取得了重大突破，多款疫苗已通过临床试验并获得批准。
            mRNA疫苗技术展现出了前所未有的有效性，保护率达到95%以上。
            辉瑞、莫德纳等公司的疫苗已在全球范围内大规模接种。
            中国的科兴、国药疫苗也在国际市场上发挥重要作用。
            疫苗接种大大降低了重症和死亡率，为疫情防控提供了有力工具。
            """
        },
        {
            "domain": "经济金融", 
            "title": "数字货币发展趋势",
            "text": """
            央行数字货币（CBDC）正在全球范围内加速发展，多国央行启动试点项目。
            中国的数字人民币已在多个城市进行大规模测试，应用场景不断扩展。
            欧洲央行也在积极研究数字欧元的可行性和实施方案。
            数字货币有望提高支付效率，降低交易成本，增强金融包容性。
            然而，隐私保护、网络安全、货币政策传导等问题仍需深入研究。
            """
        }
    ]
    
    for case in test_cases:
        print(f"\n【{case['domain']}领域】")
        print(f"标题: {case['title']}")
        print("-" * 50)
        
        processor.load_text(case['text'])
        
        # 对比传统方法和Qwen3
        methods = [('hybrid', '传统混合方法'), ('qwen3', 'Qwen3大模型')]
        
        for method, name in methods:
            try:
                summary = processor.generate_summary(num_sentences=2, method=method, title=case['title'])
                print(f"{name}: {summary}")
            except Exception as e:
                print(f"{name}: 生成失败 - {e}")
        print()

def demo_length_comparison():
    """不同摘要长度的效果对比"""
    print("\n" + "=" * 80)
    print("不同摘要长度效果对比")
    print("=" * 80)
    
    processor = TextProcessor()
    
    # 较长的测试文本
    long_text = """
    人工智能技术的快速发展正在深刻改变着各行各业的运作模式和发展轨迹。
    在医疗领域，AI辅助诊断系统能够快速分析医学影像，提高疾病检测的准确性和效率。
    机器学习算法在药物研发中也发挥重要作用，大大缩短了新药开发周期。
    
    教育行业同样受益于AI技术的进步，个性化学习平台能够根据学生的学习特点制定专属课程。
    智能教学助手可以实时回答学生问题，提供24小时的学习支持。
    自动批改系统不仅提高了教师的工作效率，还能提供详细的学习分析报告。
    
    在金融服务领域，AI技术被广泛应用于风险评估、欺诈检测和投资决策。
    智能客服系统能够处理大量客户咨询，提供准确快速的服务响应。
    算法交易系统通过分析市场数据，实现高频交易和风险管理。
    
    制造业也在积极拥抱AI技术，智能工厂通过机器视觉和预测性维护提高生产效率。
    供应链优化算法能够实时调整生产计划，降低库存成本和交付风险。
    质量检测系统使用深度学习技术，实现产品缺陷的自动识别和分类。
    """
    
    processor.load_text(long_text)
    title = "人工智能在各行业的应用"
    
    # 测试不同的摘要长度
    lengths = [1, 2, 3, 5]
    
    for length in lengths:
        print(f"\n【{length}句摘要对比】")
        print("-" * 40)
        
        methods = [('hybrid', '传统方法'), ('qwen3', 'Qwen3模型')]
        
        for method, name in methods:
            try:
                summary = processor.generate_summary(num_sentences=length, method=method, title=title)
                print(f"{name}: {summary}")
            except Exception as e:
                print(f"{name}: 生成失败 - {e}")
        print()

if __name__ == "__main__":
    # 运行所有演示
    demo_comprehensive_comparison()
    demo_different_domains()
    demo_length_comparison()
    
    print("\n" + "=" * 80)
    print("✓ 摘要算法演示完成！")
    print("\n总结:")
    print("1. 传统算法 - 快速、稳定，适合简单文本")
    print("2. TextTeaser - 多特征融合，平衡性好")
    print("3. Qwen3大模型 - 语义理解深度，效果最佳")
    print("\n建议:")
    print("• 日常使用: 混合方法或TextTeaser")
    print("• 高质量要求: Qwen3大模型")
    print("• 大批量处理: 传统算法")
    print("=" * 80)
