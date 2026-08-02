"""Strip FLAC/MP3/Opus files down to a fixed set of blocks and tags."""

import concurrent.futures
import os
import subprocess
import time

from mutagen import MutagenError
from mutagen.id3 import ID3
from mutagen.oggopus import OggOpus

from beets import ui
from beets.plugins import BeetsPlugin
from beets.util import syspath


class CleanPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.config.add(
            {
                "auto": True,
                "threads": os.cpu_count() or 1,
                "metaflac_command_path": "metaflac",
                "arguments": [
                    "--remove",
                    "--dont-use-padding",
                    "--block-type=APPLICATION",
                    "--block-type=CUESHEET",
                    "--block-type=PADDING",
                    "--block-type=PICTURE",
                    "--block-type=SEEKTABLE",
                ],
                "tags_to_keep": [
                    "ALBUM",
                    "ALBUMARTIST",
                    "ARTIST",
                    "COMMENT",
                    "COMPOSER",
                    "DISCNUMBER",
                    "FLAC_ARGUMENTS",
                    "GENRE",
                    "LYRICS",
                    "METAFLAC_ARGUMENTS",
                    "PERFORMER",
                    "REPLAYGAIN_REFERENCE_LOUDNESS",
                    "REPLAYGAIN_ALBUM_GAIN",
                    "REPLAYGAIN_ALBUM_PEAK",
                    "REPLAYGAIN_TRACK_GAIN",
                    "REPLAYGAIN_TRACK_PEAK",
                    "TITLE",
                    "TOTALDISCS",
                    "TOTALTRACKS",
                    "TRACKNUMBER",
                    "YEAR",
                ],
                "opus_tags_to_keep": [
                    "ALBUM",
                    "ALBUMARTIST",
                    "ARTIST",
                    "COMMENT",
                    "COMPOSER",
                    "DISCNUMBER",
                    "GENRE",
                    "LYRICS",
                    "PERFORMER",
                    "REPLAYGAIN_REFERENCE_LOUDNESS",
                    "REPLAYGAIN_ALBUM_GAIN",
                    "REPLAYGAIN_ALBUM_PEAK",
                    "REPLAYGAIN_TRACK_GAIN",
                    "REPLAYGAIN_TRACK_PEAK",
                    "TITLE",
                    "TOTALDISCS",
                    "TOTALTRACKS",
                    "TRACKNUMBER",
                    "YEAR",
                ],
                "mp3_frames_to_keep": [
                    "COMM",
                    "TALB",
                    "TBPM",
                    "TCOM",
                    "TCON",
                    "TDRC",
                    "TIT2",
                    "TKEY",
                    "TPE1",
                    "TPE2",
                    "TPOS",
                    "TRCK",
                    "USLT",
                ],
                "mp3_txxx_to_keep": [
                    "ACOUSTID_FINGERPRINT",
                    "ACOUSTID_ID",
                    "MUSICBRAINZ_ALBUMARTISTID",
                    "MUSICBRAINZ_ALBUMID",
                    "MUSICBRAINZ_ARTISTID",
                    "MUSICBRAINZ_RELEASEGROUPID",
                    "MUSICBRAINZ_RELEASETRACKID",
                    "MUSICBRAINZ_TRACKID",
                    "MUSICBRAINZ_WORKID",
                    "REPLAYGAIN_REFERENCE_LOUDNESS",
                    "REPLAYGAIN_ALBUM_GAIN",
                    "REPLAYGAIN_ALBUM_PEAK",
                    "REPLAYGAIN_TRACK_GAIN",
                    "REPLAYGAIN_TRACK_PEAK",
                ],
            }
        )

        if self.config["auto"].get(bool):
            self.register_listener("item_imported", self.on_item_imported)
            self.register_listener("album_imported", self.on_album_imported)

        # Unlike the FLAC listeners above, this isn't gated behind `auto`:
        # converted MP3/Opus files are usually not library items (e.g. when
        # `convert.keep_new` is off), so there is no `beets clean`-style
        # command that could reach them afterwards. Cleaning has to happen
        # as part of the convert step itself, whether that step is run
        # manually or automatically.
        self.register_listener("after_convert", self.on_after_convert)

    def commands(self):
        cmd = ui.Subcommand(
            "clean",
            help="strip FLAC files to the configured blocks and tags",
        )

        def func(lib, opts, args):
            self._run_parallel(lib.items(ui.decargs(args)), self.process_item)

        cmd.func = func
        return [cmd]

    def on_item_imported(self, lib, item):
        self.process_item(item)

    def on_album_imported(self, lib, album):
        self._run_parallel(album.items(), self.process_item)

    def on_after_convert(self, item, dest, keepnew):
        path = syspath(dest)
        if isinstance(path, bytes):
            path = path.decode()

        extension = os.path.splitext(path)[1].lower()
        if extension == ".mp3":
            self.clean_mp3(path)
        elif extension == ".opus":
            self.clean_opus(path)

    def process_item(self, item):
        if item.format != "FLAC":
            return
        self.clean(item)

    def _run_parallel(self, items, func):
        threads = self.config["threads"].get(int)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=threads
        ) as executor:
            futures = [executor.submit(func, item) for item in items]
            for future in concurrent.futures.as_completed(futures):
                future.result()

    def _run(self, argv, retries=3, retry_delay=0.2):
        # Under concurrent access, metaflac can transiently report a
        # sibling file in the same directory as missing even though it
        # exists, on some filesystems/storage backends. Retry rather than
        # fail outright, but only when the target file demonstrably still
        # exists -- a genuinely missing file still fails immediately.
        path = argv[-1]
        for attempt in range(retries):
            result = subprocess.run(argv, capture_output=True, text=True)
            if result.returncode == 0:
                return result
            if attempt == retries - 1 or not os.path.exists(path):
                return result
            time.sleep(retry_delay)
        return result

    def _with_retry(self, path, func, retries=3, retry_delay=0.2):
        # Same rationale as _run above, for the mutagen-based MP3/Opus
        # cleaning path, which doesn't go through subprocess.
        for attempt in range(retries):
            try:
                return func()
            except MutagenError:
                if attempt == retries - 1 or not os.path.exists(path):
                    raise
                time.sleep(retry_delay)

    def _get_tag(self, metaflac_command, tag, path):
        result = self._run([metaflac_command, "--show-tag", tag, path])
        line = result.stdout.strip()
        if "=" in line:
            return line.split("=", 1)[1]
        return ""

    def _set_tag(self, metaflac_command, tag, value, path):
        self._run([metaflac_command, "--set-tag", f"{tag}={value}", path])

    def clean(self, item):
        path = syspath(item.path)
        if isinstance(path, bytes):
            path = path.decode()

        metaflac_command = self.config["metaflac_command_path"].get(str)
        arguments = self.config["arguments"].get(list)
        tags_to_keep = self.config["tags_to_keep"].get(list)

        tags_to_keep_map = {}
        for tag in tags_to_keep:
            content = self._get_tag(metaflac_command, tag, path)
            if content:
                tags_to_keep_map[tag] = content

        self._run([metaflac_command, "--remove-all-tags", path])

        for tag, content in tags_to_keep_map.items():
            self._set_tag(metaflac_command, tag, content, path)

        result = self._run([metaflac_command, *arguments, path])

        if result.returncode != 0:
            self._log.error(
                "failed to clean {}: {}", path, result.stderr.strip()
            )
            return

        self._log.info("cleaned {}", path)

    def clean_opus(self, path):
        tags_to_keep = {
            tag.upper()
            for tag in self.config["opus_tags_to_keep"].get(list)
        }

        try:
            tags = self._with_retry(path, lambda: OggOpus(path))
        except MutagenError as exc:
            self._log.error("failed to read tags from {}: {}", path, exc)
            return

        for key in list(tags.keys()):
            if key.upper() not in tags_to_keep:
                del tags[key]

        try:
            self._with_retry(path, lambda: tags.save(padding=lambda _: 0))
        except MutagenError as exc:
            self._log.error("failed to clean {}: {}", path, exc)
            return

        self._log.info("cleaned {}", path)

    def clean_mp3(self, path):
        frames_to_keep = set(self.config["mp3_frames_to_keep"].get(list))
        txxx_to_keep = {
            tag.upper() for tag in self.config["mp3_txxx_to_keep"].get(list)
        }

        try:
            tags = self._with_retry(path, lambda: ID3(path))
        except MutagenError as exc:
            self._log.error("failed to read tags from {}: {}", path, exc)
            return

        for key in list(tags.keys()):
            frame = tags[key]
            if frame.FrameID == "TXXX":
                if frame.desc.upper() not in txxx_to_keep:
                    del tags[key]
            elif frame.FrameID not in frames_to_keep:
                del tags[key]

        try:
            self._with_retry(
                path,
                lambda: tags.save(path, v1=0, v2_version=4, padding=lambda _: 0),
            )
        except MutagenError as exc:
            self._log.error("failed to clean {}: {}", path, exc)
            return

        self._log.info("cleaned {}", path)
