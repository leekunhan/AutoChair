"""
ChairSearch MCP - 網絡搜索工具

此MCP工具允許用戶通過不同的搜索引擎進行網絡搜索，並返回搜索結果。
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import urllib.parse
from typing import List, Dict, Any, Optional

class SearchResult:
    """搜索結果的數據結構"""
    def __init__(self, title: str, url: str, snippet: str):
        self.title = title
        self.url = url
        self.snippet = snippet
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet
        }

class ChairSearch:
    """ChairSearch類提供不同的網絡搜索方法"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def search_google(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """
        使用Google搜索引擎進行搜索
        
        Args:
            query: 搜索查詢字符串
            num_results: 要返回的結果數量
            
        Returns:
            一個SearchResult對象列表
        """
        # 注意：這是一個簡單的網頁抓取方法，僅用於教育目的
        # 實際應用中應考慮使用官方的Google API
        
        escaped_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={escaped_query}&num={num_results}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = []
            
            # Google搜索結果通常位於具有特定類的div元素中
            result_elements = soup.select("div.g")
            
            for element in result_elements[:num_results]:
                try:
                    title_element = element.select_one("h3")
                    link_element = element.select_one("a")
                    snippet_element = element.select_one("div.VwiC3b")
                    
                    if title_element and link_element and snippet_element:
                        title = title_element.text
                        url = link_element["href"]
                        if url.startswith("/url?"):
                            url = re.search(r"url=([^&]+)", url).group(1)
                        snippet = snippet_element.text
                        
                        search_results.append(SearchResult(title, url, snippet))
                except Exception as e:
                    print(f"解析結果時出錯: {e}")
                    continue
            
            return search_results
        
        except Exception as e:
            print(f"搜索時發生錯誤: {e}")
            return []
    
    def search_duckduckgo(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """
        使用DuckDuckGo搜索引擎進行搜索
        
        Args:
            query: 搜索查詢字符串
            num_results: 要返回的結果數量
            
        Returns:
            一個SearchResult對象列表
        """
        escaped_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={escaped_query}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = []
            
            result_elements = soup.select(".result")
            
            for element in result_elements[:num_results]:
                try:
                    title_element = element.select_one(".result__title")
                    link_element = element.select_one(".result__url")
                    snippet_element = element.select_one(".result__snippet")
                    
                    if title_element and link_element and snippet_element:
                        title = title_element.text.strip()
                        url = link_element.text.strip()
                        snippet = snippet_element.text.strip()
                        
                        search_results.append(SearchResult(title, url, snippet))
                except Exception as e:
                    print(f"解析結果時出錯: {e}")
                    continue
            
            return search_results
        
        except Exception as e:
            print(f"搜索時發生錯誤: {e}")
            return []
    
    def search_bing(self, query: str, num_results: int = 5) -> List[SearchResult]:
        """
        使用Bing搜索引擎進行搜索
        
        Args:
            query: 搜索查詢字符串
            num_results: 要返回的結果數量
            
        Returns:
            一個SearchResult對象列表
        """
        escaped_query = urllib.parse.quote(query)
        url = f"https://www.bing.com/search?q={escaped_query}&count={num_results}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            search_results = []
            
            result_elements = soup.select(".b_algo")
            
            for element in result_elements[:num_results]:
                try:
                    title_element = element.select_one("h2")
                    link_element = element.select_one("cite")
                    snippet_element = element.select_one(".b_caption p")
                    
                    if title_element and link_element and snippet_element:
                        title = title_element.text.strip()
                        url = link_element.text.strip()
                        snippet = snippet_element.text.strip()
                        
                        search_results.append(SearchResult(title, url, snippet))
                except Exception as e:
                    print(f"解析結果時出錯: {e}")
                    continue
            
            return search_results
        
        except Exception as e:
            print(f"搜索時發生錯誤: {e}")
            return []

def fetch_webpage_content(url: str) -> Optional[str]:
    """
    獲取網頁的內容
    
    Args:
        url: 要獲取的網頁URL
        
    Returns:
        網頁的HTML內容，如果失敗則返回None
    """
    try:
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"獲取網頁內容時發生錯誤: {e}")
        return None

def extract_text_from_html(html_content: str) -> str:
    """
    從HTML內容中提取純文本
    
    Args:
        html_content: HTML內容
        
    Returns:
        提取的純文本
    """
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 移除腳本和樣式元素
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    # 獲取文本
    text = soup.get_text()
    
    # 突破長行
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
    # 重新組合成文本
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

# MCP API函數
def web_search(query: str, engine: str = "google", num_results: int = 5) -> List[Dict[str, str]]:
    """
    在網絡上搜索查詢並返回結果
    
    Args:
        query: 搜索查詢字符串
        engine: 使用的搜索引擎 ("google", "duckduckgo", "bing")
        num_results: 要返回的結果數量
        
    Returns:
        搜索結果字典的列表，每個字典包含標題、URL和摘要
    """
    searcher = ChairSearch()
    
    # 根據指定的引擎選擇搜索方法
    if engine.lower() == "google":
        results = searcher.search_google(query, num_results)
    elif engine.lower() == "duckduckgo":
        results = searcher.search_duckduckgo(query, num_results)
    elif engine.lower() == "bing":
        results = searcher.search_bing(query, num_results)
    else:
        # 默認使用Google
        results = searcher.search_google(query, num_results)
    
    # 將結果轉換為字典列表
    return [result.to_dict() for result in results]

def fetch_webpage(url: str, extract_text: bool = True) -> Dict[str, str]:
    """
    獲取網頁內容
    
    Args:
        url: 要獲取的網頁URL
        extract_text: 是否從HTML中提取純文本
        
    Returns:
        包含網頁內容的字典
    """
    html_content = fetch_webpage_content(url)
    
    if html_content is None:
        return {"error": "無法獲取網頁內容"}
    
    result = {"html": html_content}
    
    if extract_text:
        text_content = extract_text_from_html(html_content)
        result["text"] = text_content
    
    return result
