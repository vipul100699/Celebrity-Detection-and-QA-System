import os
import base64
import requests

class CelebrityDetector:
    """
    A class to detect celebrities in images using the Groq API.
    """
    def __init__(self):
        """
        Initialize the CelebrityDetector with API credentials and model details from environment variables.
        """
        self.api_key = os.getenv("GROQ_API_KEY") # Get API key
        self.api_url = os.getenv("GROQ_API_URL") # Get API URL
        self.model = os.getenv("GROQ_MODEL_NAME") # Get Model Name

    def identity(self, image_bytes):
        """
        Identify the celebrity in the given image bytes.

        Args:
            image_bytes (bytes): The image data in bytes.

        Returns:
            tuple: A tuple containing the full response text and the extracted name of the celebrity.
                   Returns ("Unknown", "") if the API call fails.
        """
        encoded_image = base64.b64encode(image_bytes).decode() # Encode image to base64 string

        headers = {
            "Authorization": f"Bearer {self.api_key}", # Set authorization header
            "Content-Type": "application/json"
        }

        prompt = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """
                            You are celebrity recognition expert AI.
                            Identify the celebrity in the image. If known, respond in the below format:
                            -**Full Name**
                            -**Profession**
                            -**Nationality**
                            -**Famous For**
                            -**Top Achievements**

                            If Unknown, return Unknown
                            """
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}" # Pass base64 encoded image
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.2
        }

        response = requests.post(self.api_url, headers=headers, json=prompt) # Send request to Groq API

        if response.status_code != 200:
            return "Unknown", "" # Return unknown if request failed
        
        result = response.json()['choices'][0]['message']['content'] # Extract content from response
        name = self.extract_name(result) # Extract name from content
        return result, name

    def extract_name(self, content):
        """
        Extract the full name of the celebrity from the API response content.

        Args:
            content (str): The text content returned by the API.

        Returns:
            str: The extracted full name, or "Unknown" if not found.
        """
        for line in content.splitlines():
            if line.lower().startswith("-**full name**"): # Check for name line
                return line.split(":")[1].strip() # Extract and clean name

        return "Unknown"