#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的Qwen3连接和摘要测试
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def test_qwen3_basic():
    """基础Qwen3测试"""
    print("=== Qwen3基础连接测试 ===\n")
    
    # 创建处理器
    processor = TextProcessor()
    
    # 检查连接状态
    if processor.qwen3_client:
        print("✓ Qwen3连接成功")
        print(f"✓ 模型: {processor.qwen3_model}")
        print(f"✓ API地址: {processor.qwen3_api_url}")
    else:
        print("✗ Qwen3连接失败")
        return False
    
    # 简单的摘要测试
    test_text = """
    人工智能是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    机器学习是人工智能的一个重要分支，它通过算法使计算机能够从数据中学习并做出决策或预测。
    深度学习作为机器学习的一个子集，使用神经网络来模拟人脑的工作方式。
    """
    
    processor.load_text(test_text)
    
    print("\n=== 摘要生成测试 ===")
    print(f"原文: {test_text.strip()}")
    print("-" * 60)
    
    try:
        # 测试Qwen3摘要
        summary = processor.generate_summary(num_sentences=2, method='qwen3', title='人工智能技术')
        print(f"Qwen3摘要: {summary}")
        print("✓ Qwen3摘要生成成功")
        return True
        
    except Exception as e:
        print(f"✗ Qwen3摘要生成失败: {e}")
        return False

def compare_methods():
    """对比不同摘要方法"""
    print("\n=== 摘要方法对比 ===\n")
    
    processor = TextProcessor()
    
    test_text = """
    苹果公司发布了最新的iPhone 15系列手机，搭载了全新的A17芯片。
    这款手机在摄影功能方面有显著提升，支持4K视频录制和专业级照片编辑。
    新的AI芯片为设备提供了更强大的本地计算能力，提升了用户体验。
    苹果公司的首席执行官表示，这项技术将彻底改变移动设备上的人工智能应用。
    投资者对苹果公司的未来发展前景保持乐观，股价在过去一年中上涨了25%。
    """
    
    processor.load_text(test_text)
    title = "苹果iPhone 15新品发布"
    
    methods = [
        ('hybrid', '混合方法'),
        ('textteaser', 'TextTeaser算法'),
        ('qwen3', 'Qwen3大模型')
    ]
    
    for method, name in methods:
        print(f"【{name}】")
        try:
            if method in ['textteaser', 'qwen3']:
                summary = processor.generate_summary(num_sentences=2, method=method, title=title)
            else:
                summary = processor.generate_summary(num_sentences=2, method=method)
            print(f"摘要: {summary}")
        except Exception as e:
            print(f"错误: {e}")
        print()

if __name__ == "__main__":
    # 运行基础测试
    if test_qwen3_basic():
        # 如果基础测试成功，运行对比测试
        compare_methods()
        print("=" * 60)
        print("✓ Qwen3集成测试完成！")
    else:
        print("请检查Qwen3服务状态：")
        print("1. 确保ollama服务在localhost:6006运行")
        print("2. 确保qwen3:8b模型已加载")
        print("3. 检查网络连接")
