"""
Simple script to test the LLM configuration in .env file
"""
import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

def main():
    # Get LLM configuration
    llm_provider = os.getenv("LLM_PROVIDER")
    llm_model = os.getenv("LLM_MODEL")
    
    if not llm_provider:
        print("No LLM provider configured in .env file.")
        print("Using template-based responses.")
        return
    
    print(f"LLM Provider: {llm_provider}")
    print(f"LLM Model: {llm_model}")
    
    # Check API key
    api_key_var = f"{llm_provider.upper()}_API_KEY"
    api_key = os.getenv(api_key_var)
    
    if not api_key or api_key == "your_api_key_here" or api_key == "your_deepseek_api_key_here" or api_key == "your_openrouter_api_key_here":
        print(f"WARNING: No valid API key found in {api_key_var}")
        print("Please update your .env file with a valid API key.")
        return
    
    print(f"API key for {llm_provider} is configured.")
    
    # Test connection based on the provider
    if llm_provider == "huggingface":
        test_huggingface(llm_model, api_key)
    elif llm_provider == "deepseek":
        test_deepseek(llm_model, api_key)
    elif llm_provider == "openrouter":
        test_openrouter(llm_model, api_key)
    else:
        print(f"Test connection for {llm_provider} not implemented in this script.")
        print("Please check your backend logs when running the full application.")

def test_huggingface(llm_model, api_key):
    try:
        # Simple test request to HuggingFace API
        API_URL = f"https://api-inference.huggingface.co/models/{llm_model or 'mistralai/Mistral-7B-Instruct-v0.2'}"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Just a simple request to check if the API key is valid
        response = requests.head(API_URL, headers=headers)
        
        if response.status_code == 200:
            print("Successfully connected to HuggingFace API!")
            print("Your configuration looks good.")
        else:
            print(f"Error connecting to HuggingFace API: {response.status_code}")
            print("Please check your API key and model name.")
    except Exception as e:
        print(f"Error connecting to HuggingFace API: {str(e)}")

def test_deepseek(llm_model, api_key):
    try:
        # Define headers for API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Simple test message
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello, are you working properly? Please respond with a short confirmation."
            }
        ]
        
        # Set up API endpoint and payload
        api_url = "https://api.deepseek.com/v1/chat/completions"
        payload = {
            "model": llm_model or "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        print("Testing connection to Deepseek API...")
        # Make API call
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Check for successful response
        if response.status_code == 200:
            response_json = response.json()
            print("Successfully connected to Deepseek API!")
            print("Your configuration looks good.")
            print("Sample response:", response_json.get("choices", [{}])[0].get("message", {}).get("content", ""))
        else:
            print(f"Error from Deepseek API: {response.status_code}")
            print(f"Response: {response.text}")
            print("Please check your API key and model name.")
    except Exception as e:
        print(f"Error connecting to Deepseek API: {str(e)}")

def test_openrouter(llm_model, api_key):
    try:
        # Define headers for API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Simple test message
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Hello, are you working properly? Please respond with a short confirmation."
            }
        ]
        
        # Set up API endpoint and payload
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": llm_model or "deepseek/deepseek-chat:free",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        print("Testing connection to OpenRouter API...")
        # Make API call
        response = requests.post(api_url, json=payload, headers=headers)
        
        # Check for successful response
        if response.status_code == 200:
            response_json = response.json()
            print("Successfully connected to OpenRouter API!")
            print("Your configuration looks good.")
            print("Sample response:", response_json.get("choices", [{}])[0].get("message", {}).get("content", ""))
        else:
            print(f"Error from OpenRouter API: {response.status_code}")
            print(f"Response: {response.text}")
            print("Please check your API key and model name.")
    except Exception as e:
        print(f"Error connecting to OpenRouter API: {str(e)}")

if __name__ == "__main__":
    main() 