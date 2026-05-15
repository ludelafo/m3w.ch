# Traefik

> Traefik is a leading modern open source reverse proxy and ingress controller
> that makes deploying services and APIs easy.
>
> <https://traefik.io/>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Create an Infomaniak API token](#create-an-infomaniak-api-token)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the Infomaniak access token secret](#create-the-infomaniak-access-token-secret)
  - [Create the Traefik ACME file](#create-the-traefik-acme-file)
- [Run the application with Docker](#run-the-application-with-docker)
- [Additional resources](#additional-resources)

## Pre-configuration

### Create an Infomaniak API token

Generate an API token on Infomaniak as per:

- <https://doc.traefik.io/traefik/https/acme/#providers>.
- <https://go-acme.github.io/lego/dns/infomaniak/>.

### Set the environment variables

Edit the `.env`, the [`traefik_static.yaml`](./traefik_static.yaml) and the
[`traefik_dynamic.yaml`](./traefik_dynamic.yaml) files to your needs.

### Create the Infomaniak access token secret

Create a new file called `config/infomaniak_access_token.txt` with the
Infomaniak access token. This file is used to authenticate with the Infomaniak
API to manage your DNS records.

Make sure it has the right permissions (`0600`) and the right owner
(`root:root`).

### Create the Traefik ACME file

Create a new file called `config/acme.json` (empty). This file is used by
Traefik to store the ACME certificates obtained from Let's Encrypt.

Make sure it has the right permissions (`0600`) and the right owner
(`root:root`).

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

- [Traefik](https://traefik.io/)
