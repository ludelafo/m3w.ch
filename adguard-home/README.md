# AdGuard Home

> AdGuard Home is a network-wide software for blocking ads and tracking. After
> you set it up, it'll cover all your home devices, and you won't need any
> client-side software for that.
>
> <https://adguard.com/adguard-home.html>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
- [Post-configuration](#post-configuration)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the values of the stack in [`.doco-cd.yaml`](../.doco-cd.yaml) to your
needs.

## Post-configuration

On first run, you must access the web interface to configure AdGuard Home at
`<ip of the host>:3000`.

Once the configuration is done, you can access the web interface on the port you
set during the configuration (`<ip of the host>:8053` by default).

Add/update the following configuration to the `config/AdGuardHome.yaml` file:

```yaml
# ...

user_rules:
  - "## m3w.ch"
  - "||m3w.ch^$dnsrewrite=192.168.1.2,dnstype=~CNAME|~NS|~SOA|~TXT"

# ...

dhcp:
  enabled: true
  interface_name: nic0
  local_domain_name: m3w.ch
  dhcpv4:
    gateway_ip: 192.168.1.1
    subnet_mask: 255.255.255.0
    range_start: 192.168.1.11
    range_end: 192.168.1.249
    lease_duration: 86400
    icmp_timeout_msec: 1000
    options:
      - 6 ips 192.168.1.2,192.168.1.2
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
