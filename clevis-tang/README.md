# Clevis / Tang

> Clevis is a pluggable framework for automated decryption. It can be used to
> provide automated decryption of data or even automated unlocking of LUKS
> volumes.
>
> <https://github.com/latchset/clevis>

> Tang is a server for binding data to network presence.
>
> This sounds fancy, but the concept is simple. You have some data, but you only
> want it to be available when the system containing the data is on a certain,
> usually secure, network. This is where Tang comes in.
>
> First, the client gets a list of the Tang server's advertised asymmetric keys.
> This can happen online by a simple HTTP GET. Alternatively, since the keys are
> asymmetric, the public key list can be distributed out of band.
>
> Second, the client uses one of these public keys to generate a unique,
> cryptographically strong encryption key. The data is then encrypted using this
> key. Once the data is encrypted, the key is discarded. Some small metadata is
> produced as part of this operation which the client should store in a
> convenient location. This process of encrypting data is the provisioning step.
>
> Third, when the client is ready to access its data, it simply loads the
> metadata produced in the provisioning step and performs an HTTP POST in order
> to recover the encryption key. This process is the recovery step.
>
> <https://github.com/latchset/tang>

## Table of contents

- [Clevis / Tang](#clevis--tang)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Run the application with Docker](#run-the-application-with-docker)
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

## Additional resources

- [Clevis](https://github.com/latchset/clevis)
- [Tang](https://github.com/latchset/tang)
- <https://github.com/padhi-homelab/docker_tang>
