# Homepage

> A modern, fully static, fast, secure fully proxied, highly customizable
> application dashboard with integrations for over 100 services and translations
> into multiple languages. Easily configured via YAML files or through docker
> label discovery.
>
> <https://gethomepage.dev/>

## Table of contents

- [Homepage](#homepage)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Post-configuration](#post-configuration)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `.env` file to your needs.

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

To generate the configuration files, you must access the web interface at least
one. The files will then be generated in the `config` directory if not already
present.

## Additional resources

- [Homepage](https://gethomepage.dev/>)
