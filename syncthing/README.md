# Syncthing

> Syncthing is a continuous file synchronization program. It synchronizes files
> between two or more computers in real time, safely protected from prying eyes.
> Your data is your data alone and you deserve to choose where it is stored,
> whether it is shared with some third party, and how it’s transmitted over the
> internet.
>
> <https://syncthing.net/>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the required directories](#create-the-required-directories)
- [Run the application with Docker](#run-the-application-with-docker)
- [Post-installation](#post-installation)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the required directories

Create the following directories with the right permissions:

```bash
mkdir config data

chown -R user:group config
chown -R user:group data
```

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

## Post-installation

To disable the authentication for the web GUI of Syncthing, you can edit the
`config/config.xml` file and set the following fields:

```xml
    <!-- ... -->
    <gui enabled="true" tls="false" sendBasicAuthPrompt="false">
        <!-- ... -->
        <insecureAdminAccess>true</insecureAdminAccess>
        <password></password>
        <!-- ... -->
    </gui>
```

## Additional resources

- [Syncthing](https://syncthing.net/)
- <https://www.reddit.com/r/Syncthing/comments/ea7krz/any_possibility_to_disable_danger_no_password/>
- <https://github.com/search?q=repo%3Asyncthing%2Fsyncthing+insecureAdminAccess&type=code>
