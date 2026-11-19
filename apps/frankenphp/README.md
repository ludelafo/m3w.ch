# FrankenPHP

> FrankenPHP is a modern application server for PHP built on top of the Caddy
> web server.
>
> <https://frankenphp.dev/>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
- [Create the required directories](#create-the-required-directories)
- [Usage](#usage)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the values of the stack in [`.doco-cd.yaml`](../../.doco-cd.yaml) to your
needs.

## Create the required directories

Create the following directories with the right permissions:

```bash
mkdir public
```

## Usage

Copy the files to host in the `public` directory. They are available at
`https://<FRANKENPHP_FQDN>/<path>`. An `index.html` or `index.php` file is
served when a directory is requested.

The directory is mounted read-only: PHP scripts cannot write to it.

## Additional resources

- [FrankenPHP](https://frankenphp.dev/)
- [FrankenPHP - Docker images](https://frankenphp.dev/docs/docker/)
