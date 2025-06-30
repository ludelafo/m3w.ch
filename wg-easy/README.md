# WireGuard Easy

> The easiest way to run WireGuard VPN + Web-based Admin UI.
>
> <https://github.com/wg-easy/wg-easy>

## Table of contents

- [WireGuard Easy](#wireguard-easy)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `.env` and `wg-easy.env` files to your needs.

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

- [WireGuard](https://www.wireguard.com/)
- [WireGuard Easy](https://github.com/wg-easy/wg-easy)
