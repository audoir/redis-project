from pydantic_ai import Agent
import os
import time
import asyncio
from dotenv import load_dotenv
from models import AgentOutput, Article, AgentResults
from create_datasets import create_datasets
from config import (
    OPENAI_MODEL,
    INPUT_TOKEN_COST_PER_MILLION,
    OUTPUT_TOKEN_COST_PER_MILLION,
)

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

agent = Agent(
    OPENAI_MODEL,
    output_type=AgentOutput,
    system_prompt="You are given a news article. Classify the article into one of the following topics: business, entertainment, politics, sport, tech.",
)


# Classify an article using OpenAI and create metrics
async def classify_article(article: Article) -> AgentResults:
    start_time = time.time()
    result = await agent.run(article.text)

    latency = round(time.time() - start_time, 3)

    usage = result.usage()

    input_cost = (usage.input_tokens / 1_000_000) * INPUT_TOKEN_COST_PER_MILLION
    output_cost = (usage.output_tokens / 1_000_000) * OUTPUT_TOKEN_COST_PER_MILLION
    total_cost = input_cost + output_cost

    return AgentResults(
        topic=result.output.topic,
        latency=latency,
        cost=total_cost,
        correct=result.output.topic == article.topic,
        router_match=False,
    )


if __name__ == "__main__":
    datasets = create_datasets()
    print(asyncio.run(classify_article(datasets.test.tech[1])))
