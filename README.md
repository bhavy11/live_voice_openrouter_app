# 🎙️ Live Voice-to-Text AI Assistant

A complete live hands-free speech recognition web application powered by **FastAPI**, **WebSockets**, and **OpenRouter Free LLM models** (such as LLaMA-3.3 70B, Gemini 2.0 Flash Lite, and DeepSeek R1).

## 🚀 Features
- **Live Hands-Free Speech Recognition:** Listens in real time with continuous word streaming.
- **Automatic Silence Detection:** Auto-detects pauses (1.5s, 2s, 3s) and triggers the AI automatically without pressing any buttons.
- **Multi-Mode AI Processing:** Grammar cleanup, meeting summaries, conversational Q&A, and live English translation.
- **WebSocket Streaming:** Fast bidirectional communication between browser and FastAPI backend.
- **Zero Cost:** Uses browser Speech Recognition + OpenRouter free tier models (`:free`).

---

## 🛠️ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure OpenRouter API Key
Open `.env` (or copy `.env.example` to `.env`) and insert your free API key:
```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
```
> Get a free API key at [openrouter.ai](https://openrouter.ai/)

### 3. Start the Server
```bash
uvicorn main:app --reload --port 8000
```

### 4. Open in Browser
Visit `http://localhost:8000` in Google Chrome, Microsoft Edge, or Safari, click **Start Hands-Free Mic**, allow microphone access, and speak naturally!
