# Beets

> Beets is the media library management system for obsessive music geeks.
>
> <https://beets.io/>

## Table of contents

- [Table of contents](#table-of-contents)
- [Pre-configuration](#pre-configuration)
  - [Get all the API keys and tokens you need](#get-all-the-api-keys-and-tokens-you-need)
  - [Set the environment variables](#set-the-environment-variables)
  - [Create the Beets configuration file](#create-the-beets-configuration-file)
- [Run the application with Docker](#run-the-application-with-docker)
  - [Build the Docker image](#build-the-docker-image)
  - [Login to TIDAL](#login-to-tidal)
  - [Import new items to the library](#import-new-items-to-the-library)
  - [Update the library](#update-the-library)
  - [Write the library](#write-the-library)
  - [Move the library](#move-the-library)
  - [Re-encode the FLAC library](#re-encode-the-flac-library)
  - [Apply ReplayGain to FLAC files](#apply-replaygain-to-flac-files)
  - [Fetch the cover art](#fetch-the-cover-art)
  - [Check and optimize cover art](#check-and-optimize-cover-art)
  - [Calculate the BPM](#calculate-the-bpm)
  - [Fetch the lyrics](#fetch-the-lyrics)
  - [Fetch the LRC files](#fetch-the-lrc-files)
  - [Calculate the key](#calculate-the-key)
  - [Tag the FLAC library with custom tags](#tag-the-flac-library-with-custom-tags)
  - [Clean the FLAC library](#clean-the-flac-library)
  - [Convert the library](#convert-the-library)
  - [Apply ReplayGain to MP3/Opus files](#apply-replaygain-to-mp3opus-files)
- [Additional resources](#additional-resources)

## Pre-configuration

### Get all the API keys and tokens you need

#### MetaBrainz

1. Create an account at <https://metabrainz.org/>.

#### MusicBrainz

1. Create an account at <https://musicbrainz.org/>.

#### Acoustid

1. Create an account at <https://acoustid.org/> (use your MusicBrainz account).
2. Get your API key at <https://acoustid.org/api-key>.
3. Set `ACOUSTID_API_KEY` in `beets.env`.

#### Discogs

1. Create an account at <https://www.discogs.com/>.
2. Get your API key at <https://www.discogs.com/settings/developers>.
3. Set `DISCOGS_USER_TOKEN` in `beets.env`.

#### Fanart.tv

1. Create an account at <https://fanart.tv/>.
2. Get your API key at <https://fanart.tv/get-an-api-key/>.
3. Set `FANARTTV_API_KEY` in `beets.env`.

#### Last.fm

1. Create an account at <https://www.last.fm/>.
2. Get your API key at <https://www.last.fm/api/account/create>.
3. Set `LASTFM_API_KEY` in `beets.env`.

#### Google

1. Create an account at <https://console.cloud.google.com/>.
2. Enable the Google Custom Search API at
   <https://console.cloud.google.com/apis/library/customsearch.googleapis.com>.
3. Create an API key at <https://console.cloud.google.com/apis/credentials>:
   - Name: Beets
   - Select API Restrictions: Custom Search API
   - Application restrictions: None
4. Set `GOOGLE_API_KEY` in `beets.env`.

#### ListenBrainz

1. Create an account at <https://listenbrainz.org/> (use your MusicBrainz
   account).
2. Get your API key at <https://listenbrainz.org/settings/>.
3. Set `LISTENBRAINZ_TOKEN` and `LISTENBRAINZ_USERNAME` in `beets.env`.

### Set the environment variables

Edit the `*.env` files to your needs.

### Create the Beets configuration file

Create a `config` directory with the configuration file(s) needed for Beets. You
can find an example configuration file in the `examples` directory.

## Run the application with Docker

Do not forget to set the environment variables as described in the previous
section.

Recommended order of execution:

1. [Build the Docker image](#build-the-docker-image).
2. [Login to TIDAL](#login-to-tidal).
3. [Import new items to the library](#import-new-items-to-the-library).
4. [Re-encode the FLAC library](#re-encode-the-flac-library).
5. [Apply ReplayGain to FLAC files](#apply-replaygain-to-flac-files).
6. [Fetch the cover art](#fetch-the-cover-art).
7. [Check and optimize cover art](#check-and-optimize-cover-art).
8. [Calculate the BPM](#calculate-the-bpm).
9. [Fetch the lyrics](#fetch-the-lyrics).
10. [Fetch the LRC files](#fetch-the-lrc-files).
11. [Calculate the key](#calculate-the-key).
12. [Tag the FLAC library with custom tags](#tag-the-flac-library-with-custom-tags).
13. [Clean the FLAC library](#clean-the-flac-library).
14. [Convert the library](#convert-the-library).
15. [Apply ReplayGain to MP3/Opus files](#apply-replaygain-to-mp3opus-files).

### Build the Docker image

```bash
# Build the application with Docker
docker compose build
```

### Login to TIDAL

```bash
# Login to TIDAL (only needed once)
docker compose run --rm beets tidal --auth
```

### Import new items to the library

```bash
# Import new items into the library
docker compose run --rm beets import /data/music/.to\ sort
```

### Update the library

```bash
# Update the library with new metadata
docker compose run --rm beets update
```

### Write the library

```bash
# Write the library to disk
docker compose run --rm beets write
```

### Move the library

```bash
# Move the library to a new location (e.g. after changing config.yaml)
docker compose run --rm beets move
```

### Re-encode the FLAC library

```bash
# Re-encode every FLAC already in the library (skips ones already up to date)
docker compose run --rm beets encode [--force] [--pretend]
```

### Apply ReplayGain to FLAC files

```bash
# Apply ReplayGain to the whole existing library (FLAC only, MP3/Opus must be done after conversion)
docker compose run --rm beets replaygain
```

### Fetch the cover art

```bash
# Fetch the cover art for every FLAC already in the library
docker compose run --rm beets fetchart
```

### Check and optimize cover art

```bash
# Warn if a cover is smaller than the target size, resize it down if bigger,
# and optimize every cover already in the library
docker compose run --rm beets cover
```

### Calculate the BPM

```bash
# Calculate the BPM for every FLAC already in the library
docker compose run --rm beets autobpm
```

### Fetch the lyrics

```bash
# Fetch the lyrics for every FLAC already in the library
docker compose run --rm beets lyrics
```

### Fetch the LRC files

```bash
# Fetch the LRC files for every FLAC already in the library
docker compose run --rm beets getlrc
```

### Calculate the key

```bash
# Calculate the key for every FLAC already in the library
docker compose run --rm beets keyfinder
```

### Tag the FLAC library with custom tags

```bash
# Re-apply tags to the whole existing library
docker compose run --rm beets tag [MOOD=chill]
```

### Clean the FLAC library

```bash
# Clean every FLAC already in the library
docker compose run --rm beets clean
```

### Convert the library

```bash
# Convert the library
docker compose run --rm beets convert --album [--format mp3|opus] [--pretend]
```

### Apply ReplayGain to MP3/Opus files

```bash
# Apply ReplayGain to the MP3/Opus library (after conversion)
docker compose run --rm --entrypoint rsgain beets easy [--skip-existing] /data/music/music/MP3|/data/music/music/OPUS
```

## Additional resources

- [Beets](https://beets.io/)
