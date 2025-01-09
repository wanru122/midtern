import os
import logging
from dotenv import load_dotenv
import openai
import uvicorn
from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.staticfiles import StaticFiles
from gpt import GPT

# 配置日誌
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# # 加載環境變數
# load_dotenv()

# # 配置 Azure OpenAI API
# OPENAI_ENDPOINT = os.getenv("endpointUrl")
# OPENAI_API_KEY = os.getenv("apiKey")

# # 初始化 OpenAI 設定
# openai.api_base = OPENAI_ENDPOINT
# openai.api_key = OPENAI_API_KEY
gpt = GPT(endpoint_url="https://c1121-m4kwicky-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4-2/chat/completions?api-version=2024-08-01-preview",
            azure_api_key='FHonuD7B4mLhsY4R7LAFMsZnaA4gggSDCV8RGyCuOF6PvrFqtp6OJQQJ99ALACHYHv6XJ3w3AAAAACOGiOw5')


def set():
    @app.websocket("/chat")
    async def websocket_handler(websocket: WebSocket):
        await websocket.accept()
        print("WebSocket connection established") 
        while True:
            try:
                # 接收用戶訊息
                data = await websocket.receive_text()
                print(f"User input: {data}")
                
                # 調用 generate_response 來獲取回應
                response = gpt.generate_response(data)
                
                # 發送機器人回應
                await websocket.send_text(f"Chatbot: {response}")
            except Exception as e:
                print(e)
                break
        await websocket.close()


# 初始化 FastAPI 應用
app = FastAPI()

# 設定 WebSocket 路由
set()

# 掛載靜態文件
app.mount("/", StaticFiles(directory="./", html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
