# User Service API

## Build

From project root, run `docker-compose -f docker-compose-dev.yml build`

## Development

All commands are ran from the project root

```bash
# To run the app
docker-compose -f docker-compose-dev.yml up

# to get logs
docker-compose -f docker-compose-dev.yml logs
```

### Tests

```bash
# spin up the container
docker-compose -f docker-compose-dev.yml up

# in another terminal, run the manage.py test command
docker-compose -f docker-compose-dev.yml run users python manage.py test
```
