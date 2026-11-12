# resticprofile

> Configuration profiles manager and scheduler for restic backup.
>
> <https://resticprofile.dev>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Set the environment variables](#set-the-environment-variables)
- [Check the configuration](#check-the-configuration)
- [Manual backups](#manual-backups)
- [Additional resources](#additional-resources)

## Pre-configuration

### Set the environment variables

Edit the values of the stack in [`.doco-cd.yaml`](../.doco-cd.yaml) and the
`*.env` files to your needs.

The `*.secrets.env` files contain secrets. They must be encrypted with SOPS
before being committed, see [doco-cd](../doco-cd/README.md#manage-secrets).

## Check the configuration

Replace `<user>` with the user of the instance (e.g. `ludelafo`):

```bash
docker exec -it resticprofile-<user> \
  resticprofile --config /etc/resticprofile/profiles.yaml show
```

## Manual backups

```bash
# Run a backup
docker exec -it resticprofile-<user> \
  resticprofile --config /etc/resticprofile/profiles.yaml backup

# Only print the restic commands that would be run
docker exec -it resticprofile-<user> \
  resticprofile --config /etc/resticprofile/profiles.yaml --dry-run backup

# Scan the files and show what would be backed up, without writing anything
docker exec -it resticprofile-<user> \
  resticprofile --config /etc/resticprofile/profiles.yaml backup --dry-run
```

## Additional resources

- [resticprofile](https://resticprofile.dev)
