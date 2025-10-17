# Start a Redis Instance in a Docker Container

[Docker](https://docs.docker.com/desktop/) must be installed on your machine.

To start a Redis instance, run:

```bash
docker-compose up -d
```

This runs a Redis instance in a Docker container, which can be accessed on port 6379. The Redis Stack UI can be accessed from a [web browser on port 8001](http://localhost:8001).

To stop the Redis instance, run:

```bash
docker-compose down
```

# Install Python Dependencies and Start a Virtual Environment

[Python](https://www.python.org/downloads/) must be installed on your machine.

To install the Python dependencies, run:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

You'll need to start the virtual environment every time you want to run the Python code.

```bash
source venv/bin/activate
```

# Set up environment variables

Create a .env file to store the environment variables. The .env file should contain the following variables:

```bash
DATASET_TEST_PATH="<path_to_test_dataset>"
DATASET_TRAIN_PATH="<path_to_train_dataset>"
```
