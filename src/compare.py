from models import Metrics
from file_utils import load_json
from config import OPENAI_MODEL


# Calculate percentage improvements
def calculate_improvement(baseline_val: float, router_val: float) -> float:
    if baseline_val == 0:
        return 0.0
    return ((router_val - baseline_val) / baseline_val) * 100


# Compare the results of the baseline and with router
def compare_results():
    baseline_metrics = load_json("output/baseline.json", Metrics)
    router_metrics = load_json("output/with_router.json", Metrics)

    latency_improvement = calculate_improvement(
        baseline_metrics.average_latency,
        router_metrics.average_latency,
    )
    cost_improvement = calculate_improvement(
        baseline_metrics.average_cost,
        router_metrics.average_cost,
    )
    accuracy_improvement = calculate_improvement(
        baseline_metrics.accuracy, router_metrics.accuracy
    )

    comparison_output = f"""Baseline Results using {OPENAI_MODEL}:
Average Latency: {baseline_metrics.average_latency:.3f}s, Average Cost: ${baseline_metrics.average_cost:.2e}, Accuracy: {baseline_metrics.accuracy * 100:.0f}%

With Router Results:
Average Latency: {router_metrics.average_latency:.3f}s, Average Cost: ${router_metrics.average_cost:.2e}, Accuracy: {router_metrics.accuracy * 100:.0f}%
Router Match: {router_metrics.router_match * 100:.0f}%

Percentage Improvements:
Latency: {latency_improvement:.2f}%
Cost: {cost_improvement:.2f}%
Accuracy: {accuracy_improvement:.2f}%

For 100K articles:
Latency: {((router_metrics.average_latency - baseline_metrics.average_latency) * 100000 / 3600):.2f}h
Cost: ${((router_metrics.average_cost - baseline_metrics.average_cost) * 100000):.2f}
Correct: {((router_metrics.accuracy - baseline_metrics.accuracy) * 100000):.0f}
"""
    print(comparison_output)


if __name__ == "__main__":
    compare_results()
