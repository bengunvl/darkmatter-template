"""
DarkMatter Replay Template
Replay and inspect any previous run.

Usage:
    python replay.py <ctx_id>         # replay from tip
    python replay.py <ctx_id> summary # metadata only, no payloads
"""

import sys
import json
import darkmatter as dm

ctx_id = sys.argv[1] if len(sys.argv) > 1 else None
mode   = sys.argv[2] if len(sys.argv) > 2 else "full"

if not ctx_id:
    print("Usage: python replay.py <ctx_id> [summary|full]")
    print("\nGet a ctx_id from pipeline.py output or your dashboard.")
    sys.exit(1)

print(f"\nReplaying chain: {ctx_id}")
print(f"Mode: {mode}\n")

result = dm.replay(ctx_id, mode=mode)

print(f"Chain: {'intact ✓' if result['chainIntact'] else 'BROKEN ✗'}")
print(f"Steps: {result['totalSteps']}")
print(f"Root:  {result['rootId']}")
print(f"Agents: {', '.join(result['summary']['agents'])}")
print(f"Models: {', '.join(result['summary']['models'])}")
print(f"Duration: {result['summary']['duration']}")
print()

for step in result["replay"]:
    status = "✓" if step["integrity"]["chainValid"] else "✗"
    role   = step["createdBy"].get("role", "unknown")
    model  = step["createdBy"].get("model", "unknown")
    event  = step["eventType"]
    print(f"  {status} Step {step['step']}/{result['totalSteps']}  [{role}]  {event}")
    print(f"    id:    {step['id']}")
    print(f"    model: {model}")
    if mode == "full" and step.get("payload"):
        out = step["payload"].get("output", "")
        if isinstance(out, dict):
            out = json.dumps(out)
        print(f"    output: {str(out)[:80]}{'...' if len(str(out)) > 80 else ''}")
    print()
