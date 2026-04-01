# DarkMatter Agent Pipeline Template

A ready-to-run multi-agent pipeline with DarkMatter execution records built in.

## What's included

- 3-agent pipeline (researcher → writer → reviewer)
- DarkMatter commits after every agent step
- LangGraph integration
- Anthropic SDK integration
- Chain diff between runs
- Environment setup

## Try it first — no signup required

```bash
pip install darkmatter-sdk
darkmatter demo
```

Runs a local 3-step chain with commit, verify, replay, fork, and diff. No API key needed.

## Quick start

```bash
# 1. Clone this template
git clone https://github.com/bengunvl/darkmatter-template
cd darkmatter-template

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your keys
cp .env.example .env
# Edit .env with your API keys

# 4. Run the demo pipeline
python pipeline.py

# 5. Replay what happened
python replay.py
```

## Files

| File | Description |
|------|-------------|
| `pipeline.py` | Main 3-agent pipeline with DarkMatter commits |
| `replay.py` | Replay and inspect any previous run |
| `fork_and_compare.py` | Fork from a checkpoint, run with different model, diff results |
| `single_agent.py` | Single-developer use case — no multi-agent needed |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |

## Environment variables

```bash
DARKMATTER_API_KEY=dm_sk_...     # get free at darkmatterhub.ai/signup
ANTHROPIC_API_KEY=sk-ant-...     # optional — for Claude examples
OPENAI_API_KEY=sk-...            # optional — for OpenAI examples
DARKMATTER_AGENT_A_ID=...        # your agent IDs from dashboard
DARKMATTER_AGENT_B_ID=...
DARKMATTER_AGENT_C_ID=...
```

## Links

- [DarkMatter docs](https://darkmatterhub.ai/docs)
- [Get API key](https://darkmatterhub.ai/signup)
- [Context Passport spec](https://contextpassport.com)
