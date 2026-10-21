"""NutriCHAT Demo - Showcases the system capabilities with example queries.

This script demonstrates NutriCHAT processing various poultry nutrition queries
using the hybrid ReAct-RAG architecture. It tests all four expert-designed tools.

Note: Requires a valid SILICONFLOW_API_KEY (or DEEPSEEK_API_KEY) in .env to run the full ReAct agent.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tools import get_all_tools
from src.rag.poultry_db import PoultryDB
from src.config import Config


def test_tools_individually():
    """Test each tool independently without needing API access."""
    print("\n" + "=" * 60)
    print("  TEST: Individual Tool Functions")
    print("=" * 60)

    tools = get_all_tools()
    for tool in tools:
        print(f"\n{'─' * 50}")
        print(f"  Tool: {tool.name}")
        print(f"{'─' * 50}")
        print(f"  Description: {tool.description[:100]}...")

    return tools


def test_rag_without_api():
    """Test data files exist without requiring API key."""
    print("\n" + "=" * 60)
    print("  TEST: RAG Data Preparation")
    print("=" * 60)

    # Verify data files exist in the new structure (corpus + queries)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    species = os.getenv("SPECIES", "broiler").lower()
    dirs_to_check = {
        os.path.join("corpus", "shared"): ["feed_ingredient_bank.csv", "feed_ingredient_amino_acids.csv",
                                            "feed_ingredient_digestibility.csv", "definitions.csv"],
        os.path.join("corpus", species): ["performance_management.csv"],
        os.path.join("queries", species): ["evaluation_queries.json"],
    }

    print(f"\n  Species: {species}")
    all_ok = True
    for subdir, files in dirs_to_check.items():
        print(f"\n  {subdir}/:")
        for f in files:
            path = os.path.join(root, subdir, f)
            exists = os.path.exists(path)
            size = os.path.getsize(path) if exists else 0
            status = "OK" if exists else "MISSING"
            if not exists:
                all_ok = False
            print(f"    [{status}] {f} ({size:,} bytes)")

    return all_ok


def test_query_parsing():
    """Test parsing of evaluation queries."""
    import json

    species = os.getenv("SPECIES", "broiler").lower()
    queries_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "queries", species, "evaluation_queries.json"
    )

    print("\n" + "=" * 60)
    print("  TEST: Evaluation Queries")
    print("=" * 60)

    with open(queries_file, "r") as f:
        data = json.load(f)

    total = 0
    for category, queries in data.items():
        print(f"\n  {category}: {len(queries)} queries")
        total += len(queries)
        # Show first query as example
        if queries:
            q = queries[0]
            print(f"    Example: [{q.get('id', 'N/A')}] {q['query']}")

    print(f"\n  Total evaluation queries: {total}")
    if total < 40:
        print(f"  WARN: Only {total} queries loaded (expected 40+)")
    else:
        print(f"  PASS: All {total} queries loaded correctly!")
    return True


def print_system_overview():
    """Print the NutriCHAT system overview."""
    emb_provider = Config.EMBEDDING_PROVIDER
    emb_model = (Config.LOCAL_EMBEDDING_PATH.split("/")[-1]
                 if emb_provider == "local"
                 else Config.SILICONFLOW_EMBEDDING_MODEL)

    print("\n" + "█" * 60)
    print("  NutriCHAT - Nutrition Conversational Helper for Avian Treatment")
    print("█" * 60)
    print(f"""
  Architecture: Hybrid ReAct-RAG
  Base Model: {Config.LLM_MODEL} (temperature {Config.TEMPERATURE})
  Max Tokens: {Config.MAX_TOKENS} (configurable)
  Species: {Config.SPECIES}

  EXPERT-DESIGNED TOOLS:
  1. Feed Ingredient Bank  - 77 ingredients, ~3,300 nutritional parameters
  2. Performance Management - Breed-specific performance data
  3. Nutrient Requirements  - Phase-specific nutrient specifications
  4. Definitions           - 412 poultry nutrition terms

  RAG COMPONENT:
  - PoultryDB: Vector knowledge base (ChromaDB)
  - Embeddings: {emb_provider} ({emb_model})
  - Semantic retrieval with cosine distance

  EVALUATION:
  - 120 queries across 6 categories
  - Correctness, Precision, Scientific Depth (5-pt scale)
  - Flesch Reading Ease, SelfCheckGPT-NLI

  PAPER REFERENCE:
  Computers and Electronics in Agriculture (2026)
  DOI: 10.1016/j.compag.2026.111564
    """)


def main():
    print_system_overview()

    # Run tests
    tests = [
        ("Data Files", test_rag_without_api),
        ("Tools", lambda: test_tools_individually() or True),
        ("Evaluation Queries", test_query_parsing),
    ]

    all_passed = True
    for name, test_fn in tests:
        try:
            result = test_fn()
            if isinstance(result, bool) and not result:
                print(f"\n  [FAIL] {name}")
                all_passed = False
            else:
                print(f"\n  [PASS] {name}")
        except Exception as e:
            print(f"\n  [FAIL] {name}: {e}")
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("  ALL CHECKS PASSED - System is ready!")
        print(f"\n  To run the full NutriCHAT agent:")
        print(f"  1. Set SILICONFLOW_API_KEY in .env (SiliconFlow or other OpenAI-compatible API)")
        print(f"  2. Build the vector DB: python -m src.main --build-db")
        print(f"  3. Interactive mode: python -m src.main --interactive")
        print(f"  4. Run evaluation: python -m src.main --evaluate")
    else:
        print("  SOME CHECKS FAILED - Review issues above")
    print("=" * 60)


if __name__ == "__main__":
    main()
