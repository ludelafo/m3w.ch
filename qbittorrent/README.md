# qBittorrent

> The qBittorrent project aims to provide an open-source software alternative to
> µTorrent.
>
> <https://www.qbittorrent.org/>

- [qBittorrent](#qbittorrent)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

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

## Post-configuration

Set the right port forwarding rules in your router.

## Additional resources

- [qBittorrent](https://www.qbittorrent.org/)
