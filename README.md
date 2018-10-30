# User Service API

[![Build Status](https://travis-ci.org/cubiio/user-service.svg?branch=master)](https://travis-ci.org/cubiio/user-service)

## About

User service API built with:

- Python
- Flask
- Docker
- and tested with unittest, coverage and Travis-ci

## Build

From project root, run `docker-compose -f docker-compose-dev.yml build`

## Development

All commands are ran from the project root

```bash
# To run the app
docker-compose -f docker-compose-dev.yml up


# to get logs
docker-compose -f docker-compose-dev.yml logs

# app shell
docker-compose -f docker-compose-dev.yml run users flask shell
```

### db

```bash
# recreate db
docker-compose -f docker-compose-dev.yml run users python manage.py recreate-db

# psql db
docker-compose -f docker-compose-dev.yml exec users-db psql -U postgres
```

### Tests

```bash
# spin up the container
docker-compose -f docker-compose-dev.yml up

# in another terminal, run the manage.py test command
docker-compose -f docker-compose-dev.yml run users python manage.py test
```
