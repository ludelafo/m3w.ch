# WireGuard Easy

> The easiest way to run WireGuard VPN + Web-based Admin UI.
>
> <https://github.com/wg-easy/wg-easy>

## Table of contents

- [WireGuard Easy](#wireguard-easy)
  - [Table of contents](#table-of-contents)
  - [Pre-configuration](#pre-configuration)
    - [Set the environment variables](#set-the-environment-variables)
  - [Post-configuration](#post-configuration)
  - [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the values of the stack in [`.doco-cd.yaml`](../../.doco-cd.yaml) to your
needs.

## Post-configuration

On first run, you must access the web interface to configure WireGuard Easy at
`https://${WG_EASY_FQDN}` (e.g. <https://wireguard.m3w.ch>).

Set the right port forwarding rules in your router.

## Additional resources

- [WireGuard](https://www.wireguard.com/)
- [WireGuard Easy](https://github.com/wg-easy/wg-easy)
