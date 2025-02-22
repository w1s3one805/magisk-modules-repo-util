from typing import List, Union


class ArchiveIO:
    def __init__(self, file: str, mode: str, compression: Union[str, None]) -> None: ...

    def file_exists(self, name: str) -> bool: ...

    def file_read(self, name: str) -> Union[str, None]: ...

    def namelist(self) -> List[str]: ...

    def close(self) -> None: ...
