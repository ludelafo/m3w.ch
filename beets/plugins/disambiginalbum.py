"""Add album's disambiguation to the album title."""

from __future__ import annotations

import re
from functools import cached_property
from typing import TYPE_CHECKING

from beets import ui
from beets.plugins import BeetsPlugin

if TYPE_CHECKING:
    from beets.autotag import AlbumInfo
    from beets.importer import ImportSession, ImportTask
    from beets.library import Album

_NON_WORD_RE = re.compile(r"\W+")


def _normalized(disambig: str) -> str:
    """Normalize `disambig` for comparison."""
    return _NON_WORD_RE.sub("", disambig.casefold())


class DisambigInAlbumPlugin(BeetsPlugin):
    @cached_property
    def auto(self) -> bool:
        return self.config["auto"].get(bool)

    @cached_property
    def album_format(self) -> str:
        return self.config["format"].as_str()

    @cached_property
    def ignore(self) -> set[str]:
        return {word.casefold() for word in self.config["ignore"].as_str_seq()}

    def __init__(self) -> None:
        super().__init__()

        self.config.add(
            {
                "auto": True,
                "format": "({0})",
                "ignore": [],
            }
        )

        self._command = ui.Subcommand(
            "disambiginalbum",
            help="fold an album's disambiguation into the album title",
        )

        if self.auto:
            self.register_listener(
                "albuminfo_received", self.albuminfo_received
            )

        self.import_stages = [self.imported]

    def commands(self) -> list[ui.Subcommand]:
        def func(lib, opts, args):
            write = ui.should_write()

            for album in lib.albums(ui.decargs(args)):
                if not self.update_metadata(album):
                    continue
                if write:
                    for item in album.items():
                        item.try_write()

        self._command.func = func
        return [self._command]

    def imported(self, _: ImportSession, task: ImportTask) -> None:
        if not self.auto:
            return

        for item in task.imported_items():
            album = item.get_album()
            if album is not None:
                self.update_metadata(album)

    def albuminfo_received(self, info: AlbumInfo) -> None:
        self.disambig_in_album(info)

    def update_metadata(self, album: Album) -> bool:
        """Fold `album`'s disambiguation into its title and persist the
        change to the album and its items.

        Returns True if anything was changed.
        """
        if not self.disambig_in_album(album):
            return False

        album.store()
        for item in album.items():
            item.album = album.album
            item.store()

        return True

    def disambig_in_album(self, album: Album | AlbumInfo) -> bool:
        """Look for disambiguation in the album's fields and move it
        to the title.

        Returns:
            True if the album has been modified. False otherwise.
        """
        disambig = (album.get("albumdisambig") or "").strip()

        if not disambig or disambig.casefold() in self.ignore:
            return False

        album_title = album.get("album") or ""

        if not album_title or _normalized(disambig) in _normalized(album_title):
            return False

        suffix = self.album_format.format(disambig)
        new_album = f"{album_title} {suffix}"
        self._log.info("album: {} -> {}", album_title, new_album)
        album.album = new_album

        return True
