// 全局变量
let currentText = '';
let originalText = '';
let textProcessor = null;

// DOM元素
const elements = {
    // 导航
    navItems: document.querySelectorAll('.nav-item'),
    contentPanels: document.querySelectorAll('.content-panel'),
    
    // 工具栏
    uploadBtn: document.getElementById('upload-btn'),
    fileInput: document.getElementById('file-input'),
    clearBtn: document.getElementById('clear-btn'),
    resetBtn: document.getElementById('reset-btn'),
    textStats: document.getElementById('text-stats'),
    
    // 输入区域
    inputText: document.getElementById('input-text'),

    // 快速操作按钮
    quickSearchBtn: document.getElementById('quick-search-btn'),
    quickFreqBtn: document.getElementById('quick-freq-btn'),
    quickSummaryBtn: document.getElementById('quick-summary-btn'),
    quickStatsBtn: document.getElementById('quick-stats-btn'),
    
    // 查找替换
    searchInput: document.getElementById('search-input'),
    replaceInput: document.getElementById('replace-input'),
    regexMode: document.getElementById('regex-mode'),
    caseSensitive: document.getElementById('case-sensitive'),
    findBtn: document.getElementById('find-btn'),
    replaceBtn: document.getElementById('replace-btn'),
    replaceAllBtn: document.getElementById('replace-all-btn'),
    
    // 词频统计
    wordCount: document.getElementById('word-count'),
    minWordLength: document.getElementById('min-word-length'),
    segmentationMethod: document.getElementById('segmentation-method'),
    ignoreCase: document.getElementById('ignore-case'),
    excludePunctuation: document.getElementById('exclude-punctuation'),
    excludeStopwords: document.getElementById('exclude-stopwords'),
    excludeNumbers: document.getElementById('exclude-numbers'),
    excludeSingleChars: document.getElementById('exclude-single-chars'),
    analyzeFreqBtn: document.getElementById('analyze-freq-btn'),
    manageStopwordsBtn: document.getElementById('manage-stopwords-btn'),
    stopwordsCount: document.getElementById('stopwords-count'),
    
    // 文本摘要
    sentenceCount: document.getElementById('sentence-count'),
    summaryMethod: document.getElementById('summary-method'),
    summaryTitle: document.getElementById('summary-title'),
    generateSummaryBtn: document.getElementById('generate-summary-btn'),
    
    // 结果区域
    resultsArea: document.getElementById('results-area'),
    copyResultBtn: document.getElementById('copy-result-btn'),
    downloadResultBtn: document.getElementById('download-result-btn'),

    // 停用词管理侧边栏
    stopwordsSidebar: document.getElementById('stopwords-sidebar'),
    stopwordsSidebarClose: document.getElementById('stopwords-sidebar-close'),
    quickAddStopwordsBtn: document.getElementById('quick-add-stopwords-btn'),
    quickAddSection: document.getElementById('quick-add-section'),
    quickStopwordsInput: document.getElementById('quick-stopwords-input'),
    quickAddBtn: document.getElementById('quick-add-btn'),
    newStopwordsInput: document.getElementById('new-stopwords-input'),
    addStopwordsBtn: document.getElementById('add-stopwords-btn'),
    currentStopwordsCount: document.getElementById('current-stopwords-count'),
    currentStopwordsList: document.getElementById('current-stopwords-list'),
    clearAllStopwordsBtn: document.getElementById('clear-all-stopwords-btn'),
    refreshStopwordsBtn: document.getElementById('refresh-stopwords-btn'),

    // 加载动画
    loadingOverlay: document.getElementById('loading-overlay')
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateTextStats();
    initializeTextProcessing();
});

// 初始化事件监听器
function initializeEventListeners() {
    // 导航切换
    elements.navItems.forEach(item => {
        item.addEventListener('click', () => switchPanel(item.dataset.function));
    });
    
    // 文件上传
    elements.uploadBtn.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileUpload);
    
    // 工具栏按钮
    elements.clearBtn.addEventListener('click', clearText);
    elements.resetBtn.addEventListener('click', resetText);
    
    // 文本输入
    elements.inputText.addEventListener('input', handleTextInput);

    // 快速操作按钮
    elements.quickSearchBtn.addEventListener('click', () => {
        if (checkTextInput()) {
            switchPanel('search-replace');
        }
    });

    elements.quickFreqBtn.addEventListener('click', () => {
        if (checkTextInput()) {
            switchPanel('word-freq');
            analyzeWordFrequency();
        }
    });

    elements.quickSummaryBtn.addEventListener('click', () => {
        if (checkTextInput()) {
            switchPanel('summary');
            generateSummary();
        }
    });

    elements.quickStatsBtn.addEventListener('click', () => {
        if (checkTextInput()) {
            showTextStats();
        }
    });
    
    // 查找替换
    elements.findBtn.addEventListener('click', findText);
    elements.replaceBtn.addEventListener('click', replaceText);
    elements.replaceAllBtn.addEventListener('click', replaceAllText);
    
    // 词频统计
    elements.analyzeFreqBtn.addEventListener('click', analyzeWordFrequency);
    elements.manageStopwordsBtn.addEventListener('click', openStopwordsModal);

    // 文本摘要
    elements.generateSummaryBtn.addEventListener('click', generateSummary);

    // 新增NLP功能按钮
    const extractEntitiesBtn = document.getElementById('extract-entities-btn');
    const analyzeSentimentBtn = document.getElementById('analyze-sentiment-btn');
    const analyzeSyntaxBtn = document.getElementById('analyze-syntax-btn');
    const generateRewriteBtn = document.getElementById('generate-rewrite-btn');

    // 导出功能按钮
    const exportFileBtn = document.getElementById('export-file-btn');
    const previewExportBtn = document.getElementById('preview-export-btn');

    if (extractEntitiesBtn) extractEntitiesBtn.addEventListener('click', extractEntities);
    if (analyzeSentimentBtn) analyzeSentimentBtn.addEventListener('click', analyzeSentiment);
    if (analyzeSyntaxBtn) analyzeSyntaxBtn.addEventListener('click', analyzeSyntax);
    if (generateRewriteBtn) generateRewriteBtn.addEventListener('click', generateRewrite);
    if (exportFileBtn) exportFileBtn.addEventListener('click', exportResults);
    if (previewExportBtn) previewExportBtn.addEventListener('click', previewExport);

    // 分段改写选项控制
    const segmentModeCheckbox = document.getElementById('segment-mode');
    const segmentOptions = document.getElementById('segment-options');

    if (segmentModeCheckbox && segmentOptions) {
        // 初始状态
        segmentOptions.style.display = segmentModeCheckbox.checked ? 'block' : 'none';

        // 监听复选框变化
        segmentModeCheckbox.addEventListener('change', function() {
            segmentOptions.style.display = this.checked ? 'block' : 'none';
        });
    }

    // 结果操作
    elements.copyResultBtn.addEventListener('click', copyResults);
    elements.downloadResultBtn.addEventListener('click', downloadResults);

    // 停用词管理侧边栏
    elements.stopwordsSidebarClose.addEventListener('click', closeStopwordsSidebar);
    elements.addStopwordsBtn.addEventListener('click', addStopwords);
    elements.clearAllStopwordsBtn.addEventListener('click', clearAllStopwords);
    elements.refreshStopwordsBtn.addEventListener('click', refreshStopwords);
    elements.quickAddStopwordsBtn.addEventListener('click', toggleQuickAddSection);
    elements.quickAddBtn.addEventListener('click', quickAddStopwords);

    // 点击侧边栏外部关闭
    elements.stopwordsSidebar.addEventListener('click', (e) => {
        if (e.target === elements.stopwordsSidebar) {
            closeStopwordsSidebar();
        }
    });

    // 回车键添加停用词
    elements.newStopwordsInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addStopwords();
        }
    });

    // 快速添加停用词回车键
    elements.quickStopwordsInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            quickAddStopwords();
        }
    });

    // 初始化停用词计数
    updateStopwordsCount();
}

// 切换面板
function switchPanel(functionName) {
    // 更新导航状态
    elements.navItems.forEach(item => {
        item.classList.toggle('active', item.dataset.function === functionName);
    });
    
    // 显示对应面板
    elements.contentPanels.forEach(panel => {
        panel.classList.toggle('hidden', !panel.id.includes(functionName));
    });
}

// 处理文件上传
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.txt')) {
        showError('请选择txt格式的文件');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        elements.inputText.value = text;
        handleTextInput();
        showSuccess(`成功加载文件: ${file.name}`);
    };
    reader.readAsText(file, 'UTF-8');
}

// 处理文本输入
function handleTextInput() {
    currentText = elements.inputText.value;
    if (!originalText) {
        originalText = currentText;
    }
    updateTextStats();
}

// 加载文本到后端
async function loadTextToBackend(text) {
    try {
        const response = await fetch('/api/load_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text
            })
        });

        const result = await response.json();
        if (!result.success) {
            throw new Error(result.error);
        }

        return result;
    } catch (error) {
        throw new Error('加载文本到后端失败: ' + error.message);
    }
}

// 更新文本统计
function updateTextStats() {
    const text = elements.inputText.value;
    const charCount = text.length;
    const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
    elements.textStats.textContent = `字符数: ${charCount} | 词数: ${wordCount}`;
}

// 清空文本
function clearText() {
    if (confirm('确定要清空所有文本吗？')) {
        elements.inputText.value = '';
        currentText = '';
        originalText = '';
        updateTextStats();
        clearResults();
    }
}

// 重置文本
function resetText() {
    if (originalText && confirm('确定要重置到原始文本吗？')) {
        elements.inputText.value = originalText;
        currentText = originalText;
        updateTextStats();
        showSuccess('文本已重置');
    }
}

// 查找文本
async function findText() {
    const searchTerm = elements.searchInput.value.trim();
    if (!searchTerm) {
        showError('请输入要查找的内容');
        return;
    }

    const text = elements.inputText.value;
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        // 先加载文本到后端
        await loadTextToBackend(text);

        // 调用查找API
        const response = await fetch('/api/find_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pattern: searchTerm,
                use_regex: elements.regexMode.checked,
                case_sensitive: elements.caseSensitive.checked
            })
        });

        const result = await response.json();

        if (result.success) {
            displayFindResults(result.matches, searchTerm, result.count);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('查找失败: ' + error.message);
    }
}

// 查找匹配项
function findMatches(text, pattern, useRegex, caseSensitive) {
    let regex;
    const flags = caseSensitive ? 'g' : 'gi';
    
    if (useRegex) {
        regex = new RegExp(pattern, flags);
    } else {
        regex = new RegExp(escapeRegex(pattern), flags);
    }
    
    const matches = [];
    let match;
    
    while ((match = regex.exec(text)) !== null) {
        matches.push({
            index: match.index,
            text: match[0],
            context: getContext(text, match.index, match[0].length)
        });
        
        if (!regex.global) break;
    }
    
    return matches;
}

// 获取上下文
function getContext(text, index, length, contextLength = 30) {
    const start = Math.max(0, index - contextLength);
    const end = Math.min(text.length, index + length + contextLength);
    const before = text.substring(start, index);
    const match = text.substring(index, index + length);
    const after = text.substring(index + length, end);
    
    return { before, match, after };
}

// 转义正则表达式特殊字符
function escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// 替换文本
function replaceText() {
    const searchTerm = elements.searchInput.value.trim();
    const replaceTerm = elements.replaceInput.value;

    if (!searchTerm) {
        showError('请输入要查找的内容');
        return;
    }

    // 如果有当前查找结果，则进行选择性替换（替换第一个）
    if (window.currentMatches && window.currentMatches.length > 0 && window.currentSearchTerm === searchTerm) {
        replaceSingleMatch(0); // 替换第一个匹配项
        return;
    }

    // 否则进行全部替换
    performReplace(searchTerm, replaceTerm, false);
}

// 全部替换
function replaceAllText() {
    const searchTerm = elements.searchInput.value.trim();
    const replaceTerm = elements.replaceInput.value;
    
    if (!searchTerm) {
        showError('请输入要查找的内容');
        return;
    }
    
    performReplace(searchTerm, replaceTerm, true);
}

// 执行替换
async function performReplace(searchTerm, replaceTerm, replaceAll) {
    const text = elements.inputText.value;
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        // 先加载文本到后端
        await loadTextToBackend(text);

        // 调用替换API
        const response = await fetch('/api/replace_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pattern: searchTerm,
                replacement: replaceTerm,
                use_regex: elements.regexMode.checked,
                case_sensitive: elements.caseSensitive.checked
            })
        });

        const result = await response.json();

        if (result.success) {
            elements.inputText.value = result.new_text;
            currentText = result.new_text;
            updateTextStats();
            showSuccess(result.message);
            displayReplaceResults(result.count, searchTerm, replaceTerm);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('替换失败: ' + error.message);
    }
}

// 分析词频
async function analyzeWordFrequency() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        // 先加载文本到后端
        await loadTextToBackend(text);

        const wordCount = parseInt(elements.wordCount.value) || 20;
        const minWordLength = parseInt(elements.minWordLength.value) || 1;
        const ignoreCase = elements.ignoreCase.checked;
        const excludePunctuation = elements.excludePunctuation.checked;
        const excludeStopwords = elements.excludeStopwords.checked;
        const excludeNumbers = elements.excludeNumbers.checked;
        const excludeSingleChars = elements.excludeSingleChars.checked;
        const segmentationMethod = elements.segmentationMethod.value;

        // 调用词频分析API
        const response = await fetch('/api/word_frequency', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                n: wordCount,
                ignore_case: ignoreCase,
                exclude_punctuation: excludePunctuation,
                exclude_stopwords: excludeStopwords,
                exclude_numbers: excludeNumbers,
                exclude_single_chars: excludeSingleChars,
                min_word_length: minWordLength,
                segmentation_method: segmentationMethod
            })
        });

        const result = await response.json();

        if (result.success) {
            displayWordFrequencyResults(result.word_frequency);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('词频分析失败: ' + error.message);
    }
}

// 计算词频
function calculateWordFrequency(text, options) {
    let processedText = text;
    
    if (options.ignoreCase) {
        processedText = processedText.toLowerCase();
    }
    
    if (options.excludePunctuation) {
        // 移除标点符号
        processedText = processedText.replace(/[^\w\s\u4e00-\u9fff]/g, ' ');
    }
    
    // 分词
    const words = processedText.split(/\s+/).filter(word => word.length > 0);
    
    // 统计频率
    const frequency = {};
    words.forEach(word => {
        frequency[word] = (frequency[word] || 0) + 1;
    });
    
    // 排序并返回前N个
    return Object.entries(frequency)
        .sort((a, b) => b[1] - a[1])
        .slice(0, options.maxWords);
}

// 生成摘要
async function generateSummary() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        // 先加载文本到后端
        await loadTextToBackend(text);

        const sentenceCount = parseInt(elements.sentenceCount.value) || 3;
        const method = elements.summaryMethod.value;
        const title = elements.summaryTitle.value.trim();

        // 调用摘要生成API
        const response = await fetch('/api/generate_summary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                num_sentences: sentenceCount,
                method: method,
                title: title
            })
        });

        const result = await response.json();

        if (result.success) {
            displaySummaryResults(result.summary, result.method);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('摘要生成失败: ' + error.message);
    }
}

// 生成文本摘要（简化版本）
function generateTextSummary(text, sentenceCount, method) {
    // 分割句子
    const sentences = text.split(/[。！？.!?]+/).filter(s => s.trim().length > 5);
    
    if (sentences.length <= sentenceCount) {
        return text;
    }
    
    let selectedSentences = [];
    
    switch (method) {
        case 'position':
            // 基于位置：选择开头、结尾和中间的句子
            selectedSentences = [
                sentences[0],
                sentences[Math.floor(sentences.length / 2)],
                sentences[sentences.length - 1]
            ].slice(0, sentenceCount);
            break;
            
        case 'frequency':
            // 基于词频：计算每个句子的词频得分
            const wordFreq = calculateWordFrequency(text, { ignoreCase: true, excludePunctuation: true });
            const freqMap = new Map(wordFreq);
            
            const sentenceScores = sentences.map(sentence => {
                const words = sentence.toLowerCase().split(/\s+/);
                const score = words.reduce((sum, word) => sum + (freqMap.get(word) || 0), 0);
                return { sentence, score };
            });
            
            selectedSentences = sentenceScores
                .sort((a, b) => b.score - a.score)
                .slice(0, sentenceCount)
                .map(item => item.sentence);
            break;
            
        default: // hybrid
            // 混合方法：结合位置和词频
            const wordFreqHybrid = calculateWordFrequency(text, { ignoreCase: true, excludePunctuation: true });
            const freqMapHybrid = new Map(wordFreqHybrid);
            
            const hybridScores = sentences.map((sentence, index) => {
                const words = sentence.toLowerCase().split(/\s+/);
                const freqScore = words.reduce((sum, word) => sum + (freqMapHybrid.get(word) || 0), 0);
                
                // 位置权重
                let positionWeight = 1;
                if (index === 0 || index === sentences.length - 1) {
                    positionWeight = 1.5;
                }
                
                return { sentence, score: freqScore * positionWeight };
            });
            
            selectedSentences = hybridScores
                .sort((a, b) => b.score - a.score)
                .slice(0, sentenceCount)
                .map(item => item.sentence);
    }
    
    return selectedSentences.join('。') + '。';
}

// 显示文本统计
function showTextStats() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }
    
    const stats = {
        characters: text.length,
        words: text.split(/\s+/).filter(word => word.length > 0).length,
        sentences: text.split(/[。！？.!?]+/).filter(s => s.trim().length > 0).length,
        paragraphs: text.split(/\n\s*\n/).filter(p => p.trim().length > 0).length
    };
    
    displayStatsResults(stats);
}

// 显示结果函数
function displayFindResults(matches, searchTerm, count) {
    const replaceValue = elements.replaceInput.value;

    const resultsHtml = `
        <div class="results-header">
            <h3><i class="fas fa-search"></i> 查找结果</h3>
            <div class="results-stats">
                找到 <span class="highlight">${count}</span> 个匹配项
            </div>
            <div class="results-actions">
                <button class="btn btn-sm btn-primary" id="select-all-matches">
                    <i class="fas fa-check-square"></i> 全选
                </button>
                <button class="btn btn-sm btn-secondary" id="deselect-all-matches">
                    <i class="fas fa-square"></i> 取消全选
                </button>
                <button class="btn btn-sm btn-success" id="replace-selected-matches">
                    <i class="fas fa-exchange-alt"></i> 替换选中项
                </button>
            </div>
        </div>
        <div class="results-content find-results">
            ${matches.map((match, index) => `
                <div class="result-item" data-match-index="${index}">
                    <div class="result-header">
                        <div class="result-checkbox">
                            <input type="checkbox" id="match-${index}" class="match-checkbox">
                            <label for="match-${index}" class="result-index">#${index + 1}</label>
                        </div>
                        <div class="result-actions">
                            <button class="btn btn-xs btn-primary replace-single-btn"
                                    data-match-index="${index}"
                                    title="替换此项">
                                <i class="fas fa-exchange-alt"></i>
                            </button>
                            <button class="btn btn-xs btn-secondary locate-btn"
                                    data-match-index="${index}"
                                    title="定位到此项">
                                <i class="fas fa-crosshairs"></i>
                            </button>
                        </div>
                    </div>
                    <div class="result-context">
                        <span class="context-before">${escapeHtml(match.context.before)}</span>
                        <span class="context-match">${escapeHtml(match.context.match)}</span>
                        <span class="context-after">${escapeHtml(match.context.after)}</span>
                    </div>
                    <div class="result-details">
                        <span class="result-position">位置: ${match.index}</span>
                        ${replaceValue ? `<span class="replacement-preview">替换为: "${escapeHtml(replaceValue)}"</span>` : ''}
                    </div>
                </div>
            `).join('')}
        </div>
        <div class="results-footer">
            <div class="navigation-controls">
                <button class="btn btn-sm btn-outline-primary" id="prev-match" title="上一个匹配项">
                    <i class="fas fa-chevron-up"></i>
                </button>
                <button class="btn btn-sm btn-outline-primary" id="next-match" title="下一个匹配项">
                    <i class="fas fa-chevron-down"></i>
                </button>
                <span class="current-match-info">当前: <span id="current-match-number">-</span> / ${count}</span>
            </div>
        </div>
    `;

    elements.resultsArea.innerHTML = resultsHtml;

    // 存储匹配项数据供后续使用
    window.currentMatches = matches;
    window.currentSearchTerm = searchTerm;
    window.currentMatchIndex = -1;

    // 绑定事件监听器
    bindFindResultsEvents();
}

// 绑定查找结果事件
function bindFindResultsEvents() {
    // 全选/取消全选
    const selectAllBtn = document.getElementById('select-all-matches');
    const deselectAllBtn = document.getElementById('deselect-all-matches');
    const replaceSelectedBtn = document.getElementById('replace-selected-matches');

    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', () => {
            document.querySelectorAll('.match-checkbox').forEach(checkbox => {
                checkbox.checked = true;
            });
        });
    }

    if (deselectAllBtn) {
        deselectAllBtn.addEventListener('click', () => {
            document.querySelectorAll('.match-checkbox').forEach(checkbox => {
                checkbox.checked = false;
            });
        });
    }

    if (replaceSelectedBtn) {
        replaceSelectedBtn.addEventListener('click', replaceSelectedMatches);
    }

    // 单个替换按钮
    document.querySelectorAll('.replace-single-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const matchIndex = parseInt(e.target.closest('.replace-single-btn').dataset.matchIndex);
            replaceSingleMatch(matchIndex);
        });
    });

    // 定位按钮
    document.querySelectorAll('.locate-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const matchIndex = parseInt(e.target.closest('.locate-btn').dataset.matchIndex);
            locateMatch(matchIndex);
        });
    });

    // 导航按钮
    const prevBtn = document.getElementById('prev-match');
    const nextBtn = document.getElementById('next-match');

    if (prevBtn) {
        prevBtn.addEventListener('click', () => navigateMatch(-1));
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => navigateMatch(1));
    }

    // 结果项点击高亮
    document.querySelectorAll('.result-item').forEach(item => {
        item.addEventListener('click', (e) => {
            if (!e.target.closest('button') && !e.target.closest('input')) {
                const matchIndex = parseInt(item.dataset.matchIndex);
                highlightMatch(matchIndex);
            }
        });
    });
}

// 替换选中的匹配项
async function replaceSelectedMatches() {
    const selectedCheckboxes = document.querySelectorAll('.match-checkbox:checked');
    if (selectedCheckboxes.length === 0) {
        showError('请先选择要替换的匹配项');
        return;
    }

    const selectedIndices = Array.from(selectedCheckboxes).map(cb =>
        parseInt(cb.id.replace('match-', ''))
    );

    const replaceTerm = elements.replaceInput.value;
    await performSelectiveReplace(selectedIndices, replaceTerm);
}

// 替换单个匹配项
async function replaceSingleMatch(matchIndex) {
    const replaceTerm = elements.replaceInput.value;
    await performSelectiveReplace([matchIndex], replaceTerm);
}

// 执行选择性替换
async function performSelectiveReplace(indices, replaceTerm) {
    if (!window.currentMatches || indices.length === 0) {
        showError('没有可替换的匹配项');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/api/selective_replace', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pattern: window.currentSearchTerm,
                replacement: replaceTerm,
                indices: indices,
                use_regex: elements.regexMode.checked,
                case_sensitive: elements.caseSensitive.checked
            })
        });

        const result = await response.json();

        if (result.success) {
            elements.inputText.value = result.new_text;
            updateTextStats();
            showSuccess(`成功替换 ${result.count} 个匹配项`);

            // 重新查找以更新结果
            setTimeout(() => findText(), 500);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('替换失败: ' + error.message);
    }
}

function displayReplaceResults(count, searchTerm, replaceTerm) {
    const resultsHtml = `
        <div class="result-item">
            <div class="result-title">替换结果</div>
            <div class="result-content">
                <p>将 "<strong>${searchTerm}</strong>" 替换为 "<strong>${replaceTerm}</strong>"</p>
                <p>成功替换 <strong>${count}</strong> 处</p>
            </div>
        </div>
    `;

    elements.resultsArea.innerHTML = resultsHtml;
}

function displayWordFrequencyResults(frequencies) {
    const resultsHtml = `
        <div class="result-item">
            <div class="result-title">词频统计结果</div>
            <div class="result-content">
                <div class="freq-results-header">
                    <p>点击词汇可快速添加为停用词</p>
                </div>
                <ul class="word-freq-list">
                    ${frequencies.map(([word, count], index) => `
                        <li class="word-freq-item">
                            <span class="word-freq-word clickable-word" data-word="${escapeHtml(word)}" title="点击添加为停用词">
                                ${index + 1}. ${escapeHtml(word)}
                            </span>
                            <div class="word-freq-actions">
                                <span class="word-freq-count">${count}</span>
                                <button class="btn-add-stopword" data-word="${escapeHtml(word)}" title="添加为停用词">
                                    <i class="fas fa-plus"></i>
                                </button>
                            </div>
                        </li>
                    `).join('')}
                </ul>
            </div>
        </div>
    `;

    elements.resultsArea.innerHTML = resultsHtml;

    // 绑定点击事件
    bindWordFrequencyEvents();
}

// 绑定词频结果事件
function bindWordFrequencyEvents() {
    // 点击词汇添加为停用词
    document.querySelectorAll('.clickable-word').forEach(element => {
        element.addEventListener('click', (e) => {
            const word = e.target.dataset.word;
            addWordToStopwords(word);
        });
    });

    // 点击添加按钮
    document.querySelectorAll('.btn-add-stopword').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const word = e.target.closest('.btn-add-stopword').dataset.word;
            addWordToStopwords(word);
        });
    });
}

// 添加单个词到停用词
async function addWordToStopwords(word) {
    if (!word || !word.trim()) {
        showError('无效的词汇');
        return;
    }

    try {
        const response = await fetch('/api/stopwords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                words: [word.trim()]
            })
        });

        const result = await response.json();

        if (result.success) {
            showSuccess(`已添加停用词: ${word}，请重新点击"分析词频"查看效果`);
            updateStopwordsCount();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('添加停用词失败: ' + error.message);
    }
}

function displaySummaryResults(summary, method) {
    const methodNames = {
        frequency: '基于词频',
        position: '基于位置',
        hybrid: '混合方法',
        textteaser: 'TextTeaser算法',
        qwen3: 'Qwen3大模型'
    };

    // 清理和格式化摘要内容
    const cleanSummary = cleanSummaryContent(summary);

    const resultsHtml = `
        <div class="result-item">
            <div class="result-title">
                <i class="fas fa-file-alt"></i>
                <span>文本摘要 (${methodNames[method] || method})</span>
            </div>
            <div class="result-content">
                <div class="summary-text">${formatSummaryText(cleanSummary)}</div>
                ${method === 'qwen3' ? '<div class="method-note"><i class="fas fa-robot"></i> 由Qwen3大模型生成</div>' : ''}
                ${method === 'textteaser' ? '<div class="method-note"><i class="fas fa-brain"></i> 使用TextTeaser算法</div>' : ''}
            </div>
        </div>
    `;

    elements.resultsArea.innerHTML = resultsHtml;
}

// 清理摘要内容的函数
function cleanSummaryContent(summary) {
    if (!summary) return '';

    // 移除可能的think标签内容
    let cleaned = summary.replace(/<think>[\s\S]*?<\/think>/gi, '');

    // 移除Markdown格式
    cleaned = cleaned.replace(/\*\*(.*?)\*\*/g, '$1'); // 移除粗体
    cleaned = cleaned.replace(/\*(.*?)\*/g, '$1');     // 移除斜体
    cleaned = cleaned.replace(/`(.*?)`/g, '$1');       // 移除代码标记

    // 移除可能的前缀
    const prefixes = ['摘要：', '**摘要：**', '总结：', '**总结：**'];
    for (const prefix of prefixes) {
        if (cleaned.startsWith(prefix)) {
            cleaned = cleaned.substring(prefix.length).trim();
            break;
        }
    }

    // 清理多余的空白
    cleaned = cleaned.replace(/\n\s*\n/g, '\n').trim();

    return cleaned;
}

// 格式化摘要文本显示
function formatSummaryText(text) {
    if (!text) return '<p class="no-content">未生成摘要内容</p>';

    // 将文本按句子分割并格式化
    const sentences = text.split(/[。！？.!?]/).filter(s => s.trim());

    if (sentences.length === 0) {
        return `<p>${escapeHtml(text)}</p>`;
    }

    // 如果只有一个句子，直接显示
    if (sentences.length === 1) {
        return `<p>${escapeHtml(text)}</p>`;
    }

    // 多个句子时，每个句子一行
    let formatted = '<div class="summary-sentences">';
    sentences.forEach((sentence, index) => {
        if (sentence.trim()) {
            formatted += `<p class="summary-sentence">${escapeHtml(sentence.trim())}。</p>`;
        }
    });
    formatted += '</div>';

    return formatted;
}

function displayStatsResults(stats) {
    const resultsHtml = `
        <div class="result-item">
            <div class="result-title">
                <i class="fas fa-chart-bar"></i>
                <span>文本统计信息</span>
            </div>
            <div class="result-content">
                <p><strong>字符数:</strong> ${stats.characters}</p>
                <p><strong>词数:</strong> ${stats.words}</p>
                <p><strong>句子数:</strong> ${stats.sentences}</p>
                <p><strong>段落数:</strong> ${stats.paragraphs}</p>
            </div>
        </div>
    `;

    elements.resultsArea.innerHTML = resultsHtml;
}

// 定位到匹配项
function locateMatch(matchIndex) {
    if (!window.currentMatches || matchIndex < 0 || matchIndex >= window.currentMatches.length) {
        return;
    }

    const match = window.currentMatches[matchIndex];
    const textarea = elements.inputText;

    // 设置光标位置
    textarea.focus();
    textarea.setSelectionRange(match.index, match.index + match.match.length);

    // 滚动到可见区域
    const textBeforeMatch = textarea.value.substring(0, match.index);
    const lineNumber = textBeforeMatch.split('\n').length;
    const lineHeight = 20; // 估算行高
    textarea.scrollTop = Math.max(0, (lineNumber - 5) * lineHeight);

    // 高亮当前匹配项
    highlightMatch(matchIndex);
}

// 高亮匹配项
function highlightMatch(matchIndex) {
    // 移除之前的高亮
    document.querySelectorAll('.result-item.highlighted').forEach(item => {
        item.classList.remove('highlighted');
    });

    // 高亮当前项
    const currentItem = document.querySelector(`[data-match-index="${matchIndex}"]`);
    if (currentItem) {
        currentItem.classList.add('highlighted');
        currentItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // 更新当前匹配项编号
    window.currentMatchIndex = matchIndex;
    const currentMatchNumber = document.getElementById('current-match-number');
    if (currentMatchNumber) {
        currentMatchNumber.textContent = matchIndex + 1;
    }
}

// 导航匹配项
function navigateMatch(direction) {
    if (!window.currentMatches || window.currentMatches.length === 0) {
        return;
    }

    let newIndex = window.currentMatchIndex + direction;

    // 循环导航
    if (newIndex < 0) {
        newIndex = window.currentMatches.length - 1;
    } else if (newIndex >= window.currentMatches.length) {
        newIndex = 0;
    }

    locateMatch(newIndex);
}

// HTML转义函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 重复的函数定义已删除，使用第一个定义

// 工具函数
function checkTextInput() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入或上传文本内容');
        return false;
    }
    return true;
}

function clearResults() {
    elements.resultsArea.innerHTML = `
        <div class="placeholder">
            <i class="fas fa-info-circle"></i>
            <p>处理结果将在这里显示</p>
        </div>
    `;
}

function showLoading() {
    elements.loadingOverlay.classList.remove('hidden');
    const loadingText = elements.loadingOverlay.querySelector('p');
    if (loadingText) {
        loadingText.textContent = '处理中...';
    }
}

function showLoadingWithMessage(message) {
    elements.loadingOverlay.classList.remove('hidden');
    const loadingText = elements.loadingOverlay.querySelector('p');
    if (loadingText) {
        loadingText.textContent = message;
    }
}

function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

function showSuccess(message) {
    // 简单的成功提示，可以用更好的通知组件替换
    alert('✓ ' + message);
}

function showError(message) {
    // 简单的错误提示，可以用更好的通知组件替换
    alert('✗ ' + message);
}

function showInfo(message) {
    // 简单的信息提示，可以用更好的通知组件替换
    console.log('ℹ ' + message);
    // 可以在这里添加更好的UI提示，比如toast通知
}

function copyResults() {
    const resultText = elements.resultsArea.textContent;
    navigator.clipboard.writeText(resultText).then(() => {
        showSuccess('结果已复制到剪贴板');
    }).catch(() => {
        showError('复制失败');
    });
}

function downloadResults() {
    const resultText = elements.resultsArea.textContent;
    const blob = new Blob([resultText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'text_analysis_results.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ===== 新增NLP功能 =====

// 实体识别
async function extractEntities() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    const method = document.getElementById('entity-method').value;
    const deduplicate = document.getElementById('entity-deduplicate').checked;
    showLoading();

    try {
        const response = await fetch('/api/extract_entities', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                method: method,
                deduplicate: deduplicate
            })
        });

        const result = await response.json();

        if (result.success) {
            displayEntityResults(result.entities, result.model_used, result.method, result.deduplicated);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('实体识别失败: ' + error.message);
    }
}

// 情感分析
async function analyzeSentiment() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        const response = await fetch('/api/analyze_sentiment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text
            })
        });

        const result = await response.json();

        if (result.success) {
            displaySentimentResults(
                result.sentiment,
                result.scores,
                result.methods_used,
                result.confidence,
                result.ensemble_details
            );
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('情感分析失败: ' + error.message);
    }
}

// 句法分析
async function analyzeSyntax() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    // 对于大文本给出特别提示
    if (text.length > 10000) {
        if (!confirm(`文本较长（${text.length}字符），句法分析可能需要较长时间。是否继续？`)) {
            return;
        }
        showLoadingWithMessage('正在分析句法结构，请耐心等待...');
    } else {
        showLoading();
    }

    try {
        const response = await fetch('/api/analyze_syntax', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text
            })
        });

        const result = await response.json();

        if (result.success) {
            displaySyntaxResults(result.sentences, result.model_used, result.is_truncated);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('句法分析失败: ' + error.message);
    }
}

// 智能改写生成
async function generateRewrite() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        // 先加载文本到后端
        await loadTextToBackend(text);

        const style = document.getElementById('rewrite-style').value;
        const intensity = document.getElementById('rewrite-intensity').value;
        const segmentMode = document.getElementById('segment-mode').checked;
        const maxSegmentLength = parseInt(document.getElementById('max-segment-length').value);

        // 显示处理信息
        if (segmentMode && text.length > maxSegmentLength) {
            showInfo(`文本较长（${text.length}字符），将使用分段改写模式...`);
        }

        const response = await fetch('/api/intelligent_rewrite', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                style: style,
                intensity: intensity,
                segment_mode: segmentMode,
                max_segment_length: maxSegmentLength
            })
        });

        const result = await response.json();

        if (result.success) {
            displayRewriteResults(result.rewritten_text, result.style, result.intensity, result.segment_info);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('智能改写失败: ' + error.message);
    }
}

// ===== 结果显示函数 =====

// 显示实体识别结果
function displayEntityResults(entities, modelUsed, method, deduplicated) {
    const deduplicateInfo = deduplicated ? ' | 已去重统计' : '';

    let html = `
        <div class="result-section">
            <h4><i class="fas fa-user-tag"></i> 实体识别结果</h4>
            <p class="model-info">使用模型: ${modelUsed} | 方法: ${method}${deduplicateInfo}</p>
            <p class="entity-count">找到 ${entities.length} 个${deduplicated ? '不同' : ''}实体</p>
    `;

    if (entities.length > 0) {
        html += '<div class="entity-list">';

        // 按类型分组显示
        const entityGroups = {};
        entities.forEach(entity => {
            if (!entityGroups[entity.label]) {
                entityGroups[entity.label] = [];
            }
            entityGroups[entity.label].push(entity);
        });

        for (const [label, entityList] of Object.entries(entityGroups)) {
            html += `
                <div class="entity-group">
                    <h5>${entityList[0].description} (${label})</h5>
                    <ul>
            `;
            entityList.forEach(entity => {
                if (deduplicated) {
                    // 去重后的显示格式
                    const countInfo = `<span class="entity-count-badge">${entity.count}次</span>`;
                    const sourceInfo = entity.sources && entity.sources.length > 0 ?
                        ` <span class="entity-source">[${entity.sources.join(', ')}]</span>` : '';
                    const confidenceInfo = entity.confidence ?
                        ` <span class="entity-confidence">(${(entity.confidence * 100).toFixed(0)}%)</span>` : '';

                    // 显示位置信息（可折叠）
                    const positionsId = `positions-${Math.random().toString(36).substr(2, 9)}`;
                    const positionsInfo = entity.positions && entity.positions.length > 0 ?
                        `<div class="entity-positions">
                            <button class="btn-toggle-positions" onclick="togglePositions('${positionsId}')">
                                <i class="fas fa-chevron-down"></i> 查看位置
                            </button>
                            <div id="${positionsId}" class="positions-list hidden">
                                ${entity.positions.map(pos => `<span class="position-item">[${pos.start}-${pos.end}]</span>`).join(' ')}
                            </div>
                        </div>` : '';

                    html += `<li>
                        <div class="entity-item-header">
                            <span class="entity-text">${entity.text}</span>
                            ${countInfo}${sourceInfo}${confidenceInfo}
                        </div>
                        ${positionsInfo}
                    </li>`;
                } else {
                    // 原始显示格式
                    const sourceInfo = entity.source ? ` <span class="entity-source">[${entity.source}]</span>` : '';
                    const confidenceInfo = entity.confidence ? ` <span class="entity-confidence">(${(entity.confidence * 100).toFixed(0)}%)</span>` : '';
                    html += `<li><span class="entity-text">${entity.text}</span> <span class="entity-position">[位置: ${entity.start}-${entity.end}]</span>${sourceInfo}${confidenceInfo}</li>`;
                }
            });
            html += '</ul></div>';
        }

        html += '</div>';
    } else {
        html += '<p class="no-results">未找到任何实体</p>';
    }

    html += '</div>';
    elements.resultsArea.innerHTML = html;
}

// 切换位置显示
function togglePositions(positionsId) {
    const positionsList = document.getElementById(positionsId);
    const button = positionsList.previousElementSibling;
    const icon = button.querySelector('i');

    if (positionsList.classList.contains('hidden')) {
        positionsList.classList.remove('hidden');
        icon.className = 'fas fa-chevron-up';
        button.innerHTML = '<i class="fas fa-chevron-up"></i> 隐藏位置';
    } else {
        positionsList.classList.add('hidden');
        icon.className = 'fas fa-chevron-down';
        button.innerHTML = '<i class="fas fa-chevron-down"></i> 查看位置';
    }
}

// 显示情感分析结果
function displaySentimentResults(sentiment, scores, methodsUsed, confidence = null, ensembleDetails = null) {
    let html = `
        <div class="result-section">
            <h4><i class="fas fa-brain"></i> 高级情感分析结果</h4>
            <p class="methods-info">使用方法: ${methodsUsed.join(', ')}</p>
            <div class="sentiment-result">
                <h5>情感倾向: <span class="sentiment-${sentiment}">${getSentimentLabel(sentiment)}</span></h5>
                ${confidence !== null ? `<p class="confidence-info">置信度: <strong>${(confidence * 100).toFixed(1)}%</strong></p>` : ''}
            </div>
    `;

    // 按重要性和效果排序显示模型结果
    const modelPriority = [
        // 1. 深度学习模型（最重要，效果最好）
        { key: 'uer_roberta_dianping', name: 'UER中文RoBERTa', type: 'dl', weight: '35%', description: '专业中文情感分析模型' },
        { key: 'erlangshen_roberta_330m', name: '二郎神RoBERTa-330M', type: 'dl', weight: '35%', description: '大型中文情感分析模型' },
        { key: 'erlangshen_roberta_110m', name: '二郎神RoBERTa-110M', type: 'dl', weight: '35%', description: '轻量级中文情感分析模型' },

        // 2. SnowNLP（中文专用，效果很好）
        { key: 'snownlp', name: 'SnowNLP', type: 'chinese', weight: '35%', description: '专门针对中文的情感分析' },

        // 3. 增强基础词典（中文优化）
        { key: 'basic', name: '增强基础词典', type: 'enhanced', weight: '15%', description: '支持否定词和程度副词的中文词典分析' },

        // 4. VADER（对中文效果有限）
        { key: 'vader', name: 'VADER', type: 'general', weight: '10%', description: '社交媒体情感分析（对中文支持有限）' },

        // 5. TextBlob（主要针对英文）
        { key: 'textblob', name: 'TextBlob', type: 'general', weight: '5%', description: '通用情感分析（主要针对英文）' }
    ];

    // 显示可用的模型结果（按优先级排序）
    for (const model of modelPriority) {
        if (scores[model.key]) {
            html += generateModelSection(model, scores[model.key]);
        }
    }

    // 显示模型融合详情
    if (ensembleDetails) {
        html += `
            <div class="score-section">
                <h6>模型融合详情:</h6>
                <ul>
                    <li>参与模型数: ${ensembleDetails.total_predictions}</li>
                    <li>积极概率: ${(ensembleDetails.sentiment_scores.positive * 100).toFixed(1)}%</li>
                    <li>消极概率: ${(ensembleDetails.sentiment_scores.negative * 100).toFixed(1)}%</li>
                    <li>中性概率: ${(ensembleDetails.sentiment_scores.neutral * 100).toFixed(1)}%</li>
                </ul>
            </div>
        `;
    }

    html += '</div>';
    elements.resultsArea.innerHTML = html;
}

// 生成单个模型的结果部分
function generateModelSection(model, scoreData) {
    const priorityClass = getPriorityClass(model.type);

    let html = `
        <div class="score-section ${priorityClass}">
            <div class="model-header">
                <h6>
                    <span class="model-name">${model.name}</span>
                    <span class="model-weight">(权重: ${model.weight})</span>
                    ${getModelTypeIcon(model.type)}
                </h6>
                <p class="model-description">${model.description}</p>
            </div>
    `;

    // 根据模型类型生成不同的内容
    if (model.type === 'dl') {
        // 深度学习模型
        if (Array.isArray(scoreData)) {
            html += `
                <div class="dl-predictions">
                    ${scoreData.map(pred => `
                        <div class="prediction-item">
                            <span class="prediction-label">${getSentimentLabel(pred.label)}</span>
                            <span class="prediction-score">${(pred.score * 100).toFixed(1)}%</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    } else if (model.key === 'snownlp') {
        // SnowNLP
        html += `
            <div class="score-details">
                <div class="score-item">
                    <span class="score-label">情感分数:</span>
                    <span class="score-value">${scoreData.sentiment_score.toFixed(3)}</span>
                    <span class="score-note">(0-1，>0.55为积极，<0.45为消极)</span>
                </div>
            </div>
        `;
    } else if (model.key === 'basic') {
        // 增强基础词典
        html += `
            <div class="score-details">
                <div class="score-item">
                    <span class="score-label">积极分数:</span>
                    <span class="score-value">${scoreData.positive_score?.toFixed(2) || scoreData.positive_words || 0}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">消极分数:</span>
                    <span class="score-value">${scoreData.negative_score?.toFixed(2) || scoreData.negative_words || 0}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">极性分数:</span>
                    <span class="score-value">${scoreData.polarity.toFixed(3)}</span>
                </div>
            </div>
        `;
    } else if (model.key === 'vader') {
        // VADER
        html += `
            <div class="score-details">
                <div class="score-item">
                    <span class="score-label">积极:</span>
                    <span class="score-value">${scoreData.pos.toFixed(3)}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">消极:</span>
                    <span class="score-value">${scoreData.neg.toFixed(3)}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">中性:</span>
                    <span class="score-value">${scoreData.neu.toFixed(3)}</span>
                </div>
                <div class="score-item">
                    <span class="score-label">综合:</span>
                    <span class="score-value">${scoreData.compound.toFixed(3)}</span>
                </div>
            </div>
            <p class="model-note">⚠ 注意：VADER主要针对英文设计，对中文支持有限</p>
        `;
    } else if (model.key === 'textblob') {
        // TextBlob
        html += `
            <div class="score-details">
                <div class="score-item">
                    <span class="score-label">极性:</span>
                    <span class="score-value">${scoreData.polarity.toFixed(3)}</span>
                    <span class="score-note">(-1到1，负数为消极，正数为积极)</span>
                </div>
                <div class="score-item">
                    <span class="score-label">主观性:</span>
                    <span class="score-value">${scoreData.subjectivity.toFixed(3)}</span>
                    <span class="score-note">(0到1，0为客观，1为主观)</span>
                </div>
            </div>
            <p class="model-note">⚠ 注意：TextBlob主要针对英文设计，对中文支持有限</p>
        `;
    }

    html += '</div>';
    return html;
}

// 获取模型类型图标
function getModelTypeIcon(type) {
    const icons = {
        'dl': '<i class="fas fa-brain" title="深度学习模型"></i>',
        'chinese': '<i class="fas fa-language" title="中文专用"></i>',
        'enhanced': '<i class="fas fa-book" title="增强词典"></i>',
        'general': '<i class="fas fa-globe" title="通用模型"></i>'
    };
    return icons[type] || '';
}

// 获取优先级样式类
function getPriorityClass(type) {
    const classes = {
        'dl': 'priority-high',
        'chinese': 'priority-high',
        'enhanced': 'priority-medium',
        'general': 'priority-low'
    };
    return classes[type] || '';
}

// 获取模型显示名称（保留兼容性）
function getModelDisplayName(modelKey) {
    const displayNames = {
        'uer_roberta_dianping': 'UER中文RoBERTa',
        'erlangshen_roberta_330m': '二郎神RoBERTa-330M',
        'erlangshen_roberta_110m': '二郎神RoBERTa-110M',
        'chinese_roberta_wwm_ext': '哈工大中文RoBERTa',
        'vader': 'VADER',
        'textblob': 'TextBlob',
        'snownlp': 'SnowNLP',
        'basic_dictionary': '基础词典'
    };
    return displayNames[modelKey] || modelKey;
}

// 显示句法分析结果
function displaySyntaxResults(sentences, modelUsed, isTruncated = false) {
    let html = `
        <div class="result-section">
            <h4><i class="fas fa-project-diagram"></i> 句法分析结果</h4>
            <p class="model-info">使用模型: ${modelUsed}</p>
            <p class="sentence-count">分析了 ${sentences.length} 个句子</p>
    `;

    if (isTruncated) {
        html += '<p class="truncation-warning"><i class="fas fa-exclamation-triangle"></i> 注意：由于文本较长，仅分析了前5000个字符</p>';
    }

    sentences.forEach((sentence, index) => {
        html += `
            <div class="sentence-analysis">
                <h5>句子 ${index + 1}: ${sentence.text}</h5>
                <table class="syntax-table">
                    <thead>
                        <tr>
                            <th>词汇</th>
                            <th>词性</th>
                            <th>依存关系</th>
                            <th>词根</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        sentence.words.forEach(word => {
            html += `
                <tr>
                    <td>${word.text}</td>
                    <td>${word.pos}</td>
                    <td>${word.deprel}</td>
                    <td>${word.lemma}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;
    });

    html += '</div>';
    elements.resultsArea.innerHTML = html;
}

// 显示智能改写结果
function displayRewriteResults(rewrittenText, style, intensity, segmentInfo) {
    const styleNames = {
        'formal': '正式风格',
        'casual': '轻松风格',
        'academic': '学术风格',
        'creative': '创意风格',
        'concise': '简洁风格'
    };

    const intensityNames = {
        'light': '轻度改写',
        'medium': '中度改写',
        'heavy': '重度改写'
    };

    // 构建处理信息
    let processingInfo = '';
    if (segmentInfo) {
        if (segmentInfo.enabled) {
            processingInfo = `<div class="processing-info">
                <i class="fas fa-info-circle"></i>
                处理模式: 分段改写 | 每段最大: ${segmentInfo.max_length}字符
            </div>`;
        } else {
            processingInfo = `<div class="processing-info">
                <i class="fas fa-info-circle"></i>
                处理模式: 整体改写
            </div>`;
        }
    }

    const html = `
        <div class="result-section">
            <h4><i class="fas fa-edit"></i> 智能改写结果</h4>
            <p class="method-info">改写风格: ${styleNames[style] || style} | 改写强度: ${intensityNames[intensity] || intensity}</p>
            ${processingInfo}
            <div class="rewrite-content">
                <div class="rewritten-text">${escapeHtml(rewrittenText)}</div>
            </div>
        </div>
    `;

    elements.resultsArea.innerHTML = html;
}

// 获取情感标签
function getSentimentLabel(sentiment) {
    const labels = {
        'positive': '积极',
        'negative': '消极',
        'neutral': '中性'
    };
    return labels[sentiment] || sentiment;
}

// ==================== 文段处理功能 ====================

// 初始化文段处理功能
function initializeTextProcessing() {
    const processingToggleBtn = document.getElementById('processing-toggle-btn');
    const processingOptions = document.getElementById('processing-options');
    const applyProcessingBtn = document.getElementById('apply-processing-btn');
    const previewProcessingBtn = document.getElementById('preview-processing-btn');
    const clearOptionsBtn = document.getElementById('clear-options-btn');

    // 切换面板显示/隐藏
    if (processingToggleBtn) {
        processingToggleBtn.addEventListener('click', function() {
            const isHidden = processingOptions.classList.contains('hidden');
            processingOptions.classList.toggle('hidden', !isHidden);
            processingToggleBtn.classList.toggle('active', isHidden);
        });
    }

    // 应用处理
    if (applyProcessingBtn) {
        applyProcessingBtn.addEventListener('click', applyTextProcessing);
    }

    // 预览效果
    if (previewProcessingBtn) {
        previewProcessingBtn.addEventListener('click', previewTextProcessing);
    }

    // 清除选项
    if (clearOptionsBtn) {
        clearOptionsBtn.addEventListener('click', clearProcessingOptions);
    }
}

// 应用文段处理
function applyTextProcessing() {
    const text = elements.inputText.value;
    if (!text.trim()) {
        showError('请先输入文本');
        return;
    }

    const processedText = processText(text);
    if (processedText !== text) {
        elements.inputText.value = processedText;
        currentText = processedText;
        updateTextStats();
        showSuccess('文段处理完成');
    } else {
        showInfo('没有需要处理的内容');
    }
}

// 预览文段处理效果
function previewTextProcessing() {
    const text = elements.inputText.value;
    if (!text.trim()) {
        showError('请先输入文本');
        return;
    }

    const processedText = processText(text);

    // 创建预览对话框
    const modal = createPreviewModal(text, processedText);
    document.body.appendChild(modal);
}

// 处理文本
function processText(text) {
    let processedText = text;

    // 获取选项
    const trimLines = document.getElementById('trim-lines').checked;
    const removeEmptyLines = document.getElementById('remove-empty-lines').checked;
    const mergeEmptyLines = document.getElementById('merge-empty-lines').checked;
    const removeExtraSpaces = document.getElementById('remove-extra-spaces').checked;
    const normalizeNewlines = document.getElementById('normalize-newlines').checked;
    const caseTransform = document.getElementById('case-transform').value;

    // 统一换行符
    if (normalizeNewlines) {
        processedText = processedText.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    }

    // 按行处理
    let lines = processedText.split('\n');

    // 去除首尾空格
    if (trimLines) {
        lines = lines.map(line => line.trim());
    }

    // 移除多余空格
    if (removeExtraSpaces) {
        lines = lines.map(line => line.replace(/\s+/g, ' '));
    }

    // 移除空行
    if (removeEmptyLines) {
        lines = lines.filter(line => line.trim() !== '');
    } else if (mergeEmptyLines) {
        // 合并多余空行
        const mergedLines = [];
        let lastWasEmpty = false;

        for (const line of lines) {
            const isEmpty = line.trim() === '';
            if (isEmpty && lastWasEmpty) {
                continue; // 跳过连续的空行
            }
            mergedLines.push(line);
            lastWasEmpty = isEmpty;
        }
        lines = mergedLines;
    }

    // 重新组合文本
    processedText = lines.join('\n');

    // 大小写转换
    if (caseTransform) {
        switch (caseTransform) {
            case 'upper':
                processedText = processedText.toUpperCase();
                break;
            case 'lower':
                processedText = processedText.toLowerCase();
                break;
            case 'title':
                processedText = processedText.replace(/\b\w+/g, word =>
                    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
                );
                break;
            case 'sentence':
                processedText = processedText.replace(/([.!?]\s*)([a-z])/g, (match, p1, p2) =>
                    p1 + p2.toUpperCase()
                );
                // 确保第一个字符大写
                processedText = processedText.charAt(0).toUpperCase() + processedText.slice(1);
                break;
        }
    }

    return processedText;
}

// 创建预览模态框
function createPreviewModal(originalText, processedText) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';

    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content preview-modal';

    modalContent.innerHTML = `
        <div class="modal-header">
            <h3>处理效果预览</h3>
            <button class="modal-close">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="modal-body">
            <div class="preview-container">
                <div class="preview-section">
                    <h4>原始文本</h4>
                    <div class="preview-text original-text"></div>
                    <div class="text-info">字符数: ${originalText.length}</div>
                </div>
                <div class="preview-section">
                    <h4>处理后文本</h4>
                    <div class="preview-text processed-text"></div>
                    <div class="text-info">字符数: ${processedText.length}</div>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-primary apply-btn">
                <i class="fas fa-check"></i> 应用更改
            </button>
            <button class="btn btn-secondary cancel-btn">
                <i class="fas fa-times"></i> 取消
            </button>
        </div>
    `;

    // 安全地设置文本内容
    const originalTextDiv = modalContent.querySelector('.original-text');
    const processedTextDiv = modalContent.querySelector('.processed-text');
    originalTextDiv.textContent = originalText;
    processedTextDiv.textContent = processedText;

    // 添加事件监听器
    const closeBtn = modalContent.querySelector('.modal-close');
    const applyBtn = modalContent.querySelector('.apply-btn');
    const cancelBtn = modalContent.querySelector('.cancel-btn');

    closeBtn.addEventListener('click', () => modal.remove());
    cancelBtn.addEventListener('click', () => modal.remove());
    applyBtn.addEventListener('click', () => {
        applyPreviewedText(processedText);
        modal.remove();
    });

    modal.appendChild(modalContent);
    return modal;
}

// 应用预览的文本
function applyPreviewedText(processedText) {
    elements.inputText.value = processedText;
    currentText = processedText;
    updateTextStats();
    showSuccess('文段处理完成');
}

// 清除处理选项
function clearProcessingOptions() {
    // 清除所有复选框
    document.getElementById('trim-lines').checked = false;
    document.getElementById('remove-empty-lines').checked = false;
    document.getElementById('merge-empty-lines').checked = false;
    document.getElementById('remove-extra-spaces').checked = false;
    document.getElementById('normalize-newlines').checked = false;

    // 重置下拉选择
    document.getElementById('case-transform').value = '';

    showInfo('已清除所有处理选项');
}

function showInfo(message) {
    // 简单的信息提示，可以用更好的通知组件替换
    alert('ℹ ' + message);
}

// ===== 停用词管理功能 =====

// 打开停用词管理侧边栏
function openStopwordsModal() {
    elements.stopwordsSidebar.classList.remove('hidden');
    refreshStopwords();
}

// 关闭停用词管理侧边栏
function closeStopwordsSidebar() {
    elements.stopwordsSidebar.classList.add('hidden');
    elements.newStopwordsInput.value = '';
    elements.quickStopwordsInput.value = '';
    elements.quickAddSection.classList.add('hidden');
}

// 切换快速添加区域
function toggleQuickAddSection() {
    elements.quickAddSection.classList.toggle('hidden');
    if (!elements.quickAddSection.classList.contains('hidden')) {
        elements.quickStopwordsInput.focus();
    }
}

// 快速添加停用词
async function quickAddStopwords() {
    const input = elements.quickStopwordsInput.value.trim();
    if (!input) {
        showError('请输入要添加的停用词');
        return;
    }

    // 支持中文和英文逗号分隔，以及空格、分号等分隔符
    const words = input.split(/[,，;；\s]+/)
        .map(word => word.trim())
        .filter(word => word.length > 0);

    if (words.length === 0) {
        showError('请输入有效的停用词');
        return;
    }

    try {
        const response = await fetch('/api/stopwords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                words: words
            })
        });

        const result = await response.json();

        if (result.success) {
            showSuccess(`成功添加 ${words.length} 个停用词，请重新点击"分析词频"查看效果`);
            elements.quickStopwordsInput.value = '';
            refreshStopwords();
            updateStopwordsCount();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('添加停用词失败: ' + error.message);
    }
}

// 添加停用词
async function addStopwords() {
    const input = elements.newStopwordsInput.value.trim();
    if (!input) {
        showError('请输入要添加的停用词');
        return;
    }

    // 支持中文和英文逗号分隔，以及空格、分号等分隔符
    const words = input.split(/[,，;；\s]+/)
        .map(word => word.trim())
        .filter(word => word.length > 0);

    if (words.length === 0) {
        showError('请输入有效的停用词');
        return;
    }

    try {
        const response = await fetch('/api/stopwords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                words: words
            })
        });

        const result = await response.json();

        if (result.success) {
            showSuccess(`成功添加 ${words.length} 个停用词，请重新点击"分析词频"查看效果`);
            elements.newStopwordsInput.value = '';
            refreshStopwords();
            updateStopwordsCount();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('添加停用词失败: ' + error.message);
    }
}

// 移除停用词
async function removeStopword(word) {
    try {
        const response = await fetch('/api/stopwords', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                words: [word]
            })
        });

        const result = await response.json();

        if (result.success) {
            showSuccess(`已移除停用词: ${word}，请重新点击"分析词频"查看效果`);
            refreshStopwords();
            updateStopwordsCount();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('移除停用词失败: ' + error.message);
    }
}

// 清空所有自定义停用词
async function clearAllStopwords() {
    if (!confirm('确定要清空所有自定义停用词吗？')) {
        return;
    }

    try {
        const response = await fetch('/api/stopwords/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const result = await response.json();

        if (result.success) {
            showSuccess(result.message + '，请重新点击"分析词频"查看效果');
            refreshStopwords();
            updateStopwordsCount();
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('清空停用词失败: ' + error.message);
    }
}

// 刷新停用词列表
async function refreshStopwords() {
    try {
        const response = await fetch('/api/stopwords', {
            method: 'GET'
        });

        const result = await response.json();

        if (result.success) {
            displayStopwords(result.custom_stopwords);
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('获取停用词列表失败: ' + error.message);
    }
}

// 显示停用词列表
function displayStopwords(stopwords) {
    const container = elements.currentStopwordsList;
    const countElement = elements.currentStopwordsCount;

    countElement.textContent = `(${stopwords.length}个)`;

    if (stopwords.length === 0) {
        container.innerHTML = '<p class="no-stopwords">暂无自定义停用词</p>';
        return;
    }

    const html = stopwords.map(word => `
        <span class="stopword-item">
            ${escapeHtml(word)}
            <button class="stopword-remove" onclick="removeStopword('${escapeHtml(word)}')" title="移除">
                ×
            </button>
        </span>
    `).join('');

    container.innerHTML = html;
}

// 更新停用词计数显示
async function updateStopwordsCount() {
    try {
        const response = await fetch('/api/stopwords', {
            method: 'GET'
        });

        const result = await response.json();

        if (result.success) {
            const count = result.custom_stopwords.length;
            elements.stopwordsCount.textContent = `自定义停用词: ${count}个`;
        }
    } catch (error) {
        console.error('更新停用词计数失败:', error);
    }
}

// HTML转义函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 导出结果功能
async function exportResults() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        // 先加载文本到后端
        await loadTextToBackend(text);

        const format = document.getElementById('export-format').value;
        const includeOriginal = document.getElementById('export-original').checked;
        const includeResults = document.getElementById('export-results').checked;
        const includeStats = document.getElementById('export-stats').checked;
        const includeMetadata = document.getElementById('export-metadata').checked;
        const filename = document.getElementById('export-filename').value.trim();

        const response = await fetch('/api/export_results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                format: format,
                include_original: includeOriginal,
                include_results: includeResults,
                include_stats: includeStats,
                include_metadata: includeMetadata,
                filename: filename
            })
        });

        const result = await response.json();

        if (result.success) {
            // 创建下载链接
            downloadFile(result.content, result.filename, result.mimetype);
            showSuccess(`文件 ${result.filename} 导出成功！`);
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('导出失败: ' + error.message);
    }
}

// 预览导出内容
async function previewExport() {
    const text = elements.inputText.value.trim();
    if (!text) {
        showError('请先输入文本');
        return;
    }

    showLoading();

    try {
        // 先加载文本到后端
        await loadTextToBackend(text);

        const format = document.getElementById('export-format').value;
        const includeOriginal = document.getElementById('export-original').checked;
        const includeResults = document.getElementById('export-results').checked;
        const includeStats = document.getElementById('export-stats').checked;
        const includeMetadata = document.getElementById('export-metadata').checked;
        const filename = document.getElementById('export-filename').value.trim();

        const response = await fetch('/api/export_results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                format: format,
                include_original: includeOriginal,
                include_results: includeResults,
                include_stats: includeStats,
                include_metadata: includeMetadata,
                filename: filename
            })
        });

        const result = await response.json();

        if (result.success) {
            // 显示预览
            const previewDiv = document.getElementById('export-preview');
            const previewContent = document.getElementById('preview-content');

            if (format === 'html') {
                previewContent.innerHTML = result.content;
            } else {
                previewContent.innerHTML = `<pre>${escapeHtml(result.content)}</pre>`;
            }

            previewDiv.classList.remove('hidden');
            showSuccess('预览内容已生成');
        } else {
            showError(result.error);
        }

        hideLoading();
    } catch (error) {
        hideLoading();
        showError('预览失败: ' + error.message);
    }
}

// 下载文件
function downloadFile(content, filename, mimetype) {
    const blob = new Blob([content], { type: mimetype });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}
