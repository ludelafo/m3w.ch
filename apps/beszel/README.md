# Beszel

> Beszel is a lightweight server monitoring platform that includes Docker
> statistics, historical data, and alert functions.
>
> <https://beszel.dev>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
- [Post-configuration](#post-configuration)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Refer to [Doco-CD](../doco-cd/README.md) documentation to set the environment
variables.

## Post-configuration

On first start, add a new system in Beszel:

- Name: (Name of the host).
- Host / IP: (IP of the host).
- Port: (leave as default).
- Public Key: (copy and store it in the `beszel_agent.env` file).
- Token: (copy and store it in the `beszel_agent.secrets.env` file).

Access the superuser PocketBase admin panel at `/_/`
(<https://beszel.dev/guide/user-accounts>). Change the Mail settings in the
PocketBase admin panel if needed.

## Additional resources

- [Beszel](https://beszel.dev)
- [Beszel Notifications](https://beszel.dev/guide/notifications/)
