#!/usr/bin/env bash
set -euo pipefail

format="$1"
source="$2"
dest="$3"

case "$format" in
  mp3)
    ffmpeg -i "$source" -vn -f wav - | lame -V 0 --noreplaygain - "$dest"
    ;;
  opus)
    ffmpeg -i "$source" -vn -c:a libopus -b:a 128k "$dest"
    ;;
  *)
    echo "Unknown format '$format' (expected 'mp3' or 'opus')" >&2
    exit 1
    ;;
esac
