# Usage Guide

## Prerequisites
- Python 3 installed
- Node.js installed
- Docker installed (for alternative method)

## Gemini API Key Setup
1. Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create `.env` file in project root with:
```env
GEMINI_API_KEY=<YOUR_API_KEY>

## Backend Setup

```bash
cd app
pip install -r requirements.txt  # Install Python dependencies
uvicorn main:app --reload  # Start backend server
```

## Frontend Setup

```bash
cd /client/app  # Switch to frontend directory
npm install     # Install Node dependencies
npm run dev     # Start frontend development server
```

## Access Application

Open the provided development URL in your browser to interact with the chatbot.

## Alternative Method: Using Docker

### Pull Docker Images

```bash
docker pull hailat617/langchain:latest
docker pull hailat617/langchainfront:latest
```
### Run Containers
Start backend container:

```bash
docker run -p 8000:8000 -it hailat617/langchain
```

In a new terminal, start frontend container:

```bash
docker run -p 3000:80 hailat617/langchainfront
```

Access the application at:
http://localhost:3000

Thank you for checking out the project! 🚀