# Kavach 🛡️

**A real-time scam-call guardian for India's elders, built on Sarvam AI.**
*Detect the manipulation, not the number.*

> Status: hackathon prototype (work in progress)

## Problem

"Digital arrest" scams use fear and fake authority to push people, mostly older adults, into transferring their savings. Victims are manipulated live, in their own language, often code-mixed. Caller-ID apps only block known numbers and cannot understand what is being said.

## Solution

Kavach listens to a call (speakerphone in our demo), transcribes it in real time, detects manipulation tactics, scores the risk, warns the user by voice in their own language, and alerts a family member.

```
Audio -> Sarvam STT -> Sarvam LLM tactic tags -> Risk engine -> Sarvam TTS alert + family notification
```

### Tactics detected
`authority_impersonation` · `urgency_fear` · `isolation` · `payment_demand` · `remote_access`

### Features
- Live transcript in code-mixed Indian languages
- Explainable risk score (the app shows *why* it warned)
- Spoken warning in the user's language
- Family alert with a short summary
- Kavach Dojo (planned): practice mode where an AI plays a scammer
- Privacy by design: no audio stored, only tactic labels

## Sarvam APIs used
- Speech-to-text (code-mixed / realtime)
- Chat LLM (tactic tagging)
- Text-to-speech (alerts)

Check the Sarvam docs for current model names and limits.

## Architecture

See [`docs/dfd.md`](docs/dfd.md) for DFD Level 0 and Level 1.

```
kavach/
├── backend/    FastAPI + WebSocket, STT, tagger, risk engine, TTS
├── frontend/   React PWA (mic, transcript, risk meter, alert)
├── docs/       DFDs, architecture, screenshots
└── tests/      scripted scam and benign calls
```

## Quick start

```bash
git clone git@github.com:rahulk965/kavach.git
cd kavach
cp .env.example .env        # add your SARVAM_API_KEY
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python risk_engine.py       # runs the risk engine demo
uvicorn main:app --reload   # starts the API on :8000
```

## Privacy and limitations
- No audio is stored; only anonymous tactic labels are logged.
- Phones do not allow apps to record the other side of a normal call, so the demo uses speakerphone and the microphone. A production version needs a telecom or call-bridge integration.
- Kavach is an assistive warning tool, not a guarantee. Always verify with the 1930 cyber-crime helpline.

## Roadmap
- [ ] Realtime STT streaming
- [ ] LLM tactic tagger
- [ ] Spoken alerts
- [ ] Family notification (Telegram/SMS)
- [ ] Kavach Dojo
- [ ] Evaluation on scripted scam and benign calls

## Team
- Rahul K ([@rahulk965](https://github.com/rahulk965))
- [Teammate name]
