# Samba

> Samba is an Open Source / Free Software suite that has, since 1992, provided
> file and print services to all manner of SMB/CIFS clients, including the
> numerous versions of Microsoft Windows operating systems.
>
> <https://www.samba.org/>

## Table of contents

- [Samba](#samba)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
    - [Create the `config.yaml` file](#create-the-configyaml-file)
    - [Create the user password](#create-the-user-password)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the `config.yaml` file

You must create a `config.yaml` file prior to run the container. You can check
examples in the [`examples`](./examples) directory and copy an example to
`config.yaml`.

You might need to update the `volumes` section in the `compose.yaml` file to
match your configuration.

### Create the user password

Create a new file called `user_password.txt` in this directory and add the user
password in it to access the share(s).

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
