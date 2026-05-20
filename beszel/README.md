# Beszel

> Beszel is a lightweight server monitoring platform that includes Docker
> statistics, historical data, and alert functions.
>
> <https://beszel.dev>

## Table of contents

- [Table of contents](#table-of-contents)
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

# Start the Beszel Hub only on first start
docker compose up beszel

# Add a new system to Beszel:
#
# - Name: (Name of the host).
# - Host / IP: (IP of the host).
# - Port: (leave as default).
# - Public Key: (copy and store it in the host's `beszel_agent.env` file).
# - Token: (copy and store it in the host's `beszel_agent.env` file).

# Access the superuser PocketBase admin panel at `/_/` (https://beszel.dev/guide/user-accounts).
#
# Change the Mail settings in PocketBase admin panel if needed.

# Start the application with Docker
docker compose up --detach
```

## Additional resources

- [Beszel](https://beszel.dev)
- [Beszel Notifications](https://beszel.dev/guide/notifications/)
