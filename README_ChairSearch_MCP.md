# ChairSearch MCP - 網絡搜索工具

這是一個強大的Mini Code Package (MCP)，用於在網絡上進行搜索並獲取網頁內容。此工具可以與Anthropic的Claude AI模型一起使用，讓Claude能夠搜索網絡獲取最新資訊。

## 功能特點

- 支持多個搜索引擎 (Google, DuckDuckGo, Bing)
- 返回格式化的搜索結果，包括標題、URL和摘要
- 能夠獲取完整網頁內容
- 從HTML中提取純文本

## 安裝

### 安裝依賴

確保已安裝所有必要的依賴項：

```bash
pip install requests beautifulsoup4
```

## 使用方法

### 搜索網絡

```python
from chairSearch_MCP import web_search

# 使用Google搜索
results = web_search("Claude AI 最新功能", engine="google", num_results=5)

# 使用DuckDuckGo搜索
results = web_search("自然語言處理", engine="duckduckgo", num_results=3)

# 使用Bing搜索
results = web_search("人工智能新聞", engine="bing", num_results=5)

# 處理結果
for result in results:
    print(f"標題: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"摘要: {result['snippet']}")
    print("---")
```

### 獲取網頁內容

```python
from chairSearch_MCP import fetch_webpage

# 獲取網頁內容
webpage_data = fetch_webpage("https://www.anthropic.com", extract_text=True)

# 獲取HTML內容
html_content = webpage_data.get("html")

# 獲取純文本內容
text_content = webpage_data.get("text")
```

## 作為Claude的MCP使用

要將此包用作Claude的MCP，請提供以下MCP函數接口：

### web_search

```
Function: web_search
Description: 在網絡上搜索查詢並返回結果
Parameters:
  - query (string): 搜索查詢字符串
  - engine (string, optional): 使用的搜索引擎 ("google", "duckduckgo", "bing")，默認為 "google"
  - num_results (integer, optional): 要返回的結果數量，默認為 5
Returns: 搜索結果字典的列表，每個字典包含標題、URL和摘要
```

### fetch_webpage

```
Function: fetch_webpage
Description: 獲取網頁內容
Parameters:
  - url (string): 要獲取的網頁URL
  - extract_text (boolean, optional): 是否從HTML中提取純文本，默認為 true
Returns: 包含網頁內容的字典，可能包含HTML和純文本
```

## 注意事項

- 此工具的爬蟲功能是基礎實現，可能不適用於所有網站
- 請尊重網站的robots.txt和使用條款
- 頻繁使用可能會導致IP被網站暫時封鎖
- 僅用於教育和合法目的

## 許可證

MIT 