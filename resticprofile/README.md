# resticprofile

> resticprofile is a lightweight server monitoring platform that includes Docker
> statistics, historical data, and alert functions.
>
> <https://resticprofile.dev>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
- [Run the application with Docker](#run-the-application-with-docker)
- [Check the configuration](#check-the-configuration)
- [Manual backups](#manual-backups)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

The `*.secrets.env` files contain secrets. They must be encrypted with SOPS
before being committed, see [doco-cd](../doco-cd/README.md#manage-secrets).

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

## Check the configuration

```bash
docker compose run --rm --entrypoint=/usr/bin/resticprofile resticprofile \
  --config /etc/resticprofile/profiles.yaml show
```

## Manual backups

```bash
docker compose run --rm --entrypoint=/usr/bin/resticprofile resticprofile \
  [--dry-run] backup
```

## Additional resources

- [resticprofile](https://resticprofile.dev)
