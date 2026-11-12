# m3w.ch

![m3w.ch architecture](./ansible/m3w-architecture.svg)

## Prerequisites

The following prerequisites must be filled to run these services:

- [Docker](https://docs.docker.com/get-docker/) must be installed.
- [Docker Compose](https://docs.docker.com/compose/install/) must be installed
  (it should be installed by default with Docker in most cases).

## Application configuration

The applications are deployed by [Doco-CD](./doco-cd/README.md), which polls
this repository and deploys every stack listed in [`.doco-cd.yaml`](./.doco-cd.yaml).

Each application tries to follow the same structure and configuration:

1. **Set the environment variables**: edit the `*.env` files to your needs.
   Secrets go in the `*.secrets.env` files, encrypted with SOPS (see
   [Manage secrets](./doco-cd/README.md#manage-secrets)).
2. **Add the stack to Doco-CD**: add an entry to `.doco-cd.yaml`, with the
   values of the stack (FQDN, container name, storage paths on the NAS, etc.)
   in its `environment`.
3. **Push the changes**: Doco-CD deploys the application on its next poll.

## Cheatsheet

### Generate a secure password

<https://linux.die.net/man/1/pwgen>

```bash
# Generate a password for computers
pwgen --secure [--capitalize] [--numerals] [-symbols] 20 1

# Generate a password for humans
pwgen --ambiguous [--capitalize] [--numerals] [-symbols] 20 1
```
