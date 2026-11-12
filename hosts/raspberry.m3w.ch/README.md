# `raspberry.m3w.ch`

The Raspberry Pi runs Alpine Linux in diskless mode (the system runs from RAM
and is saved to the microSD card with LBU). It hosts the
[Tang](https://github.com/latchset/tang) server used to unlock the NAS at boot
(see [nas.m3w.ch](../nas.m3w.ch/README.md#clevistang-setup)).

This document describes how to configure the host, in order. The configuration
files are stored in the [`etc`](./etc) directory, with the same paths as on the
host: they are copied as is.

> [!IMPORTANT]
>
> Alpine Linux runs in diskless mode: every change outside of the `/var`
> partition is lost at reboot unless it is saved with `doas lbu commit`. The
> `/etc` directory is saved by default, other paths must be added with
> `doas lbu include <path>`.

## Table of contents

- [Table of contents](#table-of-contents)
- [Prepare the microSD card](#prepare-the-microsd-card)
  - [Identify the microSD card](#identify-the-microsd-card)
  - [Unmount all microSD partitions](#unmount-all-microsd-partitions)
  - [Create the partition table for the microSD](#create-the-partition-table-for-the-microsd)
  - [Format the partitions](#format-the-partitions)
  - [Extract Alpine Linux to the root partition](#extract-alpine-linux-to-the-root-partition)
- [Start and configure Alpine Linux](#start-and-configure-alpine-linux)
- [Configure the system](#configure-the-system)
- [Install the Tang server](#install-the-tang-server)
- [Install the Beszel agent](#install-the-beszel-agent)
- [Improve the Wi-Fi stability](#improve-the-wi-fi-stability)
- [Install the watchdog](#install-the-watchdog)
- [Check the configuration is still applied](#check-the-configuration-is-still-applied)
- [Additional resources](#additional-resources)

## Prepare the microSD card

These steps are executed on another computer, with the microSD card inserted.

### Identify the microSD card

```sh
# List all disks to identify the microSD card
sudo fdisk --list
```

```text
Disk /dev/sdb: 7.22 GiB, 7750025216 bytes, 15136768 sectors
Disk model: TS4 Card Reader
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xf2b2a287
```

### Unmount all microSD partitions

```sh
# Ensure all microSD partitions are unmounted
sudo umount --quiet /dev/sdb?*
```

### Create the partition table for the microSD

```sh
# Start fdisk on the microSD card
sudo fdisk /dev/sdb

# Create a new empty MBR (DOS) partition table
o

# Add a new partition (root)
n

# Set the new partition as a primary partition
p

# Set the partition number
1 (default)

# Set the first sector
2048 (default)

# Set the last sector (size of 1024 MiB)
+4096M

# Change a partition type
t

# Select partition type (W95 FAT32 (LBA))
0c

# Print the partition table
p

# Write table to disk and exit
w
```

```text
Welcome to fdisk (util-linux 2.41.4).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): o
Created a new DOS (MBR) disklabel with disk identifier 0x3fefab78.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1):
First sector (2048-15136767, default 2048):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-15136767, default 15136767): +4096M

Created a new partition 1 of type 'Linux' and of size 4 GiB.
Partition #1 contains a vfat signature.

Do you want to remove the signature? [Y]es/[N]o: Y

The signature will be removed by a write command.

Command (m for help): t
Selected partition 1
Hex code or alias (type L to list all): 0c
Changed type of partition 'Linux' to 'W95 FAT32 (LBA)'.

Command (m for help): p
Disk /dev/sdb: 7.22 GiB, 7750025216 bytes, 15136768 sectors
Disk model: TS4 Card Reader
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x3fefab78

Device     Boot Start     End Sectors Size Id Type
/dev/sdb1        2048 8390655 8388608   4G  c W95 FAT32 (LBA)

Filesystem/RAID signature on partition 1 will be wiped.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

```sh
# Display the microSD card
sudo fdisk --list /dev/sdb
```

```text
Disk /dev/sdb: 7.22 GiB, 7750025216 bytes, 15136768 sectors
Disk model: TS4 Card Reader
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x3fefab78

Device     Boot Start     End Sectors Size Id Type
/dev/sdb1        2048 8390655 8388608   4G  c W95 FAT32 (LBA)
```

### Format the partitions

```sh
# Format the root partition
sudo mkfs.msdos -F32 -n root /dev/sdb1
```

### Extract Alpine Linux to the root partition

```sh
# Log in as root
sudo su

# Move to temporary directory
cd /tmp

# Download Alpine Linux (https://alpinelinux.org/downloads/)
wget https://dl-cdn.alpinelinux.org/alpine/v3.23/releases/aarch64/alpine-rpi-3.23.3-aarch64.tar.gz --output-document alpine-rpi.tar.gz

# Mount root partition
mount /dev/sdb1 /media

# Extract .tar.gz to /media
tar --extract --file alpine-rpi.tar.gz --directory /media

# Download headless overlay for Alpine Linux
#
# Source: https://wiki.alpinelinux.org/wiki/Installation_on_a_headless_host#Headless_bootstrap_overlay_file
wget https://github.com/macmpi/alpine-linux-headless-bootstrap/raw/a1320e476585e86a5ddfc3a81311f839d0cd3f93/headless.apkovl.tar.gz --output-document /media/headless.apkovl.tar.gz

# Create the wpa_supplicant configuration file for Wi-Fi connection
wpa_passphrase "mySSID" "myPassPhrase" > /media/wpa_supplicant.conf

# Remove clear passphrase from the wpa_supplicant configuration file
sed -i '/#psk="/d' /media/wpa_supplicant.conf

# Set network interface
tee /media/interfaces >/dev/null <<'EOF'
auto lo
iface lo inet loopback

auto wlan0
iface wlan0 inet static
   address 192.168.1.254
   netmask 255.255.255.0
   gateway 192.168.1.1
EOF

# Unmount root partition
sudo umount /dev/sdb1
```

## Start and configure Alpine Linux

Insert the microSD card in the Raspberry Pi and start it. The headless overlay
connects it to the Wi-Fi with the static IP `192.168.1.254` and starts an SSH
server to log in as `root` (see
[Headless bootstrap overlay](https://github.com/macmpi/alpine-linux-headless-bootstrap)).

The DNS servers are public ones (Quad9), not AdGuard Home: the Raspberry Pi runs
the Tang server used to unlock the NAS at boot, so it must not depend on the
NAS.

```text
# Set up keyboard
KEYMAPOPTS="us us"

# Set up LBU
LBUOPTS="mmcblk0p1"

# Set up hostname
HOSTNAMEOPTS=raspberry.m3w.ch

# Set up network
INTERFACESOPTS="auto lo
iface lo inet loopback

auto wlan0
iface wlan0 inet static
   address 192.168.1.254
   netmask 255.255.255.0
   gateway 192.168.1.1
"

# Set up DNS
DNSOPTS="-d m3w.ch 9.9.9.9 149.112.112.112"

# Set up HTTP/FTP proxy
PROXYOPTS=none

# Set up disk
DISKOPTS=none

# Set up timezone
TIMEZONEOPTS="-i UTC"

# Set up NTP
NTPOPTS="busybox"

# Set up repositories
APKREPOSOPTS="-c -1"

# Set up user
USEROPTS="-a -k https://github.com/ludelafo.keys alpine"

# Set up SSH
SSHDOPTS="openssh"

# Set up APK cache
APKCACHEOPTS="/media/LABEL=root/cache"
```

```sh
# Use the answer file below or run the following commands manually
setup-alpine -f PATH_TO_FILENAME

# Set up keyboard
setup-keymap us us

# Set up hostname
setup-hostname raspberry.m3w.ch

# Set up LBU
setup-lbu mmcblk0p1

# Visualize changes
lbu commit -n

# Commit changes
lbu commit

# Set up interfaces
setup-interfaces -r

# Set up Wi-Fi using wlan0 - IP 192.168.1.254 / Netmask 255.255.255.0 / Gateway 192.168.1.1

# Set up DNS
setup-dns -d m3w.ch 9.9.9.9 149.112.112.112

# Set up timezone
setup-timezone -i UTC

# Set up NTP
setup-ntp busybox

# Set up APK repositories
setup-apkrepos -c -1

# Set up APK cache
setup-apkcache /media/mmcblk0p1/cache

# Update packages
apk update
apk upgrade

# Set up SSH
setup-sshd openssh

# Set up new user
setup-user -a -k https://github.com/ludelafo.keys alpine

# Add user's home to LBU
lbu include /home/alpine

# Change user password
passwd alpine

# Disable root login
passwd -l root

# Remount root partition as read-write
mount -o remount,rw /media/mmcblk0p1

# Remove headless overlay
rm /media/mmcblk0p1/headless.apkovl.tar.gz
rm /media/mmcblk0p1/interfaces
rm /media/mmcblk0p1/wpa_supplicant.conf

# Commit changes
lbu commit -d

# Reboot the system
reboot
```

## Configure the system

Log in as `alpine` with SSH. Install the utilities and clone the repository (all
the following commands are executed from this directory):

```bash
# Install the utilities
doas apk add git ncdu vim

# Clone the repository
git clone https://github.com/ludelafo/m3w.ch.git ~/m3w.ch

# Go to this directory
cd ~/m3w.ch/hosts/raspberry.m3w.ch
```

Configure the hosts and DNS:

```bash
# Add the hostname to /etc/hosts
doas sed -i '/^127\.0\.1\.1/d' /etc/hosts
echo "127.0.1.1 raspberry.m3w.ch raspberry" | doas tee -a /etc/hosts

# Use public DNS servers (independent of the NAS)
doas install -m 0644 etc/resolv.conf /etc/resolv.conf
```

Mount the `/var` and swap partitions of the microSD card at boot:

```bash
# Mount the `/var` partition
echo "UUID=9703c838-3917-4a22-9b7e-75455df4e859 /var ext4 defaults 0 0" | doas tee -a /etc/fstab

# Enable the swap partition
echo "UUID=091eaa6e-ab8e-4abd-9d87-f8513c451217 none swap defaults 0 0" | doas tee -a /etc/fstab
doas rc-update add swap

# Create `/var/empty` (used by OpenSSH, missing on the new `/var` partition)
doas mkdir -p /var/empty
doas chmod 0755 /var/empty
```

Install Docker:

```bash
# Install Docker with its Compose plugin
doas apk add docker docker-cli-compose

# Enable and start Docker
doas rc-update add docker
doas service docker start

# Allow the `alpine` user to use Docker
doas addgroup alpine docker
```

Save the changes:

```bash
doas lbu commit
```

Check: after a reboot, `df -h /var` displays the `/var` partition, `free`
displays the swap and `docker info` works.

## Install the Tang server

Tang is only available in the `testing` repository of Alpine Linux (edge).

```bash
# Add the testing repository
echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" | doas tee -a /etc/apk/repositories

# Install Tang
doas apk add tang@testing

# Configure Tang (listen on all interfaces, port 8080)
doas install -m 0644 etc/conf.d/tang /etc/conf.d/tang

# Enable and start Tang
doas rc-update add tang
doas service tang start

# Save the Tang keys and the changes
doas lbu include /var/lib/tang
doas lbu commit
```

Check: `tang-show-keys 8080` displays the keys (used to bind the NAS disk, see
[nas.m3w.ch](../nas.m3w.ch/README.md#bind-luks-volume)).

## Install the Beszel agent

The agent sends the metrics of the Raspberry Pi to the Beszel Hub
(<https://beszel.m3w.ch>). Add a new system in the Hub to get the `KEY` and
`TOKEN` values.

```bash
# Install the Beszel agent
doas apk add beszel-agent

# Create its data directory
doas mkdir /var/lib/beszel-agent
doas chown beszel-agent:beszel-agent /var/lib/beszel-agent

# Install the service and its configuration
doas install -m 0755 etc/init.d/beszel-agent /etc/init.d/beszel-agent
doas install -m 0644 etc/conf.d/beszel-agent /etc/conf.d/beszel-agent

# Set the `KEY` and `TOKEN` values provided by the Hub (never commit them)
doas vim /etc/conf.d/beszel-agent

# Enable and start the Beszel agent
doas rc-update add beszel-agent
doas service beszel-agent start

# Save the changes
doas lbu include /var/lib/beszel-agent
doas lbu commit
```

Check: the Raspberry Pi is displayed as up in Beszel.

## Improve the Wi-Fi stability

Disable the Wi-Fi roaming and power-saving features of the Raspberry Pi Wi-Fi
driver, which can drop the connection.

```bash
doas install -m 0644 etc/modprobe.d/brcmfmac.conf /etc/modprobe.d/brcmfmac.conf
doas lbu commit
```

The change is applied at the next reboot.

## Install the watchdog

The watchdog reboots the Raspberry Pi when it hangs or when the router
(`192.168.1.1`) cannot be reached on `wlan0` anymore.

```bash
# Install the watchdog
doas apk add watchdog

# Configure the watchdog
doas install -m 0644 etc/conf.d/watchdog /etc/conf.d/watchdog
doas install -m 0644 etc/watchdog.conf /etc/watchdog.conf

# Enable and start the watchdog
doas rc-update add watchdog
doas service watchdog start

# Save the changes
doas lbu commit
```

Check: `doas service watchdog status` displays `started`.

## Check the configuration is still applied

The configuration files of the host can be compared with the ones of this
directory at any time (a difference means the host or the repository must be
updated). `/etc/conf.d/beszel-agent` is always different: its `KEY` and `TOKEN`
values are only set on the host.

```bash
cd ~/m3w.ch/hosts/raspberry.m3w.ch

# Compare every file of the `etc` directory with the host
find etc -type f -exec sh -c 'diff -u "/$1" "$1" > /dev/null || echo "Different: /$1"' _ {} \;
```

## Additional resources

- <https://wiki.alpinelinux.org/wiki/OpenRC>
- <https://wiki.alpinelinux.org/wiki/Repositories#Edge>
- <https://wiki.alpinelinux.org/wiki/Repositories#Upgrading_to_edge>
- <https://gitlab.alpinelinux.org/alpine/aports/-/tree/master/community/beszel>
- <https://github.com/raspberrypi/bookworm-feedback/issues/220>
- <https://github.com/raspberrypi/trixie-feedback/issues/25>
- <https://www.dzombak.com/blog/2023/12/maintaining-a-solid-wifi-connection-on-raspberry-pi/>
- <https://www.dzombak.com/blog/2023/12/mitigating-hardware-firmware-driver-instability-on-the-raspberry-pi/>
