import asyncio
from redisvl.extensions.router import SemanticRouter
from models import AgentResults, Article, Datasets, Metrics
import time
from openai_utils import classify_article
from create_router import create_router
from config import TOTAL_ARTICLES
from create_datasets import create_datasets, get_article_batches
import os
from file_utils import save_json

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # disable parallelism for tokenizers


# Classify an article using the router, if the router doesn't match, classify using OpenAI
async def classify_article_with_router(
    router: SemanticRouter, article: Article
) -> AgentResults:
    start_time = time.time()
    router_result = await asyncio.to_thread(router, article.text)

    if router_result.name is None:
        return await classify_article(article)

    latency = round(time.time() - start_time, 3)

    return AgentResults(
        topic=router_result.name,
        latency=latency,
        cost=0,
        correct=router_result.name == article.topic,
        router_match=True,
    )


# Process articles in batches
async def process_batch(
    router: SemanticRouter, batch: list[Article]
) -> list[AgentResults]:
    tasks = []
    for article in batch:
        print(f"Classifying {article.topic} article {article.id}...")
        tasks.append(classify_article_with_router(router, article))
    results_batch = await asyncio.gather(*tasks)
    return results_batch


# Create metrics for the router architecture using test dataset
async def create_with_router_metrics(datasets: Datasets) -> Metrics:
    router = create_router(datasets.train)
    total_latency = 0
    total_cost = 0
    total_correct = 0
    total_router_match = 0
    article_batches = get_article_batches(datasets.test)

    for batch in article_batches:
        results_batch = await process_batch(router, batch)
        for results in results_batch:
            total_latency += results.latency
            total_cost += results.cost
            total_correct += 1 if results.correct else 0
            total_router_match += 1 if results.router_match else 0
            print(results)
        print()

    return Metrics(
        average_latency=total_latency / TOTAL_ARTICLES,
        average_cost=total_cost / TOTAL_ARTICLES,
        accuracy=total_correct / TOTAL_ARTICLES,
        router_match=total_router_match / TOTAL_ARTICLES,
    )


if __name__ == "__main__":
    metrics = asyncio.run(create_with_router_metrics(create_datasets()))
    save_json(metrics, "output/with_router.json")
    print(metrics)
