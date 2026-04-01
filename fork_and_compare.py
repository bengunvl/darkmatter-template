"""
DarkMatter Fork & Compare Template
Fork from a checkpoint, run with a different model, diff the results.

This is the "replay with changed model" pattern.

Usage:
    python fork_and_compare.py <ctx_id>
"""

import sys
import os
import darkmatter_sdk as dm

ctx_id = sys.argv[1] if len(sys.argv) > 1 else None
if not ctx_id:
    print("Usage: python fork_and_compare.py <ctx_id>")
    sys.exit(1)

AGENT_ID = os.environ["DARKMATTER_AGENT_A_ID"]

print(f"\nFork & Compare")
print(f"Original tip: {ctx_id}\n")

# ── Step 1: Get the original chain ────────────────────────────────────────────
original = dm.replay(ctx_id)
print(f"Original chain: {original['totalSteps']} steps, models: {original['summary']['models']}")

# ── Step 2: Fork from the second-to-last step ─────────────────────────────────
# (or any checkpoint you want to branch from)
if original["totalSteps"] < 2:
    fork_point = original["replay"][0]["id"]
else:
    fork_point = original["replay"][-2]["id"]

print(f"\nForking from: {fork_point}")

fork_ctx = dm.fork(
    fork_point,
    to_agent_id=AGENT_ID,
    branch_key="experiment-alt-model",
)
print(f"Fork created:  {fork_ctx['id']}")
print(f"Branch:        {fork_ctx['branch_key']}")

# ── Step 3: Continue on the fork with a different model ───────────────────────
print(f"\nRunning alternative review with gpt-4o instead of claude...")

# Replace with your actual LLM call using gpt-4o:
alt_output = {
    "decision": "approved",
    "notes":    "Alternative model review: content is accurate, style is clear.",
    "edits":    [],
}

fork_continue = dm.commit(
    to_agent_id=AGENT_ID,
    payload={
        "input":    "Alternative model review",
        "output":   alt_output,
        "variables": {"approved": True},
    },
    parent_id=fork_ctx["id"],
    event_type="checkpoint",
    agent={"role": "reviewer", "provider": "openai", "model": "gpt-4o"},
)
print(f"Fork continued: {fork_continue['id']}")

# ── Step 4: Diff original vs fork ─────────────────────────────────────────────
print(f"\nDiffing original vs fork...")
d = dm.diff(ctx_id, fork_continue["id"])

print(f"\nDiff results:")
print(f"  Original chain: {d['lengthA']} steps")
print(f"  Fork chain:     {d['lengthB']} steps")
print(f"  Changed steps:  {d['changedSteps']}")
print(f"  Identical:      {d['identical']}")
print(f"  Models (A):     {d['summary']['modelsA']}")
print(f"  Models (B):     {d['summary']['modelsB']}")
print()

for step in d["steps"]:
    changed = any(d["diff"].values() for d in [step["diff"]])
    if step["diff"]["modelChanged"] or step["diff"]["payloadChanged"]:
        print(f"  Step {step['step']}:")
        if step["diff"]["modelChanged"]:
            print(f"    model:   {step['a']['model'] if step['a'] else 'none'} → {step['b']['model'] if step['b'] else 'none'}")
        if step["diff"]["payloadChanged"]:
            print(f"    payload: changed")

print(f"""
Fork complete ✓
  Original: {ctx_id}
  Fork tip: {fork_continue['id']}

To replay each:
  python replay.py {ctx_id}
  python replay.py {fork_continue['id']}
""")
