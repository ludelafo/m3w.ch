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
- [Post-configuration](#post-configuration)
  - [Create a read-only user in LDAP](#create-a-read-only-user-in-ldap)
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

## Post-configuration

### Create a read-only user in LDAP

Create a new user in LDAP with `lldap_password_manager` permissions. This user
will be used by Authelia to query the LDAP directory for authentication and
authorization purposes and allow users to update their passwords.

## Additional resources

- [Authelia](https://www.authelia.com/)
