"""Strip FLAC files down to a fixed set of blocks and tags."""

import subprocess

from beets import ui
from beets.plugins import BeetsPlugin
from beets.util import syspath


class CleanPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.config.add(
            {
                "auto": True,
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
            }
        )

        if self.config["auto"].get(bool):
            self.register_listener("item_imported", self.on_item_imported)
            self.register_listener("album_imported", self.on_album_imported)

    def commands(self):
        cmd = ui.Subcommand(
            "clean",
            help="strip FLAC files to the configured blocks and tags",
        )

        def func(lib, opts, args):
            for item in lib.items(ui.decargs(args)):
                self.process_item(item)

        cmd.func = func
        return [cmd]

    def on_item_imported(self, lib, item):
        self.process_item(item)

    def on_album_imported(self, lib, album):
        for item in album.items():
            self.process_item(item)

    def process_item(self, item):
        if item.format != "FLAC":
            return
        self.clean(item)

    def _run(self, argv):
        return subprocess.run(
            argv,
            capture_output=True,
            text=True,
        )

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
