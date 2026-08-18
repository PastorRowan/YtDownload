
from pathlib import Path

from plyer import filechooser

def ChooseDirectory(title: str = "Choose Directory") -> Path | None:

    directories = filechooser.choose_dir(
        title=title
    )

    return Path(directories[0]) if directories else None
