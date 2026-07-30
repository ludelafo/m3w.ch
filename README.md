# m3w.ch

## Prerequisites

The following prerequisites must be filled to run these services:

- [Docker](https://docs.docker.com/get-docker/) must be installed.
- [Docker Compose](https://docs.docker.com/compose/install/) must be installed
  (it should be installed by default with Docker in most cases).

## Architecture

![m3w.ch architecture](./ansible/m3w-architecture.svg)

## Application configuration

Each application tries to follow the same structure and configuration:

1. **Set the environment variables**: edit the `*.env` files to your needs.
2. **Setup the application**: create the configuration file(s) and the required
   directories with the right permissions.
3. **Run the application with Docker**: run with `docker compose up --detach`.

## Cheatsheet

### Generate a secure password

<https://linux.die.net/man/1/pwgen>

```bash
# Generate a password for computers
pwgen --secure [--capitalize] [--numerals] [-symbols] 20 1

# Generate a password for humans
pwgen --ambiguous [--capitalize] [--numerals] [-symbols] 20 1
```
