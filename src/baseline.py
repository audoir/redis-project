import asyncio
from create_datasets import create_datasets, get_article_batches
from models import Metrics, Dataset, Article, AgentResults
from openai_utils import classify_article
from config import TOTAL_ARTICLES
from file_utils import save_json
from metrics_utils import calculate_f1_scores


# Process a batch of articles
async def process_batch(batch: list[Article]) -> list[AgentResults]:
    tasks = []
    for article in batch:
        print(f"Classifying {article.topic} article {article.id}...")
        tasks.append(classify_article(article))
    results_batch = await asyncio.gather(*tasks)
    return results_batch


# Create metrics for the baseline using test dataset
async def create_baseline_metrics(test_dataset: Dataset) -> Metrics:
    total_latency = 0
    total_cost = 0
    total_correct = 0
    true_labels = []
    predicted_labels = []
    article_batches = get_article_batches(test_dataset)

    for batch in article_batches:
        results_batch = await process_batch(batch)
        for i, results in enumerate(results_batch):
            total_latency += results.latency
            total_cost += results.cost
            total_correct += 1 if results.correct else 0
            true_labels.append(batch[i].topic)
            predicted_labels.append(results.topic)

            print(results)
        print()

    macro_f1, micro_f1 = calculate_f1_scores(true_labels, predicted_labels)

    return Metrics(
        average_latency=total_latency / TOTAL_ARTICLES,
        average_cost=total_cost / TOTAL_ARTICLES,
        accuracy=total_correct / TOTAL_ARTICLES,
        macro_f1_score=macro_f1,
        micro_f1_score=micro_f1,
        router_match=0,
    )


if __name__ == "__main__":
    metrics = asyncio.run(create_baseline_metrics(create_datasets().test))
    save_json(metrics, "output/baseline.json")
    print(metrics)
