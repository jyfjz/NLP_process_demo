#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证测试脚本
用于验证测试案例和场景分析文档测试脚本是否能正常运行
"""

import sys
import os
import time

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试导入是否正常"""
    print("🔍 测试模块导入...")
    
    try:
        from code_model.text_tools import TextProcessor
        print("✓ TextProcessor 导入成功")
        return True
    except ImportError as e:
        print(f"✗ TextProcessor 导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能是否可用"""
    print("\n🔍 测试基本功能...")
    
    try:
        from code_model.text_tools import TextProcessor
        
        processor = TextProcessor()
        test_text = "这是一个测试文本，用于验证基本功能。"
        
        # 测试文本加载
        processor.load_text(test_text)
        print("✓ 文本加载功能正常")
        
        # 测试统计功能
        stats = processor.get_text_stats()
        if stats and '字符数' in stats:
            print(f"✓ 文本统计功能正常 (字符数: {stats['字符数']})")
        else:
            print("⚠ 文本统计功能异常")
            return False
        
        # 测试分词功能
        try:
            words = processor.get_top_words(n=5)
            if words:
                print(f"✓ 分词功能正常 (找到 {len(words)} 个词)")
            else:
                print("⚠ 分词功能无结果")
        except Exception as e:
            print(f"⚠ 分词功能异常: {e}")
        
        # 测试情感分析
        try:
            sentiment = processor.analyze_sentiment()
            if sentiment and sentiment.get('available'):
                print(f"✓ 情感分析功能正常 (结果: {sentiment.get('sentiment', 'unknown')})")
            else:
                print("⚠ 情感分析功能不可用")
        except Exception as e:
            print(f"⚠ 情感分析功能异常: {e}")
        
        # 测试实体识别
        try:
            entities = processor.recognize_entities()
            if entities and entities.get('available'):
                print(f"✓ 实体识别功能正常 (找到 {len(entities.get('entities', []))} 个实体)")
            else:
                print("⚠ 实体识别功能不可用")
        except Exception as e:
            print(f"⚠ 实体识别功能异常: {e}")
        
        # 测试摘要功能
        try:
            summary = processor.generate_summary(num_sentences=1, method='frequency')
            if summary and len(summary.strip()) > 0:
                print("✓ 摘要功能正常")
            else:
                print("⚠ 摘要功能无结果")
        except Exception as e:
            print(f"⚠ 摘要功能异常: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def test_document_test_scripts():
    """测试文档测试脚本是否可以导入和运行"""
    print("\n🔍 测试文档测试脚本...")
    
    # 测试综合测试套件
    try:
        from comprehensive_test_suite import DocumentBasedTestSuite
        print("✓ 综合测试套件导入成功")
        
        # 创建实例但不运行完整测试
        test_suite = DocumentBasedTestSuite()
        print("✓ 综合测试套件实例化成功")
        
    except ImportError as e:
        print(f"⚠ 综合测试套件导入失败: {e}")
    except Exception as e:
        print(f"⚠ 综合测试套件异常: {e}")
    
    # 测试核心场景测试
    try:
        from document_scenario_tests import DocumentScenarioTests
        print("✓ 核心场景测试导入成功")
        
        # 创建实例但不运行完整测试
        scenario_tests = DocumentScenarioTests()
        print("✓ 核心场景测试实例化成功")
        
    except ImportError as e:
        print(f"⚠ 核心场景测试导入失败: {e}")
    except Exception as e:
        print(f"⚠ 核心场景测试异常: {e}")

def test_sample_scenario():
    """运行一个简单的测试场景"""
    print("\n🔍 运行示例测试场景...")
    
    try:
        from code_model.text_tools import TextProcessor
        
        processor = TextProcessor()
        test_text = "北京大学的人工智能研究院在机器学习领域取得了重要突破。这是一个积极的发展。"
        
        print(f"测试文本: {test_text}")
        
        # 加载文本
        start_time = time.time()
        processor.load_text(test_text)
        load_time = time.time() - start_time
        print(f"✓ 文本加载耗时: {load_time:.3f}s")
        
        # 文本统计
        start_time = time.time()
        stats = processor.get_text_stats()
        stats_time = time.time() - start_time
        print(f"✓ 文本统计耗时: {stats_time:.3f}s, 结果: {stats}")
        
        # 分词测试
        start_time = time.time()
        words = processor.get_top_words(n=5)
        words_time = time.time() - start_time
        print(f"✓ 分词耗时: {words_time:.3f}s, 前5个词: {[w[0] for w in words[:5]]}")
        
        # 情感分析测试
        start_time = time.time()
        sentiment = processor.analyze_sentiment()
        sentiment_time = time.time() - start_time
        if sentiment['available']:
            print(f"✓ 情感分析耗时: {sentiment_time:.3f}s, 结果: {sentiment['sentiment']}")
        else:
            print(f"⚠ 情感分析不可用")
        
        # 实体识别测试
        start_time = time.time()
        entities = processor.recognize_entities()
        entities_time = time.time() - start_time
        if entities['available']:
            entity_texts = [e['text'] for e in entities['entities']]
            print(f"✓ 实体识别耗时: {entities_time:.3f}s, 找到实体: {entity_texts}")
        else:
            print(f"⚠ 实体识别不可用")
        
        return True
        
    except Exception as e:
        print(f"✗ 示例测试场景失败: {e}")
        return False

def check_test_environment():
    """检查测试环境"""
    print("\n🔍 检查测试环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要的库
    required_libs = ['jieba', 'snownlp']
    optional_libs = ['stanza', 'spacy', 'textblob', 'vaderSentiment']
    
    print("\n必要库检查:")
    for lib in required_libs:
        try:
            __import__(lib)
            print(f"✓ {lib} 可用")
        except ImportError:
            print(f"✗ {lib} 不可用")
    
    print("\n可选库检查:")
    for lib in optional_libs:
        try:
            __import__(lib)
            print(f"✓ {lib} 可用")
        except ImportError:
            print(f"⚠ {lib} 不可用 (可选)")
    
    # 检查文件结构
    print("\n文件结构检查:")
    expected_files = [
        'code_model/text_tools.py',
        'code_model/stopwords.py',
        'test/comprehensive_test_suite.py',
        'test/document_scenario_tests.py'
    ]
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} 存在")
        else:
            print(f"✗ {file_path} 不存在")

def main():
    """主函数"""
    print("🚀 测试案例和场景分析文档 - 快速验证测试")
    print("="*60)
    
    all_passed = True
    
    # 检查测试环境
    check_test_environment()
    
    # 测试导入
    if not test_imports():
        all_passed = False
    
    # 测试基本功能
    if not test_basic_functionality():
        all_passed = False
    
    # 测试文档测试脚本
    test_document_test_scripts()
    
    # 运行示例场景
    if not test_sample_scenario():
        all_passed = False
    
    # 总结
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ 快速验证测试通过 - 系统基本功能正常")
        print("📋 可以运行完整的测试案例和场景分析文档测试")
        print("\n运行命令:")
        print("  python test/document_scenario_tests.py        # 核心场景测试")
        print("  python test/comprehensive_test_suite.py       # 完整测试套件")
    else:
        print("❌ 快速验证测试发现问题 - 请检查系统配置")
        print("💡 建议:")
        print("  1. 检查Python环境和依赖库")
        print("  2. 确认代码文件完整性")
        print("  3. 查看具体错误信息并修复")
    
    print(f"{'='*60}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
