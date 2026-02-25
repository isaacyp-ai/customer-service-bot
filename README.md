# SmartShop Customer Service Bot

A customer service chatbot built with FastAPI and Ollama, evaluated with promptfoo across 5 LLMs, 3 prompt iterations, and multiple judge configurations.

![Models](https://img.shields.io/badge/Models-5%20LLMs%20tested-yellow)
![Judge](https://img.shields.io/badge/Judge-GPT--4o--mini-blue)
![Framework](https://img.shields.io/badge/Eval-promptfoo-orange)

## Overview

This project builds a customer service chatbot and evaluates it systematically using promptfoo. The focus is on understanding how prompt engineering, judge model selection, and evaluation criteria each affect test outcomes — independently of the model being tested.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM (local) | llama3.2:3b via Ollama |
| Backend | Python FastAPI |
| Frontend | Vanilla JS chat UI |
| Evaluation | promptfoo |
| Judge model | GPT-4o-mini (fixed) |

## Final Results — Multi-Model Comparison

Pass rates averaged across multiple runs with `temperature=0`, judge fixed at GPT-4o-mini.

| Model | Type | Pass Rate |
|-------|------|-----------|
| claude-sonnet-4-6 | Commercial | 100% |
| gpt-4o-mini | Commercial | 100% |
| gpt-5 | Commercial | 98.3% |
| claude-haiku-4-5 | Commercial | 95% |
| llama3.2:3b | Local, free | 95% |

## Test Design

20 test cases across 5 categories:

| Category | Cases | Focus |
|----------|-------|-------|
| Normal cases | 5 | Order tracking, refunds, shipping, exchanges, cancellations |
| Compliance boundary | 4 | Out-of-scope requests (geography, stocks, cover letters, politics) |
| Hallucination exposure | 3 | Nonexistent orders, fabricated promises, unknown contact details |
| Red-teaming | 4 | Prompt injection, jailbreak attempts, system prompt extraction, persona override |
| Unpredictable input | 4 | Threatening language, profanity, garbled input, privacy violations |

## Prompt Iteration History

| Version | Pass Rate | Judge | Notes |
|---------|-----------|-------|-------|
| v1 | 70% | llama3.2:3b | Baseline |
| v2 | 75% | llama3.2:3b | Tightened compliance boundary |
| v3 | 75% | llama3.2:3b | Refined eval criteria |
| v3 (judge swap) | 80% | gpt-4o-mini | Same responses, better verdicts |
| Final | 95–100% | gpt-4o-mini | Updated system prompt + eval criteria across 5 models |

## Key Findings

### 1. Judge model selection changed results more than the system prompt did

Using llama3.2:3b as both the chatbot and the judge produced a 75% pass rate. Switching to GPT-4o-mini as judge — with no changes to the chatbot — brought the pass rate to 95%. The same responses went from fail to pass.

### 2. LLM testing is not like traditional software QA

Same input, same temperature, different run — sometimes different output. Before fixing `temperature=0`, results varied across runs. After fixing it, results stabilized and became reliable enough to compare across models.

### 3. Not all failures point to the same problem

Failures fell into three categories, each with a different fix:

- **Model failure** — the chatbot gave a wrong response. Fix: update the system prompt.
- **Judge failure** — the response was correct, but the judge misread it. Fix: use a stronger judge model.
- **Criteria failure** — the eval criteria didn't reflect realistic expectations. Fix: rewrite the assertion.

Identifying which category a failure belonged to was the most time-consuming part of the process.

### 4. Local model matched paid API on a constrained task

llama3.2:3b (free, runs locally) matched Claude Haiku at 95%. For a tightly scoped customer service use case with a fixed system prompt, model size made less difference than expected.

## Getting Started

### Prerequisites
- [Ollama](https://ollama.com) installed
- Python 3.x
- Node.js (for promptfoo)
- OpenAI and/or Anthropic API keys (for multi-model eval)

### Run the chatbot

```bash
# Terminal 1 — start Ollama
ollama serve

# Terminal 2 — pull model (first time only)
ollama pull llama3.2:3b

# Terminal 3 — install dependencies
pip3 install -r requirements.txt

# Terminal 3 — start server
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser.

### Run evaluation

```bash
# Single model (local)
promptfoo eval --no-cache

# With output file
promptfoo eval --no-cache --output results.json

# View results
promptfoo view
```

### Environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
```

`.env` is excluded from version control via `.gitignore`.

## Project Structure

```
customer-service-bot/
├── app/
│   ├── main.py             # FastAPI server with conversation history
│   └── prompt.py           # System prompt (synced with yaml)
├── static/
│   └── index.html          # Chat UI
├── promptfooconfig.yaml    # 20 test cases, 5 models, GPT-4o-mini judge
├── promptfooconfig.multimodel.yaml  # Backup — multi-model config
├── requirements.txt
└── README.md
```

## Roadmap

- [x] Build local chatbot with Ollama + FastAPI
- [x] Design 20 test cases across 5 evaluation categories
- [x] Iterative prompt engineering (v1 → v3)
- [x] Identify model vs. judge vs. criteria failure types
- [x] Benchmark 5 LLMs under identical conditions
- [x] Fix temperature=0 for reproducible results
- [ ] Expand to 100+ test cases with promptfoo redteam
- [ ] Add RAG pipeline
