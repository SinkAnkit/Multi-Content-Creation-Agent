# Multi-Agent Content Creation System

A streamlined **multi-agent content generation system** built with [Motia](https://github.com/MotiaDev/motia) that transforms articles into engaging Twitter threads and LinkedIn posts using AI.

## Tech Stack

- **[Motia](https://github.com/MotiaDev/motia)** — Unified backend framework for multi-agent orchestration
- **[Firecrawl](https://www.firecrawl.dev/)** — Web scraping & content extraction
- **[Ollama](https://ollama.com/)** — Local LLM inference with Deepseek-R1
- **[Typefully](https://typefully.com/)** — Social media scheduling & publishing

## Workflow

```
User submits URL → Firecrawl scrapes article → Twitter & LinkedIn agents run in parallel → Content scheduled via Typefully
```

```
API (POST /generate-content)
    │
    ▼
Scrape Article (Firecrawl)
    │
    ├──────────────────┐
    ▼                  ▼
Twitter Agent      LinkedIn Agent
(Deepseek-R1)      (Deepseek-R1)
    │                  │
    ▼                  ▼
Schedule Twitter   Schedule LinkedIn
(Typefully)        (Typefully)
```

## Setup

### Prerequisites

- Node.js 18+
- Python 3.x
- [Ollama](https://ollama.com/) installed locally
- API keys for [Firecrawl](https://www.firecrawl.dev/) and [Typefully](https://typefully.com/)

### Installation

1. **Install Ollama & pull Deepseek-R1:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull deepseek-r1
   ```

2. **Install Motia CLI:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/MotiaDev/motia-cli/main/install.sh | sh
   ```

3. **Install project dependencies:**
   ```bash
   npm install
   ```

4. **Set up Python environment:**
   ```bash
   python3 -m venv python_modules
   source python_modules/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

6. **Start the development server:**
   ```bash
   npm run dev
   ```

## Usage

### Generate Content

Send a POST request to trigger content generation:

```bash
curl -X POST http://localhost:3000/generate-content \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

**Response:**
```json
{
  "message": "Content generation started",
  "requestId": "req_123456",
  "url": "https://example.com/article",
  "status": "processing"
}
```

### View Results

After processing completes:
1. Visit [Typefully Drafts](https://typefully.com/drafts)
2. Review your generated Twitter thread and LinkedIn post
3. Edit if needed and publish!

## Project Structure

```
Multi_ContentCreation_Agent/
├── steps/
│   ├── api.step.py                   # API endpoint handler
│   ├── scrape.step.py                # Firecrawl web scraping
│   ├── generate-twitter.step.py      # Ollama Twitter thread generation
│   ├── generate-linkedin.step.py     # Ollama LinkedIn post generation
│   ├── schedule-twitter.step.ts      # Typefully Twitter scheduling
│   └── schedule-linkedin.step.ts     # Typefully LinkedIn scheduling
├── prompts/
│   ├── twitter-prompt.txt            # Twitter thread prompt template
│   └── linkedin-prompt.txt           # LinkedIn post prompt template
├── config/
│   └── index.js                      # Configuration management
├── package.json
├── requirements.txt
├── tsconfig.json
├── motia-workbench.json
├── .env.example
└── README.md
```

## Monitoring

The **Motia Workbench** provides an interactive UI to debug and monitor your flows as interactive diagrams. It runs automatically with the development server.

## Environment Variables

| Variable | Description |
|---|---|
| `FIRECRAWL_API_KEY` | Your Firecrawl API key for web scraping |
| `TYPEFULLY_API_KEY` | Your Typefully API key for scheduling |
| `OLLAMA_MODEL` | Ollama model name (default: `deepseek-r1`) |
| `MOTIA_PORT` | Server port (default: `3000`) |

## Key Features

- **Multi-language support**: Python steps for AI/scraping + TypeScript steps for scheduling
- **Parallel execution**: Twitter & LinkedIn content generated simultaneously
- **Local LLM**: Uses Ollama Deepseek-R1 — no cloud AI costs
- **Event-driven**: Motia handles orchestration, retries, and fault tolerance
- **Built-in observability**: Visual flow monitoring via Motia Workbench
