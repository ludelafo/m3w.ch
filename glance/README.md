# Glance

> A lightweight, highly customizable dashboard that displays your feeds in a
> beautiful, streamlined interface.
>
> <https://github.com/glanceapp/glance>

## Table of contents

- [Glance](#glance)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
    - [Create the `glance.yml` file](#create-the-glanceyml-file)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the `glance.yml` file

You must create a `glance.yml` file prior to run the container. You can check
examples in the [`examples`](./examples) directory and copy an example to
`glance.yml`.

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

- [Glance](https://github.com/glanceapp/glance)
