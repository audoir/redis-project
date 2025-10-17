from redisvl.extensions.router import Route
from models import Dataset
from config import (
    OPENAI_EMBEDDING_MODEL,
    ROUTER_DISTANCE_THRESHOLD,
    ROUTER_VECTORIZER,
    ROUTER_NAME,
    REDIS_URL,
    HF_MODEL,
)
from typing import List
from models import TopicEnum, VectorizerEnum
from redisvl.extensions.router import SemanticRouter
from redisvl.utils.vectorize import OpenAITextVectorizer
from create_datasets import create_datasets
from redisvl.utils.vectorize import HFTextVectorizer
from typing import Optional
import time


# Define the routes for each topic
def define_routes(train_dataset: Dataset) -> List[Route]:
    routes: List[Route] = []
    for topic in TopicEnum:
        routes.append(
            Route(
                name=topic.value,
                references=[
                    article.text for article in getattr(train_dataset, topic.value)
                ],
                distance_threshold=ROUTER_DISTANCE_THRESHOLD,
            )
        )
    return routes


# Create the router using HuggingFace embeddings and the defined routes
def create_router_hf(train_dataset: Dataset) -> SemanticRouter:
    return SemanticRouter(
        name=ROUTER_NAME,
        vectorizer=HFTextVectorizer(
            model=HF_MODEL,
        ),
        routes=define_routes(train_dataset),
        redis_url=REDIS_URL,
        overwrite=True,
    )


# Create the router using OpenAI embeddings and the defined routes
def create_router_openai(train_dataset: Dataset) -> SemanticRouter:
    return SemanticRouter(
        name=ROUTER_NAME,
        vectorizer=OpenAITextVectorizer(
            model=OPENAI_EMBEDDING_MODEL,
        ),
        routes=define_routes(train_dataset),
        redis_url=REDIS_URL,
        overwrite=True,
    )


# Load the router from Redis
def load_router() -> Optional[SemanticRouter]:
    try:
        router = SemanticRouter.from_existing(name=ROUTER_NAME, redis_url=REDIS_URL)
        return router
    except ValueError:
        return None


# Create the router if it doesn't exist, otherwise load it
def create_router(train_dataset: Dataset) -> SemanticRouter:
    router = load_router()
    if router:
        print("Loading existing router")
        return router
    print("Creating new router")
    start_time = time.time()
    router = (
        create_router_openai(train_dataset)
        if ROUTER_VECTORIZER == VectorizerEnum.OPENAI
        else create_router_hf(train_dataset)
    )
    end_time = time.time()
    print(f"\nRouter created in {(end_time - start_time):.2f} seconds\n")
    return router


if __name__ == "__main__":
    datasets = create_datasets()
    router = create_router(datasets.train)
    for article in datasets.test.business:
        print(router(article.text))
    for article in datasets.test.tech:
        print(router(article.text))
