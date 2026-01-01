# Beets

> Beets is the media library management system for obsessive music geeks.
>
> <https://beets.io/>

## Table of contents

- [Beets](#beets)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
    - [Create the `config.yaml` file](#create-the-configyaml-file)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the `config.yaml` file

You must create a `config/config.yaml` file prior to run the container:

```sh
# Create the config directory
mkdir config

# Copy the configuration file to config/config.yaml
cp config.yaml config/config.yaml
```

## Run the application with Docker

Do not forget to set the environment variables as described in the previous
section.

In a terminal, run the following commands:

```bash
# Pull the latest images
docker compose pull

# Run the application with Docker
docker compose run --rm beets import /data/music/.to\ sort
```

## Additional resources

- [Beets](https://beets.io/)
- [Linux Server - Beets](https://docs.linuxserver.io/images/docker-beets)
