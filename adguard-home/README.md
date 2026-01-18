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
        address 192.168.1.2
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

Add/update the following configuration to the `config/AdGuardHome.yaml` file:

```yaml
user_rules:
  - "## m3w.ch"
  - "||m3w.ch^$dnsrewrite=192.168.1.2,dnstype=~CNAME|~NS|~SOA|~TXT"
  - "## l.m3w.ch"
  - "||l.m3w.ch^$dnsrewrite=192.168.1.3,dnstype=~CNAME|~NS|~SOA|~TXT"
  - "## m.m3w.ch"
  - "||m.m3w.ch^$dnsrewrite=192.168.1.4,dnstype=~CNAME|~NS|~SOA|~TXT"

# ...

dhcp:
  enabled: true
  interface_name: eth0
  local_domain_name: m3w.ch
  dhcpv4:
    gateway_ip: 192.168.1.1
    subnet_mask: 255.255.255.0
    range_start: 192.168.1.11
    range_end: 192.168.1.249
    lease_duration: 86400
    icmp_timeout_msec: 1000
    options:
      - 6 ips 192.168.1.254,192.168.1.254
  dhcpv6:
    range_start: ""
    lease_duration: 86400
    ra_slaac_only: false
    ra_allow_slaac: false
```

## Additional resources

- <https://adguard.com/adguard-home.html>
- <https://github.com/adguardTeam/adGuardHome/wiki/DHCP>
- <https://datatracker.ietf.org/doc/html/rfc2132#section-3.8>
- <https://www.networkshinobi.com/docker-host-cant-access-containers-running-on-macvlan/>
- <https://old.reddit.com/r/docker/comments/j544p8/issue_with_containerhost_to_containermacvlan/>
