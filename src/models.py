from pydantic import BaseModel, create_model, constr
from enum import Enum


class TopicEnum(str, Enum):
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    POLITICS = "politics"
    SPORT = "sport"
    TECH = "tech"


class Article(BaseModel):
    id: int
    text: constr(min_length=1)
    topic: TopicEnum


# Create Dataset class with fields from TopicEnum
Dataset = create_model(
    "Dataset", **{topic.value: (list[Article], ...) for topic in TopicEnum}
)


class Datasets(BaseModel):
    train: Dataset
    test: Dataset


class AgentOutput(BaseModel):
    topic: TopicEnum


class AgentResults(BaseModel):
    topic: TopicEnum
    latency: float
    cost: float
    correct: bool
    router_match: bool  # for semantic router architecture


class Metrics(BaseModel):
    average_latency: float
    average_cost: float
    accuracy: float
    router_match: float  # for semantic router architecture


class VectorizerEnum(str, Enum):
    HF = "hf"
    OPENAI = "openai"
