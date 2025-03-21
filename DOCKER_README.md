# Docker Setup for EmpathAI

This document explains how to run the EmpathAI application using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- OpenAI API Key (for langchain integration)

## Setting Up Environment Variables

1. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   If you don't have an OpenAI API key, the application will fall back to simpler rule-based analysis.

## Running the Application

1. Clone the repository:
   ```
   git clone <repository-url>
   cd empathAI
   ```

2. Build and start the containers:
   ```
   docker-compose up --build
   ```

   This command will:
   - Build the Docker images for both frontend and backend
   - Start the containers
   - Forward port 3000 for the frontend
   - Forward port 8000 for the backend

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Available API Endpoints

The EmpathAI API provides the following endpoints:

- `GET /`: Health check endpoint
- `POST /analyze/text`: Analyze emotions in text
- `POST /analyze/audio`: Analyze emotions in audio recordings
- `POST /analyze/multimodal`: Analyze emotions from text and audio together

## Docker Containers

The setup consists of two Docker containers:

1. **Backend Container**:
   - Python 3.10 with FastAPI
   - Runs on port 8000
   - Contains the emotion analysis and therapeutic response generation

2. **Frontend Container**:
   - Node.js with Next.js
   - Runs on port 3000
   - Communicates with the backend API

## Stopping the Application

To stop the application, press `Ctrl+C` in the terminal where `docker-compose up` is running.

To stop and remove the containers:
```
docker-compose down
```

## Troubleshooting

- **Backend Import Errors**: If you encounter import errors in the backend, you may need to adjust the `PYTHONPATH` in the backend Dockerfile.
- **Frontend API Connection**: If the frontend cannot connect to the backend, check the `NEXT_PUBLIC_API_URL` environment variable in the docker-compose.yml file.
- **LangChain Errors**: If you see errors related to LangChain or OpenAI, check that your API key is correctly set in the .env file. 