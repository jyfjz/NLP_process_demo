#!/usr/bin/env python3
"""
启动文本处理工具Web应用
"""

import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def check_dependencies():
    """检查依赖"""
    try:
        import flask
        from flask_cors import CORS
        print("✓ Flask 依赖检查通过")
    except ImportError:
        print("✗ 缺少必要依赖，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-cors"])
        print("✓ 依赖安装完成")

def check_files():
    """检查必要文件"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    required_files = [
        os.path.join(project_root, 'code_model', 'text_tools.py'),
        os.path.join(script_dir, 'web_backend.py'),
        os.path.join(script_dir, 'web_frontend', 'index.html'),
        os.path.join(script_dir, 'web_frontend', 'styles.css'),
        os.path.join(script_dir, 'web_frontend', 'script.js')
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(os.path.relpath(file, os.getcwd()))

    if missing_files:
        print("✗ 缺少以下文件:")
        for file in missing_files:
            print(f"  - {file}")
        return False

    print("✓ 所有必要文件检查通过")
    return True

def open_browser():
    """延迟打开浏览器"""
    time.sleep(2)  # 等待服务器启动
    webbrowser.open('http://localhost:5000')

def main():
    """主函数"""
    print("=" * 60)
    print("文本处理和分析工具 - Web版本启动器")
    print("=" * 60)
    
    # 检查依赖
    check_dependencies()
    
    # 检查文件
    if not check_files():
        print("\n请确保所有必要文件都存在后再运行此脚本")
        return
    
    print("\n启动Web服务器...")
    
    # 设置定时器打开浏览器
    timer = Timer(3.0, open_browser)
    timer.start()
    
    try:
        # 切换到web_application目录并启动Flask应用
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        os.system('python web_backend.py')
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        timer.cancel()

if __name__ == "__main__":
    main()
