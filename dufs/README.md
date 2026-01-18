# Dufs

> A file server that supports static serving, uploading, searching, accessing
> control, webdav...
>
> <https://github.com/sigoden/dufs>

## Table of contents

- [Dufs](#dufs)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Post-configuration](#post-configuration)
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

- [Dufs](https://github.com/sigoden/dufs)
