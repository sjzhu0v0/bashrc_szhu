#!/usr/bin/env python3
import os
import argparse

def calculate_total_size(file_list_path, unit='MB', silent=False):
    total_size = 0
    missing_files = []

    if not os.path.isfile(file_list_path):
        raise FileNotFoundError(f"路径列表文件不存在: {file_list_path}")

    with open(file_list_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            file_path = line.strip()
            if not file_path:
                continue  # 跳过空行

            if os.path.exists(file_path):
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
                else:
                    # 如果是目录，可选择跳过或报错；这里选择跳过并提示
                    if not silent:
                        print(f"[警告] 第 {line_num} 行是目录，已跳过: {file_path}")
            else:
                missing_files.append((line_num, file_path))

    # 单位换算
    unit_factors = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
    }
    if unit not in unit_factors:
        raise ValueError("单位必须是 B, KB, MB 或 GB")

    size_in_unit = total_size / unit_factors[unit]

    # 输出结果
    print(f"总文件大小: {total_size} 字节")
    print(f"总文件大小: {size_in_unit:.2f} {unit}")

    if not silent and missing_files:
        print(f"\n⚠️ 共 {len(missing_files)} 个文件不存在:")
        for line_num, path in missing_files:
            print(f"  [第 {line_num} 行] {path}")

    return total_size, size_in_unit

def main():
    parser = argparse.ArgumentParser(
        description="统计文本文档中列出的所有文件的总大小。"
    )
    parser.add_argument(
        '-f', '--filelist',
        required=True,
        help='包含文件路径列表的文本文件路径（每行一个路径）'
    )
    parser.add_argument(
        '-u', '--unit',
        choices=['B', 'KB', 'MB', 'GB'],
        default='MB',
        help='输出单位（默认: MB）'
    )
    parser.add_argument(
        '-s', '--silent',
        action='store_true',
        help='静默模式：不显示缺失文件和警告信息'
    )

    args = parser.parse_args()

    try:
        calculate_total_size(
            file_list_path=args.filelist,
            unit=args.unit,
            silent=args.silent
        )
    except Exception as e:
        print(f"错误: {e}")
        exit(1)

if __name__ == "__main__":
    main()
