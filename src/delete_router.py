from create_router import load_router
import redis
from config import ROUTER_NAME, REDIS_URL


# Delete router and its configuration from Redis
def clean_up_router():
    router = load_router()
    if router:
        print("Clearing and deleting router")
        router.clear()
        router.delete()

    redis_client = redis.Redis.from_url(REDIS_URL)
    redis_client.delete(f"{ROUTER_NAME}:route_config")


if __name__ == "__main__":
    clean_up_router()
