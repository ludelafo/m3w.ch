#!/usr/bin/env bash
VARIABLES_TO_REPLACE='
${ACOUSTID_API_KEY}
${DISCOGS_USER_TOKEN}
${FANARTTV_API_KEY}
${GOOGLE_API_KEY}
${LASTFM_API_KEY}
${LISTENBRAINZ_TOKEN}
${LISTENBRAINZ_USERNAME}
'

envsubst "$VARIABLES_TO_REPLACE" < "/config/config.yaml" > "/etc/beets/config.yaml"

beet --config "/etc/beets/config.yaml" "$@"
