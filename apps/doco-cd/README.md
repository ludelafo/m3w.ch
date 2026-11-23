# doco-cd

> Doco-CD is a lightweight GitOps tool that automatically deploys and updates
> Docker Compose projects and Swarm stacks via webhooks or polling when a change
> is pushed to a Git repository.
>
> <https://doco.cd>

## Table of contents

- [Table of contents](#table-of-contents)
- [How it works](#how-it-works)
  - [Hosts and deployment configuration files](#hosts-and-deployment-configuration-files)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the age keys](#create-the-age-keys)
  - [Configure SOPS](#configure-sops)
- [Manage secrets](#manage-secrets)
- [Run the application with Docker](#run-the-application-with-docker)
- [Deploy an application](#deploy-an-application)
  - [Add the application to doco-cd](#add-the-application-to-doco-cd)
- [Test a branch](#test-a-branch)
- [Additional resources](#additional-resources)

## How it works

doco-cd runs on each host and polls this repository every few minutes. When a
new commit is pushed to the polled branch, it:

1. Fetches the new revision into its own read-only copy of the repository (the
   "artifact storage", in `/data`).
2. Decrypts the SOPS-encrypted files (`*.secrets.env`) with the age private key
   of the host.
3. Runs Docker Compose for every application listed in the deployment
   configuration file of the host (see
   [Hosts and deployment configuration files](#hosts-and-deployment-configuration-files)),
   recreating only the containers whose configuration changed.

doco-cd also deploys itself: changes to this directory update doco-cd like any
other application, on every host.

Because each revision is deployed from its own copy of the repository:

- Data must never be stored in a relative bind mount (`./data`): it would be
  lost on the next revision. Applications use absolute paths on the host (e.g.
  `/srv/storage/private/debian/apps/<application>/...` on the NAS), set in the
  deployment configuration file of the host. The Compose files keep relative
  paths as defaults for local development.
- Secrets cannot be edited on the hosts anymore: they are committed encrypted
  with SOPS (see [Manage secrets](#manage-secrets)).

### Hosts and deployment configuration files

Each host runs its own doco-cd instance and reads its own deployment
configuration file, `hosts/<host>/.doco-cd.yaml`, next to the documentation of
the host. The directory is selected by the
[`DEPLOY_CONFIG_BASE_DIR`](https://doco.cd/latest/App-Settings/) app setting of
the instance (the `working_dir` of the stacks stays relative to the root of the
repository):

- [`nas.m3w.ch`](../../hosts/nas.m3w.ch/README.md): reads
  [`hosts/nas.m3w.ch/.doco-cd.yaml`](../../hosts/nas.m3w.ch/.doco-cd.yaml).
- [`offsite.m3w.ch`](../../hosts/offsite.m3w.ch/README.md): reads
  [`hosts/offsite.m3w.ch/.doco-cd.yaml`](../../hosts/offsite.m3w.ch/.doco-cd.yaml).

The app settings that differ between hosts are not in the shared `doco-cd.env`
file: they are set in the deployment configuration file of each host
(`DOCO_CD_DEPLOY_CONFIG_BASE_DIR` and `DOCO_CD_POLL_CONFIG` values of the
doco-cd stack). This way, each instance updates itself with its own settings and
paths.

Each file lists the doco-cd stack of the host first, then the applications of
the host. An application can run on several hosts: add it to each file, with the
values (paths, FQDN, etc.) of each host.

## Pre-configuration

### Set the environment variables

Edit the `doco-cd.env` file to your needs (shared by all the hosts).

Edit the values of the doco-cd stack in the deployment configuration file of the
host (paths, directory of the file in `DOCO_CD_DEPLOY_CONFIG_BASE_DIR` and poll
configuration in `DOCO_CD_POLL_CONFIG`). In particular, set the branch to deploy
from (`main` once the setup is done).

### Create the age keys

Secrets are encrypted with [SOPS](https://getsops.io) using
[age](https://age-encryption.org) keys.

Multiple keys can be used to encrypt the same secret: one for each host and one
for the personal key of the developer. This allows to edit secrets in the
repository without having to store the keys of the hosts on the developer's
computer.

Create a key on each host and each device that needs to read/edit the secrets
(on a host, store it at the `DOCO_CD_SOPS_AGE_KEY_PATH` path of its deployment
configuration file):

```bash
# Create the key pair (the public key is displayed)
age-keygen -o ./apps/doco-cd/secrets/sops_age_key.txt
```

### Configure SOPS

Edit the [`.sops.yaml`](../../.sops.yaml) file at the root of the repository and
add the **public** keys (`age1...`) of every host and developer. The public key
can be displayed again with `age-keygen -y <path to the private key>`.

After adding a key, re-encrypt all the secrets (see
[Manage secrets](#manage-secrets)) and commit them before bootstrapping the new
host: a host can only deploy the applications whose secrets are encrypted for
its key (including doco-cd itself).

## Manage secrets

Secrets are stored in `*.secrets.env` files next to the other `*.env` files of
an application, and loaded with `env_file` in the Compose file. They are
committed **encrypted**: SOPS encrypts the values, the variable names stay
readable.

In the development container (or anywhere with `sops` and the personal key):

```bash
# Encrypt a new secrets file in place (keys come from .sops.yaml)
sops encrypt --in-place apps/my-application/my-application.secrets.env

# Edit an encrypted secrets file (opens the decrypted content in an editor)
sops edit apps/my-application/my-application.secrets.env

# Display the decrypted content
sops decrypt apps/my-application/my-application.secrets.env

# Re-encrypt all the secrets after adding or removing a key in .sops.yaml
sops updatekeys **/*.secrets.env
```

Before committing, check that no secrets file is left unencrypted (this command
must not display anything):

```bash
grep -L 'ENC\[' **/*.secrets.env
```

doco-cd detects the encrypted files by their content and decrypts them with the
key of the host before each deployment. If a file cannot be decrypted (e.g. it
was not encrypted for the key of the host), the deployment of the application
using it fails and the logs of doco-cd name the file.

## Run the application with Docker

Do not forget to set the environment variables and create the age keys as
described in the previous section.

doco-cd is started once with a one-shot bootstrap container. It clones the
repository, deploys every stack of the deployment configuration file of the host
(including doco-cd itself) and exits. Afterwards, doco-cd manages its own stack
from the `compose.yaml` file of this directory.

In a terminal on the host, run the following commands (once per host, never
again). Use the values of the doco-cd stack of the host:

```bash
# Bootstrap doco-cd. Use the same release version as `compose.yaml`
# (https://github.com/kimdre/doco-cd/releases) and the branch to deploy from in
# `reference`. Add other app settings with `-e` as needed (e.g.
# `GIT_ACCESS_TOKEN`).
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v <DOCO_CD_DATA_PATH of the host>:/data \
  -e SELF_UPDATE_ENABLED=true \
  -e DEPLOY_CONFIG_BASE_DIR=/hosts/<host> \
  -e POLL_CONFIG="- url: https://github.com/ludelafo/m3w.ch.git
  reference: main" \
  ghcr.io/kimdre/doco-cd:<replace with the actual version from compose.yaml> apply-self --bootstrap

# Check doco-cd is running and follow the deployments
docker logs --follow doco-cd
```

## Deploy an application

### Add the application to doco-cd

Add a new document (separated by `---`) to the deployment configuration file of
the host (see
[Hosts and deployment configuration files](#hosts-and-deployment-configuration-files)):

```yaml
---
# My application
name: my-application
working_dir: apps/my-application
environment:
  MY_APPLICATION_FQDN: my-application.m3w.ch
  MY_APPLICATION_CONTAINER_NAME: my-application
  MY_APPLICATION_DATA_PATH: /srv/storage/private/debian/apps/my-application/data
```

- `name` is the Compose project name. It cannot be changed once deployed. Do not
  set `name:` in the `compose.yaml` file: doco-cd sets it.
- `environment` sets the values used in the `compose.yaml` file (FQDN, container
  name, absolute paths of the host, etc.), e.g.
  `${MY_APPLICATION_DATA_PATH}:/data`. The `compose.yaml` file has no `.env`
  file and no default values: all the values of the stack are set here.
- Bind mounts of host files (e.g. `/var/run/docker.sock`, `/srv/storage`) keep
  working: they are resolved by Docker on the host.

Commit and push: the application is deployed at the next poll.

## Test a branch

doco-cd only polls `main`, but its
[REST API](https://doco.cd/latest/Endpoints/REST-API/) can deploy any branch on
demand, without changing `POLL_CONFIG` or the deployment configuration files.

The API is not published on the host nor through Traefik: it is only reachable
from inside the network namespace of the doco-cd container. Calling it requires
access to Docker on the host, which already allows to do anything doco-cd can.

The API is enabled by the API key stored in the `doco-cd.secrets.env` file. The
key only allows to trigger polls and read their results (`poll:trigger`,
`runs:read`, `jobs:read`).

Push the branch, then deploy it from a terminal on the host. The doco-cd image
has no shell nor HTTP client: a temporary curl container shares the network of
doco-cd to reach the API on `localhost` (the request waits until the deployment
ends):

```bash
docker run --rm --network container:doco-cd \
  curlimages/curl:8.23.0 \
  --request POST \
  --url 'http://localhost/v1/api/poll/run?wait=true' \
  --header "x-api-key: <api key>" \
  --data '[{"url": "https://github.com/ludelafo/m3w.ch.git", "reference": "<branch>"}]'
```

doco-cd reads the deployment configuration file of the host in the branch and
deploys it like a regular poll. It is a one-off deployment: nothing is changed
in the configuration, so there is nothing to revert. However, the branch stays
deployed until `main` moves on:

- doco-cd never deploys a commit that is an ancestor of the deployed one, to
  avoid going back in time. If the branch was created from the latest `main`,
  the regular polls of `main` are skipped while the branch is deployed.
- Merging the branch (or pushing any other commit to `main`) deploys `main`
  again at the next poll.
- To go back to `main` without merging (e.g. the branch is abandoned), push a
  commit to `main`, even an empty one:

  ```bash
  git commit --allow-empty -m "Redeploy main"
  git push
  ```

- If the branch is behind `main` (commits were pushed to `main` after the branch
  was created), deploying it temporarily removes these commits: the next poll of
  `main` (within 5 minutes) deploys `main` again. Rebase the branch on `main`
  first to test it for longer.
- If the branch changes doco-cd itself, doco-cd updates itself from the branch
  too.

## Additional resources

- [doco-cd](https://doco.cd)
- [doco-cd - Migrating from Docker Compose](https://doco.cd/latest/Migrating-from-Docker-Compose/)
- [doco-cd - Encryption with SOPS](https://doco.cd/latest/Advanced/Encryption/)
- [doco-cd - Self-updating](https://doco.cd/latest/Advanced/Self-Updating/)
- [doco-cd - REST API](https://doco.cd/latest/Endpoints/REST-API/)
- [SOPS](https://getsops.io)
- [age](https://age-encryption.org)
