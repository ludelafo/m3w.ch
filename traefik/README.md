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
  - [Create the Traefik ACME file](#create-the-traefik-acme-file)
- [Additional resources](#additional-resources)

## Pre-configuration

### Create an Infomaniak API token

Generate an API token on Infomaniak as per:

- <https://doc.traefik.io/traefik/https/acme/#providers>.
- <https://go-acme.github.io/lego/dns/infomaniak/>.

### Set the environment variables

Edit the values of the stack in [`.doco-cd.yaml`](../.doco-cd.yaml), the
`*.env`, the [`traefik_static.yaml`](./config/traefik_static.yaml) and the
[`traefik_dynamic.yaml`](./config/traefik_dynamic.yaml) files to your needs.

The Infomaniak access token (`INFOMANIAK_ACCESS_TOKEN`) and the OIDC values are
stored in the `traefik.secrets.env` file.

### Create the Traefik ACME file

Create a new file called `acme.json` (empty) in the data directory. This file is
used by Traefik to store the ACME certificates obtained from Let's Encrypt.

Make sure it has the right permissions (`0600`) and the right owner
(`root:root`).

## Additional resources

- [Traefik](https://traefik.io/)
