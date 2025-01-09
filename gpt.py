import requests

class GPT:
    def __init__(self, 
                 azure_api_key: str,
                 endpoint_url: str):
                # 向 Azure OpenAI API 發送請求
        self.endpoint_url = endpoint_url
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': azure_api_key
        }
        print("GPT initialized")

    def generate_response(self, user_message):
        body = {
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 950,  # 增加最大 tokens
            "temperature": 0.7
        }
        try:
            response = requests.post(self.endpoint_url, headers=self.headers, json=body)
            response.raise_for_status()
            response_data = response.json()
            RES = response_data['choices'][0]['message']['content'].strip()
            print(f"response: {RES}")
            return RES
        except Exception as e:
            return e


if __name__ == "__main__":
    gpt = GPT(endpoint_url="https://c1121-m4kwicky-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4-2/chat/completions?api-version=2024-08-01-preview",
              azure_api_key='FHonuD7B4mLhsY4R7LAFMsZnaA4gggSDCV8RGyCuOF6PvrFqtp6OJQQJ99ALACHYHv6XJ3w3AAAAACOGiOw5')
    gpt.generate_response("hello")