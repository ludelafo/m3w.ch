# qBittorrent

> The qBittorrent project aims to provide an open-source software alternative to
> µTorrent.
>
> <https://www.qbittorrent.org/>

## Table of contents

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

In the qBittorrent web interface, go to "Tools" > "Options" > "Connection" and
set the "Port used for incoming connections" to the value of the port you have
forwarded in your router (default: `52570`).

In the qBittorrent web interface, go to "Tools" > "Options" > "Web UI" and set
the "Username" and "Password" to your desired values (default:
`admin`/`adminadmin`).

In the qBittorrent web interface, go to "Tools" > "Options" > "Web UI" and set
the "Bypass authentication for clients on localhost" option to "Enabled" for the
health check to work.

If using OIDC (Pocket ID), in the qBittorrent web interface, go to "Tools" >
"Options" > "Web UI" and set the "Bypass authentication for clients in
whitelisted IP subnets" option to "0.0.0.0/0" and set the "Enable Cross-Site
Request Forgery (CSRF) protection" option to "Disabled" for the authentication
to work.

## Additional resources

- [qBittorrent](https://www.qbittorrent.org/)
