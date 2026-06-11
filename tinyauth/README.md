# Tinyauth

> Tinyauth is a tiny OpenID Connect (OIDC) authentication and authorization
> server for your self-hosted applications.
>
> <https://tinyauth.app/>

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

As per the Tinyauth documentation (<https://tinyauth.app/docs/guides/ldap/>):

> Tinyauth requires at least two users: an observer user with read-only access
> to the database (used by Tinyauth to search for user DNs) and a normal user
> for logging in to Tinyauth and applications.
>
> After creating the user [in LDAP], select it from the list and scroll to the
> group memberships section. Add the user to the `lldap_strict_readonly` group
> by clicking **Add to Group**.

## Additional resources

- [Tinyauth](https://tinyauth.app/)
