import os
import requests

class QAEngine:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY") # Get API key
        self.api_url = os.getenv("GROQ_API_URL") # Get API URL
        self.model = os.getenv("GROQ_MODEL_NAME") # Get Model Name

    def ask_about_celebrity(self, name, question):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"""
            You are an AI Assistant who has a lot of knowledge about celebrities.
            You have to answer the questions about {name} concisely and accurately.
            Question: {question}
        """

        payload = {
            "model": self.model,
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.3,
            "max_tokens": 1024
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code != 200:
            return "Sorry! I couldn't find the answer" # Return unknown if request failed
        
        result = response.json()['choices'][0]['message']['content'] # Extract content from response
        
        return result
