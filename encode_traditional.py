#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
繁體中文編碼工具
將繁體中文字串根據編碼表轉換為編碼格式並複製到剪貼簿
"""

import argparse
import pyperclip

def load_encoding_table(encoding_file):
    """讀取編碼表文件並建立字符到編碼的映射"""
    char_to_code = {}
    
    with open(encoding_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            
            # 解析格式: CODE=字符
            code, char = line.split('=', 1)
            if char:  # 確保字符不為空
                char_to_code[char] = code
    
    return char_to_code

def encode_text(text, char_to_code):
    """將文本轉換為編碼格式"""
    encoded_parts = []
    unknown_chars = []
    is_last_coded = False
    for char in text:
        if char in char_to_code:
            encoded_parts.append(f'@{char_to_code[char]}')
            is_last_coded = True
        elif ord(char) >= 32 and ord(char) <= 126:
            if is_last_coded:
                encoded_parts.append(' ')
            encoded_parts.append(char)
            is_last_coded = False
        else:
            # 如果字符不在編碼表中且不是 ASCII 字符，才視為未知字符
            unknown_chars.append(char)
    
    # 組合成最終格式
    encoded_text = '[zh]  ' + ''.join(encoded_parts)
    
    return encoded_text, unknown_chars

def main():
    parser = argparse.ArgumentParser(description='繁體中文編碼工具')
    parser.add_argument('-e', '--encoding', default='coded_traditional.ini', 
                        help='編碼表文件路徑 (預設: coded_traditional.ini)')
    
    args = parser.parse_args()
    
    # 讀取編碼表
    print(f'正在讀取編碼表: {args.encoding}')
    char_to_code = load_encoding_table(args.encoding)
    print(f'已載入 {len(char_to_code)} 個字符編碼\n')
    print('=' * 60)
    print('繁體中文編碼工具')
    print('輸入繁體中文後按 Enter 即可編碼並複製到剪貼簿')
    print('輸入 "exit" 或 "quit" 可退出程式')
    print('=' * 60)
    
    # 無限循環
    while True:
        try:
            # 獲取用戶輸入
            text = input('\n請輸入繁體中文: ').strip()
            
            # 檢查退出命令
            if text.lower() in ['exit', 'quit', '退出', '離開']:
                print('\n再見！')
                break
            
            # 跳過空輸入
            if not text:
                continue
            
            # 編碼文本
            encoded_text, unknown_chars = encode_text(text, char_to_code)
            print(f'編碼結果: {encoded_text}')
            
            # 顯示未知字符
            if unknown_chars:
                print(f'⚠️  警告: 以下字符不在編碼表中: {", ".join(set(unknown_chars))}')
            
            # 複製到剪貼簿
            pyperclip.copy(encoded_text)
            print('✓ 已複製到剪貼簿！')
            
        except KeyboardInterrupt:
            print('\n\n程式已中斷，再見！')
            break
        except Exception as e:
            print(f'錯誤: {e}')
            continue

if __name__ == '__main__':
    main()
