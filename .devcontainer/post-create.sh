#!/usr/bin/env sh

## Configure Bash aliases
tee -a ~/.bash_aliases > /dev/null <<"EOF"
alias tree='tree --dirsfirst -A -F'
EOF

## Install required packages
# Update packages list
sudo apt update

# Install packages to optimize images (jpegoptim, optipng)
sudo apt install --yes jpegoptim optipng

# Install packages to optimize documents (ps2pdf)
sudo apt install --yes ghostscript
