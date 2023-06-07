from pathlib import Path
from typing import Optional, Tuple

from ..expansion import run_catching, Result
from ..model import TrackJson, ConfigJson, OnlineModule
from ..utils import Log


class Pull:
    _log: Log
    _local_folder: Path

    _config: ConfigJson
    _track: TrackJson

    modules_folder: Path

    def __init__(self, root_folder: Path, config: ConfigJson): ...
    @staticmethod
    def _copy_file(old: Path, new: Path, delete_old: bool = True): ...
    @staticmethod
    @run_catching
    def _safe_download(url: str, out: Path) -> Result: ...
    def _get_file_url(self, file: Path) -> str: ...
    def _get_changelog_common(self, changelog: str) -> Optional[Path]: ...
    def _from_zip_common(
        self, zip_file: Path, changelog: Optional[Path], *, delete_tmp: bool = ...
    ) -> Optional[OnlineModule]: ...
    def from_json(self, track: TrackJson, *, local: bool) -> Tuple[Optional[OnlineModule], float]: ...
    def from_url(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
    def from_git(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
    def from_zip(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
    def from_track(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
