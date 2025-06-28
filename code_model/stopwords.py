#!/usr/bin/env python3
"""
停用词管理模块
"""

import os

def load_hit_stopwords():
    """加载哈工大停用词表"""
    stopwords = set()

    # 尝试从多个可能的路径加载停用词文件
    possible_paths = [
        'hit_stopwords.txt',  # 当前目录
        '../hit_stopwords.txt',  # 上级目录
        '../../hit_stopwords.txt',  # 上上级目录
        os.path.join(os.path.dirname(__file__), '..', 'hit_stopwords.txt'),  # 相对于当前文件的上级目录
        os.path.join(os.path.dirname(__file__), '..', '..', 'hit_stopwords.txt'),  # 相对于当前文件的上上级目录
    ]

    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        word = line.strip()
                        if word and not word.startswith('#'):  # 忽略空行和注释
                            stopwords.add(word)
                print(f"成功加载停用词表: {path}，共 {len(stopwords)} 个停用词")
                return stopwords
        except Exception as e:
            print(f"加载停用词表失败 {path}: {e}")
            continue

    print("警告：未能加载停用词表文件，使用内置停用词")
    return get_builtin_chinese_stopwords()

def get_builtin_chinese_stopwords():
    """获取内置的中文停用词表（作为备用）"""
    return {
        # 代词
        '我', '你', '他', '她', '它', '我们', '你们', '他们', '她们', '它们',
        '这', '那', '这个', '那个', '这些', '那些', '这里', '那里', '这样', '那样',
        '自己', '大家', '别人', '人家', '咱们', '本人', '某人', '谁', '什么', '哪',
        '哪个', '哪些', '哪里', '怎么', '怎样', '如何', '为什么', '多少', '几',
    
    # 助词
    '的', '地', '得', '着', '了', '过', '起来', '下去', '出来', '进去',
    '上去', '下来', '起', '来', '去', '出', '进', '上', '下', '回',
    
    # 介词
    '在', '于', '从', '到', '向', '往', '朝', '对', '对于', '关于', '按照',
    '根据', '通过', '经过', '由于', '因为', '为了', '以便', '以免', '除了',
    '除非', '如果', '假如', '要是', '倘若', '万一', '只要', '只有', '无论',
    '不管', '尽管', '虽然', '即使', '哪怕', '既然', '由于', '因此', '所以',
    
    # 连词
    '和', '与', '同', '跟', '以及', '还有', '或者', '或', '要么', '不是',
    '而是', '不但', '不仅', '而且', '并且', '同时', '另外', '此外', '然而',
    '但是', '可是', '不过', '只是', '却', '反而', '相反', '否则', '不然',
    
    # 副词
    '很', '非常', '特别', '十分', '相当', '比较', '更', '最', '太', '极',
    '挺', '蛮', '颇', '相当', '还', '也', '都', '又', '再', '就', '才',
    '刚', '刚才', '马上', '立刻', '立即', '赶紧', '赶快', '快', '慢', '早',
    '晚', '先', '后', '前', '后来', '然后', '接着', '于是', '因此', '所以',
    '总之', '总的来说', '一般来说', '通常', '往往', '经常', '常常', '总是',
    '从来', '从不', '永远', '始终', '一直', '一向', '向来', '素来', '历来',
    
    # 量词
    '个', '位', '名', '只', '头', '条', '匹', '张', '间', '座', '栋', '幢',
    '层', '套', '件', '双', '对', '副', '顶', '把', '支', '根', '枝', '朵',
    '颗', '粒', '滴', '片', '块', '团', '堆', '群', '批', '些', '点', '丝',
    
    # 数词
    '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千',
    '万', '亿', '零', '两', '半', '第一', '第二', '第三', '首先', '其次',
    '再次', '最后', '另一', '每', '各', '全', '整', '所有', '任何', '某',
    
    # 时间词
    '今天', '昨天', '明天', '前天', '后天', '现在', '刚才', '以前', '以后',
    '将来', '过去', '当时', '那时', '这时', '同时', '平时', '有时', '时候',
    '时间', '年', '月', '日', '天', '小时', '分钟', '秒', '早上', '上午',
    '中午', '下午', '晚上', '夜里', '深夜', '凌晨', '白天', '黑夜',
    
    # 语气词
    '啊', '呀', '哎', '哦', '嗯', '呢', '吧', '吗', '呗', '嘛', '哪', '呐',
    '嘿', '喂', '哟', '咦', '哇', '唉', '哼', '嘘', '咳', '唔', '嗨',
    
    # 标点符号（虽然通常会被过滤，但以防万一）
    '，', '。', '！', '？', '；', '：', '"', '"', ''', ''', '（', '）',
    '【', '】', '《', '》', '、', '…', '——', '—', '·', '～', '~',
    
    # 常用虚词
    '是', '不是', '有', '没有', '会', '不会', '能', '不能', '可以', '不可以',
    '应该', '不应该', '必须', '不必', '需要', '不需要', '想', '不想', '要',
    '不要', '愿意', '不愿意', '希望', '不希望', '喜欢', '不喜欢', '讨厌',
    
    # 程度词
    '比较', '相对', '绝对', '完全', '彻底', '基本', '大致', '大概', '差不多',
    '几乎', '将近', '接近', '约', '大约', '左右', '上下', '多', '少', '更多',
    '更少', '足够', '不够', '过多', '过少', '太多', '太少', '许多', '很多',
    
    # 其他常用词
    '等', '等等', '之类', '什么的', '以及', '还是', '或者', '无论', '不管',
    '如果', '假如', '要是', '倘若', '万一', '只要', '只有', '除非', '即使',
    '尽管', '虽然', '但是', '可是', '然而', '不过', '只是', '却', '反而',
    '相反', '否则', '不然', '因此', '所以', '于是', '然后', '接着', '后来',
    '最后', '总之', '总的来说', '一般来说', '通常', '往往', '经常', '常常',
    '总是', '从来', '从不', '永远', '始终', '一直', '一向', '向来', '素来',
    '历来', '曾经', '已经', '正在', '将要', '即将', '马上', '立刻', '立即',
    '赶紧', '赶快', '快', '慢', '早', '晚', '先', '后', '前', '中', '内',
    '外', '里', '外面', '里面', '上面', '下面', '前面', '后面', '左边',
    '右边', '旁边', '附近', '周围', '四周', '到处', '处处', '各处', '某处',
    '何处', '此处', '彼处', '别处', '他处', '远处', '近处', '高处', '低处',
    '深处', '浅处', '暗处', '明处', '当地', '本地', '外地', '异地', '各地',
    '全国', '国内', '国外', '海外', '境内', '境外', '省内', '省外', '市内',
    '市外', '县内', '县外', '区内', '区外', '校内', '校外', '院内', '院外',
    '室内', '室外', '屋内', '屋外', '家里', '家外', '店内', '店外', '车内',
    '车外', '船内', '船外', '机内', '机外'
    }

# 英文常用停用词表
ENGLISH_STOPWORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'been', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to',
    'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have', 'had', 'what',
    'said', 'each', 'which', 'she', 'do', 'how', 'their', 'if', 'up', 'out',
    'many', 'then', 'them', 'these', 'so', 'some', 'her', 'would', 'make',
    'like', 'into', 'him', 'time', 'two', 'more', 'go', 'no', 'way', 'could',
    'my', 'than', 'first', 'been', 'call', 'who', 'oil', 'sit', 'now', 'find',
    'down', 'day', 'did', 'get', 'come', 'made', 'may', 'part', 'over', 'new',
    'sound', 'take', 'only', 'little', 'work', 'know', 'place', 'year', 'live',
    'me', 'back', 'give', 'most', 'very', 'after', 'thing', 'our', 'just',
    'name', 'good', 'sentence', 'man', 'think', 'say', 'great', 'where', 'help',
    'through', 'much', 'before', 'line', 'right', 'too', 'mean', 'old', 'any',
    'same', 'tell', 'boy', 'follow', 'came', 'want', 'show', 'also', 'around',
    'form', 'three', 'small', 'set', 'put', 'end', 'why', 'again', 'turn',
    'here', 'off', 'went', 'old', 'number', 'great', 'tell', 'men', 'say',
    'small', 'every', 'found', 'still', 'between', 'mane', 'should', 'home',
    'big', 'give', 'air', 'line', 'set', 'own', 'under', 'read', 'last',
    'never', 'us', 'left', 'end', 'along', 'while', 'might', 'next', 'sound',
    'below', 'saw', 'something', 'thought', 'both', 'few', 'those', 'always',
    'looked', 'show', 'large', 'often', 'together', 'asked', 'house', 'don',
    'world', 'going', 'want', 'school', 'important', 'until', 'form', 'food',
    'keep', 'children', 'feet', 'land', 'side', 'without', 'boy', 'once',
    'animal', 'life', 'enough', 'took', 'sometimes', 'four', 'head', 'above',
    'kind', 'began', 'almost', 'live', 'page', 'got', 'earth', 'need', 'far',
    'hand', 'high', 'year', 'mother', 'light', 'country', 'father', 'let',
    'night', 'picture', 'being', 'study', 'second', 'soon', 'story', 'since',
    'white', 'ever', 'paper', 'hard', 'near', 'sentence', 'better', 'best',
    'across', 'during', 'today', 'however', 'sure', 'knew', 'it\'s', 'try',
    'told', 'young', 'sun', 'thing', 'whole', 'hear', 'example', 'heard',
    'several', 'change', 'answer', 'room', 'sea', 'against', 'top', 'turned',
    'learn', 'point', 'city', 'play', 'toward', 'five', 'himself', 'usually',
    'money', 'seen', 'didn', 'car', 'morning', 'i\'m', 'body', 'upon', 'family',
    'later', 'turn', 'move', 'face', 'door', 'cut', 'done', 'group', 'true',
    'leave', 'color', 'red', 'friend', 'pretty', 'eat', 'front', 'feel',
    'fact', 'hand', 'week', 'eye', 'been', 'word', 'great', 'such', 'make',
    'even', 'here', 'old', 'any', 'after', 'us', 'two', 'how', 'our', 'out',
    'day', 'get', 'use', 'man', 'new', 'now', 'way', 'may', 'say'
}

class StopwordsManager:
    """停用词管理器"""

    def __init__(self):
        # 加载哈工大停用词表作为中文停用词
        self.chinese_stopwords = load_hit_stopwords()
        self.english_stopwords = ENGLISH_STOPWORDS.copy()
        self.custom_stopwords = set()
    
    def add_custom_stopwords(self, words):
        """添加自定义停用词"""
        if isinstance(words, str):
            words = [words]
        for word in words:
            self.custom_stopwords.add(word.strip())
    
    def remove_custom_stopwords(self, words):
        """移除自定义停用词"""
        if isinstance(words, str):
            words = [words]
        for word in words:
            self.custom_stopwords.discard(word.strip())
    
    def clear_custom_stopwords(self):
        """清空自定义停用词"""
        self.custom_stopwords.clear()
    
    def get_all_stopwords(self):
        """获取所有停用词（包括默认和自定义）"""
        return self.chinese_stopwords | self.english_stopwords | self.custom_stopwords
    
    def is_stopword(self, word):
        """判断是否为停用词"""
        return word in self.get_all_stopwords()
    
    def filter_stopwords(self, words):
        """过滤停用词"""
        stopwords = self.get_all_stopwords()
        return [word for word in words if word not in stopwords]
    
    def get_custom_stopwords(self):
        """获取自定义停用词列表"""
        return list(self.custom_stopwords)
