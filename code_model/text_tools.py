"""
文本处理工具类
包含查找替换、词频统计、文本摘要等核心功能
"""

import re
import string
import os
from collections import Counter
from typing import List, Dict, Tuple, Optional

# 高级自然语言处理库
try:
    import spacy
    SPACY_AVAILABLE = True
except (ImportError, ValueError) as e:
    SPACY_AVAILABLE = False
    print(f"spaCy不可用: {e}")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except (ImportError, ValueError) as e:
    TEXTBLOB_AVAILABLE = False
    print(f"TextBlob不可用: {e}")

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except (ImportError, ValueError) as e:
    VADER_AVAILABLE = False
    print(f"VADER不可用: {e}")

try:
    import stanza
    STANZA_AVAILABLE = True
except (ImportError, ValueError) as e:
    STANZA_AVAILABLE = False
    print(f"Stanza不可用: {e}")

# 深度学习情感分析库
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except (ImportError, ValueError) as e:
    TRANSFORMERS_AVAILABLE = False
    print(f"Transformers不可用: {e}")

try:
    from snownlp import SnowNLP
    SNOWNLP_AVAILABLE = True
except (ImportError, ValueError) as e:
    SNOWNLP_AVAILABLE = False
    print(f"SnowNLP不可用: {e}")

# 中文分词库
try:
    import jieba
    import jieba.posseg as pseg
    JIEBA_AVAILABLE = True
except (ImportError, ValueError) as e:
    JIEBA_AVAILABLE = False
    print(f"jieba不可用: {e}")

try:
    import pkuseg
    PKUSEG_AVAILABLE = True
    print("✓ pkuseg可用")
except (ImportError, ValueError) as e:
    PKUSEG_AVAILABLE = False
    print(f"pkuseg不可用: {e}")

try:
    import thulac
    THULAC_AVAILABLE = True
    print("✓ thulac可用")
except (ImportError, ValueError) as e:
    THULAC_AVAILABLE = False
    print(f"thulac不可用: {e}")

# TextTeaser摘要库（由于依赖问题，我们实现自己的轻量级版本）
# try:
#     from textteaser import TextTeaser
#     TEXTTEASER_AVAILABLE = True
#     print("✓ TextTeaser可用")
# except (ImportError, ValueError) as e:
#     TEXTTEASER_AVAILABLE = False
#     print(f"TextTeaser不可用: {e}")

# 我们实现自己的TextTeaser风格算法
TEXTTEASER_AVAILABLE = True
print("✓ 轻量级TextTeaser算法可用")

# Qwen3大模型摘要
try:
    import requests
    import json
    QWEN3_AVAILABLE = True
    print("✓ Requests库可用，支持Qwen3摘要")
except (ImportError, ValueError) as e:
    QWEN3_AVAILABLE = False
    print(f"Requests库不可用: {e}")

# 导入停用词管理器
try:
    from .stopwords import StopwordsManager
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    try:
        from stopwords import StopwordsManager
    except ImportError:
        print("停用词管理器不可用，将使用基础功能")


class TextProcessor:
    """文本处理器主类"""
    
    def __init__(self):
        self.text = ""
        self.original_text = ""

        # 初始化停用词管理器
        try:
            self.stopwords_manager = StopwordsManager()
        except NameError:
            self.stopwords_manager = None
            print("停用词管理器初始化失败，将不使用停用词过滤")

        # 初始化NLP模型和分词器
        self.nlp_models = {}
        self.segmenters = {}
        self._init_nlp_models()
        self._init_segmenters()

        # 初始化TextTeaser
        self.textteaser = None
        self._init_textteaser()

        # 初始化Qwen3客户端
        self.qwen3_client = None
        self._init_qwen3()


    
    def load_text(self, text: str) -> None:
        """加载文本"""
        self.text = text
        self.original_text = text
    
    def load_from_file(self, file_path: str, encoding: str = 'utf-8') -> None:
        """从文件加载文本"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                self.load_text(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"文件 {file_path} 不存在")
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"无法使用 {encoding} 编码读取文件")
    
    def save_to_file(self, file_path: str, encoding: str = 'utf-8') -> None:
        """保存文本到文件"""
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(self.text)
    
    def find_and_replace(self, pattern: str, replacement: str, 
                        use_regex: bool = False, case_sensitive: bool = True) -> Tuple[str, int]:
        """
        查找和替换文本
        
        Args:
            pattern: 要查找的模式
            replacement: 替换文本
            use_regex: 是否使用正则表达式
            case_sensitive: 是否区分大小写
            
        Returns:
            (替换后的文本, 替换次数)
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        
        if use_regex:
            try:
                new_text, count = re.subn(pattern, replacement, self.text, flags=flags)
            except re.error as e:
                raise ValueError(f"正则表达式错误: {e}")
        else:
            # 转义特殊字符用于字面匹配
            escaped_pattern = re.escape(pattern)
            new_text, count = re.subn(escaped_pattern, replacement, self.text, flags=flags)
        
        self.text = new_text
        return new_text, count
    
    def find_matches(self, pattern: str, use_regex: bool = False, 
                    case_sensitive: bool = True) -> List[Tuple[int, str]]:
        """
        查找所有匹配项
        
        Returns:
            [(位置, 匹配文本), ...]
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        
        if use_regex:
            try:
                matches = [(m.start(), m.group()) for m in re.finditer(pattern, self.text, flags=flags)]
            except re.error as e:
                raise ValueError(f"正则表达式错误: {e}")
        else:
            escaped_pattern = re.escape(pattern)
            matches = [(m.start(), m.group()) for m in re.finditer(escaped_pattern, self.text, flags=flags)]
        
        return matches
    
    def word_frequency(self, ignore_case: bool = True,
                      min_word_length: int = 1,
                      exclude_punctuation: bool = True,
                      segmentation_method: str = 'auto',
                      exclude_stopwords: bool = True,
                      exclude_numbers: bool = True,
                      exclude_single_chars: bool = True) -> Dict[str, int]:
        """
        统计词频（使用智能分词）

        Args:
            ignore_case: 是否忽略大小写
            min_word_length: 最小词长
            exclude_punctuation: 是否排除标点符号
            segmentation_method: 分词方法 ('auto', 'jieba', 'pkuseg', 'thulac', 'basic')
            exclude_stopwords: 是否排除停用词
            exclude_numbers: 是否排除纯数字
            exclude_single_chars: 是否排除单字符

        Returns:
            {词: 频率}
        """
        if not self.text.strip():
            return {}
        text = self.text

        if ignore_case:
            text = text.lower()

        # 移除标点符号和换行符，替换为空格
        if exclude_punctuation:
            # 中文标点符号
            chinese_punctuation = '，。！？；：""''（）【】《》、“”……'
            # 英文标点符号
            english_punctuation = string.punctuation
            all_punctuation = chinese_punctuation + english_punctuation

            # 将标点符号替换为空格，而不是直接删除
            for punct in all_punctuation:
                text = text.replace(punct, ' ')

        # 将换行符也替换为空格
        text = text.replace('\n', ' ').replace('\r', ' ')

        # 使用智能分词替代简单分割
        segments = self.segment_text(
            text=text,
            method=segmentation_method,
            mode='accurate',
            with_pos=False
        )

        # 提取词汇
        words = [seg['word'] for seg in segments]

        # 过滤标点符号（如果需要）
        if exclude_punctuation:
            # 中文标点符号
            chinese_punctuation = '，。！？；：""''（）【】《》、""……'
            # 英文标点符号
            english_punctuation = string.punctuation
            all_punctuation = chinese_punctuation + english_punctuation

            # 过滤纯标点符号的词
            words = [word for word in words if not all(c in all_punctuation for c in word)]

        # 过滤短词和空词
        words = [word for word in words if word.strip() and len(word) >= min_word_length]

        # 过滤纯数字
        if exclude_numbers:
            words = [word for word in words if not word.isdigit()]

        # 过滤单字符（如果启用）
        if exclude_single_chars:
            words = [word for word in words if len(word) > 1]

        # 过滤停用词
        if exclude_stopwords and self.stopwords_manager:
            words = self.stopwords_manager.filter_stopwords(words)

        # 统计频率
        word_count = Counter(words)

        return dict(word_count)
    
    def get_top_words(self, n: int = 10, **kwargs) -> List[Tuple[str, int]]:
        """获取出现频率最高的n个词"""
        word_freq = self.word_frequency(**kwargs)
        return Counter(word_freq).most_common(n)
    
    def generate_summary(self, num_sentences: int = 3,
                        method: str = 'frequency', title: str = '') -> str:
        """
        生成文本摘要

        Args:
            num_sentences: 摘要句子数
            method: 摘要方法 ('frequency', 'position', 'hybrid', 'textteaser', 'qwen3')
            title: 文本标题（TextTeaser和Qwen3需要）

        Returns:
            摘要文本
        """
        sentences = self._split_sentences(self.text)

        if len(sentences) <= num_sentences:
            return self.text

        if method == 'frequency':
            return self._frequency_based_summary(sentences, num_sentences)
        elif method == 'position':
            return self._position_based_summary(sentences, num_sentences)
        elif method == 'hybrid':
            return self._hybrid_summary(sentences, num_sentences)
        elif method == 'textteaser':
            return self._textteaser_summary(title, num_sentences)
        elif method == 'qwen3':
            return self._qwen3_summary(title, num_sentences)
        else:
            raise ValueError(f"未知的摘要方法: {method}")
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        # 改进的句子分割（支持中文标点符号）
        # 按段落分割，然后按句子分割
        paragraphs = text.split('\n\n')
        sentences = []

        for paragraph in paragraphs:
            if paragraph.strip():
                # 按中文和英文句号分割
                para_sentences = re.split(r'[。！？.!?]+', paragraph)
                for sent in para_sentences:
                    sent = sent.strip()
                    if sent and len(sent) > 5:  # 过滤太短的句子
                        sentences.append(sent)

        return sentences
    
    def _frequency_based_summary(self, sentences: List[str], num_sentences: int) -> str:
        """基于词频的摘要"""
        # 计算词频
        word_freq = self.word_frequency(ignore_case=True, exclude_punctuation=True)
        
        # 计算句子得分
        sentence_scores = []
        for sentence in sentences:
            words = sentence.lower().translate(str.maketrans('', '', string.punctuation)).split()
            score = sum(word_freq.get(word, 0) for word in words)
            sentence_scores.append((score, sentence))
        
        # 选择得分最高的句子
        sentence_scores.sort(reverse=True)
        top_sentences = [sent for _, sent in sentence_scores[:num_sentences]]
        
        return '. '.join(top_sentences) + '.'
    
    def _position_based_summary(self, sentences: List[str], num_sentences: int) -> str:
        """基于位置的摘要（选择开头、中间、结尾的句子）"""
        total = len(sentences)
        indices = []
        
        if num_sentences >= 1:
            indices.append(0)  # 第一句
        if num_sentences >= 2:
            indices.append(total - 1)  # 最后一句
        if num_sentences >= 3:
            indices.append(total // 2)  # 中间句子
        
        # 如果需要更多句子，均匀分布
        while len(indices) < num_sentences and len(indices) < total:
            for i in range(1, total - 1):
                if i not in indices:
                    indices.append(i)
                    if len(indices) >= num_sentences:
                        break
        
        indices.sort()
        selected_sentences = [sentences[i] for i in indices]
        return '. '.join(selected_sentences) + '.'
    
    def _hybrid_summary(self, sentences: List[str], num_sentences: int) -> str:
        """混合方法摘要"""
        # 结合词频和位置权重
        word_freq = self.word_frequency(ignore_case=True, exclude_punctuation=True)
        total_sentences = len(sentences)
        
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            words = sentence.lower().translate(str.maketrans('', '', string.punctuation)).split()
            freq_score = sum(word_freq.get(word, 0) for word in words)
            
            # 位置权重：开头和结尾句子权重更高
            if i == 0 or i == total_sentences - 1:
                position_weight = 1.5
            elif i < total_sentences * 0.2 or i > total_sentences * 0.8:
                position_weight = 1.2
            else:
                position_weight = 1.0
            
            final_score = freq_score * position_weight
            sentence_scores.append((final_score, sentence))
        
        sentence_scores.sort(reverse=True)
        top_sentences = [sent for _, sent in sentence_scores[:num_sentences]]
        
        return '. '.join(top_sentences) + '.'

    def _textteaser_summary(self, title: str = '', num_sentences: int = 3) -> str:
        """使用TextTeaser风格算法生成摘要"""
        if not self.textteaser:
            # 如果TextTeaser不可用，降级到混合方法
            print("TextTeaser不可用，使用混合方法替代")
            return self._hybrid_summary(self._split_sentences(self.text), num_sentences)

        try:
            sentences = self._split_sentences(self.text)

            if len(sentences) <= num_sentences:
                return self.text

            # 如果没有提供标题，尝试从文本第一句提取
            if not title:
                if sentences:
                    title = sentences[0][:50] + "..." if len(sentences[0]) > 50 else sentences[0]
                else:
                    title = "文本摘要"

            # 使用TextTeaser风格的评分算法
            sentence_scores = self._calculate_textteaser_scores(sentences, title)

            # 选择得分最高的句子
            sentence_scores.sort(reverse=True)
            top_sentences = [sent for _, sent in sentence_scores[:num_sentences]]

            return '. '.join(top_sentences) + '.'

        except Exception as e:
            print(f"TextTeaser摘要生成失败: {e}")
            # 降级到混合方法
            return self._hybrid_summary(self._split_sentences(self.text), num_sentences)

    def _calculate_textteaser_scores(self, sentences: List[str], title: str) -> List[Tuple[float, str]]:
        """
        计算TextTeaser风格的句子评分

        基于以下特征：
        1. 标题相似度 (Title Similarity)
        2. 句子位置 (Sentence Position)
        3. 句子长度 (Sentence Length)
        4. 关键词频率 (Keyword Frequency)
        """
        sentence_scores = []
        total_sentences = len(sentences)

        # 计算词频用于关键词评分
        word_freq = self.word_frequency(ignore_case=True, exclude_punctuation=True)

        # 预处理标题，提取关键词
        title_words = self._extract_keywords(title.lower())

        for i, sentence in enumerate(sentences):
            # 1. 标题相似度评分 (0-1)
            title_score = self._calculate_title_similarity(sentence.lower(), title_words)

            # 2. 位置评分 (0-1)
            position_score = self._calculate_position_score(i, total_sentences)

            # 3. 长度评分 (0-1)
            length_score = self._calculate_length_score(sentence)

            # 4. 关键词频率评分 (0-1)
            keyword_score = self._calculate_keyword_score(sentence, word_freq)

            # TextTeaser风格的综合评分
            # 各特征权重：标题相似度(40%), 位置(20%), 长度(15%), 关键词(25%)
            # 提高标题相似度的权重，使其对摘要结果影响更大
            final_score = (
                title_score * 0.40 +
                position_score * 0.20 +
                length_score * 0.15 +
                keyword_score * 0.25
            )

            sentence_scores.append((final_score, sentence))

        return sentence_scores

    def _extract_keywords(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        # 移除标点符号
        import string
        text = text.translate(str.maketrans('', '', string.punctuation))

        # 分词
        words = text.split()

        # 过滤停用词（如果可用）
        if self.stopwords_manager:
            words = self.stopwords_manager.filter_stopwords(words)

        # 过滤短词
        words = [word for word in words if len(word) > 2]

        return words

    def _calculate_title_similarity(self, sentence: str, title_words: List[str]) -> float:
        """计算句子与标题的相似度"""
        if not title_words:
            return 0.0

        sentence_words = self._extract_keywords(sentence)
        if not sentence_words:
            return 0.0

        # 计算交集
        common_words = set(sentence_words) & set(title_words)

        if not common_words:
            return 0.0

        # 改进的相似度计算：结合Jaccard相似度和词汇覆盖率
        jaccard_similarity = len(common_words) / len(set(sentence_words) | set(title_words))
        title_coverage = len(common_words) / len(title_words)  # 标题词汇覆盖率
        sentence_coverage = len(common_words) / len(sentence_words)  # 句子词汇覆盖率

        # 综合评分：Jaccard相似度(40%) + 标题覆盖率(40%) + 句子覆盖率(20%)
        similarity = (jaccard_similarity * 0.4 + title_coverage * 0.4 + sentence_coverage * 0.2)

        # 如果有多个匹配词，给予额外奖励
        if len(common_words) > 1:
            similarity *= 1.2

        return min(similarity, 1.0)

    def _calculate_position_score(self, position: int, total_sentences: int) -> float:
        """计算位置评分"""
        if total_sentences <= 1:
            return 1.0

        # TextTeaser风格：开头和结尾句子得分更高
        relative_position = position / (total_sentences - 1)

        if position == 0:  # 第一句
            return 1.0
        elif position == total_sentences - 1:  # 最后一句
            return 0.8
        elif relative_position <= 0.1:  # 前10%
            return 0.9
        elif relative_position >= 0.9:  # 后10%
            return 0.7
        else:  # 中间部分
            return 0.3

    def _calculate_length_score(self, sentence: str) -> float:
        """计算长度评分"""
        words = sentence.split()
        word_count = len(words)

        # TextTeaser风格：理想长度为15-25个词
        if 15 <= word_count <= 25:
            return 1.0
        elif 10 <= word_count <= 30:
            return 0.8
        elif 5 <= word_count <= 35:
            return 0.6
        elif word_count < 5:
            return 0.2  # 太短
        else:
            return 0.4  # 太长

    def _calculate_keyword_score(self, sentence: str, word_freq: Dict[str, int]) -> float:
        """计算关键词评分"""
        if not word_freq:
            return 0.0

        sentence_words = self._extract_keywords(sentence.lower())
        if not sentence_words:
            return 0.0

        # 计算句子中高频词的密度
        total_freq = sum(word_freq.values())
        sentence_freq_sum = sum(word_freq.get(word, 0) for word in sentence_words)

        if total_freq == 0:
            return 0.0

        # 归一化评分
        score = (sentence_freq_sum / total_freq) * len(sentence_words)
        return min(score, 1.0)

    def _qwen3_summary(self, title: str = '', num_sentences: int = 3) -> str:
        """使用Qwen3大模型生成摘要"""
        if not self.qwen3_client:
            # 如果Qwen3不可用，降级到TextTeaser方法
            print("Qwen3模型不可用，使用TextTeaser方法替代")
            return self._textteaser_summary(title, num_sentences)

        try:
            # 构建提示词
            if title:
                content = f"""请为以下文本生成摘要，要求：
1. 摘要应该包含{num_sentences}个句子
2. 摘要应该围绕标题"{title}"的主题
3. 摘要应该准确概括文本的核心内容
4. 使用简洁明了的语言
5. 直接输出摘要内容，不要添加额外说明

文本内容：
{self.text}

摘要："""
            else:
                content = f"""请为以下文本生成摘要，要求：
1. 摘要应该包含{num_sentences}个句子
2. 摘要应该准确概括文本的核心内容
3. 使用简洁明了的语言
4. 直接输出摘要内容，不要添加额外说明

文本内容：
{self.text}

摘要："""

            # 构建请求数据
            data = {
                "model": self.qwen3_model,
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "stream": False
            }

            # 调用Qwen3模型API
            headers = {'Content-type': 'application/json'}
            response = requests.post(self.qwen3_api_url,
                                   data=json.dumps(data),
                                   headers=headers,
                                   timeout=60)

            if response.status_code == 200:
                response_data = response.json()
                summary = response_data["message"]["content"].strip()

                # 高级后处理：清理Qwen3输出
                summary = self._clean_qwen3_output(summary)

                return summary
            else:
                print(f"Qwen3 API请求失败，状态码: {response.status_code}")
                return self._textteaser_summary(title, num_sentences)

        except Exception as e:
            print(f"Qwen3摘要生成失败: {e}")
            # 降级到TextTeaser方法
            return self._textteaser_summary(title, num_sentences)

    def _clean_qwen3_output(self, text: str) -> str:
        """清理Qwen3模型输出，移除think标签和格式化内容"""
        import re

        # 移除<think>...</think>标签及其内容
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

        # 移除可能的前缀标记
        prefixes_to_remove = [
            '摘要：', '**摘要：**', '**摘要**：',
            '总结：', '**总结：**', '**总结**：',
            '概要：', '**概要：**', '**概要**：'
        ]

        for prefix in prefixes_to_remove:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
                break

        # 移除Markdown格式标记
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # 移除粗体标记
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # 移除斜体标记
        text = re.sub(r'`(.*?)`', r'\1', text)        # 移除代码标记

        # 移除多余的换行和空格
        text = re.sub(r'\n\s*\n', '\n', text)  # 移除多余的空行
        text = re.sub(r'^\s+|\s+$', '', text)  # 移除首尾空白

        # 确保句子之间有适当的分隔
        text = re.sub(r'([。！？])\s*([^。！？\s])', r'\1 \2', text)

        return text.strip()
    
    def reset_text(self) -> None:
        """重置文本到原始状态"""
        self.text = self.original_text
    
    def get_text_stats(self) -> Dict[str, int]:
        """获取文本统计信息"""
        return {
            '字符数': len(self.text),
            '词数': len(self.text.split()),
            '句子数': len(self._split_sentences(self.text)),
            '段落数': len([p for p in self.text.split('\n\n') if p.strip()])
        }

    def add_custom_stopwords(self, words):
        """添加自定义停用词"""
        if self.stopwords_manager:
            self.stopwords_manager.add_custom_stopwords(words)
        else:
            print("停用词管理器不可用")

    def remove_custom_stopwords(self, words):
        """移除自定义停用词"""
        if self.stopwords_manager:
            self.stopwords_manager.remove_custom_stopwords(words)
        else:
            print("停用词管理器不可用")

    def clear_custom_stopwords(self):
        """清空自定义停用词"""
        if self.stopwords_manager:
            self.stopwords_manager.clear_custom_stopwords()
        else:
            print("停用词管理器不可用")

    def get_custom_stopwords(self):
        """获取自定义停用词列表"""
        if self.stopwords_manager:
            return self.stopwords_manager.get_custom_stopwords()
        else:
            return []

    def _init_nlp_models(self):
        """初始化NLP模型"""
        # 初始化spaCy模型
        if SPACY_AVAILABLE:
            try:
                # 尝试加载中文模型
                self.nlp_models['spacy_zh'] = spacy.load("zh_core_web_sm")
                print("✓ spaCy中文模型加载成功")
            except Exception as e:
                print(f"spaCy中文模型加载失败: {e}")
                try:
                    # 如果中文模型不可用，尝试英文模型
                    self.nlp_models['spacy_en'] = spacy.load("en_core_web_sm")
                    print("✓ spaCy英文模型加载成功")
                except Exception as e2:
                    print(f"spaCy英文模型加载失败: {e2}")

        # 初始化VADER情感分析器
        if VADER_AVAILABLE:
            try:
                self.nlp_models['vader'] = SentimentIntensityAnalyzer()
                print("✓ VADER情感分析器加载成功")
            except Exception as e:
                print(f"VADER加载失败: {e}")

        # 初始化Stanza模型（离线优先模式）
        if STANZA_AVAILABLE:
            try:
                # 尝试初始化中文模型（离线模式）
                self.nlp_models['stanza_zh'] = stanza.Pipeline(
                    'zh-hans',
                    processors='tokenize,pos,lemma,depparse',
                    download_method=stanza.DownloadMethod.REUSE_RESOURCES,
                    verbose=False,
                    use_gpu=False
                )
                print("✓ Stanza中文模型加载成功")
            except Exception as e:
                print(f"Stanza中文模型加载失败: {e}")
                try:
                    # 如果中文模型不可用，尝试英文模型（离线模式）
                    self.nlp_models['stanza_en'] = stanza.Pipeline(
                        'en',
                        processors='tokenize,pos,lemma,depparse',
                        download_method=stanza.DownloadMethod.REUSE_RESOURCES,
                        verbose=False,
                        use_gpu=False
                    )
                    print("✓ Stanza英文模型加载成功")
                except Exception as e2:
                    print(f"Stanza英文模型加载失败: {e2}")
                    print("💡 提示: 运行 'python download_models.py' 预下载模型文件")

        # 初始化深度学习情感分析模型
        self._init_advanced_sentiment_models()

        # 初始化SnowNLP
        if SNOWNLP_AVAILABLE:
            try:
                # SnowNLP不需要预加载，使用时直接创建实例
                self.nlp_models['snownlp'] = True  # 标记可用
                print("✓ SnowNLP中文情感分析器可用")
            except Exception as e:
                print(f"SnowNLP初始化失败: {e}")

        # 添加基础NLP功能（不依赖外部库）
        self._init_basic_nlp()

    def _init_advanced_sentiment_models(self):
        """初始化深度学习情感分析模型"""
        if not TRANSFORMERS_AVAILABLE:
            print("Transformers不可用，跳过深度学习模型初始化")
            return

        # 预训练中文情感分析模型配置（按优先级排序）
        sentiment_models = {
            'uer_roberta_dianping': {
                'model_name': 'uer/roberta-base-finetuned-dianping-chinese',
                'description': 'UER中文RoBERTa情感分析模型（大众点评数据训练）',
                'priority': 1
            },
            'erlangshen_roberta_110m': {
                'model_name': 'IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment',
                'description': '二郎神RoBERTa-110M情感分析模型（轻量级）',
                'priority': 2
            },
            'erlangshen_roberta_330m': {
                'model_name': 'IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment',
                'description': '二郎神RoBERTa-330M情感分析模型',
                'priority': 3
            },
        }

        # 尝试加载预训练情感分析模型
        loaded_models = 0
        for model_key, config in sentiment_models.items():
            try:
                print(f"尝试加载 {config['description']}...")

                # 创建情感分析pipeline
                sentiment_pipeline = pipeline(
                    "sentiment-analysis",
                    model=config['model_name'],
                    tokenizer=config['model_name'],
                    return_all_scores=True
                )

                self.nlp_models[model_key] = sentiment_pipeline
                print(f"✓ {config['description']} 加载成功")
                loaded_models += 1

                # 如果成功加载了一个高优先级模型，可以选择是否继续加载其他模型
                if config['priority'] == 1:
                    print("已加载高优先级模型，跳过其他模型以节省内存")
                    break

            except Exception as e:
                print(f"✗ {config['description']} 加载失败: {e}")
                continue

        # 如果没有成功加载任何预训练模型，尝试加载通用中文模型
        if loaded_models == 0:
            try:
                print("尝试加载通用中文BERT模型...")
                # 使用通用的中文BERT模型
                tokenizer = AutoTokenizer.from_pretrained('bert-base-chinese')
                model = AutoModelForSequenceClassification.from_pretrained('bert-base-chinese')

                self.nlp_models['bert_base_chinese'] = {
                    'tokenizer': tokenizer,
                    'model': model
                }
                print("✓ 通用中文BERT模型加载成功")
            except Exception as e:
                print(f"通用中文BERT模型加载失败: {e}")

        if loaded_models > 0:
            print(f"✓ 成功加载 {loaded_models} 个深度学习情感分析模型")
        else:
            print("⚠ 未能加载任何深度学习情感分析模型，将使用传统方法")

    def _init_basic_nlp(self):
        """初始化基础NLP功能"""
        # 扩展的情感词典
        self.sentiment_dict = {
            'positive': [
                # 中文积极词汇 - 基础情感
                '好', '棒', '优秀', '喜欢', '爱', '开心', '高兴', '满意', '赞', '完美', '成功', '胜利',
                '美好', '幸福', '快乐', '兴奋', '激动', '惊喜', '温暖', '舒适', '安全', '放心',
                '信任', '希望', '乐观', '积极', '正面', '有趣', '精彩', '出色', '卓越', '杰出',
                '优质', '优良', '先进', '创新', '突破', '进步', '发展', '繁荣', '昌盛', '兴旺',
                # 中文积极词汇 - 扩展
                '很棒', '非常好', '太好了', '真棒', '很赞', '不错', '挺好', '很满意', '很喜欢',
                '推荐', '强烈推荐', '值得', '超值', '物超所值', '性价比高', '质量好', '服务好',
                '态度好', '环境好', '味道好', '效果好', '体验好', '感觉好', '心情好', '顺利',
                '成就感', '有成就感', '很有用', '有帮助', '有效', '管用', '靠谱', '给力',
                # 英文积极词汇
                'excellent', 'good', 'great', 'love', 'like', 'happy', 'amazing', 'wonderful',
                'fantastic', 'awesome', 'brilliant', 'perfect', 'outstanding', 'superb',
                'magnificent', 'marvelous', 'delightful', 'pleasant', 'enjoyable', 'satisfying'
            ],
            'negative': [
                # 中文消极词汇 - 基础情感
                '坏', '差', '糟糕', '讨厌', '恨', '难过', '失望', '愤怒', '垃圾', '烂', '痛苦',
                '悲伤', '沮丧', '绝望', '恐惧', '害怕', '担心', '焦虑', '紧张', '压力', '困难',
                '问题', '错误', '失败', '挫折', '危险', '威胁', '损失', '破坏', '污染', '腐败',
                '欺骗', '虚假', '不良', '恶劣', '低劣', '落后', '衰退', '危机', '灾难', '悲剧',
                # 中文消极词汇 - 扩展
                '很差', '太差了', '很糟糕', '太糟糕了', '很失望', '太失望了', '不满意', '不推荐',
                '完全不推荐', '不值得', '不划算', '质量差', '服务差', '态度差', '环境差', '味道差',
                '效果差', '体验差', '感觉差', '心情差', '不顺利', '有问题', '出问题', '出bug',
                '难用', '太难用了', '不好用', '不管用', '没用', '无效', '不靠谱', '不给力',
                '界面设计很糟糕', '经常出现bug', '很沮丧', '很失望', '不好', '很难',
                # 英文消极词汇
                'bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'disappointed', 'horrible',
                'disgusting', 'annoying', 'frustrating', 'depressing', 'disturbing', 'shocking',
                'devastating', 'tragic', 'disastrous', 'pathetic', 'miserable', 'dreadful'
            ],
            # 添加否定词和程度副词
            'negation': ['不', '没', '无', '非', '未', '别', '勿', '莫', '否', '不是', '没有', '不会', '不能', '不要', '不太', '不够', '不怎么'],
            'intensifiers': {
                'strong': ['非常', '特别', '极其', '十分', '相当', '超级', '太', '很', '挺', '蛮', '超', '巨', '超级', '极度'],
                'weak': ['有点', '稍微', '略微', '还算', '比较', '相对', '算是', '稍', '略']
            },
            # 添加复合否定模式
            'complex_negation': [
                '不是很', '不太', '不够', '不怎么', '没那么', '不算', '称不上'
            ]
        }

        # 改进的实体模式
        self.entity_patterns = {
            'PERSON': [
                r'(?<![a-zA-Z\u4e00-\u9fff])[A-Z][a-z]+ [A-Z][a-z]+(?![a-zA-Z\u4e00-\u9fff])',  # 英文人名（改进边界）
                r'(?<![a-zA-Z\u4e00-\u9fff])[王李张刘陈杨黄赵吴周徐孙马朱胡郭何高林罗郑梁谢宋唐许韩冯邓曹彭曾肖田董袁潘于蒋蔡余杜叶程苏魏吕丁任沈姚卢姜崔钟谭陆汪范金石廖贾夏韦付方白邹孟熊秦邱江尹薛闫段雷侯龙史陶黎贺顾毛郝龚邵万钱严覃武戴莫孔向汤][\u4e00-\u9fff]{1,3}(?![a-zA-Z\u4e00-\u9fff])',  # 中文姓名（改进边界）
                r'史蒂夫·[a-zA-Z\u4e00-\u9fff]+',  # 特殊格式人名
                r'[a-zA-Z\u4e00-\u9fff]+·[a-zA-Z\u4e00-\u9fff]+',  # 中间有点的人名
            ],
            'ORG': [
                r'[\u4e00-\u9fff]{2,10}(?:公司|大学|学院|医院|银行|集团|企业|机构|组织|研究所|研究院|基金会|协会|联盟)',  # 中文机构（改进）
                r'[A-Z][a-zA-Z\s]{2,30}(?:Company|Corp|Inc|Ltd|University|College|Hospital|Bank|Institute|Foundation|Association)',  # 英文机构（改进）
                r'苹果公司|微软公司|谷歌公司|腾讯公司|阿里巴巴|百度公司',  # 知名公司
            ],
            'LOC': [
                r'(?:北京|上海|广州|深圳|杭州|南京|武汉|成都|重庆|天津|西安|沈阳|长沙|哈尔滨|昆明|大连|青岛|宁波|厦门|苏州|无锡|福州|济南|太原|长春|石家庄|南昌|贵阳|南宁|兰州|银川|西宁|乌鲁木齐|呼和浩特|拉萨|海口|三亚)市?',  # 中国城市（改进）
                r'(?:河北|山西|辽宁|吉林|黑龙江|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南|广东|海南|四川|贵州|云南|陕西|甘肃|青海|台湾|内蒙古|广西|西藏|宁夏|新疆)(?:省|自治区)?',  # 中国省份（改进）
                r'(?:美国|中国|日本|英国|法国|德国|意大利|加拿大|澳大利亚|韩国|印度|巴西|俄罗斯)(?![a-zA-Z\u4e00-\u9fff])',  # 国家
                r'加利福尼亚州|纽约州|德克萨斯州',  # 美国州
            ],
            'TIME': [
                r'\d{4}年\d{1,2}月\d{1,2}日',  # 中文日期
                r'\d{4}年\d{1,2}月',  # 中文年月
                r'\d{4}年',  # 年份
                r'(?:19|20)\d{2}年代',  # 年代
                r'\d{1,2}世纪',  # 世纪
            ]
        }

        print("✓ 基础NLP功能初始化完成")

    def _init_segmenters(self):
        """初始化中文分词器"""
        # 初始化jieba分词器
        if JIEBA_AVAILABLE:
            try:
                # 设置jieba为静默模式
                jieba.setLogLevel(20)
                # 预加载词典
                jieba.initialize()
                self.segmenters['jieba'] = jieba
                print("✓ jieba分词器加载成功")
            except Exception as e:
                print(f"jieba分词器加载失败: {e}")

        # 初始化pkuseg分词器
        if PKUSEG_AVAILABLE:
            try:
                # 使用默认模型，支持多种领域
                self.segmenters['pkuseg_default'] = pkuseg.pkuseg()
                print("✓ pkuseg默认分词器加载成功")

                # 尝试加载不同领域的模型
                domain_models = {
                    'pkuseg_news': 'news',      # 新闻领域
                    'pkuseg_web': 'web',        # 网络领域
                    'pkuseg_medicine': 'medicine',  # 医药领域
                    'pkuseg_tourism': 'tourism'     # 旅游领域
                }

                for model_key, domain in domain_models.items():
                    try:
                        self.segmenters[model_key] = pkuseg.pkuseg(model_name=domain)
                        print(f"✓ pkuseg {domain}领域分词器加载成功")
                    except Exception as e:
                        print(f"pkuseg {domain}领域分词器加载失败: {e}")

            except Exception as e:
                print(f"pkuseg分词器加载失败: {e}")

        # 初始化thulac分词器
        if THULAC_AVAILABLE:
            try:
                # 使用默认模型
                self.segmenters['thulac'] = thulac.thulac()
                print("✓ thulac分词器加载成功")
            except Exception as e:
                print(f"thulac分词器加载失败: {e}")

        print("✓ 分词器初始化完成")

    def _init_textteaser(self):
        """初始化TextTeaser摘要器（轻量级实现）"""
        if TEXTTEASER_AVAILABLE:
            # 我们使用自己的轻量级实现，不需要外部库
            self.textteaser = True  # 标记为可用
            print("✓ 轻量级TextTeaser算法加载成功")
        else:
            self.textteaser = None

    def _init_qwen3(self):
        """初始化Qwen3大模型客户端"""
        if QWEN3_AVAILABLE:
            try:
                # 设置API端点
                self.qwen3_api_url = 'http://localhost:6006/api/chat'
                self.qwen3_model = 'qwen3:8b'  # 根据您提供的模型信息

                # 测试连接
                test_data = {
                    "model": self.qwen3_model,
                    "messages": [
                        {
                            "role": "user",
                            "content": "测试连接"
                        }
                    ],
                    "stream": False
                }

                headers = {'Content-type': 'application/json'}
                response = requests.post(self.qwen3_api_url,
                                       data=json.dumps(test_data),
                                       headers=headers,
                                       timeout=10)

                if response.status_code == 200:
                    self.qwen3_client = True  # 标记为可用
                    print(f"✓ Qwen3模型连接成功: {self.qwen3_model}")
                else:
                    print(f"⚠ Qwen3模型连接失败，状态码: {response.status_code}")
                    self.qwen3_client = None

            except Exception as e:
                print(f"Qwen3模型连接失败: {e}")
                self.qwen3_client = None
        else:
            self.qwen3_client = None

    def segment_text(self, text: Optional[str] = None,
                    method: str = 'auto',
                    mode: str = 'accurate',
                    with_pos: bool = False) -> List[Dict]:
        """
        中文分词功能

        Args:
            text: 要分词的文本，如果为None则使用当前文本
            method: 分词方法 ('auto', 'jieba', 'pkuseg', 'thulac', 'basic')
            mode: 分词模式 ('accurate', 'full', 'search') - 仅jieba支持
            with_pos: 是否包含词性标注

        Returns:
            [{'word': '词', 'pos': '词性'}, ...] 或 [{'word': '词'}, ...]
        """
        if text is None:
            text = self.text

        if not text.strip():
            return []

        # 自动选择最佳分词器
        if method == 'auto':
            if 'pkuseg_default' in self.segmenters:
                method = 'pkuseg_default'  # pkuseg准确度较高
            elif 'jieba' in self.segmenters:
                method = 'jieba'   # jieba速度较快
            elif 'thulac' in self.segmenters:
                method = 'thulac'  # thulac也不错
            else:
                method = 'basic'   # 降级到基础方法

        # 使用指定的分词器
        if method == 'jieba' and 'jieba' in self.segmenters:
            return self._jieba_segment(text, mode, with_pos)
        elif method.startswith('pkuseg') and method in self.segmenters:
            return self._pkuseg_segment(text, with_pos, method)
        elif method == 'thulac' and 'thulac' in self.segmenters:
            return self._thulac_segment(text, with_pos)
        else:
            return self._basic_segment(text, with_pos)

    def _jieba_segment(self, text: str, mode: str = 'accurate', with_pos: bool = False) -> List[Dict]:
        """使用jieba进行分词"""
        try:
            if with_pos:
                # 带词性标注的分词
                words = pseg.cut(text)
                return [{'word': word, 'pos': pos} for word, pos in words if word.strip()]
            else:
                # 根据模式选择分词方法
                if mode == 'accurate':
                    words = jieba.cut(text, cut_all=False)
                elif mode == 'full':
                    words = jieba.cut(text, cut_all=True)
                elif mode == 'search':
                    words = jieba.cut_for_search(text)
                else:
                    words = jieba.cut(text, cut_all=False)

                return [{'word': word} for word in words if word.strip()]
        except Exception as e:
            print(f"jieba分词失败: {e}")
            return self._basic_segment(text, with_pos)

    def _pkuseg_segment(self, text: str, with_pos: bool = False, model_key: str = 'pkuseg_default') -> List[Dict]:
        """使用pkuseg进行分词"""
        try:
            segmenter = self.segmenters.get(model_key)
            if not segmenter:
                # 如果指定模型不存在，使用默认模型
                segmenter = self.segmenters.get('pkuseg_default')
                if not segmenter:
                    return self._basic_segment(text, with_pos)

            if with_pos:
                # 使用带词性标注的pkuseg
                try:
                    # 创建带词性标注的分词器
                    pos_segmenter = pkuseg.pkuseg(postag=True)
                    words_pos = pos_segmenter.cut(text)
                    return [{'word': word, 'pos': pos} for word, pos in words_pos if word.strip()]
                except:
                    # 如果词性标注失败，降级到普通分词
                    words = segmenter.cut(text)
                    return [{'word': word, 'pos': 'UNK'} for word in words if word.strip()]
            else:
                words = segmenter.cut(text)
                return [{'word': word} for word in words if word.strip()]
        except Exception as e:
            print(f"pkuseg分词失败: {e}")
            return self._basic_segment(text, with_pos)

    def _thulac_segment(self, text: str, with_pos: bool = False) -> List[Dict]:
        """使用thulac进行分词"""
        try:
            words_pos = self.segmenters['thulac'].cut(text)
            if with_pos:
                return [{'word': word, 'pos': pos} for word, pos in words_pos if word.strip()]
            else:
                return [{'word': word} for word, pos in words_pos if word.strip()]
        except Exception as e:
            print(f"thulac分词失败: {e}")
            return self._basic_segment(text, with_pos)

    def _basic_segment(self, text: str, with_pos: bool = False) -> List[Dict]:
        """基础分词方法（按标点和空白字符分割）"""
        # 中文标点符号
        chinese_punctuation = '，。！？；：""''（）【】《》、""……'
        # 英文标点符号
        english_punctuation = string.punctuation
        all_punctuation = chinese_punctuation + english_punctuation

        # 将标点符号替换为空格
        for punct in all_punctuation:
            text = text.replace(punct, ' ')

        # 将换行符也替换为空格
        text = text.replace('\n', ' ').replace('\r', ' ')

        # 分词（按空白字符分割，并过滤空字符串）
        words = [word.strip() for word in text.split() if word.strip()]

        if with_pos:
            return [{'word': word, 'pos': 'UNK'} for word in words]
        else:
            return [{'word': word} for word in words]

    def extract_entities(self, text: Optional[str] = None, method: str = 'hybrid',
                        deduplicate: bool = True) -> Dict[str, List[Dict]]:
        """
        实体识别功能

        Args:
            text: 要分析的文本，如果为None则使用当前文本
            method: 识别方法 ('spacy', 'regex', 'hybrid')
            deduplicate: 是否对实体进行去重和统计

        Returns:
            {
                'entities': [{'text': '实体文本', 'label': '实体类型', 'count': 出现次数, 'positions': [位置列表]}],
                'available': 是否可用,
                'model_used': 使用的模型,
                'deduplicated': 是否已去重
            }
        """
        if text is None:
            text = self.text

        if not text.strip():
            return {'entities': [], 'available': False, 'model_used': None, 'deduplicated': False}

        # 执行实体识别
        if method == 'regex':
            result = self._basic_entity_recognition(text)
        elif method == 'spacy':
            result = self._spacy_entity_recognition(text)
        else:  # method == 'hybrid'
            result = self._hybrid_entity_recognition(text)

        # 如果需要去重
        if deduplicate and result['available'] and result['entities']:
            result['entities'] = self._deduplicate_entities(result['entities'])
            result['deduplicated'] = True
        else:
            result['deduplicated'] = False

        return result

    def _spacy_entity_recognition(self, text: str) -> Dict[str, List[Dict]]:
        """使用spaCy进行实体识别"""
        # 优先使用中文spaCy模型
        if 'spacy_zh' in self.nlp_models:
            doc = self.nlp_models['spacy_zh'](text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'description': spacy.explain(ent.label_) or ent.label_,
                    'confidence': 1.0  # spaCy不提供置信度，设为1.0
                })
            return {
                'entities': entities,
                'available': True,
                'model_used': 'spacy_zh'
            }

        # 使用英文spaCy模型
        elif 'spacy_en' in self.nlp_models:
            doc = self.nlp_models['spacy_en'](text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'description': spacy.explain(ent.label_) or ent.label_,
                    'confidence': 1.0
                })
            return {
                'entities': entities,
                'available': True,
                'model_used': 'spacy_en'
            }

        # 降级到基础实体识别
        return self._basic_entity_recognition(text)

    def _deduplicate_entities(self, entities: List[Dict]) -> List[Dict]:
        """
        对实体进行去重和统计

        Args:
            entities: 原始实体列表

        Returns:
            去重后的实体列表，包含统计信息
        """
        entity_stats = {}

        for entity in entities:
            # 使用实体文本和标签作为唯一标识
            key = (entity['text'].strip().lower(), entity['label'])

            if key not in entity_stats:
                entity_stats[key] = {
                    'text': entity['text'].strip(),
                    'label': entity['label'],
                    'description': entity.get('description', entity['label']),
                    'count': 0,
                    'positions': [],
                    'sources': set(),
                    'confidence': entity.get('confidence', 1.0)
                }

            entity_stats[key]['count'] += 1
            entity_stats[key]['positions'].append({
                'start': entity['start'],
                'end': entity['end']
            })

            if 'source' in entity:
                entity_stats[key]['sources'].add(entity['source'])

        # 转换为列表格式
        deduplicated = []
        for (text, label), stats in entity_stats.items():
            deduplicated.append({
                'text': stats['text'],
                'label': label,
                'description': stats['description'],
                'count': stats['count'],
                'positions': stats['positions'],
                'sources': list(stats['sources']) if stats['sources'] else [],
                'confidence': stats['confidence']
            })

        # 按出现次数降序排列
        deduplicated.sort(key=lambda x: x['count'], reverse=True)

        return deduplicated

    def _hybrid_entity_recognition(self, text: str) -> Dict[str, List[Dict]]:
        """混合实体识别：结合spaCy和正则表达式"""
        # 获取spaCy识别结果
        spacy_result = self._spacy_entity_recognition(text)

        # 获取正则表达式识别结果
        regex_result = self._basic_entity_recognition(text)

        if not spacy_result['available']:
            return regex_result

        # 合并和过滤结果
        merged_entities = []

        # 1. 添加高质量的spaCy结果（过滤掉一些不可靠的类型）
        reliable_spacy_labels = {'PERSON', 'ORG', 'GPE', 'DATE', 'TIME', 'MONEY', 'PERCENT'}
        for entity in spacy_result['entities']:
            if entity['label'] in reliable_spacy_labels and len(entity['text'].strip()) > 1:
                # 过滤掉过短或包含特殊字符的实体
                if not re.match(r'^[，。！？；：\s]+$', entity['text']):
                    entity['source'] = 'spacy'
                    merged_entities.append(entity)

        # 2. 添加正则表达式的高精度结果（避免重复）
        for regex_entity in regex_result['entities']:
            # 检查是否与spaCy结果重叠
            is_duplicate = False
            for spacy_entity in merged_entities:
                if self._entities_overlap(regex_entity, spacy_entity):
                    is_duplicate = True
                    break

            if not is_duplicate:
                regex_entity['source'] = 'regex'
                merged_entities.append(regex_entity)

        # 3. 按位置排序
        merged_entities.sort(key=lambda x: x['start'])

        return {
            'entities': merged_entities,
            'available': True,
            'model_used': 'hybrid_spacy_regex'
        }

    def _entities_overlap(self, entity1: Dict, entity2: Dict) -> bool:
        """检查两个实体是否重叠"""
        return not (entity1['end'] <= entity2['start'] or entity2['end'] <= entity1['start'])

    def _basic_entity_recognition(self, text: str) -> Dict[str, List[Dict]]:
        """基础实体识别（使用正则表达式）"""
        entities = []

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    entities.append({
                        'text': match.group(),
                        'label': entity_type,
                        'start': match.start(),
                        'end': match.end(),
                        'description': self._get_entity_description(entity_type),
                        'confidence': 0.9  # 正则表达式置信度
                    })

        return {
            'entities': entities,
            'available': True,
            'model_used': 'basic_regex'
        }

    def _get_entity_description(self, entity_type: str) -> str:
        """获取实体类型描述"""
        descriptions = {
            'PERSON': '人名',
            'ORG': '机构组织',
            'LOC': '地点位置',
            'TIME': '时间日期'
        }
        return descriptions.get(entity_type, entity_type)

    def analyze_sentiment(self, text: Optional[str] = None) -> Dict:
        """
        情感分析功能

        Args:
            text: 要分析的文本，如果为None则使用当前文本

        Returns:
            {
                'sentiment': 情感倾向,
                'scores': 详细分数,
                'available': 是否可用,
                'methods_used': 使用的方法列表
            }
        """
        if text is None:
            text = self.text

        if not text.strip():
            return {'sentiment': 'neutral', 'scores': {}, 'available': False, 'methods_used': []}

        results = {
            'sentiment': 'neutral',
            'scores': {},
            'available': False,
            'methods_used': [],
            'confidence': 0.0,
            'model_details': {}
        }

        # 存储所有模型的预测结果，用于融合
        all_predictions = []

        # 1. 使用深度学习模型进行情感分析（优先级最高）
        dl_result = self._analyze_with_deep_learning(text)
        if dl_result['available']:
            results['scores'].update(dl_result['scores'])
            results['methods_used'].extend(dl_result['methods_used'])
            results['model_details'].update(dl_result['model_details'])
            results['available'] = True
            all_predictions.append({
                'sentiment': dl_result['sentiment'],
                'confidence': dl_result['confidence'],
                'weight': 0.35  # 深度学习模型权重
            })

        # 2. 使用SnowNLP进行中文情感分析（权重最高，因为专门针对中文）
        snow_result = self._analyze_with_snownlp(text)
        if snow_result['available']:
            results['scores'].update(snow_result['scores'])
            results['methods_used'].extend(snow_result['methods_used'])
            results['available'] = True
            all_predictions.append({
                'sentiment': snow_result['sentiment'],
                'confidence': snow_result['confidence'],
                'weight': 0.35  # SnowNLP权重，专门针对中文
            })

        # 3. 使用VADER进行情感分析（对中文效果不好，降低权重）
        if 'vader' in self.nlp_models:
            vader_scores = self.nlp_models['vader'].polarity_scores(text)
            results['scores']['vader'] = vader_scores
            results['methods_used'].append('vader')
            results['available'] = True

            # 根据compound分数确定情感倾向
            compound = vader_scores['compound']
            if compound >= 0.05:
                vader_sentiment = 'positive'
                vader_confidence = min(abs(compound), 1.0)
            elif compound <= -0.05:
                vader_sentiment = 'negative'
                vader_confidence = min(abs(compound), 1.0)
            else:
                vader_sentiment = 'neutral'
                vader_confidence = 1.0 - abs(compound)

            # 只有当VADER有明确判断时才加入融合（避免中性结果干扰）
            if abs(compound) > 0.1:
                all_predictions.append({
                    'sentiment': vader_sentiment,
                    'confidence': vader_confidence,
                    'weight': 0.10  # VADER权重较低，对中文支持有限
                })

        # 4. 使用TextBlob进行情感分析
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity

                results['scores']['textblob'] = {
                    'polarity': polarity,
                    'subjectivity': subjectivity
                }
                results['methods_used'].append('textblob')
                results['available'] = True

                # 确定TextBlob的情感倾向
                if polarity > 0.1:
                    textblob_sentiment = 'positive'
                    textblob_confidence = min(abs(polarity), 1.0)
                elif polarity < -0.1:
                    textblob_sentiment = 'negative'
                    textblob_confidence = min(abs(polarity), 1.0)
                else:
                    textblob_sentiment = 'neutral'
                    textblob_confidence = 1.0 - abs(polarity)

                # 只有当TextBlob有明确判断时才加入融合
                if abs(polarity) > 0.1:
                    all_predictions.append({
                        'sentiment': textblob_sentiment,
                        'confidence': textblob_confidence,
                        'weight': 0.05  # TextBlob权重很低，主要针对英文
                    })
            except Exception:
                pass

        # 5. 使用增强的基础情感分析（总是运行，作为补充）
        basic_result = self._basic_sentiment_analysis(text)
        if basic_result['available']:
            results['scores'].update(basic_result['scores'])
            if not results['available']:  # 如果没有其他方法可用
                results['methods_used'].extend(basic_result['methods_used'])
                results['available'] = True
                all_predictions.append({
                    'sentiment': basic_result['sentiment'],
                    'confidence': basic_result['confidence'],
                    'weight': 1.0  # 如果只有基础方法，权重为1
                })
            else:  # 作为补充方法
                results['methods_used'].extend(basic_result['methods_used'])
                # 只有当基础方法有明确判断时才加入融合
                if basic_result['confidence'] > 0.6:
                    all_predictions.append({
                        'sentiment': basic_result['sentiment'],
                        'confidence': basic_result['confidence'],
                        'weight': 0.15  # 基础方法作为补充
                    })

        # 6. 融合所有模型的预测结果
        if all_predictions:
            final_result = self._ensemble_predictions(all_predictions)
            results['sentiment'] = final_result['sentiment']
            results['confidence'] = final_result['confidence']
            results['ensemble_details'] = final_result['details']

        return results

    def _analyze_with_deep_learning(self, text: str) -> Dict:
        """使用深度学习模型进行情感分析"""
        result = {
            'sentiment': 'neutral',
            'confidence': 0.0,
            'scores': {},
            'available': False,
            'methods_used': [],
            'model_details': {}
        }

        # 检查可用的深度学习模型（按优先级顺序）
        dl_models = [
            'uer_roberta_dianping', 'erlangshen_roberta_110m', 'erlangshen_roberta_330m',
            'chinese_roberta_wwm_ext', 'chinese_bert_wwm', 'bert_base_chinese'
        ]

        for model_key in dl_models:
            if model_key in self.nlp_models:
                try:
                    if model_key in ['bert_base_chinese', 'chinese_bert_wwm', 'chinese_roberta_wwm_ext']:
                        # 处理需要微调的通用模型（暂时跳过）
                        print(f"跳过未微调的模型: {model_key}")
                        continue
                    else:
                        # 处理预训练的情感分析模型
                        dl_result = self._predict_with_pipeline(text, model_key)

                    if dl_result['available']:
                        result.update(dl_result)
                        break

                except Exception as e:
                    print(f"深度学习模型 {model_key} 预测失败: {e}")
                    continue

        return result

    def _predict_with_pipeline(self, text: str, model_key: str) -> Dict:
        """使用pipeline模型进行预测"""
        try:
            pipeline_model = self.nlp_models[model_key]

            # 限制文本长度，避免超出模型限制
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]

            predictions = pipeline_model(text)

            # 解析预测结果
            if predictions and len(predictions) > 0:
                # 处理不同模型的输出格式
                if isinstance(predictions[0], list):
                    # 如果是嵌套列表，取第一个
                    predictions = predictions[0]

                # 找到最高分数的预测
                best_pred = max(predictions, key=lambda x: x['score'])

                # 标准化标签（支持更多格式）
                label = str(best_pred['label']).lower().strip()
                score = float(best_pred['score'])

                # 映射标签到标准格式（支持中英文标签）
                sentiment = 'neutral'  # 默认值

                if any(pos_word in label for pos_word in ['pos', 'positive', '1', '积极', '正面', 'good']):
                    sentiment = 'positive'
                elif any(neg_word in label for neg_word in ['neg', 'negative', '0', '消极', '负面', 'bad']):
                    sentiment = 'negative'
                elif any(neu_word in label for neu_word in ['neu', 'neutral', '中性', 'normal']):
                    sentiment = 'neutral'
                else:
                    # 如果标签无法识别，根据分数判断
                    if score > 0.6:
                        sentiment = 'positive'
                    elif score < 0.4:
                        sentiment = 'negative'
                    else:
                        sentiment = 'neutral'

                # 计算置信度
                confidence = score if sentiment != 'neutral' else max(score, 1.0 - score)

                return {
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'scores': {model_key: predictions},
                    'available': True,
                    'methods_used': [model_key],
                    'model_details': {model_key: {
                        'best_prediction': best_pred,
                        'all_predictions': predictions,
                        'model_type': 'transformer_pipeline'
                    }}
                }

        except Exception as e:
            print(f"Pipeline预测失败: {e}")

        return {'available': False}

    def _predict_with_bert(self, text: str, model_key: str) -> Dict:
        """使用通用BERT模型进行预测（需要自定义分类逻辑）"""
        try:
            # 这里可以实现自定义的BERT分类逻辑
            # 由于通用BERT模型没有预训练的情感分析头，这里返回不可用
            return {'available': False}
        except Exception as e:
            print(f"BERT预测失败: {e}")
            return {'available': False}

    def _analyze_with_snownlp(self, text: str) -> Dict:
        """使用SnowNLP进行中文情感分析"""
        result = {
            'sentiment': 'neutral',
            'confidence': 0.0,
            'scores': {},
            'available': False,
            'methods_used': []
        }

        if not SNOWNLP_AVAILABLE or 'snownlp' not in self.nlp_models:
            return result

        try:
            snow = SnowNLP(text)
            sentiment_score = snow.sentiments  # 返回0-1之间的值，>0.5为积极

            # 确定情感倾向（调整阈值，让判断更敏感）
            if sentiment_score > 0.55:
                sentiment = 'positive'
                confidence = sentiment_score
            elif sentiment_score < 0.45:
                sentiment = 'negative'
                confidence = 1.0 - sentiment_score
            else:
                sentiment = 'neutral'
                confidence = 1.0 - abs(sentiment_score - 0.5) * 2

            result.update({
                'sentiment': sentiment,
                'confidence': confidence,
                'scores': {'snownlp': {'sentiment_score': sentiment_score}},
                'available': True,
                'methods_used': ['snownlp']
            })

        except Exception as e:
            print(f"SnowNLP分析失败: {e}")

        return result

    def _ensemble_predictions(self, predictions: List[Dict]) -> Dict:
        """融合多个模型的预测结果"""
        if not predictions:
            return {'sentiment': 'neutral', 'confidence': 0.0, 'details': {}}

        # 计算加权投票
        sentiment_scores = {'positive': 0.0, 'negative': 0.0, 'neutral': 0.0}
        total_weight = 0.0

        for pred in predictions:
            weight = pred['weight'] * pred['confidence']
            sentiment_scores[pred['sentiment']] += weight
            total_weight += weight

        # 归一化分数
        if total_weight > 0:
            for sentiment in sentiment_scores:
                sentiment_scores[sentiment] /= total_weight

        # 选择最高分数的情感
        final_sentiment = max(sentiment_scores, key=sentiment_scores.get)
        final_confidence = sentiment_scores[final_sentiment]

        return {
            'sentiment': final_sentiment,
            'confidence': final_confidence,
            'details': {
                'sentiment_scores': sentiment_scores,
                'total_predictions': len(predictions),
                'total_weight': total_weight
            }
        }

    def _basic_sentiment_analysis(self, text: str) -> Dict:
        """增强的基础情感分析（基于词典，支持否定词和程度副词）"""
        # 预处理文本
        text_clean = text.strip()

        # 使用jieba分词（如果可用）
        if JIEBA_AVAILABLE:
            try:
                words = list(jieba.cut(text_clean))
            except:
                words = text_clean.split()
        else:
            # 简单的中文分词（按字符和标点分割）
            import re
            words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+|\d+', text_clean)

        positive_score = 0.0
        negative_score = 0.0
        sentiment_details = []

        # 分析每个词及其上下文
        for i, word in enumerate(words):
            word_lower = word.lower()

            # 检查是否为情感词
            is_positive = any(pos_word in word_lower for pos_word in self.sentiment_dict['positive'])
            is_negative = any(neg_word in word_lower for neg_word in self.sentiment_dict['negative'])

            if is_positive or is_negative:
                # 基础分数
                base_score = 1.0

                # 检查程度副词
                intensifier_multiplier = 1.0
                for j in range(max(0, i-2), i):  # 检查前两个词
                    prev_word = words[j]
                    if any(strong in prev_word for strong in self.sentiment_dict['intensifiers']['strong']):
                        intensifier_multiplier = 1.5
                        break
                    elif any(weak in prev_word for weak in self.sentiment_dict['intensifiers']['weak']):
                        intensifier_multiplier = 0.7
                        break

                # 检查否定词（改进版本）
                is_negated = False

                # 首先检查复合否定模式
                text_before_word = ''.join(words[max(0, i-3):i])
                for complex_neg in self.sentiment_dict['complex_negation']:
                    if complex_neg in text_before_word:
                        is_negated = True
                        break

                # 如果没有复合否定，检查简单否定词
                if not is_negated:
                    for j in range(max(0, i-3), i):  # 检查前三个词
                        prev_word = words[j]
                        if any(neg in prev_word for neg in self.sentiment_dict['negation']):
                            is_negated = True
                            break

                # 计算最终分数
                final_score = base_score * intensifier_multiplier

                if is_positive:
                    if is_negated:
                        negative_score += final_score
                        sentiment_details.append(f"否定的积极词: {word}")
                    else:
                        positive_score += final_score
                        sentiment_details.append(f"积极词: {word}")
                elif is_negative:
                    if is_negated:
                        positive_score += final_score
                        sentiment_details.append(f"否定的消极词: {word}")
                    else:
                        negative_score += final_score
                        sentiment_details.append(f"消极词: {word}")

        # 计算情感倾向
        total_score = positive_score + negative_score
        if total_score == 0:
            sentiment = 'neutral'
            polarity = 0.0
            confidence = 0.5
        else:
            polarity = (positive_score - negative_score) / total_score
            if polarity > 0.2:
                sentiment = 'positive'
                confidence = min(polarity + 0.5, 1.0)
            elif polarity < -0.2:
                sentiment = 'negative'
                confidence = min(abs(polarity) + 0.5, 1.0)
            else:
                sentiment = 'neutral'
                confidence = 1.0 - abs(polarity)

        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'scores': {
                'basic': {
                    'positive_score': positive_score,
                    'negative_score': negative_score,
                    'polarity': polarity,
                    'total_words': len(words),
                    'sentiment_words': len(sentiment_details)
                }
            },
            'available': True,
            'methods_used': ['enhanced_basic_dictionary'],
            'details': sentiment_details[:10]  # 最多显示10个情感词
        }

    def analyze_syntax(self, text: Optional[str] = None, max_length: int = 5000) -> Dict:
        """
        依存句法分析功能（支持大文本分块处理）

        Args:
            text: 要分析的文本，如果为None则使用当前文本
            max_length: 单次处理的最大字符数，超过则分块处理

        Returns:
            {
                'sentences': [句法分析结果],
                'available': 是否可用,
                'model_used': 使用的模型,
                'is_truncated': 是否被截断
            }
        """
        if text is None:
            text = self.text

        if not text.strip():
            return {'sentences': [], 'available': False, 'model_used': None, 'is_truncated': False}

        # 对于大文本，只分析前面部分以提高性能
        is_truncated = False
        if len(text) > max_length:
            text = text[:max_length]
            is_truncated = True

        # 使用Stanza进行句法分析
        if 'stanza_zh' in self.nlp_models:
            try:
                doc = self.nlp_models['stanza_zh'](text)
                sentences = []
                for sent in doc.sentences:
                    words = []
                    for word in sent.words:
                        words.append({
                            'text': word.text,
                            'lemma': word.lemma,
                            'pos': word.upos,
                            'head': word.head,
                            'deprel': word.deprel
                        })
                    sentences.append({
                        'text': sent.text,
                        'words': words
                    })
                return {
                    'sentences': sentences,
                    'available': True,
                    'model_used': 'stanza_zh',
                    'is_truncated': is_truncated
                }
            except Exception:
                pass

        elif 'stanza_en' in self.nlp_models:
            try:
                doc = self.nlp_models['stanza_en'](text)
                sentences = []
                for sent in doc.sentences:
                    words = []
                    for word in sent.words:
                        words.append({
                            'text': word.text,
                            'lemma': word.lemma,
                            'pos': word.upos,
                            'head': word.head,
                            'deprel': word.deprel
                        })
                    sentences.append({
                        'text': sent.text,
                        'words': words
                    })
                return {
                    'sentences': sentences,
                    'available': True,
                    'model_used': 'stanza_en',
                    'is_truncated': is_truncated
                }
            except Exception:
                pass

        # 使用基础句法分析
        result = self._basic_syntax_analysis(text)
        result['is_truncated'] = is_truncated
        return result

    def _basic_syntax_analysis(self, text: str) -> Dict:
        """基础句法分析（简化版）"""
        sentences = self._split_sentences(text)
        analyzed_sentences = []

        for sentence in sentences:
            words = sentence.split()
            analyzed_words = []

            for i, word in enumerate(words):
                # 简单的词性和依存关系推断
                pos = self._guess_pos(word)
                deprel = self._guess_deprel(word, i, len(words))

                analyzed_words.append({
                    'text': word,
                    'lemma': word.lower(),  # 简化的词根
                    'pos': pos,
                    'head': 0,  # 简化处理
                    'deprel': deprel
                })

            analyzed_sentences.append({
                'text': sentence,
                'words': analyzed_words
            })

        return {
            'sentences': analyzed_sentences,
            'available': True,
            'model_used': 'basic_rules'
        }

    def _guess_pos(self, word: str) -> str:
        """简单的词性推断"""
        # 基于简单规则的词性推断
        if re.match(r'\d+', word):
            return 'NUM'
        elif word in ['的', '了', '着', '过', 'the', 'a', 'an']:
            return 'DET'
        elif word in ['和', '与', 'and', 'or']:
            return 'CCONJ'
        elif word in ['在', 'in', 'on', 'at']:
            return 'ADP'
        else:
            return 'NOUN'  # 默认为名词

    def _guess_deprel(self, word: str, position: int, total_words: int) -> str:
        """简单的依存关系推断"""
        if position == 0:
            return 'nsubj'  # 第一个词通常是主语
        elif position == total_words - 1:
            return 'obj'    # 最后一个词通常是宾语
        elif position == 1 or '是' in word or 'is' in word.lower():
            return 'root'   # 谓语
        else:
            return 'amod'   # 修饰语

    def generate_enhanced_summary(self, num_sentences: int = 3,
                                method: str = 'enhanced_hybrid') -> str:
        """
        增强的文本摘要生成（集成句法分析）

        Args:
            num_sentences: 摘要句子数
            method: 摘要方法 ('enhanced_hybrid', 'syntax_based', 或原有方法)

        Returns:
            摘要文本
        """
        if method in ['frequency', 'position', 'hybrid']:
            # 使用原有方法
            return self.generate_summary(num_sentences, method)

        sentences = self._split_sentences(self.text)

        if len(sentences) <= num_sentences:
            return self.text

        if method == 'enhanced_hybrid':
            return self._enhanced_hybrid_summary(sentences, num_sentences)
        elif method == 'syntax_based':
            return self._syntax_based_summary(sentences, num_sentences)
        else:
            # 默认使用增强混合方法
            return self._enhanced_hybrid_summary(sentences, num_sentences)

    def intelligent_rewrite(self, style: str = 'formal', intensity: str = 'medium',
                          segment_mode: bool = True, max_segment_length: int = 1000) -> str:
        """
        智能改写文本（支持分段处理）

        Args:
            style: 改写风格 ('formal', 'casual', 'academic', 'creative', 'concise')
            intensity: 改写强度 ('light', 'medium', 'heavy')
            segment_mode: 是否启用分段模式（推荐长文本使用）
            max_segment_length: 每段最大字符数

        Returns:
            改写后的文本
        """
        if not self.text:
            return ""

        # 如果文本较短或不启用分段模式，直接处理
        if not segment_mode or len(self.text) <= max_segment_length:
            if self.qwen3_client:
                return self._qwen3_rewrite(style, intensity)
            else:
                return self._basic_rewrite(style, intensity)

        # 长文本分段处理
        return self._segmented_rewrite(style, intensity, max_segment_length)

    def _enhanced_hybrid_summary(self, sentences: List[str], num_sentences: int) -> str:
        """增强的混合方法摘要（结合句法分析）"""
        word_freq = self.word_frequency(ignore_case=True, exclude_punctuation=True)
        total_sentences = len(sentences)

        sentence_scores = []
        for i, sentence in enumerate(sentences):
            # 基础词频分数
            words = sentence.lower().translate(str.maketrans('', '', string.punctuation)).split()
            freq_score = sum(word_freq.get(word, 0) for word in words)

            # 位置权重
            if i == 0 or i == total_sentences - 1:
                position_weight = 1.5
            elif i < total_sentences * 0.2 or i > total_sentences * 0.8:
                position_weight = 1.2
            else:
                position_weight = 1.0

            # 句法复杂度权重（如果可用）
            syntax_weight = self._calculate_syntax_weight(sentence)

            # 实体权重（如果可用）
            entity_weight = self._calculate_entity_weight(sentence)

            final_score = freq_score * position_weight * syntax_weight * entity_weight
            sentence_scores.append((final_score, sentence))

        sentence_scores.sort(reverse=True)
        top_sentences = [sent for _, sent in sentence_scores[:num_sentences]]

        return '. '.join(top_sentences) + '.'

    def _syntax_based_summary(self, sentences: List[str], num_sentences: int) -> str:
        """基于句法分析的摘要"""
        sentence_scores = []

        for sentence in sentences:
            syntax_analysis = self.analyze_syntax(sentence)
            score = 0

            if syntax_analysis['available']:
                # 根据句法结构计算分数
                for sent_data in syntax_analysis['sentences']:
                    for word in sent_data['words']:
                        # 主语、谓语、宾语权重更高
                        if word['deprel'] in ['nsubj', 'root', 'obj', 'dobj']:
                            score += 2
                        elif word['deprel'] in ['amod', 'compound']:
                            score += 1
            else:
                # 如果句法分析不可用，使用句子长度作为简单指标
                score = len(sentence.split())

            sentence_scores.append((score, sentence))

        sentence_scores.sort(reverse=True)
        top_sentences = [sent for _, sent in sentence_scores[:num_sentences]]

        return '. '.join(top_sentences) + '.'

    def _calculate_syntax_weight(self, sentence: str) -> float:
        """计算句法复杂度权重"""
        syntax_analysis = self.analyze_syntax(sentence)

        if not syntax_analysis['available']:
            return 1.0

        weight = 1.0
        for sent_data in syntax_analysis['sentences']:
            # 包含更多重要句法关系的句子权重更高
            important_relations = ['nsubj', 'root', 'obj', 'dobj', 'amod']
            relation_count = sum(1 for word in sent_data['words']
                               if word['deprel'] in important_relations)
            if relation_count > 3:
                weight += 0.2

        return weight

    def _calculate_entity_weight(self, sentence: str) -> float:
        """计算实体权重"""
        entities = self.extract_entities(sentence)

        if not entities['available']:
            return 1.0

        # 包含更多实体的句子权重更高
        entity_count = len(entities['entities'])
        if entity_count > 0:
            return 1.0 + (entity_count * 0.1)

        return 1.0

    def get_nlp_capabilities(self) -> Dict:
        """获取当前可用的NLP功能"""
        # 检查可用的情感分析方法
        sentiment_methods = []
        if self.nlp_models.get('vader'):
            sentiment_methods.append('vader')
        if TEXTBLOB_AVAILABLE:
            sentiment_methods.append('textblob')
        if self.nlp_models.get('snownlp'):
            sentiment_methods.append('snownlp')

        # 检查深度学习模型
        dl_models = ['erlangshen_roberta_330m', 'erlangshen_roberta_110m', 'chinese_roberta_wwm_ext']
        available_dl_models = [model for model in dl_models if model in self.nlp_models]
        if available_dl_models:
            sentiment_methods.extend(available_dl_models)

        # 基础方法总是可用
        sentiment_methods.append('basic_dictionary')

        return {
            'entity_recognition': {
                'available': True,
                'methods': ['basic_regex']
            },
            'sentiment_analysis': {
                'available': True,
                'methods': sentiment_methods
            },
            'syntax_analysis': {
                'available': True,
                'methods': ['basic'] + ([model for model in ['stanza_zh', 'stanza_en'] if model in self.nlp_models])
            },
            'enhanced_summary': True,
            'textteaser_summary': bool(self.textteaser),
            'qwen3_summary': bool(self.qwen3_client),
            'intelligent_rewrite': True,
            'qwen3_rewrite': bool(self.qwen3_client),
            'advanced_entity_recognition': bool(self.nlp_models.get('spacy_zh') or self.nlp_models.get('spacy_en')),
            'advanced_sentiment_analysis': len(sentiment_methods) > 1,
            'advanced_syntax_analysis': bool(self.nlp_models.get('stanza_zh') or self.nlp_models.get('stanza_en'))
        }

    def _qwen3_rewrite(self, style: str, intensity: str) -> str:
        """使用Qwen3模型进行智能改写"""
        try:
            # 读取提示词文件
            prompt_content = self._load_rewrite_prompt()

            # 构建改写风格描述
            style_descriptions = {
                'formal': '正式风格（Formal）- 使用正式、严谨的语言，适合商务文档、官方报告等场合',
                'casual': '口语化（Casual/Spoken）- 使用轻松、自然的口语表达，贴近日常对话',
                'academic': '学术风格（Academic）- 使用专业、严谨的学术语言，适合学术论文、研究报告',
                'creative': '文学化（Literary）- 使用富有创意、生动形象的文学表达',
                'concise': '简洁凝练（Concise）- 使用精炼、简洁的语言，去除冗余表达'
            }

            # 构建改写强度描述
            intensity_descriptions = {
                'light': '轻度改写 - 保持原文的句式结构，主要调整用词和表达方式，确保语言风格的转换',
                'medium': '中度改写 - 适度调整句式结构和表达方式，在保持原意的基础上进行较大程度的语言风格转换',
                'heavy': '重度改写 - 大幅改写句式和表达方式，用完全不同的语言风格重新表达相同的内容'
            }

            # 构建完整的提示词
            content = f"""{prompt_content}

改写任务：
请将以下文本改写为：{style_descriptions.get(style, style_descriptions['formal'])}

改写强度：{intensity_descriptions.get(intensity, intensity_descriptions['medium'])}

改写要求：
1. 严格保持原文的核心意思和所有重要信息
2. 改写后的文本必须流畅自然，符合目标语言风格
3. 根据指定的改写强度进行相应程度的调整
4. 直接输出改写后的文本，不要添加任何解释、说明或标记
5. 保持文本的逻辑结构和段落划分

原始文本：
{self.text}

改写后的文本："""

            # 构建请求数据
            data = {
                "model": self.qwen3_model,
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "stream": False
            }

            # 调用Qwen3模型API
            headers = {'Content-type': 'application/json'}
            response = requests.post(self.qwen3_api_url,
                                   data=json.dumps(data),
                                   headers=headers,
                                   timeout=60)

            if response.status_code == 200:
                response_data = response.json()
                rewritten_text = response_data["message"]["content"].strip()

                # 清理输出
                rewritten_text = self._clean_rewrite_output(rewritten_text)

                return rewritten_text
            else:
                print(f"Qwen3 API请求失败，状态码: {response.status_code}")
                return self._basic_rewrite(style, intensity)

        except Exception as e:
            print(f"Qwen3改写失败: {e}")
            # 降级到基础改写方法
            return self._basic_rewrite(style, intensity)

    def _basic_rewrite(self, style: str, intensity: str) -> str:
        """基础改写方法"""
        try:
            sentences = self._split_sentences(self.text)
            rewritten_sentences = []

            for sentence in sentences:
                if not sentence.strip():
                    continue

                rewritten_sentence = self._rewrite_sentence(sentence, style, intensity)
                rewritten_sentences.append(rewritten_sentence)

            return ''.join(rewritten_sentences)

        except Exception as e:
            print(f"基础改写失败: {e}")
            return self.text

    def _rewrite_sentence(self, sentence: str, style: str, intensity: str) -> str:
        """改写单个句子"""
        # 基础的句子改写逻辑
        rewritten = sentence

        # 根据风格调整
        if style == 'formal':
            # 正式风格：使用更正式的词汇
            replacements = {
                '很': '非常',
                '挺': '相当',
                '特别': '尤其',
                '真的': '确实',
                '好的': '良好的',
                '不错': '优秀',
                '厉害': '出色'
            }
        elif style == 'casual':
            # 轻松风格：使用更口语化的表达
            replacements = {
                '非常': '很',
                '相当': '挺',
                '尤其': '特别',
                '确实': '真的',
                '良好的': '好的',
                '优秀': '不错',
                '出色': '厉害'
            }
        elif style == 'academic':
            # 学术风格：使用更专业的词汇
            replacements = {
                '显示': '表明',
                '说明': '阐述',
                '因为': '由于',
                '所以': '因此',
                '但是': '然而',
                '而且': '此外'
            }
        elif style == 'creative':
            # 创意风格：使用更生动的表达
            replacements = {
                '很大': '巨大',
                '很小': '微小',
                '很快': '迅速',
                '很慢': '缓慢',
                '很好': '绝佳',
                '很差': '糟糕'
            }
        elif style == 'concise':
            # 简洁风格：去除冗余词汇
            replacements = {
                '非常的': '',
                '十分的': '',
                '相当的': '',
                '比较的': '',
                '有一些': '一些',
                '进行了': '',
                '实施了': ''
            }
        else:
            replacements = {}

        # 应用替换
        for old, new in replacements.items():
            rewritten = rewritten.replace(old, new)

        # 根据强度调整
        if intensity == 'heavy':
            # 重度改写：尝试改变句式结构
            rewritten = self._restructure_sentence(rewritten)

        return rewritten

    def _restructure_sentence(self, sentence: str) -> str:
        """重构句子结构"""
        # 简单的句式变换
        if '，' in sentence:
            parts = sentence.split('，')
            if len(parts) == 2:
                # 尝试颠倒顺序
                return f"{parts[1]}，{parts[0]}"

        return sentence

    def _clean_rewrite_output(self, text: str) -> str:
        """清理改写输出"""
        # 移除可能的前缀
        prefixes_to_remove = [
            "改写后的文本：",
            "改写结果：",
            "重写后：",
            "修改后：",
            "改写：",
            "结果："
        ]

        for prefix in prefixes_to_remove:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()

        # 移除多余的引号
        text = text.strip('"').strip("'").strip()

        text = re.sub(
                        r'<think>.*?</think>',  # 非贪婪匹配任意字符
                        '',                     # 替换为空字符串
                        text, 
                        flags=re.DOTALL          # 使.匹配换行符
                    )

        return text

    def _segmented_rewrite(self, style: str, intensity: str, max_segment_length: int) -> str:
        """
        分段改写长文本

        Args:
            style: 改写风格
            intensity: 改写强度
            max_segment_length: 每段最大字符数

        Returns:
            改写后的完整文本
        """
        try:
            # 智能分段：优先按段落分割，然后按句子分割
            segments = self._smart_segment_text(self.text, max_segment_length)

            print(f"文本分为 {len(segments)} 段进行改写...")

            rewritten_segments = []

            for i, segment in enumerate(segments):
                if not segment.strip():
                    rewritten_segments.append(segment)
                    continue

                print(f"正在改写第 {i+1}/{len(segments)} 段...")

                # 为每个段落创建临时处理器实例或直接处理
                if self.qwen3_client:
                    rewritten_segment = self._qwen3_rewrite_segment(segment, style, intensity, i+1, len(segments))
                    rewritten_segment = re.sub(
                        r'<think>.*?</think>',  # 非贪婪匹配任意字符
                        '',                     # 替换为空字符串
                        rewritten_segment, 
                        flags=re.DOTALL          # 使.匹配换行符
                    )
                else:
                    rewritten_segment = self._basic_rewrite_segment(segment, style, intensity)

                rewritten_segments.append(rewritten_segment)

                # 添加短暂延迟，避免API请求过于频繁
                if self.qwen3_client and i < len(segments) - 1:
                    import time
                    time.sleep(0.5)

            # 合并所有改写后的段落
            result = ''.join(rewritten_segments)
            print("分段改写完成！")

            return result

        except Exception as e:
            print(f"分段改写失败: {e}")
            # 降级到基础改写
            return self._basic_rewrite(style, intensity)

    def _smart_segment_text(self, text: str, max_length: int) -> List[str]:
        """
        智能分段：优先保持段落和句子的完整性

        Args:
            text: 要分段的文本
            max_length: 每段最大长度

        Returns:
            分段后的文本列表
        """
        if len(text) <= max_length:
            return [text]

        segments = []

        # 首先按双换行符分割段落
        paragraphs = text.split('\n\n')

        current_segment = ""

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # 如果当前段落加上新段落不超过限制，直接添加
            if len(current_segment + '\n\n' + paragraph) <= max_length:
                if current_segment:
                    current_segment += '\n\n' + paragraph
                else:
                    current_segment = paragraph
            else:
                # 如果当前段落有内容，先保存
                if current_segment:
                    segments.append(current_segment)
                    current_segment = ""

                # 如果单个段落就超过限制，需要按句子分割
                if len(paragraph) > max_length:
                    sentence_segments = self._segment_by_sentences(paragraph, max_length)
                    segments.extend(sentence_segments)
                else:
                    current_segment = paragraph

        # 添加最后一段
        if current_segment:
            segments.append(current_segment)

        return segments

    def _segment_by_sentences(self, text: str, max_length: int) -> List[str]:
        """
        按句子分割文本

        Args:
            text: 要分割的文本
            max_length: 每段最大长度

        Returns:
            分割后的文本段落列表
        """
        sentences = self._split_sentences(text)
        segments = []
        current_segment = ""

        for sentence in sentences:
            if not sentence.strip():
                continue

            # 如果单个句子就超过限制，强制分割
            if len(sentence) > max_length:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = ""

                # 按字符强制分割
                for i in range(0, len(sentence), max_length):
                    segments.append(sentence[i:i+max_length])
            else:
                # 检查添加这个句子是否会超过限制
                if len(current_segment + sentence) <= max_length:
                    current_segment += sentence
                else:
                    if current_segment:
                        segments.append(current_segment)
                    current_segment = sentence

        if current_segment:
            segments.append(current_segment)

        return segments

    def _qwen3_rewrite_segment(self, segment: str, style: str, intensity: str,
                              segment_num: int, total_segments: int) -> str:
        """
        使用Qwen3模型改写单个文本段落

        Args:
            segment: 要改写的文本段落
            style: 改写风格
            intensity: 改写强度
            segment_num: 当前段落编号
            total_segments: 总段落数

        Returns:
            改写后的段落
        """
        try:
            # 读取提示词文件
            prompt_content = self._load_rewrite_prompt()

            # 构建改写风格描述
            style_descriptions = {
                'formal': '正式风格（Formal）- 使用正式、严谨的语言，适合商务文档、官方报告等场合',
                'casual': '口语化（Casual/Spoken）- 使用轻松、自然的口语表达，贴近日常对话',
                'academic': '学术风格（Academic）- 使用专业、严谨的学术语言，适合学术论文、研究报告',
                'creative': '文学化（Literary）- 使用富有创意、生动形象的文学表达',
                'concise': '简洁凝练（Concise）- 使用精炼、简洁的语言，去除冗余表达'
            }

            # 构建改写强度描述
            intensity_descriptions = {
                'light': '轻度改写 - 保持原文的句式结构，主要调整用词和表达方式，确保语言风格的转换',
                'medium': '中度改写 - 适度调整句式结构和表达方式，在保持原意的基础上进行较大程度的语言风格转换',
                'heavy': '重度改写 - 大幅改写句式和表达方式，用完全不同的语言风格重新表达相同的内容'
            }

            # 构建分段改写的特殊提示词
            content = f"""{prompt_content}

改写任务：
请将以下文本段落改写为：{style_descriptions.get(style, style_descriptions['formal'])}

改写强度：{intensity_descriptions.get(intensity, intensity_descriptions['medium'])}

特别说明：
- 这是第 {segment_num} 段，共 {total_segments} 段
- 请保持段落的独立性和完整性
- 确保改写后的段落能够与其他段落自然衔接
- 保持段落内部的逻辑结构

改写要求：
1. 严格保持原文的核心意思和所有重要信息
2. 改写后的文本必须流畅自然，符合目标语言风格
3. 根据指定的改写强度进行相应程度的调整
4. 直接输出改写后的文本，不要添加任何解释、说明或标记
5. 保持段落的逻辑结构和格式

原始文本段落：
{segment}

改写后的文本段落："""

            # 构建请求数据
            data = {
                "model": self.qwen3_model,
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "stream": False
            }

            # 调用Qwen3模型API
            headers = {'Content-type': 'application/json'}
            response = requests.post(self.qwen3_api_url,
                                   data=json.dumps(data),
                                   headers=headers,
                                   timeout=60)

            if response.status_code == 200:
                response_data = response.json()
                rewritten_text = response_data["message"]["content"].strip()

                # 清理输出
                rewritten_text = self._clean_rewrite_output(rewritten_text)

                return rewritten_text
            else:
                print(f"Qwen3 API请求失败，状态码: {response.status_code}")
                return self._basic_rewrite_segment(segment, style, intensity)

        except Exception as e:
            print(f"Qwen3段落改写失败: {e}")
            # 降级到基础改写方法
            return self._basic_rewrite_segment(segment, style, intensity)

    def _basic_rewrite_segment(self, segment: str, style: str, intensity: str) -> str:
        """
        基础方法改写单个文本段落

        Args:
            segment: 要改写的文本段落
            style: 改写风格
            intensity: 改写强度

        Returns:
            改写后的段落
        """
        try:
            sentences = self._split_sentences(segment)
            rewritten_sentences = []

            for sentence in sentences:
                if not sentence.strip():
                    continue

                rewritten_sentence = self._rewrite_sentence(sentence, style, intensity)
                rewritten_sentences.append(rewritten_sentence)

            return ''.join(rewritten_sentences)

        except Exception as e:
            print(f"基础段落改写失败: {e}")
            return segment

    def _load_rewrite_prompt(self) -> str:
        """加载改写提示词"""
        try:
            # 尝试从多个可能的路径读取prompt.txt
            possible_paths = [
                'prompt.txt',
                '../prompt.txt',
                '../../prompt.txt',
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompt.txt')
            ]

            for path in possible_paths:
                try:
                    if os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as f:
                            return f.read().strip()
                except Exception:
                    continue

            # 如果找不到文件，返回默认提示词
            return """角色设定：
你是一位语言风格专家，擅长根据不同需求对文本进行改写。你理解各种语言风格之间的区别，并能保留原文的核心含义，在不同风格下进行自然、流畅、符合语境的表达。

任务要求：
用户将提供一段原始文本，并指定希望的改写风格，你需要在保持原意的基础上，对文本进行改写，使其风格更贴近用户的要求。"""

        except Exception as e:
            print(f"加载提示词文件失败: {e}")
            return "你是一位语言风格专家，请根据用户要求对文本进行改写。"

    def _is_offline_mode(self) -> bool:
        """检测是否处于离线模式（无法连接到huggingface.co）"""
        try:
            import urllib.request
            import socket

            # 尝试连接huggingface.co，超时时间设为3秒
            socket.setdefaulttimeout(3)
            urllib.request.urlopen('https://huggingface.co', timeout=3)
            return False  # 能连接，不是离线模式
        except Exception:
            return True   # 无法连接，是离线模式

    def get_text_stats(self) -> Dict[str, any]:
        """
        获取文本统计信息

        Returns:
            包含各种统计信息的字典
        """
        if not self.text:
            return {}

        # 基础统计
        stats = {
            '字符总数': len(self.text),
            '字符数（不含空格）': len(self.text.replace(' ', '').replace('\n', '').replace('\t', '')),
            '行数': len(self.text.split('\n')),
            '段落数': len([p for p in self.text.split('\n\n') if p.strip()]),
        }

        # 句子统计
        sentences = self._split_sentences(self.text)
        stats['句子数'] = len([s for s in sentences if s.strip()])

        # 词汇统计
        try:
            word_freq = self.word_frequency()
            stats['词汇总数'] = sum(word_freq.values())
            stats['不重复词汇数'] = len(word_freq)
            if word_freq:
                stats['平均词频'] = round(sum(word_freq.values()) / len(word_freq), 2)
                stats['最高词频'] = max(word_freq.values())
        except Exception:
            stats['词汇总数'] = 0
            stats['不重复词汇数'] = 0

        # 平均长度统计
        if stats['句子数'] > 0:
            stats['平均句子长度'] = round(stats['字符总数'] / stats['句子数'], 2)

        return stats
