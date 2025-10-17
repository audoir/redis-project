# Start Redis Instance in a Docker Container

You must first install [Docker](https://docs.docker.com/desktop/) on your machine.

Navigate to the docker directory and run:

```bash
./start-redis.sh
```

To stop the redis instance, run:

```bash
./stop-redis.sh
```

# Install the Necessary Python Packages and Start Virtual Environment

You must first install [Python](https://www.python.org/downloads/) and pip on your machine.

Navigate to the root directory of the project and run:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install redisvl numpy\<2.0 sentence-transformers
```

You'll need to start the virtual environment every time you want to run the Python code.
