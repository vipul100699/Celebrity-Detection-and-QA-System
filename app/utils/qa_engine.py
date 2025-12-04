import os
import requests

class QAEngine:
    """
    A class to handle Question and Answer interactions about celebrities using the Groq API.
    
    Attributes:
        api_key (str): The API key for accessing the Groq service.
        api_url (str): The endpoint URL for the Groq API.
        model (str): The specific model name to be used for generating responses.
    """

    def __init__(self):
        """
        Initializes the QAEngine by retrieving configuration from environment variables.
        """
        self.api_key = os.getenv("GROQ_API_KEY") # Get API key from environment variables
        self.api_url = os.getenv("GROQ_API_URL") # Get API URL from environment variables
        self.model = os.getenv("GROQ_MODEL_NAME") # Get Model Name from environment variables

    def ask_about_celebrity(self, name, question):
        """
        Sends a query to the Groq API to ask a specific question about a celebrity.

        Args:
            name (str): The name of the celebrity.
            question (str): The question to ask about the celebrity.

        Returns:
            str: The answer provided by the AI model, or an error message if the request fails.
        """
        # Set up the headers for the API request, including authentication
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Construct the prompt to guide the AI's response
        prompt = f"""
            You are an AI Assistant who has a lot of knowledge about celebrities.
            You have to answer the questions about {name} concisely and accurately.
            Question: {question}
        """

        # Prepare the payload with model details, messages, and parameters
        payload = {
            "model": self.model,
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.3, # Low temperature for more deterministic/concise answers
            "max_tokens": 1024
        }

        # Make the POST request to the Groq API
        response = requests.post(self.api_url, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"QA Engine API Error: Status Code {response.status_code}")
            print(f"QA Engine API Response: {response.text}")
            return "Sorry! I couldn't find the answer" # Return default message if request failed
        
        # Extract and return the content from the API response
        result = response.json()['choices'][0]['message']['content'] 
        
        return result
