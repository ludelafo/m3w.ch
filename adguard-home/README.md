# AdGuard Home

> AdGuard Home is a network-wide software for blocking ads and tracking. After
> you set it up, it'll cover all your home devices, and you won't need any
> client-side software for that.
>
> <https://adguard.com/adguard-home.html>

## Table of contents

- [AdGuard Home](#adguard-home)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
    - [Add MACVLAN bridge](#add-macvlan-bridge)
  - [Run the application with Docker](#run-the-application-with-docker)
  - [Post-configuration](#post-configuration)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the `.env` file to your needs.

### Add MACVLAN bridge

By default, Docker containers using MACVLAN networks and the host cannot
communicate together. We need to add a bridge between the host and the container
to make it work.

Install ifupdown2 on the host with the following command:

```sh
# Install ifupdown2 (Debian)
sudo apt install --yes ifupdown2

# Install ifupdown2 (Alpine Linux)
doas apk add iproute2
```

Update `/etc/network/interfaces` add following lines at the end of the file as
shown below:

```text
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
        address 192.168.1.250
        netmask 255.255.255.0
        gateway 192.168.1.1
        post-up ip link add host_macvlan link eth0 type macvlan mode bridge
        post-up ip link set host_macvlan up
        post-up ip route add 192.168.1.254/32 dev host_macvlan
        post-down ip link del host_macvlan
```

Restart all the network interfaces with the following command:

```sh
# Restart all the network interfaces
sudo ifreload --all
```

Then you can start the AdGuard Home container.

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

On first run, you must access the web interface to configure AdGuard Home at
`192.168.1.254:3000`.

Once the configuration is done, you can access the web interface on the port you
set during the configuration (`192.168.1.254:80` by default).

## Additional resources

- [AdGuard Home](https://adguard.com/adguard-home.html)
- [_"Docker host can’t access containers running on macvlan"_ by Karlo Abaga / 2021-11-05](https://www.networkshinobi.com/docker-host-cant-access-containers-running-on-macvlan/)
- [_Issue with Container/Host to Container/macvlan communication_ by necromancyr\_ / 2020-10-04](https://old.reddit.com/r/docker/comments/j544p8/issue_with_containerhost_to_containermacvlan/)
