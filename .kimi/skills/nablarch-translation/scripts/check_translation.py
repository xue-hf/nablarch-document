#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查翻译状态（辅助工具）

本脚本用于辅助检查翻译状态，AI 可以直接完成相同功能。

使用方法：
    python .kimi/skills/nablarch-translation/scripts/check_translation.py

输出：
    - 已翻译文件数
    - 未翻译文件数
    - 翻译进度百分比
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
JA_DIR = PROJECT_ROOT / "ja"
ZH_DIR = PROJECT_ROOT / "zh_CN"


def contains_japanese_kana(text):
    """检查文本是否包含日文假名"""
    hiragana = re.search(r'[\u3040-\u309f]', text)
    katakana = re.search(r'[\u30a0-\u30ff]', text)
    return hiragana is not None or katakana is not None


def check_file_status(ja_path, zh_path):
    """检查单个文件的翻译状态"""
    if not zh_path.exists():
        return 'missing'
    
    # 检查是否完全相同
    with open(ja_path, 'rb') as f1, open(zh_path, 'rb') as f2:
        if f1.read() == f2.read():
            return 'identical'
    
    # 检查是否包含日文假名
    with open(zh_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if contains_japanese_kana(content):
        return 'untranslated'
    else:
        return 'translated'


def main():
    print("=" * 60)
    print("Nablarch 文档翻译状态检查")
    print("=" * 60)
    print()
    
    # 获取所有日文文件
    ja_files = []
    for root, dirs, files in os.walk(JA_DIR):
        for file in files:
            if file.endswith('.rst'):
                ja_files.append(os.path.join(root, file))
    
    translated = 0
    identical = 0
    untranslated = 0
    missing = 0
    
    for ja_path in ja_files:
        rel_path = os.path.relpath(ja_path, JA_DIR)
        zh_path = ZH_DIR / rel_path
        
        status = check_file_status(ja_path, zh_path)
        
        if status == 'missing':
            missing += 1
        elif status == 'identical':
            identical += 1
        elif status == 'untranslated':
            untranslated += 1
        else:
            translated += 1
    
    total = len(ja_files)
    progress = translated / total * 100 if total > 0 else 0
    
    print(f"总文件数: {total}")
    print(f"已翻译:   {translated}")
    print(f"未翻译:   {identical + untranslated}")
    print(f"  - 与原文相同: {identical}")
    print(f"  - 包含日文:   {untranslated}")
    print(f"缺失文件: {missing}")
    print(f"进度:     {progress:.1f}%")
    print()
    print("=" * 60)
    print("提示：AI 可以直接完成翻译和进度更新任务")
    print("      本脚本仅作为辅助检查工具")
    print("=" * 60)


if __name__ == '__main__':
    main()
