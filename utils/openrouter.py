import os
import requests
import json
from typing import Optional

# Get API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

def call_text_model(model: str, system_prompt: str, user_prompt: str) -> str:
    """
    Call a text-only model via OpenRouter API
    
    Args:
        model: Model identifier (e.g., "mistralai/mistral-small-3.2-24b-instruct:free")
        system_prompt: System instruction for the model
        user_prompt: User's input text
    
    Returns:
        Model's response text
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # For Streamlit local dev
        "X-Title": "Ecosync AI Multi-Agent System"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": user_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1500,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()
        else:
            return "I apologize, but I couldn't generate a response. Please try again."
            
    except requests.exceptions.RequestException as e:
        return f"Network error occurred: {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid response format from the API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def call_vision_model(model: str, system_prompt: str, user_prompt: str, image_base64: str) -> str:
    """
    Call a vision-capable model via OpenRouter API
    
    Args:
        model: Model identifier (e.g., "moonshotai/kimi-vl-a3b-thinking:free")
        system_prompt: System instruction for the model
        user_prompt: User's input text
        image_base64: Base64 encoded image string
    
    Returns:
        Model's response text analyzing the image
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Ecosync AI Multi-Agent System"
    }
    
    # Construct the message with both text and image
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            }
        ]
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            user_message
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()
        else:
            return "I apologize, but I couldn't analyze the image. Please try again."
            
    except requests.exceptions.RequestException as e:
        return f"Network error occurred while analyzing image: {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid response format from the vision API."
    except Exception as e:
        return f"An unexpected error occurred during image analysis: {str(e)}"

def test_openrouter_connection() -> bool:
    """
    Test if OpenRouter API is accessible with current credentials
    
    Returns:
        True if connection is successful, False otherwise
    """
    try:
        response = call_text_model(
            model="mistralai/mistral-small-3.2-24b-instruct:free",
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'Hello, OpenRouter is working!' and nothing else."
        )
        
        return "Hello, OpenRouter is working!" in response
        
    except Exception:
        return False

# Optional: Helper function to get available models (if needed)
def get_available_models() -> list:
    """
    Get list of available models from OpenRouter
    Note: This is optional and mainly for debugging
    """
    url = "https://openrouter.ai/api/v1/models"
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        return [model['id'] for model in result.get('data', [])]
        
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

# Usage example and testing
if __name__ == "__main__":
    # Test the connection
    print("Testing OpenRouter connection...")
    if test_openrouter_connection():
        print("✅ OpenRouter connection successful!")
    else:
        print("❌ OpenRouter connection failed. Check your API key.")
    
    # Test text model
    print("\nTesting text model...")
    response = call_text_model(
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        system_prompt="You are an environmental expert.",
        user_prompt="What is ocean acidification in one sentence?"
    )
    print(f"Response: {response}")