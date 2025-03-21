"""
Test script for OpenRouter API using the OpenAI SDK
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def main():
    # Get the OpenRouter API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key or api_key == "your_openrouter_api_key_here":
        print("ERROR: No valid OpenRouter API key found in OPENROUTER_API_KEY")
        print("Please update your .env file with a valid API key.")
        return
    
    print("Testing OpenRouter API with OpenAI SDK...")
    model = os.getenv("LLM_MODEL") or "deepseek/deepseek-chat:free"
    print(f"Using model: {model}")
    
    try:
        # Initialize OpenAI client with OpenRouter base URL
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Call the API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello, are you working properly? Please respond with a short confirmation."}
            ],
            temperature=0.7,
            max_tokens=50
        )
        
        # Print response
        print("\nResponse from OpenRouter API:")
        print(response.choices[0].message.content)
        print("\nConfiguration successful! You can now use OpenRouter in your EmpathAI application.")
        
    except Exception as e:
        print(f"Error connecting to OpenRouter API: {str(e)}")
        print("Please check your API key and model name.")

if __name__ == "__main__":
    main() 