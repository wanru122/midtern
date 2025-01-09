import requests

class GPT:
    def __init__(self, 
                 azure_api_key: str,
                 endpoint_url: str):
                
        self.endpoint_url = endpoint_url
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': azure_api_key
        }
        print("GPT initialized")

    def generate_response(self, user_message):
        body = {
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 950, 
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
    gpt = GPT(endpoint_url="https://linebot1029.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview",
              azure_api_key='G7ntjQXvYJ59h7q1EJWrErTyjJwAMTo6F8mKEC1gglF9yB28JDN7JQQJ99AJACYeBjFXJ3w3AAABACOGkqN8')
    gpt.generate_response("hello")