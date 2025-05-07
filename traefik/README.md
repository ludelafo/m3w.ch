# Traefik

> Traefik is a leading modern open source reverse proxy and ingress controller
> that makes deploying services and APIs easy.
>
> <https://traefik.io/>

## Prerequisites

The following prerequisites must be filled to run this service:

- [Docker](https://docs.docker.com/get-docker/) must be installed.
- [Docker Compose](https://docs.docker.com/compose/install/) must be installed
  (it should be installed by default with Docker in most cases).

## Set the environment variables

Edit the `.env`, the [`traefik_static.yaml`](./traefik_static.yaml) and the
[`traefik_dynamic.yaml`](./traefik_dynamic.yaml) files to your needs.

Create a new file called `infomaniak_access_token.txt` in this directory and add
your Infomaniak access token in it. This file is used to authenticate with the
Infomaniak API to manage your DNS records.

Related to the previous paragraph, you might need to edit the `compose.yaml`
file if you want to change the Traefik provider environment variables to use
your own DNS provider.

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
