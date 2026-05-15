# Scrutiny

> Scrutiny is a Hard Drive Health Dashboard & Monitoring solution, merging
> manufacturer provided S.M.A.R.T metrics with real-world failure rates.
>
> <https://github.com/Starosdev/scrutiny>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
  - [Map the device mount points](#map-the-device-mount-points)
- [Run the application with Docker](#run-the-application-with-docker)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Map the device mount points

In order to make performance benchmarks, devices must be mounted in the
container as described in the `compose.yaml`, `collector.yaml`,
`collector-performance.yaml` files.

You can make symlinks to the real device mount points in the `devices` directory
matching the ones in the files mentioned above.

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

- [Scrutiny](https://github.com/Starosdev/scrutiny)
