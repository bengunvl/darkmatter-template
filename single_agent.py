"""
DarkMatter Single-Agent Template
For solo developers — no multi-agent pipeline needed.

Record your own pipeline step by step.
Replay it later. Fork it. Compare runs.

Usage:
    python single_agent.py
"""

import os
import darkmatter as dm

MY_AGENT = os.environ["DARKMATTER_AGENT_A_ID"]

print("\nDarkMatter — single agent pipeline")
print("Recording your own workflow step by step.\n")

# ── Simulate a multi-step pipeline ───────────────────────────────────────────
pipeline_steps = [
    {"name": "fetch_data",     "input": "Q1 earnings data",  "output": {"rows": 142, "status": "ok"}},
    {"name": "analyze",        "input": "142 rows loaded",   "output": {"trend": "up", "delta": "+34%"}},
    {"name": "generate_report","input": {"trend": "up"},     "output": "Q1 APAC report: strong growth..."},
    {"name": "review",         "input": "draft report",      "output": {"approved": True, "edits": 0}},
]

parent_id = None
ctx_ids = []
trace_id = f"trc_{os.urandom(4).hex()}"

for i, step in enumerate(pipeline_steps):
    ctx = dm.commit(
        to_agent_id=MY_AGENT,   # commit to yourself — totally valid
        payload={
            "input":  step["input"],
            "output": step["output"],
            "memory": {"step_name": step["name"]},
        },
        parent_id=parent_id,
        trace_id=trace_id,
        agent={"role": step["name"]},
    )
    parent_id = ctx["id"]
    ctx_ids.append(ctx["id"])
    print(f"  Step {i+1}/{len(pipeline_steps)}  [{step['name']}]  {ctx['id'][-16:]}")

tip_ctx_id = ctx_ids[-1]

# ── Replay ────────────────────────────────────────────────────────────────────
print(f"\nReplaying chain...")
replay = dm.replay(tip_ctx_id)
print(f"  {replay['totalSteps']} steps, chain intact: {replay['chainIntact']}")

# ── Search ────────────────────────────────────────────────────────────────────
print(f"\nSearching history for 'analyze' steps...")
results = dm.search(event="commit", trace_id=trace_id)
print(f"  Found {results['count']} commits in this trace")

# ── Verify ────────────────────────────────────────────────────────────────────
print(f"\nVerifying integrity...")
v = dm.verify(tip_ctx_id)
print(f"  chain_intact: {v['chain_intact']}, length: {v['length']}")

print(f"""
Done ✓
  Tip ctx_id: {tip_ctx_id}
  Trace:      {trace_id}

Replay anytime:
  python replay.py {tip_ctx_id}

Fork from any step:
  python fork_and_compare.py {tip_ctx_id}
""")
