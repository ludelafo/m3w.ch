# Dynacat

> Self-hosted dashboard built for people who want their information in one
> place.
>
> Forked from [Glance](https://github.com/glanceapp/glance) - it focuses on
> dynamic content updates and seamless integration with external applications.
>
> <https://github.com/Panonim/dynacat>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the Dynacat configuration file(s)](#create-the-dynacat-configuration-files)
- [Run the application with Docker](#run-the-application-with-docker)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the Dynacat configuration file(s)

Create a `config` directory with the configuration file(s) needed for Dynacat.
You can find an example configuration file in the `examples` directory.

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

- [Dynacat](https://github.com/Panonim/dynacat)
