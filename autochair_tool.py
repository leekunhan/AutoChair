from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

