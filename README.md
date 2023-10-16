# Autotesting framework for kiwi.com application

Simple test framework with automatic tests written on python.

## Getting Started

To use the app python 3 should be installed on you computer.

### Installing

To install and run tests:

```
python3 -m virtualenv venv

source venv/bin/activate

pip3 install -r requirements.txt

pytest -v
```

### Run with docker container

These autotests can be launched in docker container.

#### Prerequisites

Doker should be installed and daemon should be running
https://docs.docker.com/config/daemon/start/

#### Build image and start container

```
docker build -t docker-c-teleport-test-task .

docker run -it docker-c-teleport-test-task /bin/bash
```

To launch test, run following command inside container

```
xvfb-run pytest -v
```

## Built With

* [PyTest](https://docs.pytest.org/en/latest/) - Test framework
* [Playwright](https://playwright.dev/python/) - UI automation library
