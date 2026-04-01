"""
DarkMatter Pipeline Template
3-agent pipeline: researcher → writer → reviewer
Each step committed as a Context Passport.

Usage:
    python pipeline.py "Analyze Q1 2026 earnings for APAC region"
"""

import os
import sys
import darkmatter_sdk as dm

# ── Config ────────────────────────────────────────────────────────────────────
AGENT_A = os.environ["DARKMATTER_AGENT_A_ID"]   # researcher
AGENT_B = os.environ["DARKMATTER_AGENT_B_ID"]   # writer
AGENT_C = os.environ["DARKMATTER_AGENT_C_ID"]   # reviewer

task = sys.argv[1] if len(sys.argv) > 1 else "Summarize key trends in AI infrastructure Q1 2026"
trace_id = f"trc_{os.urandom(4).hex()}"

print(f"\nDarkMatter Pipeline Template")
print(f"Task: {task}")
print(f"Trace: {trace_id}\n")

# ── Step 1: Research ──────────────────────────────────────────────────────────

print("Step 1/3  Researcher agent...")

# Replace this with your actual LLM call:
research_output = {
    "summary":    f"Research findings for: {task}",
    "key_points": ["point 1", "point 2", "point 3"],
    "confidence": 0.92,
}

ctx1 = dm.commit(
    to_agent_id=AGENT_B,
    payload={
        "input":  task,
        "output": research_output,
        "memory": {"model": "claude-opus-4-6", "provider": "anthropic"},
    },
    trace_id=trace_id,
    event_type="commit",
    agent={"role": "researcher", "provider": "anthropic", "model": "claude-opus-4-6"},
)

print(f"  committed: {ctx1['id']}")
print(f"  integrity: {ctx1['integrity']['verification_status']}")

# ── Step 2: Write ─────────────────────────────────────────────────────────────

print("\nStep 2/3  Writer agent...")

# Replace with your actual LLM call:
draft = f"## Report\n\nBased on research: {research_output['summary']}\n\n"

ctx2 = dm.commit(
    to_agent_id=AGENT_C,
    payload={
        "input":  research_output,
        "output": draft,
        "memory": {"word_count": len(draft.split()), "model": "gpt-4o"},
    },
    parent_id=ctx1["id"],   # ← links the chain
    trace_id=trace_id,
    agent={"role": "writer", "provider": "openai", "model": "gpt-4o"},
)

print(f"  committed: {ctx2['id']}")
print(f"  parent:    {ctx2['parent_id'][-12:]}")

# ── Step 3: Review ────────────────────────────────────────────────────────────

print("\nStep 3/3  Reviewer agent...")

# Replace with your actual LLM call:
review = {"decision": "approved", "edits": [], "notes": "Report is clear and accurate."}

ctx3 = dm.commit(
    to_agent_id=AGENT_A,    # back to researcher for any follow-up
    payload={
        "input":    draft,
        "output":   review,
        "variables": {"approved": True, "final_report": draft},
    },
    parent_id=ctx2["id"],   # ← extends the chain
    trace_id=trace_id,
    event_type="checkpoint",
    agent={"role": "reviewer", "provider": "anthropic", "model": "claude-opus-4-6"},
)

print(f"  committed: {ctx3['id']}")
print(f"  event:     {ctx3['event']['type']}")

# ── Verify ────────────────────────────────────────────────────────────────────

print("\nVerifying chain integrity...")
v = dm.verify(ctx3["id"])
print(f"  chain_intact: {v['chain_intact']}")
print(f"  length:       {v['length']} commits")
print(f"  root_hash:    {v['root_hash'][:32]}...")

# ── Summary ───────────────────────────────────────────────────────────────────

print(f"""
Chain committed ✓
  Root:    {ctx1['id']}
  Tip:     {ctx3['id']}
  Trace:   {trace_id}

Replay this run:
  python replay.py {ctx3['id']}

View in dashboard:
  https://darkmatterhub.ai/dashboard
""")
