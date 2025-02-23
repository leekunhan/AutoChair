import os
import getpass
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from langchain_core.documents import Document
from PIL import Image

load_dotenv()

userInput = "我想要有大腰靠的椅子"

if not os.getenv("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

infinite_max_document_1 = Document(
    page_content="""不只大，要就最大，無限MAX 超跑人體工學椅，我們累計了銷售10,000+的消費者使用體驗，並針對大家最重視的腰部支撐再進化！寬度、高度與厚度同步加大，完全滿足 '' 支撐加倍 X 舒適加倍 ''""",
    metadata={"source": "https://www.marsrhino.com/tw/product_detail?id=54&class_id=13",
              "chair": "infinite_max",
              "max_weight": 150,
              "has_waist_support": True,
              "image_path": "/home/kh/AutoChair/chair_image/infinite_max.jpg"
              }
)

infinite_max_document_2 = Document(
    page_content="""3D ''大'' 體感腰靠，藉由腰靠的高低、前後手動調整，及對應腰部曲線角度自動旋轉，完美支撐腰部，達到舒適與放鬆。""",
    metadata={"source": "https://www.marsrhino.com/tw/product_detail?id=54&class_id=13",
              "chair": "infinite_max",
              "max_weight": 150,
              "has_waist_support": True,
              "image_path": "/home/kh/AutoChair/chair_image/infinite_max.jpg"
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
    metadata={"source": "https://www.marsrhino.com/tw/product_detail?id=54&class_id=13",
              "chair": "infinite_max",
              "max_weight": 150,
              "has_waist_support": True,
              "image_path": "/home/kh/AutoChair/chair_image/infinite_max.jpg"
              }
)

documents = [
    infinite_max_document_1,
    infinite_max_document_2,
    infinite_max_document_3
]
uuids = [str(uuid4()) for _ in range(len(documents))]

vector_store.add_documents(documents=documents, ids=uuids)

results = vector_store.similarity_search(
    userInput,
    k=1,
    filter={"has_waist_support": True},
)

img_path = Image.open(results.metadata["image_path"]).show()
url = results.metadata["source"]

output = f"Here is the chair that you are looking for: {results.metadata['chair']}\n" \
         f"Maximum weight: {results.metadata['max_weight']} kg\n" \
         f"Source: {url}"