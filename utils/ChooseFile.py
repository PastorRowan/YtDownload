
from pathlib import Path

from plyer import filechooser

def ChooseFile(title: str = "Choose File") -> Path | None:

    files = filechooser.open_file(
        title=title,
        multiple=False
    )

    if not files:
        return None

    return Path(files[0])
