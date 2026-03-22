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
+1024M

# Add a new partition (var)
n

# Set the new partition as a primary partition
p

# Set the partition number
2 (default)

# Set the first sector
2099200 (default)

# Set the last sector (size of 2048 MiB)
+2048M

# Add a new partition (swap)
n

# Set the new partition as a primary partition
p

# Set the partition number
3 (default)

# Set the first sector
6293504 (default)

# Set the last sector (size of 2048 MiB)
+2048M

# Change a partition type
t

# Select root partition
1

# Select partition type (W95 FAT32 (LBA))
0c

# Change a partition type
t

# Select var partition
2

# Select partition type (Linux)
83

# Change a partition type
t

# Select swap partition
3

# Select partition type (Linux swap / Solaris)
82

# Print the partition table
p

# Write table to disk and exit
w
```

```text
sudo fdisk /dev/sdb

Welcome to fdisk (util-linux 2.40.4).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help): o
Created a new DOS (MBR) disklabel with disk identifier 0x87397cca.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-15136767, default 2048): 2048
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-15136767, default 15136767): +1024M

Created a new partition 1 of type 'Linux' and of size 1 GiB.

Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 2
First sector (2099200-15136767, default 2099200): 2099200
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2099200-15136767, default 15136767): +2048M

Created a new partition 2 of type 'Linux' and of size 2 GiB.

Command (m for help): n
Partition type
   p   primary (2 primary, 0 extended, 2 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (3,4, default 3): 3
First sector (6293504-15136767, default 6293504): 6293504
Last sector, +/-sectors or +/-size{K,M,G,T,P} (6293504-15136767, default 15136767): +2048M

Created a new partition 3 of type 'Linux' and of size 2 GiB.

Command (m for help): t
Partition number (1-3, default 3): 1
Hex code or alias (type L to list all): 0c

Changed type of partition 'Linux' to 'W95 FAT32 (LBA)'.

Command (m for help): t
Partition number (1-3, default 3): 2
Hex code or alias (type L to list all): 83

Changed type of partition 'Linux' to 'Linux'.

Command (m for help): t
Partition number (1-3, default 3): 3
Hex code or alias (type L to list all): 82

Changed type of partition 'Linux' to 'Linux swap / Solaris'.

Command (m for help): p
Disk /dev/sdb: 7.22 GiB, 7750025216 bytes, 15136768 sectors
Disk model: TS4 Card Reader
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x87397cca

Device     Boot   Start      End Sectors Size Id Type
/dev/sdb1          2048  2099199 2097152   1G  c W95 FAT32 (LBA)
/dev/sdb2       2099200  6293503 4194304   2G 83 Linux
/dev/sdb3       6293504 10487807 4194304   2G 82 Linux swap / Solaris

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
Disk identifier: 0x87397cca

Device     Boot   Start      End Sectors Size Id Type
/dev/sdb1          2048  2099199 2097152   1G  c W95 FAT32 (LBA)
/dev/sdb2       2099200  6293503 4194304   2G 83 Linux
/dev/sdb3       6293504 10487807 4194304   2G 82 Linux swap / Solaris
```

## Format the partitions

```sh
# Format the root partition
sudo mkfs.msdos -F32 -n root /dev/sdb1

# Format the var partition
sudo mkfs.ext4 -L var /dev/sdb2

# Format the swap partition
sudo mkswap -L swap /dev/sdb3
```

## Extract Alpine Linux to the root partition

```sh
# Move to temporary directory
cd /tmp

# Download Alpine Linux (https://alpinelinux.org/downloads/)
wget https://dl-cdn.alpinelinux.org/alpine/v3.23/releases/aarch64/alpine-rpi-3.23.3-aarch64.tar.gz --output-document alpine-rpi.tar.gz

# Mount root partition
sudo mount /dev/sdb1 /media

# Extract .tar.gz to /media
sudo tar --extract --file alpine-rpi.tar.gz --directory /media

# Unmount root partition
sudo umount /dev/sdb1
```

## Start and configure Alpine Linux

```sh
# Login to the Raspberry Pi 3 with the default credentials (root / no password)

# Setup keyboard
setup-keymap us us

# Setup hostname
setup-hostname raspberry.m3w.ch

# Setup LBU
setup-lbu mmcblk0p1

# Visualize changes
lbu commit -n

# Commit changes
lbu commit

# Setup interfaces
setup-interfaces -r

# Setup Wi-Fi using wlan0 - IP 192.168.1.250 / Netmask 255.255.255.0 / Gateway 192.168.1.1

# Setup DNS (Quad9)
setup-dns -d m3w.ch 9.9.9.9 149.112.112.112

# Setup timezone
setup-timezone -i UTC

# Setup NTP
setup-ntp busybox

# Setup APK repositories
setup-apkrepos -c -1

# Setup APK cache
setup-apkcache /media/mmcblk0p1/cache

# Update packages
apk update
apk upgrade

# Setup SSH
setup-sshd openssh

# Create new user's home
mkdir /home/alpine

# Setup new user
setup-user -a -k https://github.com/ludelafo.keys alpine

# Change user's home permissions
chown -R alpine:alpine /home/alpine

# Add user's home to LBU
lbu include /home/alpine

# Change user password
passwd alpine

# Disable root login
passwd -l root

# Logout as root
exit

# Login as alpine again

# Install utils
doas apk add vim bottom ncdu

# Update fstab to mount the var and swap partitions
doas vim /etc/fstab

# Enable swap on boot
doas rc-update add swap

# Install Docker and Docker Compose
doas apk add docker docker-cli-compose

# Enable Docker on boot
doas rc-update add docker

# Add `alpine` user to Docker group
doas addgroup alpine docker

# Commit changes
doas lbu commit -d

# Reboot the system
doas reboot

# Re-create the `/var/empty` directory after reboot
doas mkdir -p /var/empty
```

```text
UUID=8DD4-F41C                                  /media/mmcblk0p1        vfat    noauto,ro       0       0
UUID=9703c838-3917-4a22-9b7e-75455df4e859       /var                    ext4    defaults        0       0
UUID=091eaa6e-ab8e-4abd-9d87-f8513c451217       none                    swap    defaults        0       0
```

- <https://wiki.alpinelinux.org/wiki/Docker>
- <https://wiki.alpinelinux.org/wiki/Swap>
- <https://wiki.alpinelinux.org/wiki/OpenRC>
