# WebSocket Test

The intent of this project is to just play around with WebSockets in Python and testing it with [k6](https://k6.io/).

Some other stuff that I learned a bit on this project:

- Asyncio
- Testing with pytest
- Pydantic
- Dependency management with Poetry
- CI/CD with GitHub actions

## Requirements

- Python 3.9 (maybe it works with Python 3.7 and 3.8 but I won't test it)
- Docker and DockerCompose
- Node 14 (again, maybe it works with other versions)
- Yarn

## Setup

1. Clone the repo

2. Install Poetry dependencies

        poetry install

2. Install pre-commit hooks

        pre-commit install
        pre-commit install -t pre-push

## Run

Run `run.sh`

## Use

1. Connect via WebSocket

2. Send a message subscribing to a stream. Available streams: `default`, `even`, `odd`
    ```json
    {
        "action": "subscribe" ,
        "stream": "even"
    }
    ```

3. Now you'll receive all entries for the stream you have subscribed

4. (Optional) Send a message unsubscribe from a stream:
    ```json
    {
        "action": "unsubscribe" ,
        "stream": "even"
    }
    ```
