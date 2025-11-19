#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
台灣慣用詞替換工具
從字典檔載入詞彙對照表，替換文件中的詞彙
"""

import argparse
import json
from pathlib import Path


def load_dict(dict_file):
    """從 JSON 字典檔載入詞彙對照表"""
    term_dict = {}
    
    if not Path(dict_file).exists():
        print(f'錯誤：字典檔不存在 - {dict_file}')
        return term_dict
    
    try:
        with open(dict_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 過濾掉以底線開頭的 key（如 _comment）
            term_dict = {k: v for k, v in data.items() if not k.startswith('_')}
    except json.JSONDecodeError as e:
        print(f'錯誤：JSON 格式錯誤 - {e}')
    except Exception as e:
        print(f'錯誤：無法讀取 JSON 檔案 - {e}')
    
    return term_dict


def replace_terms(text, term_dict):
    """替換文本中的詞彙"""
    result = text
    replacements = []
    
    # 按詞長度排序，優先替換較長的詞（避免部分替換問題）
    sorted_terms = sorted(term_dict.items(), key=lambda x: len(x[0]), reverse=True)
    
    for old_term, new_term in sorted_terms:
        if old_term in result:
            count = result.count(old_term)
            if count > 0:
                replacements.append((old_term, new_term, count))
                result = result.replace(old_term, new_term)
    
    return result, replacements


def process_file(input_file, output_file, dict_file, verbose=False):
    """處理文件替換"""
    # 載入字典
    print(f'正在載入字典檔: {dict_file}')
    term_dict = load_dict(dict_file)
    
    if not term_dict:
        print('字典檔為空或載入失敗')
        return
    
    print(f'已載入 {len(term_dict)} 個詞彙對照')
    
    # 讀取輸入文件
    print(f'\n正在讀取文件: {input_file}')
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f'錯誤：無法讀取文件 - {e}')
        return
    
    # 執行替換
    print('正在進行詞彙替換...')
    result, replacements = replace_terms(content, term_dict)
    
    # 寫入輸出文件
    print(f'正在寫入文件: {output_file}')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
    except Exception as e:
        print(f'錯誤：無法寫入文件 - {e}')
        return
    
    # 顯示統計信息
    print('\n' + '=' * 60)
    print('替換完成！')
    print('=' * 60)
    print(f'原始文件: {input_file}')
    print(f'輸出文件: {output_file}')
    print(f'字典檔案: {dict_file}')
    print(f'共替換了 {len(replacements)} 種詞彙')
    
    # 統計總替換次數
    total_count = sum(count for _, _, count in replacements)
    print(f'總替換次數: {total_count}')
    
    # 顯示詳細替換信息
    if verbose and replacements:
        print('\n替換詳情：')
        print('-' * 60)
        print(f'{"原詞":20s} -> {"新詞":20s} {"次數":>8s}')
        print('-' * 60)
        for old_term, new_term, count in sorted(replacements, key=lambda x: x[2], reverse=True):
            print(f'{old_term:20s} -> {new_term:20s} {count:8d}')


def main():
    parser = argparse.ArgumentParser(
        description='台灣慣用詞替換工具 - 使用獨立字典檔',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用範例:
  %(prog)s -i global_chs.ini -o global_cht_fixed.ini
  %(prog)s -i input.txt -o output.txt -d custom_dict.json
  %(prog)s -i input.txt -o output.txt -v
  
字典檔格式 (JSON):
  {
    "_comment": "註釋",
    "軟件": "軟體",
    "信息": "資訊"
  }
        '''
    )
    
    parser.add_argument('-i', '--input', required=True,
                        help='輸入文件路徑')
    parser.add_argument('-o', '--output',
                        help='輸出文件路徑')
    parser.add_argument('-d', '--dict', default='term_dict.json',
                        help='字典檔路徑 (預設: term_dict.json)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='顯示詳細替換信息')
    
    args = parser.parse_args()
    if not args.output:
        args.output = args.input
    # 處理文件
    process_file(args.input, args.output, args.dict, args.verbose)


if __name__ == '__main__':
    main()
