# -*- coding: utf-8 -*-
"""
检查 zh_CN 目录下的文件翻译状态
判断标准：文件中没有日文假名（平假名/片假名）则认为已翻译
排除日文标点符号：・(U+30FB)、ー(U+30FC)、～(U+FF5E)等

用法：
  python check_translation.py                          # 检查所有文件
  python check_translation.py -d <目录>                # 检查指定目录
  python check_translation.py -f <文件路径>            # 检查单个文件
  python check_translation.py -d <目录> --missing      # 只显示缺失的文件
"""
import os
import re
import sys
import argparse

# 设置stdout编码为utf-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def contains_japanese_kana(text):
    """检查文本是否包含日文假名（平假名或片假名）
    排除日文符号：・(U+30FB)、ー(U+30FC)、～(U+FF5E)等
    """
    # 平假名: \u3040-\u309f（排除 \u309B-\u309C 浊音符号）
    # 片假名: \u30a0-\u30ff（排除 \u30FB-\u30FE 符号）
    hiragana = re.search(r'[\u3040-\u309a\u309d-\u309f]', text)  # 排除 309B-309C
    katakana = re.search(r'[\u30a0-\u30fa]', text)  # 排除 30FB-30FE
    return hiragana is not None or katakana is not None


def check_file_status(ja_path, zh_path):
    """
    检查单个文件的翻译状态
    返回: ('translated', 'untranslated', 'identical', 或 'missing')
    """
    if not os.path.exists(zh_path):
        return 'missing'
    
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


def get_rst_files(directory):
    """获取指定目录下的所有.rst文件（相对路径）"""
    rst_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.rst'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, directory).replace('\\', '/')
                rst_files.append(rel_path)
    return sorted(rst_files)


def check_all():
    """检查所有文件的翻译状态"""
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
        
        status = check_file_status(ja_path, zh_path)
        
        if status == 'missing':
            missing.append(rel_path)
            untranslated.append(rel_path)
        elif status == 'identical':
            identical.append(rel_path)
            untranslated.append(rel_path)
        elif status == 'untranslated':
            untranslated.append(rel_path)
        else:
            translated.append(rel_path)
    
    # 输出统计
    print("=" * 60)
    print("Nablarch 文档中文翻译进度统计")
    print("=" * 60)
    print("\n判断标准：文件中不包含日文假名（平假名/片假名，排除标点符号）")
    print("\n总文件数: {}".format(len(ja_files)))
    print("已翻译:   {}".format(len(translated)))
    print("未翻译:   {}".format(len(untranslated)))
    print("  - 与原文相同: {}".format(len(identical)))
    print("  - 包含日文:   {}".format(len(untranslated) - len(identical) - len(missing)))
    print("  - 文件缺失:   {}".format(len(missing)))
    print("进度:     {:.1f}%".format(len(translated)/len(ja_files)*100 if ja_files else 0))
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
    if missing:
        print("\n【文件缺失】")
        for f in sorted(missing):
            print("  [MISSING] {}".format(f))
    
    if identical:
        print("\n【与原文完全相同】")
        for f in sorted(identical)[:20]:
            print("  [==] {}".format(f))
        if len(identical) > 20:
            print("  ... 还有 {} 个".format(len(identical) - 20))
    
    japanese_files = [f for f in untranslated if f not in identical and f not in missing]
    if japanese_files:
        print("\n【包含日文假名】")
        for f in sorted(japanese_files)[:30]:
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


def check_directory(directory, show_missing_only=False):
    """检查指定目录的翻译状态"""
    ja_dir = os.path.join('ja', directory)
    zh_dir = os.path.join('zh_CN', directory)
    
    if not os.path.exists(ja_dir):
        print("错误：日文目录不存在: {}".format(ja_dir))
        return
    
    # 获取该目录下的所有.rst文件
    ja_files = []
    for root, dirs, files in os.walk(ja_dir):
        for file in files:
            if file.endswith('.rst'):
                full_path = os.path.join(root, file)
                # 计算相对路径（相对于ja目录）
                rel_path = os.path.relpath(full_path, 'ja').replace('\\', '/')
                ja_files.append(rel_path)
    
    if not ja_files:
        print("目录 {} 下没有找到.rst文件".format(directory))
        return
    
    translated = []
    untranslated = []
    identical = []
    missing = []
    
    for rel_path in ja_files:
        ja_path = os.path.join('ja', rel_path)
        zh_path = os.path.join('zh_CN', rel_path)
        
        status = check_file_status(ja_path, zh_path)
        
        if status == 'missing':
            missing.append(rel_path)
            if show_missing_only:
                untranslated.append(rel_path)
        elif status == 'identical':
            identical.append(rel_path)
            if not show_missing_only:
                untranslated.append(rel_path)
        elif status == 'untranslated':
            untranslated.append(rel_path)
        else:
            translated.append(rel_path)
    
    # 输出统计
    print("=" * 60)
    print("目录翻译状态: {}".format(directory))
    print("=" * 60)
    print("\n总文件数: {}".format(len(ja_files)))
    print("已翻译:   {}".format(len(translated)))
    print("未翻译:   {}".format(len(untranslated)))
    if not show_missing_only:
        print("  - 与原文相同: {}".format(len(identical)))
        print("  - 包含日文:   {}".format(len([f for f in untranslated if f not in identical and f not in missing])))
    print("  - 文件缺失:   {}".format(len(missing)))
    print("进度:     {:.1f}%".format(len(translated)/len(ja_files)*100 if ja_files else 0))
    print()
    
    if not show_missing_only:
        # 输出已翻译文件
        if translated:
            print("=" * 60)
            print("已翻译文件 ({}个)".format(len(translated)))
            print("=" * 60)
            for f in sorted(translated):
                print("  [OK] {}".format(f))
            print()
    
    # 输出未翻译文件
    if untranslated:
        print("=" * 60)
        if show_missing_only:
            print("缺失文件列表 ({}个)".format(len(untranslated)))
        else:
            print("未翻译文件列表 ({}个)".format(len(untranslated)))
        print("=" * 60)
        
        if missing:
            print("\n【文件缺失】")
            for f in sorted(missing):
                print("  [MISSING] {}".format(f))
        
        if not show_missing_only:
            if identical:
                print("\n【与原文完全相同】")
                for f in sorted(identical):
                    print("  [==] {}".format(f))
            
            japanese_files = [f for f in untranslated if f not in identical and f not in missing]
            if japanese_files:
                print("\n【包含日文假名】")
                for f in sorted(japanese_files):
                    print("  [JP] {}".format(f))
        
        print()


def check_single_file(file_path):
    """检查单个文件的翻译状态"""
    # 处理相对路径
    if file_path.startswith('ja/'):
        rel_path = file_path[3:]
        ja_path = file_path
    elif file_path.startswith('zh_CN/'):
        rel_path = file_path[6:]
        ja_path = os.path.join('ja', rel_path)
    else:
        rel_path = file_path
        ja_path = os.path.join('ja', file_path)
    
    zh_path = os.path.join('zh_CN', rel_path)
    
    # 检查文件是否存在
    if not os.path.exists(ja_path):
        print("错误：日文原文文件不存在: {}".format(ja_path))
        return
    
    if not ja_path.endswith('.rst'):
        print("错误：只支持.rst文件")
        return
    
    print("=" * 60)
    print("单个文件翻译状态检查")
    print("=" * 60)
    print("\n文件路径: {}".format(rel_path))
    print("日文原文: {}".format(ja_path))
    print("中文译文: {}".format(zh_path))
    print()
    
    status = check_file_status(ja_path, zh_path)
    
    status_map = {
        'translated': ('已翻译', '✅ 该文件已翻译完成，不含日文假名'),
        'untranslated': ('未翻译', '🟡 该文件包含日文假名，需要翻译'),
        'identical': ('与原文相同', '🔴 该文件与原文完全相同'),
        'missing': ('文件缺失', '🔴 中文译文文件不存在')
    }
    
    status_text, description = status_map.get(status, ('未知', ''))
    print("状态: {}".format(status_text))
    print(description)
    
    # 如果文件存在，显示部分内容
    if os.path.exists(zh_path):
        print("\n" + "-" * 60)
        print("中文文件前10行预览：")
        print("-" * 60)
        with open(zh_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            for i, line in enumerate(lines, 1):
                print("{:3d}| {}".format(i, line.rstrip()))


def main():
    parser = argparse.ArgumentParser(
        description='检查 Nablarch 文档的中文翻译状态',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python check_translation.py                          # 检查所有文件
  python check_translation.py -d application_framework/handlers  # 检查指定目录
  python check_translation.py -f application_framework/handlers/web/index.rst  # 检查单个文件
  python check_translation.py -d development_tools --missing     # 只显示缺失的文件
        '''
    )
    
    parser.add_argument('-d', '--directory', 
                        help='检查指定目录（相对于ja目录的路径，如: application_framework/handlers）')
    parser.add_argument('-f', '--file', 
                        help='检查单个文件（相对路径，如: application_framework/handlers/web/index.rst）')
    parser.add_argument('--missing', action='store_true',
                        help='只显示缺失的文件（与-d选项配合使用）')
    
    args = parser.parse_args()
    
    if args.file:
        # 检查单个文件
        check_single_file(args.file)
    elif args.directory:
        # 检查指定目录
        check_directory(args.directory, show_missing_only=args.missing)
    else:
        # 检查所有文件
        check_all()


if __name__ == '__main__':
    main()
