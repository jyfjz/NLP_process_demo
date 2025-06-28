#!/usr/bin/env python3
"""
文本处理工具 - Web后端API
使用Flask提供RESTful API接口
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import sys
from datetime import datetime

# 添加父目录到路径，以便导入code_model模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code_model.text_tools import TextProcessor

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局文本处理器实例
processor = TextProcessor()

@app.route('/')
def index():
    """返回前端页面"""
    return send_from_directory('web_frontend', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件"""
    return send_from_directory('web_frontend', filename)

@app.route('/api/load_text', methods=['POST'])
def load_text():
    """加载文本"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        processor.load_text(text)
        
        # 返回文本统计信息
        stats = processor.get_text_stats()
        
        return jsonify({
            'success': True,
            'message': '文本加载成功',
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/find_text', methods=['POST'])
def find_text():
    """查找文本"""
    try:
        data = request.get_json()
        pattern = data.get('pattern', '')
        use_regex = data.get('use_regex', False)
        case_sensitive = data.get('case_sensitive', True)
        
        if not pattern:
            return jsonify({
                'success': False,
                'error': '查找内容不能为空'
            }), 400
        
        matches = processor.find_matches(pattern, use_regex, case_sensitive)
        
        # 格式化匹配结果
        formatted_matches = []
        for pos, match in matches:
            # 获取上下文
            context_length = 30
            start = max(0, pos - context_length)
            end = min(len(processor.text), pos + len(match) + context_length)

            before = processor.text[start:pos]
            after = processor.text[pos + len(match):end]

            formatted_matches.append({
                'index': pos,
                'match': match,
                'context': {
                    'before': before,
                    'match': match,
                    'after': after
                }
            })
        
        return jsonify({
            'success': True,
            'matches': formatted_matches,
            'count': len(matches)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/replace_text', methods=['POST'])
def replace_text():
    """替换文本"""
    try:
        data = request.get_json()
        pattern = data.get('pattern', '')
        replacement = data.get('replacement', '')
        use_regex = data.get('use_regex', False)
        case_sensitive = data.get('case_sensitive', True)

        if not pattern:
            return jsonify({
                'success': False,
                'error': '查找内容不能为空'
            }), 400

        new_text, count = processor.find_and_replace(
            pattern, replacement, use_regex, case_sensitive)

        return jsonify({
            'success': True,
            'new_text': new_text,
            'count': count,
            'message': f'成功替换 {count} 处'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/selective_replace', methods=['POST'])
def selective_replace():
    """选择性替换文本"""
    try:
        data = request.get_json()
        pattern = data.get('pattern', '')
        replacement = data.get('replacement', '')
        indices = data.get('indices', [])  # 要替换的匹配项索引列表
        use_regex = data.get('use_regex', False)
        case_sensitive = data.get('case_sensitive', True)

        if not pattern:
            return jsonify({
                'success': False,
                'error': '查找内容不能为空'
            }), 400

        if not indices:
            return jsonify({
                'success': False,
                'error': '请选择要替换的匹配项'
            }), 400

        # 首先找到所有匹配项
        matches = processor.find_matches(pattern, use_regex, case_sensitive)

        if not matches:
            return jsonify({
                'success': False,
                'error': '没有找到匹配项'
            }), 400

        # 验证索引
        valid_indices = [i for i in indices if 0 <= i < len(matches)]
        if not valid_indices:
            return jsonify({
                'success': False,
                'error': '没有有效的匹配项索引'
            }), 400

        # 按位置倒序排列，从后往前替换，避免位置偏移
        selected_matches = [(matches[i][0], matches[i][1]) for i in sorted(valid_indices, reverse=True)]

        new_text = processor.text
        count = 0

        for pos, match_text in selected_matches:
            start_pos = pos
            end_pos = start_pos + len(match_text)
            new_text = new_text[:start_pos] + replacement + new_text[end_pos:]
            count += 1

        # 更新处理器中的文本
        processor.load_text(new_text)

        return jsonify({
            'success': True,
            'new_text': new_text,
            'count': count,
            'message': f'成功替换 {count} 个选中的匹配项'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/word_frequency', methods=['POST'])
def word_frequency():
    """词频统计（支持智能分词）"""
    try:
        data = request.get_json()
        n = data.get('n', 20)
        ignore_case = data.get('ignore_case', True)
        min_word_length = data.get('min_word_length', 1)
        exclude_punctuation = data.get('exclude_punctuation', True)
        exclude_stopwords = data.get('exclude_stopwords', True)
        exclude_numbers = data.get('exclude_numbers', True)
        exclude_single_chars = data.get('exclude_single_chars', True)
        segmentation_method = data.get('segmentation_method', 'auto')

        top_words = processor.get_top_words(
            n=n,
            ignore_case=ignore_case,
            min_word_length=min_word_length,
            exclude_punctuation=exclude_punctuation,
            exclude_stopwords=exclude_stopwords,
            exclude_numbers=exclude_numbers,
            exclude_single_chars=exclude_single_chars,
            segmentation_method=segmentation_method
        )

        return jsonify({
            'success': True,
            'word_frequency': top_words,
            'segmentation_method': segmentation_method,
            'exclude_stopwords': exclude_stopwords
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/segment_text', methods=['POST'])
def segment_text():
    """文本分词"""
    try:
        data = request.get_json()
        text = data.get('text', processor.text)
        method = data.get('method', 'auto')
        mode = data.get('mode', 'accurate')
        with_pos = data.get('with_pos', False)

        if not text:
            return jsonify({
                'success': False,
                'error': '文本内容不能为空'
            }), 400

        # 直接使用全局处理器进行分词
        segments = processor.segment_text(
            text=text,
            method=method,
            mode=mode,
            with_pos=with_pos
        )

        return jsonify({
            'success': True,
            'segments': segments,
            'method': method,
            'mode': mode,
            'with_pos': with_pos
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/generate_summary', methods=['POST'])
def generate_summary():
    """生成摘要"""
    try:
        data = request.get_json()
        num_sentences = data.get('num_sentences', 3)
        method = data.get('method', 'hybrid')
        title = data.get('title', '')  # 添加标题参数支持

        # 根据方法决定是否传递标题参数
        if method in ['textteaser', 'qwen3']:
            summary = processor.generate_summary(num_sentences, method, title)
        else:
            summary = processor.generate_summary(num_sentences, method)

        return jsonify({
            'success': True,
            'summary': summary,
            'method': method,
            'title': title
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/text_stats', methods=['GET'])
def text_stats():
    """获取文本统计信息"""
    try:
        stats = processor.get_text_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/reset_text', methods=['POST'])
def reset_text():
    """重置文本"""
    try:
        processor.reset_text()
        stats = processor.get_text_stats()
        
        return jsonify({
            'success': True,
            'text': processor.text,
            'stats': stats,
            'message': '文本已重置'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# 新增高级NLP功能API

@app.route('/api/extract_entities', methods=['POST'])
def extract_entities():
    """实体识别"""
    try:
        data = request.get_json()
        text = data.get('text', processor.text)
        method = data.get('method', 'hybrid')  # 默认使用混合方法
        deduplicate = data.get('deduplicate', True)  # 默认启用去重

        if not text:
            return jsonify({
                'success': False,
                'error': '文本内容不能为空'
            }), 400

        # 使用指定方法进行实体识别
        entities = processor.extract_entities(text, method=method, deduplicate=deduplicate)

        return jsonify({
            'success': True,
            'entities': entities['entities'],
            'model_used': entities['model_used'],
            'available': entities['available'],
            'method': method,
            'deduplicated': entities.get('deduplicated', False)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    """情感分析"""
    try:
        data = request.get_json()
        text = data.get('text', processor.text)

        if not text:
            return jsonify({
                'success': False,
                'error': '文本内容不能为空'
            }), 400

        # 直接使用全局处理器进行分析
        sentiment = processor.analyze_sentiment(text)

        return jsonify({
            'success': True,
            'sentiment': sentiment['sentiment'],
            'scores': sentiment['scores'],
            'methods_used': sentiment['methods_used'],
            'available': sentiment['available'],
            'confidence': sentiment.get('confidence', 0.0),
            'ensemble_details': sentiment.get('ensemble_details', None),
            'model_details': sentiment.get('model_details', {})
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/analyze_syntax', methods=['POST'])
def analyze_syntax():
    """句法分析"""
    try:
        data = request.get_json()
        text = data.get('text', processor.text)

        if not text:
            return jsonify({
                'success': False,
                'error': '文本内容不能为空'
            }), 400

        # 直接使用全局处理器进行分析
        syntax = processor.analyze_syntax(text)

        return jsonify({
            'success': True,
            'sentences': syntax['sentences'],
            'model_used': syntax['model_used'],
            'available': syntax['available']
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/intelligent_rewrite', methods=['POST'])
def intelligent_rewrite():
    """智能改写（支持分段处理）"""
    try:
        data = request.get_json()
        style = data.get('style', 'formal')
        intensity = data.get('intensity', 'medium')
        segment_mode = data.get('segment_mode', True)  # 默认启用分段模式
        max_segment_length = data.get('max_segment_length', 1000)  # 默认每段1000字符

        if not processor.text:
            return jsonify({
                'success': False,
                'error': '请先加载文本'
            }), 400

        # 检查文本长度，给出建议
        text_length = len(processor.text)
        use_segmentation = segment_mode and text_length > max_segment_length

        rewritten_text = processor.intelligent_rewrite(
            style=style,
            intensity=intensity,
            segment_mode=segment_mode,
            max_segment_length=max_segment_length
        )

        return jsonify({
            'success': True,
            'rewritten_text': rewritten_text,
            'style': style,
            'intensity': intensity,
            'text_length': text_length,
            'used_segmentation': use_segmentation,
            'segment_info': {
                'enabled': segment_mode,
                'max_length': max_segment_length,
                'recommended': text_length > 500  # 建议超过500字符使用分段
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/nlp_capabilities', methods=['GET'])
def nlp_capabilities():
    """获取NLP功能可用性"""
    try:
        capabilities = processor.get_nlp_capabilities()

        return jsonify({
            'success': True,
            'capabilities': capabilities
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/advanced_analysis', methods=['POST'])
def advanced_analysis():
    """高级文本分析（保留原有功能）"""
    try:
        data = request.get_json()
        analysis_type = data.get('type', 'sentiment')

        if analysis_type == 'sentiment':
            # 使用新的情感分析功能
            sentiment = processor.analyze_sentiment()
            if sentiment['available']:
                return jsonify({
                    'success': True,
                    'sentiment': sentiment['sentiment'],
                    'scores': sentiment['scores'],
                    'methods_used': sentiment['methods_used']
                })
            else:
                # 降级到简单版本
                text = processor.text.lower()
                positive_words = ['好', '棒', '优秀', '喜欢', '满意', '成功', '快乐', '美好']
                negative_words = ['坏', '差', '糟糕', '讨厌', '失败', '难过', '痛苦', '问题']

                positive_count = sum(1 for word in positive_words if word in text)
                negative_count = sum(1 for word in negative_words if word in text)

                if positive_count > negative_count:
                    sentiment = '积极'
                    score = positive_count / (positive_count + negative_count + 1)
                elif negative_count > positive_count:
                    sentiment = '消极'
                    score = negative_count / (positive_count + negative_count + 1)
                else:
                    sentiment = '中性'
                    score = 0.5

                return jsonify({
                    'success': True,
                    'sentiment': sentiment,
                    'score': score,
                    'positive_count': positive_count,
                    'negative_count': negative_count
                })



        else:
            return jsonify({
                'success': False,
                'error': '不支持的分析类型'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stopwords', methods=['GET'])
def get_stopwords():
    """获取自定义停用词列表"""
    try:
        custom_stopwords = processor.get_custom_stopwords()
        return jsonify({
            'success': True,
            'custom_stopwords': custom_stopwords
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stopwords', methods=['POST'])
def add_stopwords():
    """添加自定义停用词"""
    try:
        data = request.get_json()
        words = data.get('words', [])

        if isinstance(words, str):
            # 支持多种分隔符：中文逗号、英文逗号、分号、空格等
            import re
            words = re.split(r'[,，;；\s]+', words)
            words = [word.strip() for word in words if word.strip()]
        elif isinstance(words, list):
            # 确保列表中的每个词都是字符串且去除空白
            words = [str(word).strip() for word in words if str(word).strip()]

        if not words:
            return jsonify({
                'success': False,
                'error': '请提供有效的停用词'
            }), 400

        processor.add_custom_stopwords(words)

        return jsonify({
            'success': True,
            'message': f'已添加 {len(words)} 个停用词',
            'added_words': words
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stopwords', methods=['DELETE'])
def remove_stopwords():
    """移除自定义停用词"""
    try:
        data = request.get_json()
        words = data.get('words', [])

        if isinstance(words, str):
            # 支持多种分隔符
            import re
            words = re.split(r'[,，;；\s]+', words)
            words = [word.strip() for word in words if word.strip()]
        elif isinstance(words, list):
            words = [str(word).strip() for word in words if str(word).strip()]

        if not words:
            return jsonify({
                'success': False,
                'error': '请提供要移除的停用词'
            }), 400

        processor.remove_custom_stopwords(words)

        return jsonify({
            'success': True,
            'message': f'已移除 {len(words)} 个停用词',
            'removed_words': words
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/stopwords/clear', methods=['POST'])
def clear_stopwords():
    """清空自定义停用词"""
    try:
        processor.clear_custom_stopwords()
        return jsonify({
            'success': True,
            'message': '已清空所有自定义停用词'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/export_results', methods=['POST'])
def export_results():
    """导出处理结果"""
    try:
        data = request.get_json()
        export_format = data.get('format', 'txt')
        include_original = data.get('include_original', True)
        include_results = data.get('include_results', True)
        include_stats = data.get('include_stats', False)
        include_metadata = data.get('include_metadata', False)
        filename = data.get('filename', '')

        # 收集要导出的数据
        export_data = {}

        if include_original and processor.text:
            export_data['original_text'] = processor.text

        if include_stats and processor.text:
            export_data['statistics'] = processor.get_text_stats()

        if include_metadata:
            export_data['metadata'] = {
                'export_time': datetime.now().isoformat(),
                'export_format': export_format,
                'text_length': len(processor.text) if processor.text else 0
            }

        # 生成文件名
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'text_analysis_results_{timestamp}'

        # 根据格式生成内容
        if export_format == 'txt':
            content = generate_txt_export(export_data, include_results)
            mimetype = 'text/plain'
            extension = '.txt'
        elif export_format == 'json':
            content = generate_json_export(export_data, include_results)
            mimetype = 'application/json'
            extension = '.json'
        elif export_format == 'csv':
            content = generate_csv_export(export_data, include_results)
            mimetype = 'text/csv'
            extension = '.csv'
        elif export_format == 'html':
            content = generate_html_export(export_data, include_results)
            mimetype = 'text/html'
            extension = '.html'
        else:
            return jsonify({
                'success': False,
                'error': '不支持的导出格式'
            }), 400

        return jsonify({
            'success': True,
            'content': content,
            'filename': filename + extension,
            'mimetype': mimetype
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def generate_txt_export(export_data, include_results):
    """生成TXT格式导出"""
    lines = []
    lines.append("=" * 50)
    lines.append("文本分析结果导出")
    lines.append("=" * 50)

    if 'metadata' in export_data:
        lines.append(f"导出时间: {export_data['metadata']['export_time']}")
        lines.append(f"文本长度: {export_data['metadata']['text_length']} 字符")
        lines.append("")

    if 'original_text' in export_data:
        lines.append("原始文本:")
        lines.append("-" * 20)
        lines.append(export_data['original_text'])
        lines.append("")

    if 'statistics' in export_data:
        lines.append("文本统计:")
        lines.append("-" * 20)
        for key, value in export_data['statistics'].items():
            lines.append(f"{key}: {value}")
        lines.append("")

    return '\n'.join(lines)

def generate_json_export(export_data, include_results):
    """生成JSON格式导出"""
    import json
    return json.dumps(export_data, ensure_ascii=False, indent=2)

def generate_csv_export(export_data, include_results):
    """生成CSV格式导出"""
    lines = []
    lines.append("项目,内容")

    if 'original_text' in export_data:
        # CSV中需要处理换行符和引号
        text = export_data['original_text'].replace('"', '""').replace('\n', '\\n')
        lines.append(f'"原始文本","{text}"')

    if 'statistics' in export_data:
        for key, value in export_data['statistics'].items():
            lines.append(f'"{key}","{value}"')

    return '\n'.join(lines)

def generate_html_export(export_data, include_results):
    """生成HTML格式导出"""
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文本分析结果</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
        .header { border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }
        .section { margin-bottom: 30px; }
        .section h2 { color: #333; border-left: 4px solid #007bff; padding-left: 10px; }
        .original-text { background: #f8f9fa; padding: 15px; border-radius: 5px; white-space: pre-wrap; }
        .stats-table { border-collapse: collapse; width: 100%; }
        .stats-table th, .stats-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .stats-table th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>文本分析结果</h1>"""

    if 'metadata' in export_data:
        html += f"<p>导出时间: {export_data['metadata']['export_time']}</p>"

    html += "</div>"

    if 'original_text' in export_data:
        html += f"""
    <div class="section">
        <h2>原始文本</h2>
        <div class="original-text">{export_data['original_text']}</div>
    </div>"""

    if 'statistics' in export_data:
        html += """
    <div class="section">
        <h2>文本统计</h2>
        <table class="stats-table">
            <tr><th>项目</th><th>数值</th></tr>"""

        for key, value in export_data['statistics'].items():
            html += f"<tr><td>{key}</td><td>{value}</td></tr>"

        html += "</table></div>"

    html += "</body></html>"
    return html

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': '接口不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    # 确保前端文件夹存在
    if not os.path.exists('web_frontend'):
        print("错误: web_frontend 文件夹不存在")
        print("请确保 HTML、CSS 和 JavaScript 文件在 web_frontend 文件夹中")
        exit(1)

    # 检查是否为开发环境
    import sys
    debug_mode = '--debug' in sys.argv or os.environ.get('FLASK_ENV') == 'development'

    print("启动文本处理工具 Web 服务器...")
    print("访问地址: http://localhost:5000")
    if debug_mode:
        print("运行在开发模式（debug=True）")
        print("注意：开发模式下Flask会启动两个进程（主进程+重载器）")
    print("按 Ctrl+C 停止服务器")

    app.run(debug=debug_mode, host='0.0.0.0', port=5000, use_reloader=debug_mode)
