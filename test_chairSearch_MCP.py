#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
測試chairSearch_MCP的功能的腳本
"""

import json
from chairSearch_MCP import web_search, fetch_webpage

def test_web_search():
    """測試網絡搜索功能"""
    print("開始測試網絡搜索...")
    
    # 測試Google搜索
    query = "Claude AI 最新功能"
    engine = "google"
    num_results = 3
    
    print(f"使用 {engine} 搜索: '{query}'，返回 {num_results} 個結果")
    results = web_search(query, engine, num_results)
    
    print(f"找到 {len(results)} 個結果:")
    for i, result in enumerate(results, 1):
        print(f"\n結果 #{i}:")
        print(f"標題: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"摘要: {result['snippet'][:150]}...")
    
    print("\n測試網絡搜索完成！")

def test_fetch_webpage():
    """測試網頁內容獲取功能"""
    print("\n開始測試網頁內容獲取...")
    
    # 測試獲取網頁內容
    url = "https://www.anthropic.com"
    print(f"獲取網頁內容: {url}")
    
    result = fetch_webpage(url)
    
    if "error" in result:
        print(f"錯誤: {result['error']}")
    else:
        print("成功獲取網頁內容！")
        html_length = len(result.get("html", ""))
        text_length = len(result.get("text", ""))
        print(f"HTML 內容長度: {html_length} 字符")
        print(f"純文本內容長度: {text_length} 字符")
        # 顯示前 200 個字符的純文本
        if "text" in result:
            print(f"\n前 200 個字符的純文本預覽:\n{result['text'][:200]}...")
    
    print("\n測試網頁內容獲取完成！")

if __name__ == "__main__":
    print("=" * 50)
    print("ChairSearch MCP 測試")
    print("=" * 50)
    
    try:
        test_web_search()
    except Exception as e:
        print(f"網絡搜索測試出錯: {e}")
    
    try:
        test_fetch_webpage()
    except Exception as e:
        print(f"網頁內容獲取測試出錯: {e}")
    
    print("\n" + "=" * 50)
    print("測試完成！")
    print("=" * 50) 