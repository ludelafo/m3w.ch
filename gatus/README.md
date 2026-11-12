# Gatus

> Gatus is a lightweight server monitoring platform that includes Docker
> statistics, historical data, and alert functions.
>
> <https://gatus.dev>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the values of the stack in [`.doco-cd.yaml`](../.doco-cd.yaml) and the
`*.env` files to your needs.

The `*.secrets.env` files contain secrets. They must be encrypted with SOPS
before being committed, see [doco-cd](../doco-cd/README.md#manage-secrets).

## Additional resources

- [Gatus](https://gatus.dev)
