# Health State Bot Lite

> **Lightweight Telegram bot that turns fitness data into clear daily states. No medical claims. No external APIs. Just rules.**

## 🎯 Why

Most people have health data but don't understand what to do with it.  
This bot shows **how to interpret raw numbers** into human states (without AI hype).

## ✨ Core features

- **Simple onboarding** (age/goal/activity)
- **Energy Avatar** (🐢 → 🏃 → 🚀) based on your metrics
- **Clear advice** with no medical promises
- **Zero dependencies** on LLMs or payment systems

## 🔍 Why it's minimal

Payments, OCR, Qwen API, rate limiting, and complex storage are intentionally excluded.  
This is a **proof of concept** for human-centered health interpretation, not a production app.

## ▶️ How to run

1. `pip install -r requirements.txt`
2. `TELEGRAM_TOKEN=your_token python bot.py`
3. Send: `sleep:7.5 hrv:62 steps:9800`

## 💡 Key takeaway

**Clarity > complexity.**  
This bot shows how to build trust through simple, explainable rules instead of black-box AI.

## What this project demonstrates

This project is not about Telegram bots.

It demonstrates:
- how to reduce complex health data into simple human states
- how to design non-medical feedback without fear-based language
- how to build a minimal product before scaling features or platforms

*Made with ❤️ for people who believe health tech should be honest.*
