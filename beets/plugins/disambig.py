"""Titlecase albumdisambig and fold it into the album title on import.

The beets-titlecase plugin's `all_lowercase` option returns any fully
lowercase string untouched, before its `replace` list or general titlecasing
ever run. MusicBrainz disambiguation strings (e.g. "deluxe edition") are
exactly this shape, so listing `albumdisambig` under `titlecase.fields` has
no effect on it -- it's never actually cased on import.

This plugin bypasses beets-titlecase entirely for this one field, calling
the `titlecase` library directly. It also appends the (titlecased)
disambiguation to the album title itself -- e.g. "Some Album" becomes
"Some Album (Deluxe Edition)" -- so every track's ALBUM tag carries it, not
just the on-disk folder name.
"""

from titlecase import titlecase

from beets.autotag import AlbumInfo
from beets.plugins import BeetsPlugin


class DisambigPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()
        self.register_listener("trackinfo_received", self.received_info)
        self.register_listener("albuminfo_received", self.received_info)

    def received_info(self, info):
        disambig = getattr(info, "albumdisambig", None)
        if not disambig or disambig == "explicit":
            return

        cased = titlecase(disambig)
        info.albumdisambig = cased

        if isinstance(info, AlbumInfo) and info.album:
            info.album = f"{info.album} ({cased})"
