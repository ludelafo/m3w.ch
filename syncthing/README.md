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
- [Post-installation](#post-installation)
  - [Set the sync protocol listen address](#set-the-sync-protocol-listen-address)
  - [Forward the sync port on the router](#forward-the-sync-port-on-the-router)
  - [Disable the web GUI authentication](#disable-the-web-gui-authentication)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the values of the stack in [`.doco-cd.yaml`](../.doco-cd.yaml) and the
`*.env` files to your needs.

### Create the required directories

Create the following directories with the right permissions:

```bash
mkdir config data

chown -R user:group config
chown -R user:group data
```

## Post-installation

### Set the sync protocol listen address

Syncthing announces the port it listens on to the other devices. The published
port (`SYNCTHING_PORT`) is the same inside and outside the container, so
Syncthing must listen on that port too.

If `SYNCTHING_PORT` is not `22000` (e.g. `22001` for a second instance), go to
**Settings > Connections** in the web GUI and set the **Sync Protocol Listen
Addresses** to:

```text
tcp://:22001, quic://:22001
```

Until this is done, the devices cannot connect directly to this instance and
fall back to relays.

### Forward the sync port on the router

Forward `SYNCTHING_PORT` (TCP and UDP) from the router to the NAS, with the same
port on both sides (e.g. `22001` to `22001`).

This is recommended but not required: without it, devices outside the local
network connect through the public relays (slower). Devices on the local
network do not need it.

Syncthing cannot open the port itself (UPnP/NAT-PMP does not work from a Docker
bridge network), so the rule must be added manually. Nothing needs to be done on
the NAS firewall: Docker opens the published ports itself.

### Disable the web GUI authentication

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
