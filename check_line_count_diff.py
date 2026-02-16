#!/usr/bin/env python3
"""
检查翻译前后文件行数偏差
用于检测翻译内容是否严重不足

用法:
    python check_line_count_diff.py [目录路径]
    
    如果不指定目录，则检查所有文件
    如果指定目录，则检查该目录下的所有文件
    
输出格式:
    文件路径: +偏差值 (中文行数-日文行数)
    例如: application_framework/web/index.rst: +5 (120->125)
    
    偏差值说明:
    +N  中文比日文多N行（可能添加了说明或格式调整）
    -N  中文比日文少N行（可能翻译不完整）
    0   行数相同
"""

import os
import sys
import argparse
from pathlib import Path


def count_lines(filepath):
    """计算文件行数"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception as e:
        return None


def get_relative_path(abs_path, base_dir):
    """获取相对路径"""
    try:
        return Path(abs_path).relative_to(base_dir).as_posix()
    except:
        return abs_path


def check_file_pair(ja_file, zh_file):
    """检查一对文件的行数差异"""
    ja_lines = count_lines(ja_file)
    zh_lines = count_lines(zh_file)
    
    if ja_lines is None or zh_lines is None:
        return None
    
    diff = zh_lines - ja_lines
    return {
        'ja_lines': ja_lines,
        'zh_lines': zh_lines,
        'diff': diff
    }


def find_rst_files(directory):
    """递归查找所有 .rst 文件"""
    rst_files = []
    for root, dirs, files in os.walk(directory):
        # 排除 _build 目录
        dirs[:] = [d for d in dirs if d != '_build']
        for file in files:
            if file.endswith('.rst'):
                rst_files.append(os.path.join(root, file))
    return rst_files


def check_directory(ja_dir, zh_dir, subdir=None):
    """检查指定目录下的所有文件"""
    results = []
    
    if subdir:
        ja_path = os.path.join(ja_dir, subdir)
        zh_path = os.path.join(zh_dir, subdir)
    else:
        ja_path = ja_dir
        zh_path = zh_dir
    
    if not os.path.exists(ja_path):
        print(f"错误: 日文目录不存在: {ja_path}")
        return results
    
    if not os.path.exists(zh_path):
        print(f"错误: 中文目录不存在: {zh_path}")
        return results
    
    # 获取所有日文文件
    ja_files = find_rst_files(ja_path)
    
    for ja_file in ja_files:
        # 计算相对路径
        rel_path = get_relative_path(ja_file, ja_path)
        
        # 构建对应的中文文件路径
        zh_file = os.path.join(zh_path, rel_path)
        
        if not os.path.exists(zh_file):
            results.append({
                'file': rel_path,
                'status': 'missing',
                'ja_lines': count_lines(ja_file),
                'zh_lines': 0,
                'diff': None
            })
            continue
        
        # 检查行数差异
        result = check_file_pair(ja_file, zh_file)
        if result:
            results.append({
                'file': rel_path,
                'status': 'ok',
                **result
            })
    
    return results


def print_results(results, threshold=10):
    """打印结果
    
    threshold: 偏差阈值，超过此值的会高亮显示
    """
    if not results:
        print("没有找到可比较的文件")
        return
    
    # 分类
    missing = [r for r in results if r['status'] == 'missing']
    large_negative = [r for r in results if r['status'] == 'ok' and r['diff'] <= -threshold]
    negative = [r for r in results if r['status'] == 'ok' and -threshold < r['diff'] < 0]
    zero = [r for r in results if r['status'] == 'ok' and r['diff'] == 0]
    positive = [r for r in results if r['status'] == 'ok' and r['diff'] > 0]
    
    # 按偏差值排序
    large_negative.sort(key=lambda x: x['diff'])
    negative.sort(key=lambda x: x['diff'])
    positive.sort(key=lambda x: x['diff'], reverse=True)
    
    print("=" * 80)
    print("翻译文件行数偏差检查报告")
    print("=" * 80)
    print(f"检查文件总数: {len(results)}")
    print(f"  - 中文缺失: {len(missing)}")
    print(f"  - 严重不足 (偏差 <= -{threshold}): {len(large_negative)}")
    print(f"  - 轻微不足 (-{threshold} < 偏差 < 0): {len(negative)}")
    print(f"  - 行数相同: {len(zero)}")
    print(f"  - 中文更多: {len(positive)}")
    print()
    
    # 显示严重不足的翻译
    if large_negative:
        print("-" * 80)
        print(f"[WARNING] 严重不足的翻译 (偏差 <= -{threshold})")
        print("-" * 80)
        for r in large_negative:
            print(f"  {r['file']}: {r['diff']:+d} ({r['ja_lines']} -> {r['zh_lines']})")
        print()
    
    # 显示轻微不足的翻译
    if negative:
        print("-" * 80)
        print(f"[INFO] 轻微不足的翻译 (-{threshold} < 偏差 < 0)")
        print("-" * 80)
        for r in negative:
            print(f"  {r['file']}: {r['diff']:+d} ({r['ja_lines']} -> {r['zh_lines']})")
        print()
    
    # 显示中文缺失的文件
    if missing:
        print("-" * 80)
        print("❌ 中文文件缺失")
        print("-" * 80)
        for r in missing:
            print(f"  {r['file']}: 缺失 (日文 {r['ja_lines']} 行)")
        print()
    
    # 显示中文更多的文件（可选，默认不显示）
    if positive and len(sys.argv) > 1 and '--verbose' in sys.argv:
        print("-" * 80)
        print("[INFO] 中文行数更多的文件")
        print("-" * 80)
        for r in positive[:20]:  # 只显示前20个
            print(f"  {r['file']}: +{r['diff']} ({r['ja_lines']} -> {r['zh_lines']})")
        if len(positive) > 20:
            print(f"  ... 还有 {len(positive) - 20} 个文件")
        print()
    
    # 汇总统计
    print("=" * 80)
    print("统计汇总")
    print("=" * 80)
    
    all_diffs = [r['diff'] for r in results if r['status'] == 'ok']
    if all_diffs:
        avg_diff = sum(all_diffs) / len(all_diffs)
        max_diff = max(all_diffs)
        min_diff = min(all_diffs)
        
        print(f"平均偏差: {avg_diff:+.1f} 行")
        print(f"最大偏差: +{max_diff} 行")
        print(f"最小偏差: {min_diff} 行")
    
    print()
    print("说明:")
    print("  - 中文翻译通常应该与日文原文行数相近")
    print("  - 偏差 < -10 可能表示翻译严重不完整")
    print("  - 偏差 > +50 可能表示添加了过多解释或格式问题")


def main():
    parser = argparse.ArgumentParser(
        description='检查翻译前后文件行数偏差',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python check_line_count_diff.py
    检查所有文件
    
  python check_line_count_diff.py application_framework/handlers
    只检查 handlers 目录
    
  python check_line_count_diff.py --threshold 5
    使用阈值 5 来判断严重不足
        """
    )
    parser.add_argument(
        'directory',
        nargs='?',
        help='要检查的子目录（相对于 ja/ 和 zh_CN/ 的路径）'
    )
    parser.add_argument(
        '-t', '--threshold',
        type=int,
        default=10,
        help='偏差阈值，小于此负值的视为严重不足 (默认: 10)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细信息，包括中文更多的文件'
    )
    
    args = parser.parse_args()
    
    # 项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = script_dir
    
    ja_dir = os.path.join(root_dir, 'ja')
    zh_dir = os.path.join(root_dir, 'zh_CN')
    
    if not os.path.exists(ja_dir):
        print(f"错误: 找不到日文原文目录: {ja_dir}")
        sys.exit(1)
    
    if not os.path.exists(zh_dir):
        print(f"错误: 找不到中文翻译目录: {zh_dir}")
        sys.exit(1)
    
    # 执行检查
    results = check_directory(ja_dir, zh_dir, args.directory)
    
    # 打印结果
    if args.verbose:
        sys.argv.append('--verbose')
    print_results(results, args.threshold)


if __name__ == '__main__':
    main()
