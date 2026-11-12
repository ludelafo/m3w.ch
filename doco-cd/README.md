# doco-cd

> Doco-CD is a lightweight GitOps tool that automatically deploys and updates
> Docker Compose projects and Swarm stacks via webhooks or polling when a change
> is pushed to a Git repository.
>
> <https://doco.cd>

## Table of contents

- [Table of contents](#table-of-contents)
- [How it works](#how-it-works)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the age keys](#create-the-age-keys)
  - [Configure SOPS](#configure-sops)
- [Manage secrets](#manage-secrets)
- [Run the application with Docker](#run-the-application-with-docker)
- [Deploy an application](#deploy-an-application)
  - [Add the application to doco-cd](#add-the-application-to-doco-cd)
- [Additional resources](#additional-resources)

## How it works

doco-cd runs on the NAS and polls this repository every few minutes. When a new
commit is pushed to the polled branch, it:

1. Fetches the new revision into its own read-only copy of the repository (the
   "artifact storage", in `/data`).
2. Decrypts the SOPS-encrypted files (`*.secrets.env`) with the age private key
   of the NAS.
3. Runs Docker Compose for every application listed in the
   [`.doco-cd.yaml`](../.doco-cd.yaml) file, recreating only the containers
   whose configuration changed.

doco-cd also deploys itself: changes to this directory update doco-cd like any
other application.

Because each revision is deployed from its own copy of the repository:

- Data must never be stored in a relative bind mount (`./data`): it would be
  lost on the next revision. Applications use absolute paths on the NAS
  (`/srv/storage/private/debian/apps/<application>/...`), set in the
  `.doco-cd.yaml` file. The Compose files keep relative paths as defaults for
  local development.
- Secrets cannot be edited on the NAS anymore: they are committed encrypted with
  SOPS (see [Manage secrets](#manage-secrets)).

## Pre-configuration

### Set the environment variables

Edit the `doco-cd.env` file to your needs. In particular, set the branch to
deploy from in `POLL_CONFIG` (`main` once the setup is done).

### Create the age keys

Secrets are encrypted with [SOPS](https://getsops.io) using
[age](https://age-encryption.org) keys.

Multiple keys can be used to encrypt the same secret: one for the NAS and one
for the personal key of the developer. This allows to edit secrets in the
repository without having to store the NAS key on the developer's computer.

Create the personal key on each device that needs to read/edit the secrets:

```bash
# Create the key pair (the public key is displayed)
age-keygen -o ./doco-cd/secrets/sops_age_key.txt
```

### Configure SOPS

Edit the [`.sops.yaml`](../.sops.yaml) file at the root of the repository and
replace the placeholders with the two **public** keys (`age1...`). The public
key can be displayed again with `age-keygen -y <path to the private key>`.

## Manage secrets

Secrets are stored in `*.secrets.env` files next to the other `*.env` files of
an application, and loaded with `env_file` in the Compose file. They are
committed **encrypted**: SOPS encrypts the values, the variable names stay
readable.

In the development container (or anywhere with `sops` and the personal key):

```bash
# Encrypt a new secrets file in place (keys come from .sops.yaml)
sops encrypt --in-place my-application/my-application.secrets.env

# Edit an encrypted secrets file (opens the decrypted content in an editor)
sops edit my-application/my-application.secrets.env

# Display the decrypted content
sops decrypt my-application/my-application.secrets.env

# Re-encrypt all the secrets after adding or removing a key in .sops.yaml
sops updatekeys **/*.secrets.env
```

Before committing, check that no secrets file is left unencrypted (this command
must not display anything):

```bash
grep -L 'ENC\[' **/*.secrets.env
```

doco-cd detects the encrypted files by their content and decrypts them with the
NAS key before each deployment. If a file cannot be decrypted (e.g. it was not
encrypted for the NAS key), the deployment of the application using it fails and
the logs of doco-cd name the file.

## Run the application with Docker

Do not forget to set the environment variables and create the age keys as
described in the previous section.

doco-cd is started once with a one-shot bootstrap container. It clones the
repository, deploys every stack of the `.doco-cd.yaml` file (including doco-cd
itself) and exits. Afterwards, doco-cd manages its own stack from the
`compose.yaml` file of this directory.

In a terminal on the NAS, run the following commands (once per host, never
again):

```bash
# Bootstrap doco-cd. Use the same release version as `compose.yaml`
# (https://github.com/kimdre/doco-cd/releases) and the branch to deploy from in
# `reference`. Add other app settings with `-e` as needed (e.g.
# `GIT_ACCESS_TOKEN`).
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /srv/storage/private/debian/apps/doco-cd/data:/data \
  -e SELF_UPDATE_ENABLED=true \
  -e POLL_CONFIG="- url: https://github.com/ludelafo/m3w.ch.git
  reference: main" \
  ghcr.io/kimdre/doco-cd:<replace with the actual version from compose.yaml> apply-self --bootstrap

# Check doco-cd is running and follow the deployments
docker logs --follow doco-cd
```

## Deploy an application

### Add the application to doco-cd

Add a new document (separated by `---`) to the `.doco-cd.yaml` file:

```yaml
---
# My application
name: my-application
working_dir: my-application
environment:
  MY_APPLICATION_FQDN: my-application.m3w.ch
  MY_APPLICATION_CONTAINER_NAME: my-application
  MY_APPLICATION_DATA_PATH: /srv/storage/private/debian/apps/my-application/data
```

- `name` is the Compose project name. It cannot be changed once deployed. Do not
  set `name:` in the `compose.yaml` file: doco-cd sets it.
- `environment` sets the values used in the `compose.yaml` file (FQDN, container
  name, absolute paths of the NAS, etc.), e.g.
  `${MY_APPLICATION_DATA_PATH}:/data`. The `compose.yaml` file has no `.env`
  file and no default values: all the values of the stack are set here.
- Bind mounts of host files (e.g. `/var/run/docker.sock`, `/srv/storage`) keep
  working: they are resolved by Docker on the NAS.

Commit and push: the application is deployed at the next poll.

## Additional resources

- [doco-cd](https://doco.cd)
- [doco-cd - Migrating from Docker Compose](https://doco.cd/latest/Migrating-from-Docker-Compose/)
- [doco-cd - Encryption with SOPS](https://doco.cd/latest/Advanced/Encryption/)
- [doco-cd - Self-updating](https://doco.cd/latest/Advanced/Self-Updating/)
- [SOPS](https://getsops.io)
- [age](https://age-encryption.org)
