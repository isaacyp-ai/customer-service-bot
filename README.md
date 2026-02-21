# SmartShop Customer Service Bot

A local AI-powered customer service chatbot built with FastAPI and Ollama (llama3.2:3b), tested with promptfoo.

## Tech Stack
- **LLM**: llama3.2:3b via Ollama (runs 100% locally)
- **Backend**: Python FastAPI
- **Testing**: promptfoo (assertions + llm-rubric)

## Getting Started

### Prerequisites
- [Ollama](https://ollama.com) installed
- Python 3.x
- Node.js (for promptfoo)

### Run the chatbot
```bash
# 1. Start Ollama
ollama serve

# 2. Pull the model
ollama pull llama3.2:3b

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000 in your browser.

### Run tests
```bash
promptfoo eval
promptfoo view
```

## Test Results
- 7/7 tests passed (normal cases, out-of-scope, edge cases)
