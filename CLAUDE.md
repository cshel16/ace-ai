# Ace AI - Baseball Analytics Agent

## Project Goal
Natural language interface over Statcast/FanGraphs data. Ask complex baseball questions, get AI-powered analysis backed by real pitch-by-pitch data.

## Developer Mode
**CRITICAL: I am writing all code myself. Claude Code is here as a senior engineer to:**
- Review my code and question my decisions
- Explain concepts I don't understand
- Catch bugs and suggest improvements
- Help me debug when I'm stuck

**Claude Code should NOT:**
- Write code for me unprompted
- Scaffold files without me asking
- Make architectural decisions without explaining tradeoffs first

The goal is learning and conviction, not speed. If I'm about to make a mistake, ask me why I'm doing it that way before fixing it.

## Tech Stack
- Python 3.12
- pybaseball for data
- Anthropic API for agent layer
- FastAPI + React frontend (later)
- cachebox for caching

## Architecture
```
User question → Claude (via Anthropic API) → calls tools → pybaseball → returns data → Claude answers
```

Tools are service layer functions. Claude orchestrates them via tool use.

## Current Phase
Building core data tools. No FastAPI, no frontend yet. Just proving pybaseball works and understanding the data.