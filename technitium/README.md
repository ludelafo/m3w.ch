# Technitium

> Technitium DNS Server is an open source authoritative as well as recursive DNS
> server that can be used for self hosting a DNS server for privacy & security.
> It works out-of-the-box with no or minimal configuration and provides a user
> friendly web console accessible using any modern web browser.
>
> <https://technitium.com/dns/>

## Table of contents

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

- [Technitium](https://technitium.com/dns/)
