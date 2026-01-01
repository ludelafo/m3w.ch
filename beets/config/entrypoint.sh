#!/usr/bin/env sh

# Install the artistcountry plugin (<https://github.com/agrausem/beets-artistcountry>)
pip install --quiet beets-artistcountry

# Pass arguments to beets
beet "$@"
