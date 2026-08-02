"""Re-encode FLAC files with a fixed, idempotent set of `flac` arguments."""

import re
import subprocess

from beets import ui
from beets.plugins import BeetsPlugin
from beets.util import syspath

FLAC_VERSION_FROM_COMMAND_RE = re.compile(r"flac ([\d]+\.[\d]+\.[\d]+)")
FLAC_VERSION_FROM_FILE_RE = re.compile(
    r"reference libFLAC ([\d]+\.[\d]+\.[\d]+) [\d]+"
)


class EncodePlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.config.add(
            {
                "auto": True,
                "flac_command_path": "flac",
                "metaflac_command_path": "metaflac",
                "arguments": [
                    "--compression-level-8",
                    "--exhaustive-model-search",
                    "--no-padding",
                    "--qlp-coeff-precision-search",
                    "--verify",
                    "--warnings-as-errors",
                ],
                "encode_if_flac_versions_mismatch": True,
                "encode_if_encode_argument_tags_mismatch": True,
                "save_encode_arguments_in_tag": True,
                "save_encode_arguments_in_tag_name": "FLAC_ARGUMENTS",
                "force": False,
            }
        )

        if self.config["auto"].get(bool):
            self.register_listener("item_imported", self.on_item_imported)
            self.register_listener("album_imported", self.on_album_imported)

    def commands(self):
        cmd = ui.Subcommand(
            "encode",
            help="re-encode FLAC files with the configured settings",
        )
        cmd.parser.add_option(
            "-f",
            "--force",
            action="store_true",
            dest="force",
            default=False,
            help="re-encode even if the version/argument checks match",
        )

        def func(lib, opts, args):
            for item in lib.items(ui.decargs(args)):
                self.process_item(item, force=opts.force)

        cmd.func = func
        return [cmd]

    def on_item_imported(self, lib, item):
        self.process_item(item)

    def on_album_imported(self, lib, album):
        for item in album.items():
            self.process_item(item)

    def process_item(self, item, force=False):
        if item.format != "FLAC":
            return
        self.encode(item, force=force)

    def _run(self, argv):
        return subprocess.run(
            argv,
            capture_output=True,
            text=True,
        )

    def _flac_version_from_command(self, flac_command):
        result = self._run([flac_command, "--version"])
        match = FLAC_VERSION_FROM_COMMAND_RE.search(
            result.stdout + result.stderr
        )
        return match.group(1) if match else None

    def _flac_version_from_file(self, metaflac_command, path):
        result = self._run([metaflac_command, "--show-vendor-tag", path])
        match = FLAC_VERSION_FROM_FILE_RE.search(result.stdout + result.stderr)
        return match.group(1) if match else None

    def _get_tag(self, metaflac_command, tag, path):
        result = self._run([metaflac_command, "--show-tag", tag, path])
        line = result.stdout.strip()
        if "=" in line:
            return line.split("=", 1)[1]
        return ""

    def _set_tag(self, metaflac_command, tag, value, path):
        self._run([metaflac_command, "--remove-tag", tag, path])
        self._run([metaflac_command, "--set-tag", f"{tag}={value}", path])

    def encode(self, item, force=False):
        path = syspath(item.path)
        if isinstance(path, bytes):
            path = path.decode()

        flac_command = self.config["flac_command_path"].get(str)
        metaflac_command = self.config["metaflac_command_path"].get(str)
        arguments = self.config["arguments"].get(list)
        tag_name = self.config["save_encode_arguments_in_tag_name"].get(str)
        arguments_as_string = " ".join(arguments)

        need_to_encode = False

        if self.config["encode_if_flac_versions_mismatch"].get(bool):
            flac_version_from_command = self._flac_version_from_command(
                flac_command
            )
            flac_version_from_file = self._flac_version_from_file(
                metaflac_command, path
            )
            if flac_version_from_command != flac_version_from_file:
                need_to_encode = True

        if self.config["encode_if_encode_argument_tags_mismatch"].get(bool):
            encode_arguments_tag_content = self._get_tag(
                metaflac_command, tag_name, path
            )
            if encode_arguments_tag_content != arguments_as_string:
                need_to_encode = True

        if need_to_encode or force or self.config["force"].get(bool):
            result = self._run(
                [
                    flac_command,
                    *arguments,
                    "--force",
                    "--silent",
                    path,
                ]
            )

            if result.returncode != 0:
                self._log.error(
                    "failed to encode {}: {}", path, result.stderr.strip()
                )
                return

            self._log.info("encoded {}", path)

            # The re-encode changes the file's size/bitrate on disk even
            # though the audio itself is unchanged (lossless); refresh the
            # library's cached audio properties so they don't go stale.
            item.read()
            item.store()

        if self.config["save_encode_arguments_in_tag"].get(bool):
            self._set_tag(metaflac_command, tag_name, arguments_as_string, path)
