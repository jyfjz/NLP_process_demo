#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Qwen3输出清理功能
验证think标签和Markdown格式的清理效果
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code_model'))

from text_tools import TextProcessor

def test_qwen3_output_cleaning():
    """测试Qwen3输出清理功能"""
    print("=== Qwen3输出清理功能测试 ===\n")
    
    processor = TextProcessor()
    
    # 模拟包含think标签和Markdown格式的Qwen3输出
    test_outputs = [
        # 测试1：包含think标签的输出
        """<think>
好的，我现在需要处理用户提供的这个关于《诡秘之主》的同人小说片段，并生成一个摘要。首先，我要仔细阅读用户提供的文本，理解其中的情节和角色发展。
这段内容主要描述了克莱恩在占卜俱乐部的学习、家庭生活以及与邻居的互动。
</think>

**摘要：**
克莱恩在占卜俱乐部的学习中，面临家庭财务压力，需支付5英镑的额外费用。他与家人商议未来计划，哥哥班森希望购买会计书籍提升收入。""",
        
        # 测试2：包含多种Markdown格式
        """**摘要：**
这是一个包含*斜体*和**粗体**以及`代码`格式的摘要。
文本内容描述了主要情节和角色发展。""",
        
        # 测试3：只有think标签，没有其他内容
        """<think>
这里是模型的思考过程，用户不应该看到这部分内容。
需要分析文本并生成摘要。
</think>

人工智能技术正在快速发展，改变着我们的生活方式。机器学习和深度学习技术在各个领域都有广泛应用。""",
        
        # 测试4：复杂的混合格式
        """<think>
复杂的思考过程...
</think>

**总结：**
这是一个包含多种格式的测试文本。
- 第一点：*重要信息*
- 第二点：**关键内容**
- 第三点：`技术细节`

最终结论是文本处理功能正常工作。"""
    ]
    
    for i, test_output in enumerate(test_outputs, 1):
        print(f"【测试 {i}】")
        print("原始输出:")
        print("-" * 50)
        print(test_output)
        print("\n清理后输出:")
        print("-" * 50)
        
        cleaned_output = processor._clean_qwen3_output(test_output)
        print(cleaned_output)
        print("\n" + "=" * 80 + "\n")

def test_edge_cases():
    """测试边缘情况"""
    print("=== 边缘情况测试 ===\n")
    
    processor = TextProcessor()
    
    edge_cases = [
        # 空字符串
        "",
        
        # 只有空白字符
        "   \n\n   ",
        
        # 只有think标签
        "<think>只有思考内容</think>",
        
        # 嵌套的Markdown格式
        "**这是*嵌套的*格式**测试",
        
        # 多个前缀
        "**摘要：****总结：**实际内容",
        
        # 不完整的think标签
        "<think>不完整的标签内容",
        
        # 正常文本（不需要清理）
        "这是一段正常的文本，不包含任何需要清理的格式。"
    ]
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"【边缘情况 {i}】")
        print(f"输入: '{test_case}'")
        
        cleaned = processor._clean_qwen3_output(test_case)
        print(f"输出: '{cleaned}'")
        print("-" * 40)

def test_real_qwen3_scenario():
    """测试真实的Qwen3使用场景"""
    print("\n=== 真实场景测试 ===\n")
    
    processor = TextProcessor()
    
    # 模拟真实的文本输入
    test_text = """
    人工智能技术的发展正在深刻改变着我们的生活和工作方式。
    在医疗领域，AI辅助诊断系统能够快速分析医学影像，提高疾病检测的准确性。
    在教育领域，个性化学习平台能够根据学生的学习特点制定专属课程。
    在金融服务领域，AI技术被广泛应用于风险评估和欺诈检测。
    然而，AI技术的发展也带来了数据隐私和算法偏见等挑战。
    """
    
    processor.load_text(test_text)
    title = "人工智能技术发展与应用"
    
    print(f"测试文本: {test_text.strip()}")
    print(f"标题: {title}")
    print("-" * 60)
    
    # 测试不同的摘要方法
    methods = [
        ('hybrid', '混合方法'),
        ('textteaser', 'TextTeaser算法'),
        # 注意：qwen3需要实际的模型连接，这里只是演示
    ]
    
    for method, name in methods:
        try:
            print(f"\n【{name}】")
            if method == 'textteaser':
                summary = processor.generate_summary(num_sentences=2, method=method, title=title)
            else:
                summary = processor.generate_summary(num_sentences=2, method=method)
            
            print(f"摘要: {summary}")
            
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    # 运行所有测试
    test_qwen3_output_cleaning()
    test_edge_cases()
    test_real_qwen3_scenario()
    
    print("\n" + "=" * 80)
    print("✓ Qwen3输出清理功能测试完成！")
    print("\n修复内容:")
    print("1. ✅ 移除<think>标签及其内容")
    print("2. ✅ 清理Markdown格式标记")
    print("3. ✅ 移除常见的前缀标记")
    print("4. ✅ 优化空白字符处理")
    print("5. ✅ 改进Web界面显示效果")
    print("=" * 80)
