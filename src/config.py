from models import TopicEnum, VectorizerEnum

# Redis Configuration
REDIS_URL = "redis://localhost:6379"
# REDIS_URL = "redis://[username]:[password]@[host]:[port]" # use this for Redis Cloud

# Dataset Configuration
TRAIN_DATASET_SIZE_PER_TOPIC = 50
TEST_DATASET_SIZE_PER_TOPIC = 10
TOTAL_ARTICLES = len(TopicEnum) * TEST_DATASET_SIZE_PER_TOPIC

# OpenAI Configuration
OPENAI_MODEL = "gpt-5-nano"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
BATCH_SIZE = 3

# HF Vectorizer Configuration
HF_MODEL = "sentence-transformers/all-mpnet-base-v2"

# GPT-5-nano Pricing (per 1M tokens)
INPUT_TOKEN_COST_PER_MILLION = 0.05
OUTPUT_TOKEN_COST_PER_MILLION = 0.40

# Router Configuration
# The distance threshold is chosen as a good balance between non-matches and false matches
# The lower the threshold, the more non-matches
# The higher the threshold, the more false matches
ROUTER_DISTANCE_THRESHOLD = 0.6
ROUTER_VECTORIZER = VectorizerEnum.HF
ROUTER_NAME = "topic-router"
