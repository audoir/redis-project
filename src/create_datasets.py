from models import Article, TopicEnum, Datasets, Dataset
from config import (
    TRAIN_DATASET_SIZE_PER_TOPIC,
    TEST_DATASET_SIZE_PER_TOPIC,
    BATCH_SIZE,
)
from dotenv import load_dotenv
import os
import csv
from typing import Optional
from file_utils import save_json, load_json

load_dotenv()

DATASET_PATH = os.environ.get("DATASET_PATH")


# Creates train and test datasets by splitting articles from each topic.
def create_new_datasets() -> Datasets:
    datasets = Datasets(
        train=Dataset(**{topic.value: [] for topic in TopicEnum}),
        test=Dataset(**{topic.value: [] for topic in TopicEnum}),
    )
    for topic in TopicEnum:
        articles_for_topic = get_articles_for_topic(topic)
        setattr(
            datasets.train,
            topic.value,
            articles_for_topic[:TRAIN_DATASET_SIZE_PER_TOPIC],
        )
        setattr(
            datasets.test,
            topic.value,
            articles_for_topic[TRAIN_DATASET_SIZE_PER_TOPIC:],
        )
    return datasets


# Retrieves articles for a specific topic from the training dataset CSV file.
def get_articles_for_topic(topic: TopicEnum) -> list[Article]:
    articles: list[Article] = []
    with open(DATASET_PATH, mode="r", newline="") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        article_cnt = 0
        while article_cnt < TRAIN_DATASET_SIZE_PER_TOPIC + TEST_DATASET_SIZE_PER_TOPIC:
            try:
                row = next(csv_reader)
            except StopIteration:
                break
            if row[2] == topic.value:
                article_cnt += 1
                articles.append(
                    Article(id=row[0], text=row[1], topic=TopicEnum(row[2]))
                )
    return articles


# Load datasets from output/datasets.json file.
def load_datasets() -> Optional[Datasets]:
    try:
        datasets = load_json("output/datasets.json", Datasets)
        print("Loaded datasets from output/datasets.json")
        return datasets
    except Exception:
        return None


# Create datasets if they don't exist, otherwise load them
def create_datasets() -> Datasets:
    datasets = load_datasets()
    if datasets is None:
        print("Creating new datasets")
        datasets = create_new_datasets()
    save_json(datasets, "output/datasets.json")
    return datasets


# Get batches of articles from dataset
def get_article_batches(dataset: Dataset) -> list[list[Article]]:
    articles_to_process = []
    for topic in TopicEnum:
        for article in getattr(dataset, topic.value):
            articles_to_process.append(article)
    batches = []
    for i in range(0, len(articles_to_process), BATCH_SIZE):
        batches.append(articles_to_process[i : i + BATCH_SIZE])
    return batches


if __name__ == "__main__":
    datasets = create_datasets()
    print(datasets.test.tech[1])
    print(len(datasets.train.tech))
