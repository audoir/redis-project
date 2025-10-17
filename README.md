# Start Redis Instance in a Docker Container

You must first install [Docker](https://docs.docker.com/desktop/) on your machine.

To start the redis instance, run:

```bash
docker-compose up -d
```

This runs the Redis instance in a Docker container, which can be accessed on port 6379. The Redis Stack UI can be accessed from a [web browser on port 8001](http://localhost:8001).

To stop the redis instance, run:

```bash
docker-compose down
```

# Install the Python Dependencies and Start Virtual Environment

You must first install [Python](https://www.python.org/downloads/) and pip on your machine.

To install the Python dependencies, run:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install redisvl numpy\<2.0 sentence-transformers
```

You'll need to start the virtual environment every time you want to run the Python code.

```bash
source venv/bin/activate
```
