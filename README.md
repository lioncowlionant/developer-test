The `Makefile` is self documented, to know what is available just do `make` or `make help`

# Pre requisites
- make
- docker with docker compose plugin

# Installation
- `make setup`

# Server (backend & frontend)
Once started, backend UI should be available as [SwaggerUI](http://127.0.0.1:8000/docs) or [Redocs](http://127.0.0.1:8000/redoc)

## Start everything
- `make up`

## To stop running server
- `make stop`

# Using the cli

Due to the CLI being run inside a docker container, example mounted into `/data/examples`
Also, arguments should be given as args on the command line

Running example
```shell
make cli args="/data/examples/example1/millennium-falcon.json /data/examples/example1/empire.json"
```

Accessing the help of the CLI
```shell
make cli args="--help"
```

Incorrect one
```shell
make cli args="/data/examples/example1/empire.json /data/examples/example1/empire.json"
```
