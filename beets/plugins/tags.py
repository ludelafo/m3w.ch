"""Set arbitrary Vorbis comment tags on FLAC files.

Tags configured under `tags.tags` (fixed KEY: value pairs) are applied to
every imported FLAC automatically. The `beet tag KEY=VALUE ... [query]`
command additionally lets you set ad hoc tags on demand.
"""

import concurrent.futures
import os
import re
import subprocess
import time

from beets import ui
from beets.plugins import BeetsPlugin
from beets.util import syspath

ASSIGNMENT_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$")


class TagsPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()

        self.config.add(
            {
                "auto": True,
                "threads": os.cpu_count() or 1,
                "metaflac_command_path": "metaflac",
                "tags": {},
            }
        )

        if self.config["auto"].get(bool):
            self.register_listener("item_imported", self.on_item_imported)
            self.register_listener("album_imported", self.on_album_imported)

    def commands(self):
        cmd = ui.Subcommand(
            "tag",
            help="set arbitrary tags on FLAC files (KEY=VALUE ...)",
        )

        def func(lib, opts, args):
            tags = {}
            query = []

            for arg in ui.decargs(args):
                match = ASSIGNMENT_RE.match(arg)
                if match:
                    tags[match.group(1)] = match.group(2)
                else:
                    query.append(arg)

            if not tags and not self.config["tags"].get(dict):
                raise ui.UserError(
                    "no tags specified and tags.tags is empty; use KEY=VALUE"
                    " (e.g. beet tag MOOD=chill albumartist:'Some Artist')"
                )

            self._run_parallel(
                lib.items(query),
                lambda item: self.process_item(item, extra_tags=tags),
            )

        cmd.func = func
        return [cmd]

    def on_item_imported(self, lib, item):
        self.process_item(item)

    def on_album_imported(self, lib, album):
        self._run_parallel(album.items(), self.process_item)

    def _run_parallel(self, items, func):
        threads = self.config["threads"].get(int)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=threads
        ) as executor:
            futures = [executor.submit(func, item) for item in items]
            for future in concurrent.futures.as_completed(futures):
                future.result()

    def process_item(self, item, extra_tags=None):
        if item.format != "FLAC":
            return

        tags = dict(self.config["tags"].get(dict))
        if extra_tags:
            tags.update(extra_tags)

        if not tags:
            return

        self.set_tags(item, tags)

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

    def set_tags(self, item, tags):
        path = syspath(item.path)
        if isinstance(path, bytes):
            path = path.decode()

        metaflac_command = self.config["metaflac_command_path"].get(str)

        for tag, value in tags.items():
            self._run([metaflac_command, "--remove-tag", tag, path])
            result = self._run(
                [metaflac_command, "--set-tag", f"{tag}={value}", path]
            )

            if result.returncode != 0:
                self._log.error(
                    "failed to set tag {} on {}: {}",
                    tag,
                    path,
                    result.stderr.strip(),
                )
                continue

            self._log.info("set {}={} on {}", tag, value, path)
