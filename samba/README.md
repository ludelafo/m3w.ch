# Samba

> Samba is an Open Source / Free Software suite that has, since 1992, provided
> file and print services to all manner of SMB/CIFS clients, including the
> numerous versions of Microsoft Windows operating systems.
>
> <https://www.samba.org/>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the configuration file(s)](#create-the-configuration-files)
- [Run the application with Docker](#run-the-application-with-docker)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the configuration file(s)

Create a `config` directory with the configuration file(s) needed for the
service.

You can find example configuration files in the `examples` directory.

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

- [Samba](https://www.samba.org/)
- [docker-samba](https://github.com/crazy-max/docker-samba)
