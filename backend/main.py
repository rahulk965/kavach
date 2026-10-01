"""Kavach backend skeleton. Wire up Sarvam STT / LLM / TTS where marked TODO."""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from risk_engine import RiskEngine

load_dotenv()
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
app = FastAPI(title="Kavach")


@app.get("/health")
def health():
    return {"status": "ok"}


async def transcribe(audio_chunk: bytes) -> str:
    # TODO: send audio to Sarvam speech-to-text (realtime or REST) and return text
    return ""


async def tag_tactics(window_text: str) -> list[str]:
    # TODO: call Sarvam chat model with a strict JSON prompt, return tactic tags
    return []


async def synthesize_alert(text: str, lang: str) -> str:
    # TODO: call Sarvam text-to-speech, return audio URL or base64
    return ""


@app.websocket("/ws/call")
async def call_ws(ws: WebSocket):
    await ws.accept()
    engine = RiskEngine()
    transcript = ""
    try:
        while True:
            chunk = await ws.receive_bytes()
            text = await transcribe(chunk)
            if text:
                transcript += " " + text
                await ws.send_json({"type": "transcript", "text": text, "is_final": True})
                tags = await tag_tactics(transcript[-800:])
                await ws.send_json({"type": "tactics", "tags": tags})
                result = engine.update(tags)
                await ws.send_json({"type": "risk", **result})
                if engine.should_alert(result):
                    audio = await synthesize_alert("Yeh call shayad scam hai. Kripya phone kaat dein.", "hi-IN")
                    await ws.send_json({"type": "alert", "lang": "hi-IN", "audio": audio})
    except WebSocketDisconnect:
        pass
