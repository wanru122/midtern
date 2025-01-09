import os
import logging
import uvicorn
from fastapi import FastAPI, WebSocket, APIRouter
from fastapi.staticfiles import StaticFiles
from gpt import GPT


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
gpt = GPT(endpoint_url="https://linebot1029.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview",
              azure_api_key='G7ntjQXvYJ59h7q1EJWrErTyjJwAMTo6F8mKEC1gglF9yB28JDN7JQQJ99AJACYeBjFXJ3w3AAABACOGkqN8')

def set():
    @app.websocket("/chat")
    async def websocket_handler(websocket: WebSocket):
        await websocket.accept()
        print("WebSocket connection established") 
        while True:
            try:
                data = await websocket.receive_text()
                print(f"User input: {data}")
                
                response = gpt.generate_response(data)
                
                await websocket.send_text(f"Chatbot: {response}")
            except Exception as e:
                print(e)
                break
        await websocket.close()


app = FastAPI()

set()

app.mount("/", StaticFiles(directory="./", html=True))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
