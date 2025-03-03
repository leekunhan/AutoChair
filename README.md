# AutoChair
Use LLM auto choose the suitable chair.

## 系統概述

AutoChair 是一個智能椅子推薦系統，使用 LLM (大型語言模型) 和向量數據庫來自動選擇適合用戶需求的椅子。系統由 React 前端和 FastAPI 後端組成，使用 OpenAI 的嵌入模型來處理自然語言查詢。

## 功能特點

- 基於用戶自然語言描述推薦合適的椅子
- 顯示椅子的詳細信息，包括最大承重和產品圖片
- 提供產品鏈接以便進一步查看
- 使用向量數據庫進行高效的相似度搜索

## 安裝與設置

### 前提條件

- Node.js 和 npm (用於前端)
- Python 3.8+ (用於後端)
- OpenAI API 密鑰

### 安裝依賴

1. **後端依賴**

```bash
pip install -r requirements.txt
```

2. **前端依賴**

```bash
cd sample-website
npm install
```

### 配置環境變量

1. 在項目根目錄創建 `.env` 文件並添加您的 OpenAI API 密鑰：

```bash
OPENAI_API_KEY=your_openai_api_key
```

2. 確保 `chair_image` 目錄存在並包含必要的椅子圖片。

## 啟動服務

### 啟動後端 FastAPI 服務

```bash
uvicorn vectordb_fastapi:app --reload --host 0.0.0.0 --port 8000
```
這將啟動 FastAPI 服務器在 `http://localhost:8000`。首次運行時，系統將創建一個新的向量數據庫 `chairDB`。

### 啟動前端 React 應用

```bash
cd sample-website
npm start
```

這將在 `http://localhost:3000` 啟動 React 應用。

## 使用方法

1. 打開瀏覽器並訪問 `http://localhost:3000`
2. 點擊「開啟機器人」按鈕打開聊天界面
3. 在聊天框中輸入您的椅子需求，例如：
   - "我需要一張有腰部支撐的椅子"
   - "推薦一張承重大的椅子"
   - "適合長時間工作的人體工學椅"
4. 系統將分析您的需求並推薦最合適的椅子，顯示其詳細信息和圖片

## 系統架構

- **前端**：React.js 構建的用戶界面，包含聊天機器人組件
- **後端**：FastAPI 服務器，處理查詢請求並返回椅子推薦
- **向量數據庫**：使用 FAISS 和 LangChain 實現的向量存儲，用於相似度搜索
- **嵌入模型**：使用 OpenAI 的 text-embedding-3-large 模型將文本轉換為向量

## 故障排除

- **圖片無法顯示**：確保 `chair_image` 目錄包含所有必要的圖片文件
- **API 錯誤**：檢查 OpenAI API 密鑰是否有效，以及是否有足夠的配額
- **連接問題**：確保前端和後端服務都在運行，並且端口設置正確

## 擴展數據庫

要添加更多椅子到數據庫，請修改 `vectordb_fastapi.py` 文件中的初始化部分，添加更多的 `Document` 對象，然後重新運行後端服務。

