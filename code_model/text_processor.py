#!/usr/bin/env python3
"""
文本处理和分析工具 - 主程序
提供交互式命令行界面
"""

import os
import sys
from code_model.text_tools import TextProcessor


class TextProcessorCLI:
    """命令行界面类"""
    
    def __init__(self):
        self.processor = TextProcessor()
        self.commands = {
            '1': self.load_text,
            '2': self.find_and_replace,
            '3': self.word_frequency,
            '4': self.generate_summary,
            '5': self.text_stats,
            '6': self.save_text,
            '7': self.reset_text,
            '0': self.exit_program
        }
    
    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*50)
        print("           文本处理和分析工具")
        print("="*50)
        print("1. 加载文本")
        print("2. 查找和替换")
        print("3. 词频统计")
        print("4. 生成摘要")
        print("5. 文本统计")
        print("6. 保存文本")
        print("7. 重置文本")
        print("0. 退出")
        print("-"*50)
    
    def load_text(self):
        """加载文本"""
        print("\n选择加载方式:")
        print("1. 从文件加载")
        print("2. 直接输入文本")
        
        choice = input("请选择 (1/2): ").strip()
        
        if choice == '1':
            file_path = input("请输入文件路径: ").strip()
            try:
                self.processor.load_from_file(file_path)
                print(f"✓ 成功加载文件: {file_path}")
                print(f"文本长度: {len(self.processor.text)} 字符")
            except Exception as e:
                print(f"✗ 加载失败: {e}")
        
        elif choice == '2':
            print("请输入文本 (输入 'END' 结束):")
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            
            text = '\n'.join(lines)
            self.processor.load_text(text)
            print(f"✓ 成功加载文本，长度: {len(text)} 字符")
        
        else:
            print("✗ 无效选择")
    
    def find_and_replace(self):
        """查找和替换功能"""
        if not self.processor.text:
            print("✗ 请先加载文本")
            return
        
        print("\n查找和替换")
        pattern = input("请输入要查找的文本/正则表达式: ")
        if not pattern:
            print("✗ 查找内容不能为空")
            return
        
        # 先显示匹配项
        use_regex = input("使用正则表达式? (y/n): ").lower() == 'y'
        case_sensitive = input("区分大小写? (y/n): ").lower() == 'y'
        
        try:
            matches = self.processor.find_matches(pattern, use_regex, case_sensitive)
            if matches:
                print(f"\n找到 {len(matches)} 个匹配项:")
                for i, (pos, match) in enumerate(matches[:10]):  # 只显示前10个
                    print(f"  {i+1}. 位置 {pos}: '{match}'")
                if len(matches) > 10:
                    print(f"  ... 还有 {len(matches)-10} 个匹配项")
                
                # 确认替换
                replacement = input("\n请输入替换文本: ")
                confirm = input(f"确认将 '{pattern}' 替换为 '{replacement}'? (y/n): ")
                
                if confirm.lower() == 'y':
                    new_text, count = self.processor.find_and_replace(
                        pattern, replacement, use_regex, case_sensitive)
                    print(f"✓ 成功替换 {count} 处")
                else:
                    print("取消替换")
            else:
                print("✗ 未找到匹配项")
        
        except Exception as e:
            print(f"✗ 错误: {e}")
    
    def word_frequency(self):
        """词频统计功能"""
        if not self.processor.text:
            print("✗ 请先加载文本")
            return
        
        print("\n词频统计设置:")
        ignore_case = input("忽略大小写? (y/n): ").lower() == 'y'
        min_length = input("最小词长 (默认1): ").strip()
        min_length = int(min_length) if min_length.isdigit() else 1
        
        try:
            top_words = self.processor.get_top_words(
                n=20, ignore_case=ignore_case, min_word_length=min_length)
            
            print(f"\n词频统计结果 (前20个):")
            print("-" * 30)
            for i, (word, freq) in enumerate(top_words, 1):
                print(f"{i:2d}. {word:<15} {freq:>5}")
            
            # 询问是否保存结果
            save_result = input("\n保存结果到文件? (y/n): ").lower() == 'y'
            if save_result:
                filename = input("输入文件名 (默认: word_frequency.txt): ").strip()
                if not filename:
                    filename = "word_frequency.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("词频统计结果\n")
                    f.write("=" * 30 + "\n")
                    for i, (word, freq) in enumerate(top_words, 1):
                        f.write(f"{i:2d}. {word:<15} {freq:>5}\n")
                
                print(f"✓ 结果已保存到 {filename}")
        
        except Exception as e:
            print(f"✗ 错误: {e}")
    
    def generate_summary(self):
        """生成摘要功能"""
        if not self.processor.text:
            print("✗ 请先加载文本")
            return
        
        print("\n摘要生成设置:")
        num_sentences = input("摘要句子数 (默认3): ").strip()
        num_sentences = int(num_sentences) if num_sentences.isdigit() else 3
        
        print("摘要方法:")
        print("1. 基于词频")
        print("2. 基于位置")
        print("3. 混合方法")
        print("4. TextTeaser算法")
        print("5. Qwen3大模型")

        method_choice = input("选择方法 (1/2/3/4/5): ").strip()
        method_map = {'1': 'frequency', '2': 'position', '3': 'hybrid', '4': 'textteaser', '5': 'qwen3'}
        method = method_map.get(method_choice, 'frequency')
        
        try:
            summary = self.processor.generate_summary(num_sentences, method)
            print(f"\n摘要 ({method} 方法):")
            print("-" * 50)
            print(summary)
            print("-" * 50)
            
            # 询问是否保存摘要
            save_summary = input("\n保存摘要到文件? (y/n): ").lower() == 'y'
            if save_summary:
                filename = input("输入文件名 (默认: summary.txt): ").strip()
                if not filename:
                    filename = "summary.txt"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"文本摘要 ({method} 方法)\n")
                    f.write("=" * 50 + "\n")
                    f.write(summary)
                
                print(f"✓ 摘要已保存到 {filename}")
        
        except Exception as e:
            print(f"✗ 错误: {e}")
    
    def text_stats(self):
        """显示文本统计信息"""
        if not self.processor.text:
            print("✗ 请先加载文本")
            return
        
        stats = self.processor.get_text_stats()
        print("\n文本统计信息:")
        print("-" * 20)
        for key, value in stats.items():
            print(f"{key}: {value}")
    
    def save_text(self):
        """保存当前文本"""
        if not self.processor.text:
            print("✗ 没有文本可保存")
            return
        
        filename = input("输入保存文件名: ").strip()
        if not filename:
            print("✗ 文件名不能为空")
            return
        
        try:
            self.processor.save_to_file(filename)
            print(f"✓ 文本已保存到 {filename}")
        except Exception as e:
            print(f"✗ 保存失败: {e}")
    
    def reset_text(self):
        """重置文本"""
        if not self.processor.original_text:
            print("✗ 没有原始文本可重置")
            return
        
        confirm = input("确认重置文本到原始状态? (y/n): ")
        if confirm.lower() == 'y':
            self.processor.reset_text()
            print("✓ 文本已重置")
        else:
            print("取消重置")
    
    def exit_program(self):
        """退出程序"""
        print("感谢使用文本处理工具！")
        sys.exit(0)
    
    def run(self):
        """运行主程序"""
        print("欢迎使用文本处理和分析工具！")
        
        while True:
            self.show_menu()
            choice = input("请选择功能 (0-7): ").strip()
            
            if choice in self.commands:
                try:
                    self.commands[choice]()
                except KeyboardInterrupt:
                    print("\n\n操作被中断")
                except Exception as e:
                    print(f"\n✗ 发生错误: {e}")
            else:
                print("✗ 无效选择，请重新输入")


def main():
    """主函数"""
    cli = TextProcessorCLI()
    cli.run()


if __name__ == "__main__":
    main()
