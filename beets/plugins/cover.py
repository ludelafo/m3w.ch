"""Check album art dimensions and optimize cover JPEGs with jpegoptim."""

import concurrent.futures
import contextvars
import os
import subprocess

from beets import ui
from beets.plugins import BeetsPlugin
from beets.util import syspath


class CoverPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.config.add(
            {
                "auto": True,
                "threads": os.cpu_count() or 1,
                "identify_command_path": "identify",
                "convert_command_path": "convert",
                "jpegoptim_command_path": "jpegoptim",
                "width": 1200,
                "height": 1200,
                "arguments": [
                    "--strip-all",
                ],
            }
        )

        if self.config["auto"].get(bool):
            self.register_listener("album_imported", self.on_album_imported)

    def commands(self):
        cmd = ui.Subcommand(
            "cover",
            help="check and optimize album cover art",
        )

        def func(lib, opts, args):
            self._run_parallel(
                lib.albums(ui.decargs(args)), self.process_album
            )

        cmd.func = func
        return [cmd]

    def on_album_imported(self, lib, album):
        self.process_album(album)

    def _run_parallel(self, items, func):
        threads = self.config["threads"].get(int)

        # Item/Album paths are resolved lazily on first access, by expanding
        # the DB-stored value against beets' music directory, which is
        # tracked in a contextvar set on the main thread. That var isn't
        # inherited by worker threads by default, so without copying it
        # explicitly, the first (path-resolving) access from a worker thread
        # silently returns the un-expanded, directory-relative path instead.
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=threads
        ) as executor:
            # Each task needs its own context snapshot -- a single Context
            # object can't be entered by more than one call at a time, so
            # sharing one across tasks would serialize them (or, run
            # concurrently, raise "cannot enter context: already entered").
            futures = [
                executor.submit(contextvars.copy_context().run, func, item)
                for item in items
            ]
            for future in concurrent.futures.as_completed(futures):
                future.result()

    def _run(self, argv):
        return subprocess.run(
            argv,
            capture_output=True,
            text=True,
        )

    def _dimensions(self, identify_command, path):
        result = self._run([identify_command, "-format", "%w %h", path])
        parts = result.stdout.strip().split()
        if len(parts) != 2:
            return None
        try:
            return int(parts[0]), int(parts[1])
        except ValueError:
            return None

    def _resize(self, convert_command, path, width, height):
        result = self._run(
            [convert_command, path, "-resize", f"{width}x{height}", path]
        )

        if result.returncode != 0:
            self._log.error(
                "failed to resize cover {}: {}", path, result.stderr.strip()
            )
            return

        self._log.info("resized cover {} to fit {}x{}", path, width, height)

    def process_album(self, album):
        if not album.artpath:
            self._log.warning("no cover art found for {}", album)
            return

        path = syspath(album.artpath)
        if isinstance(path, bytes):
            path = path.decode()

        identify_command = self.config["identify_command_path"].get(str)
        convert_command = self.config["convert_command_path"].get(str)
        jpegoptim_command = self.config["jpegoptim_command_path"].get(str)
        expected_width = self.config["width"].get(int)
        expected_height = self.config["height"].get(int)

        dimensions = self._dimensions(identify_command, path)
        if dimensions is None:
            self._log.warning("could not read dimensions of cover {}", path)
        else:
            width, height = dimensions
            if width < expected_width or height < expected_height:
                self._log.warning(
                    "cover {} is {}x{}, smaller than the target {}x{}",
                    path,
                    width,
                    height,
                    expected_width,
                    expected_height,
                )
            elif width > expected_width or height > expected_height:
                self._resize(
                    convert_command, path, expected_width, expected_height
                )

        if not path.lower().endswith((".jpg", ".jpeg")):
            self._log.debug(
                "cover {} is not a JPEG, skipping optimization", path
            )
            return

        arguments = self.config["arguments"].get(list)
        size_before = os.path.getsize(path)

        result = self._run([jpegoptim_command, *arguments, path])

        if result.returncode != 0:
            self._log.error(
                "failed to optimize cover {}: {}", path, result.stderr.strip()
            )
            return

        size_after = os.path.getsize(path)
        self._log.info(
            "optimized cover {} ({} -> {} bytes)",
            path,
            size_before,
            size_after,
        )
