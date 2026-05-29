# raspberry.m3w.ch

## Identify the microSD card

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

## Unmount all microSD partitions

```sh
# Ensure all microSD partitions are unmounted
sudo umount --quiet /dev/sdb?*
```

## Create the partition table for the microSD

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

## Format the partitions

```sh
# Format the root partition
sudo mkfs.msdos -F32 -n root /dev/sdb1
```

## Extract Alpine Linux to the root partition

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
DNSOPTS="-d m3w.ch 192.168.1.2"

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

# Set up Wi-Fi using wlan0 - IP 192.168.1.250 / Netmask 255.255.255.0 / Gateway 192.168.1.1

# Set up DNS
setup-dns -d m3w.ch 192.168.1.2

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
rm /media/mmcblk0p1/alpine-headless.apkovl.tar.gz
rm /media/mmcblk0p1/interfaces
rm /media/mmcblk0p1/wpa_supplicant.conf

# Commit changes
lbu commit -d

# Reboot the system
reboot

# Add testing repository
echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

doas apk add tang@testing

doas tee /etc/conf.d/tang >/dev/null <<'EOF'
# Tang server configuration

# Listen on all network interfaces
tang_address="0.0.0.0"

# Use default port
tang_port="8080"
EOF

doas rc-update add tang

doas service tang start

doas lbu include /var/lib/tang

doas lbu commit

tang-show-keys 8080

doas apk add beszel-agent

doas mkdir /var/lib/beszel-agent

doas chown beszel-agent:beszel-agent /var/lib/beszel-agent


doas tee /etc/init.d/beszel-agent >/dev/null <<'EOF'
#!/sbin/openrc-run

name="beszel-agent"
description="Beszel Agent Service"
command="/usr/bin/beszel-agent"
command_user="beszel-agent"
command_background="yes"
pidfile="/run/\${RC_SVCNAME}.pid"
output_log="/var/log/beszel-agent/beszel-agent.log"
error_log="/var/log/beszel-agent/beszel-agent.err"

start_pre() {
    checkpath -f -p -m 0644 -o beszel-agent:beszel-agent "\$output_log" "\$error_log"
    checkpath --directory -o beszel-agent:beszel-agent ${pidfile%/*}

    export PORT="$PORT"
    export KEY="$KEY"
    export HUB_URL="$HUB_URL"
    export TOKEN="$TOKEN"
    export EXCLUDE_SMART="$EXCLUDE_SMART"
}

depend() {
    need net
    after firewall
}
EOF

doas tee /etc/conf.d/beszel-agent >/dev/null <<'EOF'
# Disable the SSH server completely (WebSocket connection only).
DISABLE_SSH=true

# URL of the Hub.
HUB_URL="https://beszel.m3w.ch"

# Public SSH key(s) to use for authentication. Provided in Hub.
KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILi8MTmsrveQdtQ9hDfcEmr4tnP4rAsLiB42WA+Fjde5"

# WebSocket registration token. Provided in Hub.
TOKEN="a388a0e1-4063-4e11-a27f-e2c1e7076cb9"

# Exclude S.M.A.R.T. devices from being monitored.
EXCLUDE_SMART=true
EOF

doas lbu include /etc/init.d/beszel-agent
doas lbu include /etc/conf.d/beszel-agent
doas lbu include /var/lib/beszel-agent


doas rc-update add beszel-agent

doas service beszel-agent start

doas lbu ci
```

- <https://wiki.alpinelinux.org/wiki/OpenRC>
- <https://wiki.alpinelinux.org/wiki/Repositories#Edge>
- <https://wiki.alpinelinux.org/wiki/Repositories#Upgrading_to_edge>
- <https://gitlab.alpinelinux.org/alpine/aports/-/tree/master/community/beszel>
