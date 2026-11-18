import os
import json
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI(title="Live Voice-to-Text with OpenRouter")

# Ensure static dir exists & mount
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.websocket("/ws/transcribe")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Receive real-time transcript payload from the browser
            data = await websocket.receive_text()
            payload = json.loads(data)

            raw_text = payload.get("text", "").strip()
            task_instruction = payload.get("instruction", "Clean up grammar, format, and structure.")

            if not raw_text:
                continue

            current_key = os.getenv("OPENROUTER_API_KEY", OPENROUTER_API_KEY)
            if not current_key or "your-openrouter-key-here" in current_key:
                await websocket.send_json({
                    "event": "error",
                    "data": "OPENROUTER_API_KEY not configured. Please set your API key in the .env file."
                })
                continue

            # Notify UI that LLM processing has started
            await websocket.send_json({"event": "llm_start"})

            # Request refinement from OpenRouter
            async with httpx.AsyncClient(timeout=45.0) as client:
                try:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {current_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "http://localhost:8000",
                            "X-Title": "Live Voice AI App"
                        },
                        json={
                            "model": os.getenv("OPENROUTER_MODEL", OPENROUTER_MODEL),
                            "messages": [
                                {
                                    "role": "system",
                                    "content": f"You are an expert real-time voice copilot. {task_instruction} Output ONLY the final polished or requested response text directly, without markdown intro or disclaimers."
                                },
                                {"role": "user", "content": raw_text}
                            ]
                        }
                    )

                    if response.status_code == 200:
                        result = response.json()
                        refined_text = result["choices"][0]["message"]["content"]
                        await websocket.send_json({
                            "event": "llm_result",
                            "data": refined_text
                        })
                    else:
                        await websocket.send_json({
                            "event": "error",
                            "data": f"OpenRouter API Error ({response.status_code}): {response.text}"
                        })
                except Exception as ex:
                    await websocket.send_json({
                        "event": "error",
                        "data": f"Failed to connect to OpenRouter: {str(ex)}"
                    })

    except WebSocketDisconnect:
        pass
