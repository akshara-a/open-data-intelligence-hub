import asyncio
import json
from app.evaluation.engine import execute_benchmark_suite
from app.evaluation.models import ExecuteBenchmarkRequest

async def main():
    repo_id = "12fac9bd-0ebb-4844-a239-e518e812b6bb"
    commit_sha = "d730e05672cb7673365022a44d3814bdc66ec033"
    print(f"Starting 12-case live benchmark on repo {repo_id} @ commit {commit_sha[:8]}...")
    req = ExecuteBenchmarkRequest(
        repo_id=repo_id,
        commit_sha=commit_sha,
    )
    detail = await execute_benchmark_suite(
        request=req,
        created_by="benchmark_tester",
    )
    print("\n================ BENCHMARK EXECUTION COMPLETED ================")
    print(f"Run ID: {detail.run_id}")
    print(f"Status: {detail.status}")
    print(f"Sample Count: {detail.sample_count}")
    print(f"Provider: {detail.provider_name}")
    print("\n--- METRICS SUMMARY ---")
    metrics_dict = detail.metrics.model_dump()
    for k, v in metrics_dict.items():
        if k != "categories":
            print(f"  {k}: {v}")

    print("\n--- PER-CATEGORY METRICS ---")
    for cat in detail.metrics.categories:
        print(f"  {cat.category:25s} | N={cat.sample_count} | P={cat.precision:.4f} | R={cat.recall:.4f} | F1={cat.f1:.4f} | Cov={cat.grounding_accuracy:.4f} | Lat={cat.avg_latency_ms:.1f}ms")

    print("\n--- INDIVIDUAL QUERY RESULTS ---")
    for qr in detail.query_results:
        print(f"  [{qr.test_id}] Passed={qr.passed} | Latency={qr.latency_ms:.1f}ms | PredEnts={qr.predicted_entities} | PredEvs={qr.predicted_evidence_ids} | Err={qr.error}")

    if detail.failure_analysis:
        print("\n--- FAILURE ANALYSIS ---")
        for fa in detail.failure_analysis:
            print(f"  {fa}")

if __name__ == "__main__":
    asyncio.run(main())
