# Minecraft server

> Build anything you can imagine, uncover eerie mysteries, and survive the night
> in the ultimate sandbox adventure game.
>
> <https://www.minecraft.net/about-minecraft>

## Table of contents

- [Minecraft server](#minecraft-server)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Run Minecraft commands](#run-minecraft-commands)
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

## Run Minecraft commands

To run Minecraft commands, you can use the `docker compose attach` command to
access the Minecraft server console.

```bash
# Attach to the Minecraft server console
docker compose attach minecraft-server
```

Then, in the Minecraft server console, you can type any Minecraft command, for
example:

```bash
# Say hello to all players
say Hello, players!
```

To detach from the Minecraft server console without stopping the server, press
`Ctrl + P` followed by `Ctrl + Q`.

## Additional resources

- [Minecraft server](https://www.minecraft.net/download/server)
- [Docker Minecraft Server](https://github.com/itzg/docker-minecraft-server)
- [Commands - Minecraft Wiki](https://minecraft.wiki/w/Commands)
