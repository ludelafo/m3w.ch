# `offsite.m3w.ch`

The offsite host is a Linux box, outside of the home network, that stores the
backups of the NAS. Its applications are deployed with Docker by
[Doco-CD](../../apps/doco-cd/README.md), from the
[`.doco-cd.yaml`](./.doco-cd.yaml) file of this directory.

> [!NOTE]
>
> The configuration of this host is not documented yet.

## Install Doco-CD

1. Install Docker (see [Prerequisites](../../README.md#prerequisites)).
2. Create the age key of the host at the `DOCO_CD_SOPS_AGE_KEY_PATH` path of the
   [`.doco-cd.yaml`](./.doco-cd.yaml) file, add its public key to
   [`.sops.yaml`](../../.sops.yaml) and re-encrypt the secrets (see
   [doco-cd](../../apps/doco-cd/README.md#create-the-age-keys)).
3. Bootstrap Doco-CD with `DEPLOY_CONFIG_BASE_DIR=/hosts/offsite.m3w.ch` (see
   [doco-cd](../../apps/doco-cd/README.md#run-the-application-with-docker)).
