#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen3大模型摘要功能测试脚本
测试集成的Qwen3模型摘要效果
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def test_qwen3_connection():
    """测试Qwen3模型连接"""
    print("=== Qwen3模型连接测试 ===\n")
    
    processor = TextProcessor()
    
    # 检查Qwen3是否可用
    capabilities = processor.get_nlp_capabilities()
    
    if capabilities.get('qwen3_summary', False):
        print("✓ Qwen3模型连接成功")
        if hasattr(processor, 'qwen3_model'):
            print(f"✓ 使用模型: {processor.qwen3_model}")
        return True
    else:
        print("✗ Qwen3模型连接失败")
        print("请确保:")
        print("1. Ollama服务正在运行 (http://localhost:6006)")
        print("2. Qwen3模型已正确部署")
        return False

def test_qwen3_vs_other_methods():
    """对比Qwen3与其他摘要方法的效果"""
    print("\n=== Qwen3摘要效果对比测试 ===\n")
    
    processor = TextProcessor()
    
    # 测试文本：关于人工智能的技术文章
    test_text = """
    人工智能技术正在经历前所未有的快速发展，深刻改变着我们的生活和工作方式。
    
    在自然语言处理领域，大型语言模型如GPT、BERT和Qwen等的出现，使得机器能够更好地理解和生成人类语言。
    这些模型在文本摘要、机器翻译、问答系统等任务上表现出色，为各行各业带来了新的可能性。
    
    计算机视觉技术也取得了重大突破。深度学习算法在图像识别、目标检测、人脸识别等方面的准确率已经超越了人类水平。
    自动驾驶汽车、医疗影像诊断、智能监控系统等应用正在逐步走向实用化。
    
    在机器学习算法方面，强化学习、联邦学习、元学习等新兴技术不断涌现。
    这些技术使得AI系统能够在更复杂的环境中学习和适应，提高了模型的泛化能力和实用性。
    
    然而，人工智能的发展也面临着诸多挑战。数据隐私保护、算法公平性、模型可解释性等问题需要得到重视。
    此外，AI技术的快速发展也引发了对就业市场、社会结构等方面的担忧。
    
    展望未来，人工智能将继续在医疗健康、教育培训、金融服务、智能制造等领域发挥重要作用。
    我们需要在推动技术进步的同时，也要关注其社会影响，确保AI技术能够造福全人类。
    """
    
    processor.load_text(test_text)
    title = "人工智能技术发展现状与挑战"
    
    print(f"测试文本长度: {len(test_text)} 字符")
    print(f"标题: {title}")
    print("-" * 80)
    
    # 测试不同的摘要方法
    methods = [
        ('frequency', '基于词频'),
        ('hybrid', '混合方法'),
        ('textteaser', 'TextTeaser算法'),
        ('qwen3', 'Qwen3大模型')
    ]
    
    for method, method_name in methods:
        print(f"\n【{method_name}】")
        print("-" * 50)
        
        try:
            if method in ['textteaser', 'qwen3']:
                # 这些方法需要标题参数
                summary = processor.generate_summary(num_sentences=3, method=method, title=title)
            else:
                summary = processor.generate_summary(num_sentences=3, method=method)
            
            print(f"摘要: {summary}")
            print(f"长度: {len(summary)} 字符")
            
        except Exception as e:
            print(f"错误: {e}")
    
    print("\n" + "=" * 80)

def test_qwen3_different_lengths():
    """测试Qwen3在不同摘要长度下的表现"""
    print("\n=== Qwen3不同长度摘要测试 ===\n")
    
    processor = TextProcessor()
    
    # 较长的测试文本
    test_text = """
    区块链技术作为一种分布式账本技术，正在重塑数字经济的基础设施。
    
    比特币的成功证明了区块链技术的可行性，随后以太坊引入了智能合约概念，进一步扩展了区块链的应用场景。
    智能合约允许在区块链上执行自动化的协议，无需第三方中介，大大降低了交易成本和信任风险。
    
    去中心化金融（DeFi）是区块链技术最成功的应用之一。通过智能合约，用户可以进行借贷、交易、保险等金融服务，
    而无需传统银行或金融机构的参与。这种模式提高了金融服务的可及性和透明度。
    
    非同质化代币（NFT）为数字艺术品和收藏品创造了新的市场。艺术家可以通过NFT确保作品的唯一性和所有权，
    收藏者也能够验证和交易数字资产。这为创意产业带来了新的商业模式。
    
    在供应链管理方面，区块链技术提供了前所未有的透明度和可追溯性。
    从原材料采购到最终产品交付，每个环节都可以被记录在区块链上，消费者可以验证产品的真实性和来源。
    
    然而，区块链技术也面临着可扩展性、能耗和监管等挑战。
    目前大多数区块链网络的交易处理能力有限，高能耗的共识机制也引发了环保担忧。
    各国政府正在制定相关法规，以平衡创新发展和风险控制。
    
    未来，区块链技术有望在数字身份、投票系统、知识产权保护等更多领域发挥作用。
    随着技术的不断成熟和监管框架的完善，区块链将成为数字化转型的重要推动力。
    """
    
    processor.load_text(test_text)
    title = "区块链技术应用与发展前景"
    
    # 测试不同的摘要长度
    sentence_counts = [1, 2, 3, 5]
    
    for count in sentence_counts:
        print(f"\n【{count}句摘要】")
        print("-" * 40)
        
        try:
            summary = processor.generate_summary(num_sentences=count, method='qwen3', title=title)
            print(f"摘要: {summary}")
            print(f"长度: {len(summary)} 字符")
            
        except Exception as e:
            print(f"错误: {e}")

def test_qwen3_title_sensitivity():
    """测试Qwen3对不同标题的敏感性"""
    print("\n=== Qwen3标题敏感性测试 ===\n")
    
    processor = TextProcessor()
    
    # 包含多个主题的文本
    test_text = """
    苹果公司在最新的财报中显示，iPhone销量持续增长，特别是在中国市场表现强劲。
    公司的服务业务收入也创下新高，包括App Store、iCloud和Apple Music等服务。
    
    与此同时，苹果公司在人工智能领域加大投入，推出了更智能的Siri助手和机器学习功能。
    新的AI芯片为设备提供了更强大的本地计算能力，提升了用户体验。
    
    在环保方面，苹果公司承诺到2030年实现碳中和，并在产品设计中使用更多可回收材料。
    公司还投资了多个可再生能源项目，以减少其运营对环境的影响。
    
    投资者对苹果公司的未来发展前景保持乐观，股价在过去一年中上涨了25%。
    分析师认为，苹果在高端智能手机市场的领导地位将继续巩固。
    """
    
    processor.load_text(test_text)
    
    # 测试不同焦点的标题
    titles = [
        "苹果公司财务业绩分析",
        "苹果AI技术发展战略", 
        "苹果环保可持续发展",
        "苹果股价投资价值"
    ]
    
    for title in titles:
        print(f"\n标题: {title}")
        print("-" * 50)
        
        try:
            summary = processor.generate_summary(num_sentences=2, method='qwen3', title=title)
            print(f"摘要: {summary}")
            
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    # 首先测试连接
    if test_qwen3_connection():
        # 如果连接成功，运行其他测试
        test_qwen3_vs_other_methods()
        test_qwen3_different_lengths()
        test_qwen3_title_sensitivity()
        
        print("\n" + "=" * 80)
        print("✓ Qwen3摘要功能测试完成！")
        print("\nQwen3大模型摘要的优势:")
        print("1. 语义理解能力强 - 能够深度理解文本含义")
        print("2. 上下文感知 - 考虑全文语境生成摘要")
        print("3. 标题导向 - 能够根据标题调整摘要重点")
        print("4. 语言流畅性 - 生成的摘要更加自然流畅")
        print("5. 智能筛选 - 自动识别和提取关键信息")
        print("=" * 80)
    else:
        print("\n请检查Qwen3模型部署状态后重试。")
