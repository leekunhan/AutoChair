import os
import faiss
from uuid import uuid4
from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# LangChain 相關 (若你用的是 langchain_community，請確認套件名稱)
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 載入 .env 以取得 OPENAI_API_KEY
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("請先在環境變數或 .env 檔案中設置 OPENAI_API_KEY")

# 建立 FastAPI 應用
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 若要指定特定網域，例如 ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/chair_image", StaticFiles(directory="chair_image"), name="chair_image")

# ========== 1. 初始化 Embeddings ==========
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# ========== 2. 嘗試載入或建立向量索引 ==========
INDEX_DIR = "chairDB"

try:
    # load_local() 會讀取該資料夾內的 index.faiss / index.pkl
    vector_store = FAISS.load_local(
        INDEX_DIR, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    print("成功載入既有的向量索引！")
except:
    print("無法載入既有索引，將建立新的索引...")
    sample_vector = embeddings.embed_query("hello world")
    dimension = len(sample_vector)
    index = faiss.IndexFlatL2(dimension)

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    # 這裡示範初始化一些文件
    infinite_max_document_1 = Document(
        page_content="""
            不只大，要就最大，無限MAX 超跑人體工學椅，我們累計了銷售10,000+的消費者使用體驗，
            並針對大家最重視的腰部支撐再進化！寬度、高度與厚度同步加大，完全滿足
            '支撐加倍 X 舒適加倍'
        """,
        metadata={
            "url": "https://www.marsrhino.com/tw/product_detail?id=54&class_id=13",
            "chair": "infinite_max",
            "max_weight": 150,
            "has_waist_support": True,
            "image_path": "./chair_image/infinite_max.jpg"
        }
    )

    infinite_max_document_2 = Document(
        page_content="""
            3D '大' 體感腰靠，藉由腰靠的高低、前後手動調整，及對應腰部曲線角度自動旋轉，
            完美支撐腰部，達到舒適與放鬆。
        """,
        metadata={
            "url": "https://www.marsrhino.com/tw/product_detail?id=54&class_id=13",
            "chair": "infinite_max",
            "max_weight": 150,
            "has_waist_support": True,
            "image_path": "./chair_image/infinite_max.jpg"
        }
    )

    infinite_max_document_3 = Document(
        page_content="""
            建議身形 身高 : 165 - 200cm,
            最大承重 150kg,
            頭枕 / 椅背 / 椅座 ( 獨創透氣紓壓技術 )
            表層 : 防潑水彈性布
            內層 : 高密度泡棉
            底層 : 透氣網布
        """,
        metadata={
            "url": "https://www.marsrhino.com/tw/product_detail?id=54&class_id=13",
            "chair": "infinite_max",
            "max_weight": 150,
            "has_waist_support": True,
            "image_path": "./chair_image/infinite_max.jpg"
        }
    )

    documents = [infinite_max_document_1, infinite_max_document_2, infinite_max_document_3]
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)

    vector_store.save_local(INDEX_DIR)
    print("向量索引已建立並儲存在 chairDB/")

# ========== 3. 建立 Pydantic Model (API 回傳格式 + 請求格式) ==========

# 回傳格式
class ChairSearchResult(BaseModel):
    chair: str
    max_weight: int
    source: str
    image_path: str
    message: str

# 請求格式：用於 POST 時，讀取 JSON 內容
class ChairSearchRequest(BaseModel):
    userInput: str

# ========== 4. 定義內部函式：相似度搜尋 (Core Logic) ==========
def _search_chair(user_input: str) -> ChairSearchResult:
    results = vector_store.similarity_search(
        user_input,
        k=1,
        filter={"has_waist_support": True}
    )

    if not results:
        return ChairSearchResult(
            chair="",
            max_weight=0,
            source="",
            image_path="",
            message="找不到符合需求的椅子"
        )

    result = results[0]
    metadata = result.metadata

    output_msg = (
        f"Here is the chair that you are looking for: {metadata.get('chair')}\n"
        f"Maximum weight: {metadata.get('max_weight')} kg\n"
        f"Source: {metadata.get('source')}"
    )

    return ChairSearchResult(
        chair=metadata.get("chair", ""),
        max_weight=metadata.get("max_weight", 0),
        source=metadata.get("source", ""),
        image_path=metadata.get("image_path", ""),
        message=output_msg
    )

@app.get("/search_chair", response_model=ChairSearchResult)
def search_chair_get(userInput: str = Query(..., description="使用者關鍵字")):
    return _search_chair(userInput)

@app.post("/search_chair", response_model=ChairSearchResult)
def search_chair_post(request: ChairSearchRequest):
    return _search_chair(request.userInput)
