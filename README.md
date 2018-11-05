# User Service API

[![Build Status](https://travis-ci.org/cubiio/user-service.svg?branch=master)](https://travis-ci.org/cubiio/user-service)

## About

User service API built with:

- Python
- Flask
- Docker
- PostgreSQL
- SQLAlchemy
- and tested with unittest, coverage and Travis-CI

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

To make schema changes, make the changes to the Model, then run:

```bash
docker-compose -f docker-compose-dev.yml run users python manage.py db migrate

docker-compose -f docker-compose-dev.yml run users python manage.py db upgrade
```

### Tests

```bash
# spin up the container
docker-compose -f docker-compose-dev.yml up

# in another terminal, run the manage.py test command
docker-compose -f docker-compose-dev.yml run users python manage.py test
```
