# Pocket ID

> A simple and easy-to-use OIDC provider that allows users to authenticate with
> their passkeys to your services.
>
> <https://pocket-id.org/>

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

# Start the application with Docker
docker compose up --detach
```

Access Pocket ID at `https://auth.m3w.ch/setup` and follow the instructions to
set up your account and create a passkey.

## Additional resources

- [Pocket ID](https://pocket-id.org/)
