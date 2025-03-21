# EmpathAI LLM Integration

This document explains how to configure and use the LLM (Large Language Model) integration in the EmpathAI system.

## Overview

EmpathAI now supports multiple LLM providers for generating more dynamic, personalized therapeutic responses. The system can be configured to use various LLM APIs, with graceful fallback to template-based responses if no LLM is configured or if the LLM call fails.

## Supported LLM Providers

The following LLM providers are supported:

1. **OpenAI** - Requires API key, offers powerful models like GPT-3.5 and GPT-4
2. **HuggingFace Inference API** - Free tier available, many open models available
3. **Ollama** - Free local deployment option, requires running Ollama locally
4. **Together.ai** - Free tier available, offers various open-source models
5. **Google Gemini** - Free tier available for Gemini models
6. **Anthropic Claude** - Requires API key, offers Claude models

## Configuration

To configure an LLM provider:

1. Copy the `.env.example` file to `.env` in the backend directory:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file to set your preferred LLM provider and model:
   ```
   LLM_PROVIDER=huggingface  # Options: openai, huggingface, ollama, together_ai, google, anthropic
   LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2  # Specific model to use
   
   # Add the relevant API key
   HUGGINGFACE_API_KEY=your_api_key_here
   ```

3. Restart the backend server for changes to take effect

## Free Options

If you want to use a free LLM provider, consider these options:

1. **HuggingFace Inference API**:
   - Sign up at huggingface.co for a free account
   - Get your API key from your settings page
   - In your `.env` file:
     ```
     LLM_PROVIDER=huggingface
     LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
     HUGGINGFACE_API_KEY=your_api_key_here
     ```
   - Free tier has rate limits but is sufficient for personal/development use

2. **Ollama (Local Deployment)**:
   - Install Ollama from https://ollama.ai/
   - Run the Ollama server locally
   - In your `.env` file:
     ```
     LLM_PROVIDER=ollama
     LLM_MODEL=llama2
     OLLAMA_API_URL=http://localhost:11434/api/generate
     ```
   - No API key required, but requires more powerful hardware

3. **Google Gemini API**:
   - Sign up for Google AI Studio to get a free API key
   - In your `.env` file:
     ```
     LLM_PROVIDER=google
     LLM_MODEL=gemini-pro
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Generous free tier available

4. **Together.ai**:
   - Sign up at together.ai for a free account
   - Get your API key from your account dashboard
   - In your `.env` file:
     ```
     LLM_PROVIDER=together_ai
     LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
     TOGETHER_AI_API_KEY=your_api_key_here
     ```
   - Free credits available for new accounts

## Using Different LLM Providers

### OpenRouter (Recommended)

OpenRouter is a unified API that provides access to many models including Deepseek models. This is now the recommended approach for using Deepseek models due to ease of use.

1. Create an account on [OpenRouter](https://openrouter.ai/)
2. Generate an API key
3. Update your `.env` file:
   ```
   LLM_PROVIDER=openrouter
   LLM_MODEL=deepseek/deepseek-chat:free
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
4. Run the test script to verify your setup:
   ```
   python test_openrouter.py
   ```

### Deepseek Direct API

## Testing

You can test the LLM integration through the Settings page in the frontend UI.

The page allows you to:
1. View the current LLM configuration
2. See available LLM providers
3. Test the response generation with different inputs

## Fallback Mechanism

If the LLM call fails for any reason (network error, rate limit, etc.), the system will automatically fall back to using the template-based responses. This ensures that EmpathAI will always provide a meaningful response to users.

## Adding Custom LLM Providers

If you want to add a custom LLM provider, modify the `response_generator/generator.py` file:

1. Add your provider to the `LLM_PROVIDERS` dictionary
2. Create a new `_generate_with_your_provider` method
3. Add your provider to the conditional logic in the `generate` method

## Troubleshooting

If you encounter issues with the LLM integration:

1. Check the backend logs for error messages
2. Verify your API keys are correctly set in the `.env` file
3. Check if you've exceeded any rate limits for your LLM provider
4. Try using a different LLM provider or model
5. Ensure the backend can access the internet (for remote APIs) or the local Ollama server (for local deployment) 