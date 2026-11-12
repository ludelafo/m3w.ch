# `nas.m3w.ch`

The NAS runs Debian 13 (trixie) and hosts all the applications of this
repository with Docker (deployed by [Doco-CD](../../apps/doco-cd/README.md)).

This document describes how to configure the host, in order. The configuration
files are stored in the [`etc`](./etc) directory, with the same paths as on the
host: they are copied as is.

## Table of contents

- [Table of contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Set the timezone](#set-the-timezone)
- [Configure the network](#configure-the-network)
- [Configure the updates and packages](#configure-the-updates-and-packages)
- [Configure the encrypted disks](#configure-the-encrypted-disks)
- [Create the users and groups](#create-the-users-and-groups)
- [Install Docker](#install-docker)
- [Apply the boot configuration and reboot](#apply-the-boot-configuration-and-reboot)
- [Check the configuration is still applied](#check-the-configuration-is-still-applied)
- [LUKS cheatsheet](#luks-cheatsheet)
- [Clevis/Tang cheatsheet](#clevistang-cheatsheet)
- [Clevis/Tang setup](#clevistang-setup)
- [Additional resources](#additional-resources)

## Prerequisites

- Debian 13 (trixie) is installed with a `debian` user (UID `1000`) that can use
  `sudo`.
- The host is accessible with SSH.

Clone the repository on the host and go to this directory. All the following
commands are executed from there:

```bash
# Install Git
sudo apt update
sudo apt install --yes git

# Clone the repository
git clone https://github.com/ludelafo/m3w.ch.git ~/m3w.ch

# Go to this directory
cd ~/m3w.ch/hosts/nas.m3w.ch
```

## Set the timezone

```bash
# Set the timezone and the hardware clock to UTC
sudo timedatectl set-timezone UTC
sudo timedatectl set-local-rtc 0
```

Check: `timedatectl` displays `Time zone: UTC` and `RTC in local TZ: no`.

## Configure the network

The NAS has two network interfaces, renamed from their MAC address so their
names never change:

- `nic0` (10 Gbit/s): main interface, static IP `192.168.1.2`.
- `nic1` (2.5 Gbit/s): renamed only, not configured.

The DNS server is AdGuard Home, running on the NAS itself.

```bash
# Rename the network interfaces from their MAC address
sudo install --mode 0644 etc/systemd/network/10-nic0-persistent-link.link /etc/systemd/network/
sudo install --mode 0644 etc/systemd/network/11-nic1-persistent-link.link /etc/systemd/network/

# Configure the static IP address of `nic0`
sudo install --mode 0644 etc/network/interfaces /etc/network/interfaces

# Configure the DNS, hosts and hostname
sudo install --mode 0644 etc/resolv.conf /etc/resolv.conf
sudo install --mode 0644 etc/hosts /etc/hosts
sudo install --mode 0644 etc/hostname /etc/hostname
```

The network must also be configured at boot, before the root disk is unlocked
(to unlock it with Clevis/Tang, see [Clevis/Tang setup](#clevistang-setup)).
Edit `/etc/default/grub` and set the `GRUB_CMDLINE_LINUX` line to:

```text
GRUB_CMDLINE_LINUX="ifname=nic0:6c:1f:f7:56:2f:71 ip=192.168.1.2::192.168.1.1:255.255.255.0:nas:nic0:none:192.168.1.2"
```

The changes are applied at the end, in
[Apply the boot configuration and reboot](#apply-the-boot-configuration-and-reboot).

## Configure the updates and packages

The updates are installed automatically every day with `unattended-upgrades`
(Debian and Debian security updates, except the kernel). The host reboots
automatically at 02:00 when an update needs it.

```bash
# Upgrade all packages and clean up
sudo apt update
sudo apt upgrade --yes
sudo apt autoremove --yes
sudo apt autoclean

# Install and enable unattended-upgrades
sudo apt install --yes unattended-upgrades
echo "unattended-upgrades unattended-upgrades/enable_auto_updates boolean true" | sudo debconf-set-selections
sudo dpkg-reconfigure --frontend noninteractive unattended-upgrades

# Configure unattended-upgrades
sudo install --mode 0644 etc/apt/apt.conf.d/22auto-upgrades-local /etc/apt/apt.conf.d/
sudo install --mode 0644 etc/apt/apt.conf.d/52unattended-upgrades-local /etc/apt/apt.conf.d/
sudo systemctl restart unattended-upgrades

# Install additional packages
sudo apt install --yes git neovim rsync tmux tree
```

Check: `sudo unattended-upgrades --dry-run --debug` lists the allowed origins
and does not report errors.

## Configure the encrypted disks

The two data disks are encrypted with LUKS and unlocked at boot with a key file
stored on the (encrypted) root disk:

| Disk       | LUKS name       | Key file                | Label     | Mount point    |
| ---------- | --------------- | ----------------------- | --------- | -------------- |
| `/dev/sda` | `storage_crypt` | `/etc/luks/storage.key` | `storage` | `/srv/storage` |
| `/dev/sdb` | `backups_crypt` | `/etc/luks/backups.key` | `backups` | `/srv/backups` |

> [!CAUTION]
>
> `luksFormat` and `mkfs` **erase the disk**. Only run them on a new disk. For
> an existing disk, skip them and only add the disk to `/etc/crypttab` and
> `/etc/fstab` (with its existing key file).

For each disk (example with `storage`):

```bash
# Create the key file (once)
sudo mkdir --parents /etc/luks
sudo chmod 0700 /etc/luks
sudo dd if=/dev/urandom of=/etc/luks/storage.key bs=512 count=8
sudo chmod 0400 /etc/luks/storage.key

# Encrypt the disk with the key file (ERASES THE DISK)
sudo cryptsetup luksFormat /dev/sda /etc/luks/storage.key

# Open the encrypted disk
sudo cryptsetup open --key-file /etc/luks/storage.key --allow-discards /dev/sda storage_crypt

# Create the filesystem (ERASES THE DISK)
sudo mkfs.ext4 -L storage /dev/mapper/storage_crypt

# Unlock the disk at boot
echo "storage_crypt /dev/sda /etc/luks/storage.key luks,discard,x-initrd.attach" | sudo tee --append /etc/crypttab

# Mount the disk at boot and now
sudo mkdir --parents /srv/storage
echo "/dev/mapper/storage_crypt /srv/storage ext4 defaults,noatime 0 0" | sudo tee --append /etc/fstab
sudo systemctl daemon-reload
sudo mount /srv/storage
```

Check: `lsblk --fs` displays `storage_crypt` mounted on `/srv/storage` and
`backups_crypt` mounted on `/srv/backups`.

## Create the users and groups

| User       | UID    | Groups                              | SSH keys                              |
| ---------- | ------ | ----------------------------------- | ------------------------------------- |
| `debian`   | `1000` | `debian`, `docker`, `sudo`, `users` | `ludelafo` and `heaspery` GitHub keys |
| `ludelafo` | `1001` | `ludelafo`, `docker`, `users`       | `ludelafo` GitHub keys                |
| `heaspery` | `1002` | `heaspery`, `docker`, `users`       | `heaspery` GitHub keys                |

The `docker` group is created **before** installing Docker, so it has a fixed
GID (`973`). The `users` group (GID `100`) exists by default on Debian.

```bash
# Create the `docker` group with a fixed GID
sudo groupadd --gid 973 docker

# Add the groups to the `debian` user
sudo usermod --append --groups docker,sudo,users debian

# Create the `ludelafo` and `heaspery` users
sudo groupadd --gid 1001 ludelafo
sudo useradd --create-home --uid 1001 --gid ludelafo --groups docker,users --comment "Ludovic Delafontaine" --shell /bin/bash ludelafo

sudo groupadd --gid 1002 heaspery
sudo useradd --create-home --uid 1002 --gid heaspery --groups docker,users --comment "Mathilde Ançay" --shell /bin/bash heaspery
```

Add the SSH keys from GitHub to each user:

```bash
# Add the SSH keys of a GitHub account to a user
add_github_keys() {
  user="$1"
  github_user="$2"
  home=$(getent passwd "$user" | cut -d: -f6)

  sudo install --directory --mode 0700 --owner "$user" --group "$user" "$home/.ssh"
  curl --fail --silent --show-error "https://github.com/$github_user.keys" | sudo tee --append "$home/.ssh/authorized_keys" > /dev/null
  sudo chown "$user:$user" "$home/.ssh/authorized_keys"
  sudo chmod 0600 "$home/.ssh/authorized_keys"
}

add_github_keys debian ludelafo
add_github_keys debian heaspery
add_github_keys ludelafo ludelafo
add_github_keys heaspery heaspery
```

Check: `id debian`, `id ludelafo` and `id heaspery` display the right UIDs and
groups, and each user can log in with SSH.

## Install Docker

Docker is installed from its official APT repository.

```bash
# Download the Docker GPG key and check its checksum
sudo install --directory --mode 0755 /etc/apt/keyrings
sudo curl --fail --silent --show-error --location https://download.docker.com/linux/debian/gpg --output /etc/apt/keyrings/docker.asc
echo "1500c1f56fa9e26b9b8f42452a553675796ade0807cdce11975eb98170b3a570  /etc/apt/keyrings/docker.asc" | sha256sum --check
sudo chmod 0644 /etc/apt/keyrings/docker.asc

# Add the Docker APT repository (update `Suites` when upgrading Debian)
sudo install --mode 0644 etc/apt/sources.list.d/docker.sources /etc/apt/sources.list.d/

# Install Docker with its Compose plugin
sudo apt update
sudo apt install --yes docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Send the containers logs to journald
sudo install --mode 0644 etc/docker/daemon.json /etc/docker/daemon.json

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl restart docker
```

Check: `docker info --format '{{.LoggingDriver}}'` displays `journald`.

## Apply the boot configuration and reboot

```bash
# Apply the GRUB configuration (network at boot)
sudo update-grub

# Apply the network and disks configuration to the initramfs
sudo update-initramfs -u -k all

# Reboot
sudo reboot
```

Check: after the reboot, `ip address` displays `nic0` with `192.168.1.2` and the
disks are mounted (`lsblk --fs`).

The host is ready: install Doco-CD to deploy the applications, see
[doco-cd](../../apps/doco-cd/README.md).

## Check the configuration is still applied

The configuration files of the host can be compared with the ones of this
directory at any time (a difference means the host or the repository must be
updated):

```bash
cd ~/m3w.ch/hosts/nas.m3w.ch

# Compare every file of the `etc` directory with the host
find etc -type f -exec sh -c 'diff --unified "/$1" "$1" > /dev/null || echo "Different: /$1"' _ {} \;
```

## LUKS cheatsheet

### Check LUKS slots

```bash
sudo cryptsetup luksDump /dev/nvme0n1p3
```

```text
Keyslots:
  0: luks2
```

This output means there is one key slot used using LUKS 2.

### Add new LUKS slots

```bash
sudo cryptsetup luksAddKey /dev/nvme0n1p3 [<key file>]
```

### Remove LUKS slots

```bash
sudo cryptsetup luksRemoveKey /dev/nvme0n1p3 [<key file>]
```

### Change LUKS passphrase

```bash
sudo cryptsetup luksChangeKey /dev/nvme0n1p3 [<key file>]
```

## Clevis/Tang cheatsheet

> Clevis is a pluggable framework for automated decryption. It can be used to
> provide automated decryption of data or even automated unlocking of LUKS
> volumes.
>
> <https://github.com/latchset/clevis>

> Tang is a server for binding data to network presence.
>
> This sounds fancy, but the concept is simple. You have some data, but you only
> want it to be available when the system containing the data is on a certain,
> usually secure, network. This is where Tang comes in.
>
> First, the client gets a list of the Tang server's advertised asymmetric keys.
> This can happen online by a simple HTTP GET. Alternatively, since the keys are
> asymmetric, the public key list can be distributed out of band.
>
> Second, the client uses one of these public keys to generate a unique,
> cryptographically strong encryption key. The data is then encrypted using this
> key. Once the data is encrypted, the key is discarded. Some small metadata is
> produced as part of this operation which the client should store in a
> convenient location. This process of encrypting data is the provisioning step.
>
> Third, when the client is ready to access its data, it simply loads the
> metadata produced in the provisioning step and performs an HTTP POST in order
> to recover the encryption key. This process is the recovery step.
>
> <https://github.com/latchset/tang>

## Clevis/Tang setup

On Debian-based systems, install Clevis with the following command:

```bash
# Install required packages
sudo apt install --yes clevis clevis-luks clevis-initramfs
```

### Check Tang keys

On the Tang server, check the keys with the following command:

```bash
# Check Tang keys
tang-show-keys 8080
```

### Bind LUKS volume

To bind LUKS volumes with Clevis and Tang, use the following command on the
client machine. Validate the key from previous section:

```bash
# Bind LUKS volume with Clevis and Tang
sudo clevis luks bind -d /dev/nvme0n1p3 tang '{"url": "http://192.168.1.254:8080"}'
```

### Check LUKS slots

```bash
sudo cryptsetup luksDump /dev/nvme0n1p3
```

```text
Tokens:
  0: clevis
	Keyslot:    0
```

This output means there is one key slot used for Clevis in keyslot 0.

### Unbind LUKS volume

```bash
# Unbind LUKS volume from Clevis and Tang
sudo clevis luks unbind -d /dev/nvme0n1p3 -s 0
```

### Update initramfs

Finally, update the initramfs with the following command:

```bash
# Update initramfs
sudo update-initramfs -u -k 'all'
```

If needed, the content of the generated initramfs can be inspected with the
following commands:

```bash
# Validate the CA certificates are included in initramfs
lsinitramfs "/boot/initrd.img-$(uname -r)" | grep "clevis"
```

## Additional resources

### Main resources

- <https://github.com/latchset/clevis>
- <https://github.com/latchset/tang>
- <https://github.com/padhi-homelab/docker_tang>
- <https://github.com/latchset/clevis/issues/175>
- <https://github.com/francsw/clevis-HTTPS>

### Articles and tutorials

- <https://www.ogselfhosting.com/index.php/2023/12/25/tang-clevis-for-a-luks-encrypted-debian-server/>
- <https://www.tqdev.com/2023-luks-with-https-unlock/>
- <https://blog.haschek.at/2020/the-encrypted-homelab.html>
- <https://www.cyberciti.biz/security/how-to-unlock-luks-using-dropbear-ssh-keys-remotely-in-linux/>

### Posts

- <https://www.reddit.com/r/sysadmin/comments/yu1c2w/unlock_luks_disk_remotely/>
- <https://www.reddit.com/r/sysadmin/comments/1hw2urb/clevis_and_tang/>
- <https://www.reddit.com/r/Fedora/comments/15rl9y7/what_is_the_most_secure_way_to_unlock_luks_full/>
- <https://www.reddit.com/r/linuxadmin/comments/1p0npid/how_to_securely_autodecrypt_luks_on_boot_up/>
- <https://www.reddit.com/r/linuxquestions/comments/dq7xmd/how_luks_encrypted_server_using_remote_network/>
- <https://superuser.com/questions/1916993/how-to-release-renew-ip-address-on-debian-13>
- <https://askubuntu.com/questions/101801/set-up-eth0-network-interface-using-dhcp-in-initramfs>
- <https://unix.stackexchange.com/questions/550021/where-is-the-documentation-for-the-ip-variable-in-initramfs-conf>

### Alternatives

- <https://github.com/johndoe31415/luksrku>
- <https://github.com/gsauthof/dracut-sshd>
- <https://github.com/cloggo/tangd>
- <https://blitiri.com.ar/p/kxd/>

### Miscellaneous

- <https://manpages.debian.org/trixie/initramfs-tools-core/initramfs-tools.7.en.html>
- <https://www.kernel.org/doc/Documentation/filesystems/nfs/nfsroot.txt>
