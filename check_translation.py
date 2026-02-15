# -*- coding: utf-8 -*-
"""
检查 zh_CN 目录下的文件翻译状态
判断标准：文件中没有日文假名（平假名/片假名）则认为已翻译
"""
import os
import re
import sys

# 设置stdout编码为utf-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def contains_japanese_kana(text):
    """检查文本是否包含日文假名（平假名或片假名）"""
    # 平假名: \u3040-\u309f
    # 片假名: \u30a0-\u30ff
    hiragana = re.search(r'[\u3040-\u309f]', text)
    katakana = re.search(r'[\u30a0-\u30ff]', text)
    return hiragana is not None or katakana is not None

def check_translation_status(ja_path, zh_path):
    """
    检查翻译状态
    返回: ('translated', 'untranslated', 或 'identical')
    """
    # 首先检查文件是否完全相同
    with open(ja_path, 'rb') as f1, open(zh_path, 'rb') as f2:
        if f1.read() == f2.read():
            return 'identical'
    
    # 读取中文文件内容
    with open(zh_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含日文假名
    if contains_japanese_kana(content):
        return 'untranslated'
    else:
        return 'translated'

def main():
    ja_files = []
    for root, dirs, files in os.walk('ja'):
        for file in files:
            if file.endswith('.rst'):
                ja_files.append(os.path.join(root, file))
    
    translated = []
    untranslated = []
    identical = []
    missing = []
    
    for ja_path in ja_files:
        rel_path = ja_path.replace('ja\\', '').replace('ja/', '')
        zh_path = os.path.join('zh_CN', rel_path)
        
        if not os.path.exists(zh_path):
            missing.append(rel_path)
            continue
        
        status = check_translation_status(ja_path, zh_path)
        
        if status == 'identical':
            identical.append(rel_path)
            untranslated.append(rel_path)  # 完全相同的也算未翻译
        elif status == 'untranslated':
            untranslated.append(rel_path)
        else:
            translated.append(rel_path)
    
    # 输出统计
    print("=" * 60)
    print("Nablarch 文档中文翻译进度统计")
    print("=" * 60)
    print("\n判断标准：文件中不包含日文假名（平假名/片假名）")
    print("\n总文件数: {}".format(len(ja_files)))
    print("已翻译:   {}".format(len(translated)))
    print("未翻译:   {}".format(len(untranslated)))
    print("  - 与原文相同: {}".format(len(identical)))
    print("  - 包含日文:   {}".format(len(untranslated) - len(identical)))
    print("进度:     {:.1f}%".format(len(translated)/len(ja_files)*100))
    print()
    
    # 输出已翻译文件
    print("=" * 60)
    print("已翻译文件列表 ({}个)".format(len(translated)))
    print("=" * 60)
    for f in sorted(translated):
        print("  [OK] {}".format(f))
    print()
    
    # 输出未翻译文件
    print("=" * 60)
    print("未翻译文件列表 ({}个)".format(len(untranslated)))
    print("=" * 60)
    
    # 分类显示
    identical_files = sorted(identical)
    japanese_files = sorted([f for f in untranslated if f not in identical])
    
    if identical_files:
        print("\n【与原文完全相同】")
        for f in identical_files[:20]:
            print("  [==] {}".format(f))
        if len(identical_files) > 20:
            print("  ... 还有 {} 个".format(len(identical_files) - 20))
    
    if japanese_files:
        print("\n【包含日文假名】")
        for f in japanese_files[:30]:
            print("  [JP] {}".format(f))
        if len(japanese_files) > 30:
            print("  ... 还有 {} 个".format(len(japanese_files) - 30))
    
    # 保存结果
    with open('_translated.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(translated)))
    with open('_untranslated.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(untranslated)))
    
    print("\n" + "=" * 60)
    print("结果已保存到 _translated.txt 和 _untranslated.txt")
    print("=" * 60)

if __name__ == '__main__':
    main()
