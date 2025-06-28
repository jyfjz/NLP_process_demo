# 中文文本处理和NLP分析工具

一个功能丰富的中文文本处理工具，提供Web界面和命令行两种使用方式，支持文本处理、NLP分析、情感分析等功能。

## 🌟 主要功能

### 基础文本处理
- **📝 文本输入**: 支持直接输入和文件上传
- **🔍 查找替换**: 支持普通文本和正则表达式查找替换
- **📊 词频统计**: 智能中文分词和词频分析，支持停用词过滤
- **📄 文本摘要**: 多种摘要算法（传统算法 + 大语言模型）

### 高级NLP功能
- **🧠 情感分析**: 多模型融合情感分析（深度学习模型 + SnowNLP + 词典方法）
- **🏷️ 实体识别**: 人名、地名、机构名等实体识别
- **🌳 句法分析**: 依存句法分析和词性标注
- **✂️ 中文分词**: 支持jieba和pkuseg多种分词工具

## 📁 项目结构

```
├── code_model/                    # 核心模块
│   ├── text_tools.py             # 核心文本处理和NLP分析类
│   ├── text_processor.py         # 命令行交互界面
│   └── stopwords.py              # 停用词处理
├── web_application/              # Web应用
│   ├── web_backend.py            # Flask后端API服务器
│   ├── start_web_app.py          # Web应用启动脚本（一键启动）
│   └── web_frontend/             # 前端文件夹
│       ├── index.html           # 主页面
│       ├── styles.css           # 样式文件
│       └── script.js            # JavaScript逻辑
├── test/                         # 测试和示例
│   ├── demo.py                  # 基础功能演示脚本
│   ├── demo_all_summary_methods.py  # 摘要方法对比演示
│   ├── test_complete_integration.py # 完整集成测试
│   ├── test_segmentation.py     # 分词功能测试
│   ├── test_qwen3_*.py          # Qwen3大模型相关测试
│   ├── test_frontend.html       # 前端界面测试页面
│   ├── sample_text.txt          # 示例文本文件
│   └── README.md                # 测试说明文档
├── hit_stopwords.txt             # 中文停用词列表
├── prompt.txt                    # 智能改写提示词模板
└── README.md                     # 主说明文档
```

## 🚀 快速开始

### Web应用（推荐）

**一键启动**：
```bash
python web_application/start_web_app.py
```

启动脚本会自动：
- 检查并安装必要依赖
- 启动Web服务器
- 自动打开浏览器访问 `http://localhost:5000`

### 命令行界面

```bash
python code_model/text_processor.py
```

### 依赖安装

**基础功能**（只需Python标准库）：
- 文本处理、查找替换、基础词频统计

**Web功能**（推荐安装）：
```bash
pip install flask flask-cors jieba snownlp
```

**高级NLP功能**（可选）：
```bash
# 深度学习情感分析和实体识别
pip install transformers torch stanza spacy textblob nltk

# 高级中文分词
pip install pkuseg

# 注意：某些库可能需要额外的系统依赖或模型下载
```

### 🤖 大语言模型功能（可选）

如需使用Qwen3等大语言模型进行智能摘要和改写：

**服务器端配置**（如使用autoDL等云服务）：
```bash
# 启动Ollama服务
ollama serve

# 拉取Qwen3模型
ollama pull qwen3:8b
```

**本地配置**：
```bash
# 建立SSH隧道连接到远程服务
# 确保localhost:6006可访问Qwen3 API
```

**API端点配置**：
- 默认端点：`http://localhost:6006/api/chat`
- 可在代码中修改为其他兼容的API端点

## 📖 使用指南

### Web界面功能

#### 📝 文本处理
- **文本输入**: 直接输入或上传txt文件
- **查找替换**: 支持正则表达式和普通文本查找替换
- **词频统计**: 中文智能分词，支持停用词过滤
- **文本摘要**: 多种算法生成摘要

#### 🧠 NLP分析
- **情感分析**: 多模型融合的中文情感分析
- **实体识别**: 识别人名、地名、机构名等
- **句法分析**: 词性标注和依存句法分析
- **智能摘要**: 支持传统算法和大语言模型
- **智能改写**: 基于Qwen3大模型的文本风格转换，支持分段处理

#### 🔧 实用工具
- **文本清理**: 去除空白行、修剪空格
- **统计信息**: 实时显示字符数、词数等
- **结果导出**: 支持复制和下载结果

## 💡 功能特色

### 🧠 多模型情感分析
- **深度学习模型**: UER中文RoBERTa等专业模型（权重35%）
- **中文专用**: SnowNLP中文情感分析（权重35%）
- **增强词典**: 支持否定词和程度副词（权重15%）
- **通用模型**: VADER、TextBlob作为补充（权重15%）
- **智能融合**: 多模型加权投票，提高准确性

### ✂️ 智能中文分词
- **jieba分词**: 快速准确的中文分词
- **pkuseg分词**: 支持多领域模型（新闻、网络、医学、旅游）
- **停用词过滤**: 使用哈工大停用词表
- **自定义词典**: 支持用户自定义分词

### 📄 多样化文本摘要
- **传统算法**: 基于词频、位置、混合方法
- **大语言模型**: 集成Qwen3等先进模型
- **智能选择**: 根据文本长度自动选择最佳算法

### ✏️ 智能文本改写
- **多种风格**: 正式、轻松、学术、创意、简洁风格
- **可调强度**: 轻度、中度、重度改写
- **分段处理**: 长文本智能分段，提高改写质量和稳定性
- **Qwen3驱动**: 基于先进大语言模型，保证改写质量

## 🔧 编程接口

### Python API示例

```python
from code_model.text_tools import TextProcessor

# 创建处理器
processor = TextProcessor()
processor.load_text("要分析的中文文本")

# 基础文本处理
new_text, count = processor.find_and_replace("查找内容", "替换内容")
top_words = processor.get_top_words(n=10)
summary = processor.generate_summary(num_sentences=3)

# NLP分析
sentiment_result = processor.analyze_sentiment()
entities = processor.recognize_entities()
syntax_result = processor.analyze_syntax()

# 智能改写
rewritten_text = processor.intelligent_rewrite(
    style='formal',           # 改写风格
    intensity='medium',       # 改写强度
    segment_mode=True,        # 启用分段模式
    max_segment_length=1000   # 每段最大字符数
)
```

### Web API接口

**基础文本处理**：
```bash
# 加载文本
POST /api/load_text
{"text": "要处理的文本"}

# 查找文本
POST /api/find_text
{"pattern": "查找内容", "use_regex": false, "case_sensitive": false}

# 替换文本
POST /api/replace_text
{"pattern": "查找内容", "replacement": "替换内容", "use_regex": false}

# 词频统计
POST /api/word_frequency
{"n": 20, "segmenter": "jieba", "use_stopwords": true}

# 文本分词
POST /api/segment_text
{"text": "要分词的文本", "segmenter": "jieba"}
```

**高级NLP分析**：
```bash
# 情感分析
POST /api/analyze_sentiment
{"text": "要分析的文本"}

# 实体识别
POST /api/extract_entities
{"text": "要分析的文本"}

# 句法分析
POST /api/analyze_syntax
{"text": "要分析的文本"}

# 文本摘要
POST /api/generate_summary
{"text": "要摘要的文本", "method": "hybrid", "num_sentences": 3}

# 智能改写
POST /api/intelligent_rewrite
{
  "style": "formal",
  "intensity": "medium",
  "segment_mode": true,
  "max_segment_length": 1000
}
```

**实用工具**：
```bash
# 停用词管理
POST /api/stopwords
{"words": ["自定义", "停用词"]}

POST /api/stopwords/clear
{}

# 导出结果
POST /api/export_results
{"format": "txt", "content": "要导出的内容"}

# 重置文本
POST /api/reset_text
{}
```

## 🧪 使用示例

### 情感分析示例

```python
from code_model.text_tools import TextProcessor

processor = TextProcessor()
text = "这个产品真的很棒，我非常喜欢！质量很好，服务也很周到。"
processor.load_text(text)

# 进行情感分析
result = processor.analyze_sentiment()
print(f"情感倾向: {result['sentiment']}")
print(f"置信度: {result['confidence']:.2f}")
print(f"使用模型: {result['methods_used']}")
```

### 实体识别示例

```python
text = "张三在北京大学学习，他来自上海市。"
processor.load_text(text)

entities = processor.recognize_entities()
for entity in entities['entities']:
    print(f"{entity['text']} - {entity['label']}")
# 输出: 张三 - PERSON, 北京大学 - ORG, 上海市 - GPE
```

### 智能摘要示例

```python
long_text = """
人工智能是计算机科学的一个分支，它企图了解智能的实质，
并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
机器学习是人工智能的一个重要分支，通过算法使机器能够从数据中学习。
深度学习是机器学习的一个子集，使用神经网络来模拟人脑的工作方式。
"""

processor.load_text(long_text)
summary = processor.generate_summary(num_sentences=2, method='hybrid')
print("摘要:", summary)
```

### 智能改写示例

```python
text = "这个产品真的很棒，我非常喜欢！质量很好，服务也很周到。"
processor.load_text(text)

# 改写为正式风格
formal_text = processor.intelligent_rewrite(
    style='formal',
    intensity='medium'
)
print("正式风格:", formal_text)

# 改写为学术风格（长文本分段处理）
long_text = "..." # 长文本
processor.load_text(long_text)
academic_text = processor.intelligent_rewrite(
    style='academic',
    intensity='heavy',
    segment_mode=True,
    max_segment_length=800
)
print("学术风格:", academic_text)
```

## 🛠️ 技术架构

### 系统架构
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端界面      │    │   Flask API     │    │   核心处理器    │
│  (Web/CLI)      │◄──►│   (REST API)    │◄──►│  (TextProcessor)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────────────────────┼─────────────────────────────────┐
                       │                                 │                                 │
                ┌─────────────┐                   ┌─────────────┐                 ┌─────────────┐
                │  基础文本   │                   │  NLP分析    │                 │  外部服务   │
                │  处理模块   │                   │  模块       │                 │  集成       │
                └─────────────┘                   └─────────────┘                 └─────────────┘
                       │                                 │                                 │
            ┌──────────┼──────────┐               ┌──────┼──────┐                 ┌──────┼──────┐
            │          │          │               │      │      │                 │      │      │
        ┌───────┐ ┌───────┐ ┌───────┐      ┌───────┐ ┌───────┐ ┌───────┐    ┌───────┐ ┌───────┐
        │查找替换│ │词频统计│ │文本摘要│      │情感分析│ │实体识别│ │句法分析│    │Qwen3  │ │停用词 │
        └───────┘ └───────┘ └───────┘      └───────┘ └───────┘ └───────┘    │大模型 │ │词典  │
                                                                            └───────┘ └───────┘
```

### 核心技术栈
- **后端框架**: Flask + Flask-CORS
- **核心语言**: Python 3.7+
- **中文分词**: jieba、pkuseg
- **深度学习**: transformers、torch
- **传统NLP**: SnowNLP、TextBlob、NLTK、Stanza
- **大语言模型**: Qwen3 (通过Ollama API)

### 前端技术
- **界面技术**: HTML5、CSS3、JavaScript
- **响应式设计**: 自适应布局
- **图标库**: Font Awesome
- **交互体验**: 实时反馈、进度提示

### 设计理念
- **模块化设计**: 功能独立，便于维护和扩展
- **渐进增强**: 基础功能稳定，高级功能可选
- **多模型融合**: 结合传统方法和深度学习优势
- **用户友好**: 提供Web界面和命令行两种交互方式

## 📋 依赖说明

### 核心依赖（必需）
```bash
# Web框架和基础NLP
pip install flask flask-cors jieba snownlp
```

### 高级NLP功能（可选）
```bash
# 深度学习模型
pip install transformers torch

# 多语言NLP工具
pip install stanza spacy textblob nltk

# 高级中文分词
pip install pkuseg

# 注意事项：
# 1. 某些库可能需要下载预训练模型
# 2. Windows用户安装pkuseg可能需要Visual C++构建工具
# 3. GPU版本的torch需要根据CUDA版本选择对应版本
```

### 兼容性说明
- **Python版本**：推荐Python 3.7+
- **操作系统**：支持Windows、macOS、Linux
- **内存要求**：基础功能512MB，高级NLP功能建议2GB+
- **网络要求**：首次使用高级功能时需要下载模型文件

## ✨ 项目特色

### 🎯 专注中文处理
- 针对中文文本优化的分词和分析算法
- 支持中文停用词过滤
- 多种中文情感分析模型

### 🧠 智能分析
- 多模型融合提高分析准确性
- 深度学习模型与传统方法结合
- 智能权重分配和结果融合

### 🌐 易于使用
- 现代化Web界面，无需安装客户端
- 一键启动，自动依赖检查
- 支持文件上传和在线编辑

## 🧪 测试和演示

项目提供了丰富的测试脚本和演示程序：

### 快速演示
```bash
# 基础功能演示
python test/demo.py

# 摘要方法对比演示
python test/demo_all_summary_methods.py

# 完整集成测试
python test/test_complete_integration.py
```

### 专项测试
```bash
# 分词功能测试
python test/test_segmentation.py

# Qwen3大模型测试
python test/test_qwen3_simple.py

# 前端界面预览
# 在浏览器中打开 test/test_frontend.html
```

详细的测试说明请参考 [`test/README.md`](test/README.md)

## 🔧 故障排除

### 常见问题

**1. 依赖安装失败**
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ package_name
```

**2. 模型下载失败**
- 检查网络连接
- 使用VPN或代理
- 手动下载模型文件

**3. pkuseg安装失败（Windows）**
```bash
# 安装Visual C++构建工具
# 或使用预编译版本
pip install pkuseg-python
```

**4. Qwen3连接失败**
- 检查Ollama服务状态
- 确认端口6006可访问
- 验证模型是否正确加载

### 性能优化建议

- **大文本处理**：启用分段模式，设置合适的段落长度
- **批量处理**：使用命令行界面，避免重复加载模型
- **内存优化**：处理完成后及时清理，避免同时加载多个大模型

---

**感谢使用中文文本处理和NLP分析工具！** 🎉

> 本项目专为中文文本处理和自然语言处理分析而设计，提供了从基础文本操作到高级NLP分析的完整解决方案。无论您是研究人员、开发者还是普通用户，都能在这里找到适合的文本处理工具。

**项目特色**：
- 🎯 **专注中文**：针对中文文本特点优化
- 🧠 **智能分析**：多模型融合，提高准确性
- 🌐 **易于使用**：Web界面 + 命令行，满足不同需求
- 🔧 **高度可扩展**：模块化设计，便于二次开发

**适用场景**：
- 📚 学术研究和论文分析
- 📰 新闻文本处理和摘要
- 💼 商务文档智能处理
- 🎓 中文NLP教学和学习
- 🔍 文本挖掘和数据分析
