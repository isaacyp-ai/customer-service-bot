# SmartShop Customer Service Bot

A local AI-powered customer service chatbot built with FastAPI and Ollama (llama3.2:3b), evaluated with promptfoo across 3 prompt iterations.

![Tests](https://img.shields.io/badge/Tests-15%2F20%20Passed-yellow)
![Model](https://img.shields.io/badge/Model-llama3.2%3A3b-blue)
![Framework](https://img.shields.io/badge/Eval-promptfoo-orange)

## Overview

This project explores LLM evaluation by building a customer service chatbot and systematically testing it using promptfoo. The goal is to identify model limitations, refine prompts iteratively, and document findings.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | llama3.2:3b via Ollama (100% local, no API cost) |
| Backend | Python FastAPI |
| Frontend | Vanilla JS chat UI |
| Evaluation | promptfoo |

## Evaluation Results

### Prompt Version Comparison

| Version | Passed | Failed | Pass Rate | Change |
|---------|--------|--------|-----------|--------|
| v1 (Baseline) | 14/20 | 6/20 | 70% | — |
| v2 (Improved) | 15/20 | 5/20 | 75% | +5% |
| v3 (Refined eval criteria) | 15/20 | 5/20 | 75% | — |

### Category Breakdown (v3)

| Category | Result | Notes |
|----------|--------|-------|
| Normal Cases | 5/5 ✅ | All passed |
| Compliance Boundary | 3/4 | Cover letter refusal failed |
| Hallucination Exposure | 1/3 | 2 false negatives from evaluator |
| Red-teaming | 2/4 | Jailbreak resistance weak on 3b model |
| Unpredictable Input | 4/4 ✅ | All passed |

### Key Findings

1. **Prompt engineering improved pass rate from 70% to 75%** — political boundary compliance fixed in v2
2. **Model vs. evaluator limitation distinction** — 2 failures were caused by llama3.2:3b misreading context as evaluator, not actual bot failures
3. **Small model jailbreak vulnerability** — llama3.2:3b failed role-persistence under adversarial prompts; expected to improve with larger models
4. **Next step** — benchmark same test suite against commercial models to quantify performance gap

## Getting Started

### Prerequisites
- [Ollama](https://ollama.com) installed
- Python 3.x
- Node.js (for promptfoo)

### Run the chatbot
```bash
# Terminal 1 — Start Ollama
ollama serve

# Terminal 2 — Pull model (first time only)
ollama pull llama3.2:3b

# Terminal 3 — Install dependencies
pip3 install -r requirements.txt

# Terminal 3 — Start server
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser.

### Run evaluation
```bash
promptfoo eval
promptfoo view
```

## Project Structure
```
customer-service-bot/
├── app/
│   ├── main.py          # FastAPI server with conversation history
│   └── prompt.py        # System prompt (v3)
├── static/
│   └── index.html       # Chat UI
├── tests/
│   └── results-dashboard.html  # Visual eval results
├── promptfooconfig.yaml  # 20 test cases across 5 categories
├── requirements.txt
└── README.md
```

## Roadmap

- [x] Build local chatbot with Ollama + FastAPI
- [x] Design 20 test cases across 5 evaluation categories
- [x] Iterative prompt engineering (v1 → v3)
- [x] Identify model vs. evaluator limitations
- [ ] Benchmark against commercial models (GPT-4o-mini, Claude Haiku)
- [ ] Expand to 100+ test cases with promptfoo redteam
- [ ] Add RAG pipeline
