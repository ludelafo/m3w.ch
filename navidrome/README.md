# Navidrome

> Navidrome allows you to enjoy your music collection from anywhere, by making
> it available through a modern Web UI and through a wide range of third-party
> compatible mobile apps, for both iOS and Android devices.
>
> <https://www.navidrome.org/>

## Table of contents

- [Navidrome](#navidrome)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Create the required directories](#create-the-required-directories)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

## Create the required directories

Create the following directories with the right permissions:

```bash
mkdir config music
```

## Run the application with Docker

Do not forget to set the environment variables as described in the previous
section.

In a terminal, run the following commands:

```bash
# Pull the latest images
docker compose pull

# Start the application with Docker
docker compose up --detach
```

## Additional resources

- [Navidrome](https://www.navidrome.org/)
