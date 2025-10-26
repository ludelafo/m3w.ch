# Ansible

## Prerequisites

- Debian 12 must be installed on the host.

## `proxmox.m3w.ch` host

### Configure host with Ansible

Install Ansible and Git:

```sh
# Update the package lists
apt update

# Install packages
apt install --yes ansible git
```

Execute Ansible:

```sh
# Execute Ansible for the first time to pull the files
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/host/playbook.yaml --check [--checkout <name of the branch>]

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/proxmox.m3w.ch/playbook.yaml --extra-vars "@~/.ansible/pull/proxmox.m3w.ch/ansible/proxmox.m3w.ch/variables.yaml" [--checkout <name of the branch>]
```

## `common.m3w.ch` host

### Create the virtual machine within Proxmox

Create the following virtual machine within Proxmox:

- **General**:
  - Node: `proxmox`
  - VM ID: `100`
  - Name: `common`
  - Start at boot: `checked`
- **OS**:
  - Storage: `local`
  - ISO image: `debian-13.1.0-amd64-netinst.iso`
- **System**:
  - Graphic card: `Default`
  - Machine: `q35`
  - SCSI Controller: `VirtIO SCSI single`
  - BIOS: `OVMF (UEFI)`
  - Add EFI Disk: `checked`
  - EFI Storage: `local`
  - Format: `QEMU image format (qcow2)`
  - Pre-Enroll keys: `checked`
- **Disks**:
  - Bus/Device: `SATA0`
  - Storage: `local`
  - Size size (GiB): `10`
  - Format: `QEMU image format`
  - Backup: `unchecked`
- **CPU**:
  - Socket: `1`
  - Cores: `2`
  - Type: `host`
- **Memory**:
  - Memory (MiB): `4096`
  - Minimum memory (MiB): `4096`
  - Ballooning Device: `checked`
- **Network**:
  - _Leave all by default_
- **Confirm**:
  - Start after created: `unchecked`

## `ludelafo.m3w.ch` host

### Create the virtual machine within Proxmox

Create the following virtual machine within Proxmox:

- **General**:
  - Node: `proxmox`
  - VM ID: `101`
  - Name: `ludelafo`
  - Start at boot: `checked`
- **OS**:
  - Storage: `local`
  - ISO image: `debian-13.1.0-amd64-netinst.iso`
- **System**:
  - Graphic card: `Default`
  - Machine: `q35`
  - SCSI Controller: `VirtIO SCSI single`
  - BIOS: `OVMF (UEFI)`
  - Add EFI Disk: `checked`
  - EFI Storage: `local`
  - Format: `QEMU image format (qcow2)`
  - Pre-Enroll keys: `checked`
- **Disks**:
  - Bus/Device: `SATA0`
  - Storage: `local`
  - Size size (GiB): `10`
  - Format: `QEMU image format`
  - Backup: `unchecked`
- **CPU**:
  - Socket: `1`
  - Cores: `2`
  - Type: `host`
- **Memory**:
  - Memory (MiB): `4096`
  - Minimum memory (MiB): `4096`
  - Ballooning Device: `checked`
- **Network**:
  - _Leave all by default_
- **Confirm**:
  - Start after created: `unchecked`

## `mathilde.m3w.ch` host

### Create the virtual machine within Proxmox

Create the following virtual machine within Proxmox:

- **General**:
  - Node: `proxmox`
  - VM ID: `102`
  - Name: `common`
  - Start at boot: `checked`
- **OS**:
  - Storage: `local`
  - ISO image: `debian-13.1.0-amd64-netinst.iso`
- **System**:
  - Graphic card: `Default`
  - Machine: `q35`
  - SCSI Controller: `VirtIO SCSI single`
  - BIOS: `OVMF (UEFI)`
  - Add EFI Disk: `checked`
  - EFI Storage: `local`
  - Format: `QEMU image format (qcow2)`
  - Pre-Enroll keys: `checked`
- **Disks**:
  - Bus/Device: `SATA0`
  - Storage: `local`
  - Size size (GiB): `10`
  - Format: `QEMU image format`
  - Backup: `unchecked`
- **CPU**:
  - Socket: `1`
  - Cores: `2`
  - Type: `host`
- **Memory**:
  - Memory (MiB): `4096`
  - Minimum memory (MiB): `4096`
  - Ballooning Device: `checked`
- **Network**:
  - _Leave all by default_
- **Confirm**:
  - Start after created: `unchecked`

### Finalize Proxmox configuration for the virtual machine with Ansible

These steps must be executed on the `proxmox.m3w.ch` host to finalize the
virtual machine configuration before the first boot.

```sh
# Execute Ansible to finalize the configuration of the virtual machine on Proxmox
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/proxmox.m3w.ch/playbook.yaml --extra-vars "@~/.ansible/pull/proxmox.m3w.ch/ansible/mathilde.m3w.ch/variables.yaml" [--checkout <name of the branch>]
```

This will add the disk to the virtual machine.

### Install the operating system

Start the Proxmox virtual machine and install the operating system.

### Configure the virtual machine with Ansible

Install Ansible and Git:

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git
```

Execute Ansible:

```sh
# Execute Ansible for the first time to pull the files
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/mathilde.m3w.ch/playbook.yaml --check [--checkout <name of the branch>]

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/mathilde.m3w.ch/playbook.yaml --extra-vars "@~/.ansible/pull/mathilde.m3w.ch/ansible/mathilde.m3w.ch/variables.yaml" [--checkout <name of the branch>]

# Set the password for user
passwd mathilde

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```

# OLD DOCUMENTATION

## Run Ansible playbooks

### On `proxmox.m3w.ch`

Access Proxmox and create a LXC container:

- General
  - Node: `proxmox`
  - CT ID: `100`
  - Hostname: `common`
  - Unprivileged: `unchecked`
  - Nested: `unchecked`
  - SSH public key(s): `*`
- Template
  - Storage: `local`
  - Template: `debian`
- Disks
  - Storage: `local`
  - Size: `8GiB`
- CPU
  - Cores: `2`
- Memory:
  - Memory: `8192 MiB`
  - Swap: `8192 MiB`
- Network
  - IPv4:
    - IP: `192.168.1.2/24`
    - Gateway: `192.168.1.1`
  - IPv6: `None`
- DNS
  - DNS domain: `use host settings`
  - DNS servers: `use host settings`
- Confirm
  - Start after created: `unchecked`

Execute Ansible:

```sh
# Execute Ansible for the first time to pull the files
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/host/playbook.yaml [--checkout <name of the branch>] --check

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/host/playbook.yaml --extra-vars "@~/.ansible/pull/proxmox.m3w.ch/ansible/variables/common-ct.yaml" [--checkout <name of the branch>]
```

### On `common` LXC container

Install Ansible and Git:

```sh
# Update the package lists
apt update

# Install packages
apt install --yes ansible git
```

Execute Ansible:

```sh
# Execute Ansible for the first time to pull the files
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/lxcs/playbook.yaml [--checkout <name of the branch>] --check

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/lxcs/playbook.yaml --extra-vars "@~/.ansible/pull/common/ansible/variables/common-ct.yaml" [--checkout <name of the branch>]
```

## Generic configuration

```sh
# Fetch the latest package lists
apt update

# Install updates
apt upgrade --yes

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible pull
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/playbook.yaml --extra-vars "@~/.ansible/pull/<hostname>/ansible/variables/variables.yaml"

# or
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbook.yaml --extra-vars "user=user user_id=user_id group=group group_id=group_id"

# or
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbook.yaml --extra-vars "{\"user\": \"user\", \"user_id\": user_id, \"group\": \"group\", \"group_id\": group_id}"

# or
ansible-pull --url https://github.com/ludelafo/m3w.ch --checkout <name of the branch> ansible/playbooks/playbook.yaml --extra-vars "@~/.ansible/pull/<hostname>/ansible/variables/variables.yaml"
```

## On `proxmox.m3w.ch` host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible pull
ansible-pull --url https://github.com/ludelafo/m3w.ch --checkout 5-add-ansible ansible/playbooks/proxmox/playbook.yaml --extra-vars "@~/.ansible/pull/proxmox.m3w.ch/ansible/variables/home-ct.yaml"

ansible-pull --url https://github.com/ludelafo/m3w.ch --extra-vars "@~/.ansible/pull/proxmox.m3w.ch/ansible/variables/ludelafo-ct.yaml"

ansible-pull --url https://github.com/ludelafo/m3w.ch --extra-vars "@~/.ansible/pull/proxmox.m3w.ch/ansible/variables/mathilde-ct.yaml"
```

## On `home.m3w.ch` host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Configure Git to store credentials
git config --global credential.helper store

# Clone the repository a first time
git clone https://github.com/ludelafo/m3w.ch

# Execute Ansible pull for the first time to pull the files
ansible-pull --url https://github.com/ludelafo/m3w.ch --checkout 5-add-ansible ansible/playbooks/container/playbook.yaml

# Execute Ansible pull for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch --checkout 5-add-ansible ansible/playbooks/container/playbook.yaml --extra-vars "@~/.ansible/pull/home.m3w.ch/ansible/variables/home-ct.yaml"

# Set the password for user
passwd debian

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```

## On `ludelafo.m3w.ch` host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible for the first time to pull the files
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/ludelafo.m3w.ch/playbook.yaml [--checkout <name of the branch>] --check

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/ludelafo.m3w.ch/playbook.yaml [--checkout <name of the branch>] --extra-vars "@~/.ansible/pull/ludelafo.m3w.ch/ansible/ludelafo.m3w.ch/variables.yaml"

# Set the password for user
passwd ludelafo

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```
