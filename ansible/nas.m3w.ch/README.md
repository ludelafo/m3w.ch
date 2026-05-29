# nas.m3w.ch

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
