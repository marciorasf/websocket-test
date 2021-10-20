# Performance Tests

## Requirements

- DockerCompose
- Node.js 14 or above
- Yarn

## Setup

1. You just need to install the dependencies:

      ```bash
      yarn
      ```

## Run a test

1. Run the server:

    ```bash
      docker-compose up
    ```

2. Run the test:

    ```bash
    ./run_test <test_name>
    ```

    The `<test_name>` should be the name of a test inside `src` without the `ts` extension.
    For example:

    ```bash
    ./run_test default_load
    ```
