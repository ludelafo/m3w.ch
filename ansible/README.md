# Ansible

## Prerequisites

- Debian 12 must be installed on the host.

## Run Ansible playbooks

### On host

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
ansible-pull --url https://github.com/ludelafo/m3w.ch --check ansible/playbooks/host/playbook.yaml [--checkout <name of the branch>]

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/host/playbook.yaml --extra-vars "@.ansible/pull/proxmox.m3w.ch/ansible/variables/proxmox-host.yaml" [--checkout <name of the branch>]
```

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
ansible-pull --url https://github.com/ludelafo/m3w.ch --check ansible/playbooks/host/playbook.yaml [--checkout <name of the branch>]

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch --ask-become-pass ansible/host/playbook.yaml --extra-vars "@.ansible/pull/proxmox.m3w.ch/ansible/variables/common-lxc.yaml" [--checkout <name of the branch>]
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
ansible-pull --url https://github.com/ludelafo/m3w.ch --check ansible/playbooks/lxcs/playbook.yaml [--checkout <name of the branch>]

# Execute Ansible for the second time to apply the configuration
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/lxcs/playbook.yaml --extra-vars "@.ansible/pull/common/ansible/variables/common-lxc.yaml" [--checkout <name of the branch>]
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
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/playbook.yaml --extra-vars "@.ansible/pull/<hostname>/ansible/variables/variables.yaml"

# or
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbook.yaml --extra-vars "user=user user_id=user_id group=group group_id=group_id"

# or
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbook.yaml --extra-vars "{\"user\": \"user\", \"user_id\": user_id, \"group\": \"group\", \"group_id\": group_id}"

# or
ansible-pull --url https://github.com/ludelafo/m3w.ch --checkout <name of the branch> ansible/playbooks/playbook.yaml --extra-vars "@.ansible/pull/<hostname>/ansible/variables/variables.yaml"
```

## On `proxmox.m3w.ch` host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible pull
ansible-pull --url https://github.com/ludelafo/m3w.ch --checkout 5-add-ansible ansible/playbooks/proxmox/playbook.yaml --extra-vars "@.ansible/pull/proxmox.m3w.ch/ansible/variables/home-lxc.yaml"

ansible-pull --url https://github.com/ludelafo/m3w.ch --extra-vars "@.ansible/pull/proxmox.m3w.ch/ansible/variables/ludelafo-lxc.yaml"

ansible-pull --url https://github.com/ludelafo/m3w.ch --extra-vars "@.ansible/pull/proxmox.m3w.ch/ansible/variables/mathilde-lxc.yaml"
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
ansible-pull --url https://github.com/ludelafo/m3w.ch --checkout 5-add-ansible ansible/playbooks/container/playbook.yaml --extra-vars "@.ansible/pull/home.m3w.ch/ansible/variables/home-lxc.yaml"

# Set the password for user
passwd debian

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```

## On ludelafo host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible pull
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/container.yaml --extra-vars "@.ansible/pull/ludelafo.local/ansible/variables/ludelafo.yaml"

# Set the password for user
passwd ludelafo

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```

## On matthieu host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible pull
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/container.yaml --extra-vars "@.ansible/pull/matthieu.local/ansible/variables/matthieu.yaml"

# Set the password for user
passwd matthieu

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```

## On yannis host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible pull
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/container.yaml --extra-vars "@.ansible/pull/yannis.local/ansible/variables/yannis.yaml"

# Set the password for user
passwd yannis

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```

On fonkylan host

```sh
# Fetch the latest package lists
apt update

# Install Ansible and Git
apt install --yes ansible git

# Execute Ansible pull
ansible-pull --url https://github.com/ludelafo/m3w.ch ansible/playbooks/container.yaml --extra-vars "@.ansible/pull/fonkylan.local/ansible/variables/fonkylan.yaml"

# Set the password for user
passwd fonkylan

# Log out and log in again with the new user
logout

# Delete the root home
sudo rm -rf /root
```
