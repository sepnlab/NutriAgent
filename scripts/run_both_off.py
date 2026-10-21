"""Run both_off ablation condition only - full 107 queries."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.config import Config
from v1.src.knowledge_graph.graph_store import PNKGStore
from v1.src.agent.kg_multi_agent import KGMultiAgentEngine
from src.utils.query_loader import load_queries as ql

KG_PATH = "v1/data/pnkg.json"
store = PNKGStore()
store.load(KG_PATH)

# Load queries from both species preserving separate IDs
all_qs = []
for species in ["broiler", "layer"]:
    fpath = f"queries/{species}/evaluation_queries_curated.json"
    if os.path.exists(fpath):
        qs = ql(queries_file=fpath, query_set="all")
        for q in qs:
            q["species"] = species
        all_qs.extend(qs)
        print(f"{species}: {len(qs)} queries")

print(f"Total: {len(all_qs)} queries")

engine = KGMultiAgentEngine(pnkg=store, model=Config.LLM_MODEL, temperature=0.0,
    max_tokens=Config.MAX_TOKENS, base_url=Config.LLM_BASE_URL,
    api_key=Config.LLM_API_KEY, ablation={"no_graphrag": True, "no_tools": True})

results = []
errors = 0
for i, q in enumerate(all_qs):
    s = q["query"][:60].replace("\n", " ")
    print(f"  [{i+1}/{len(all_qs)}] {q['species']}: {q['id']}: {s}...", end=" ")
    sys.stdout.flush()
    try:
        t0 = time.time()
        r = engine.answer(q["query"])
        t = time.time() - t0
        results.append({"id": q["id"], "query": q["query"], "response": r["response"],
            "species": q["species"], "type": q.get("type", ""),
            "category": q.get("category", ""),
            "time": t, "tools_used": r.get("tools_used", []),
            "graph_context": r.get("graph_context", ""), "steps": r.get("steps", [])})
        print(f"OK ({t:.1f}s)")
    except Exception as e:
        print(f"ERR: {e}")
        results.append({"id": q["id"], "query": q["query"], "response": f"[Error: {e}]",
            "species": q["species"], "type": q.get("type", ""), "category": q.get("category", ""),
            "error": str(e)})
        errors += 1

print(f"\nDone: {len(results)} results, {errors} errors")
out = {"queries": all_qs, "results": results}
os.makedirs("logs", exist_ok=True)
with open("logs/both_off_raw.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("Saved logs/both_off_raw.json")
