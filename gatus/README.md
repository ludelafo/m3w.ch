# Gatus

> Gatus is a lightweight server monitoring platform that includes Docker
> statistics, historical data, and alert functions.
>
> <https://gatus.dev>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the Gatus configuration file(s)](#create-the-gatus-configuration-files)
- [Run the application with Docker](#run-the-application-with-docker)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the Gatus configuration file(s)

Create a `config` directory with the configuration file(s) needed for Gatus. You
can find some example configuration files in the `examples` directory.

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

- [Gatus](https://gatus.dev)
