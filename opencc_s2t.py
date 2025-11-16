#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
簡體中文轉繁體中文腳本
使用 OpenCC 將 coded.ini 中的簡體字轉換為繁體字
"""

import argparse
from opencc import OpenCC

def convert_file(input_file, output_file, mode):
    # 初始化 OpenCC 轉換器 (簡體轉繁體台灣標準)
    cc = OpenCC(mode)
    
    print(f'正在讀取文件: {input_file}')
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('正在進行簡繁轉換...')
    # 進行轉換
    converted_content = cc.convert(content)
    
    # 寫入轉換後的文件
    print(f'正在寫入文件: {output_file}')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted_content)
    
    print('轉換完成！')
    print(f'原始文件: {input_file}')
    print(f'轉換後文件: {output_file}')
    
    # 統計轉換情況
    lines_original = content.count('\n') + 1
    lines_converted = converted_content.count('\n') + 1
    print(f'\n總行數: {lines_original}')

def main():
    parser = argparse.ArgumentParser(description='簡體中文轉繁體中文工具')
    parser.add_argument('-i', '--input', required=True, help='輸入文件路徑')
    parser.add_argument('-o', '--output', required=True, help='輸出文件路徑')
    parser.add_argument('-m', '--mode', default='s2tw', help='轉換模式 (例如 s2t, s2tw)')
    
    args = parser.parse_args()
    convert_file(args.input, args.output, args.mode)

if __name__ == '__main__':
    main()
