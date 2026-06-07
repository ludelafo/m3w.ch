# Authelia

> Authelia is an open-source authentication and authorization server and portal
> fulfilling the identity and access management (IAM) role of information
> security in providing multi-factor authentication and single sign-on (SSO) for
> your applications via a web portal.
>
> <https://www.authelia.com/>

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

- [Authelia](https://www.authelia.com/)
