
from pathlib import Path

from plyer import filechooser

def ChooseDirectory(title: str = "Choose Directory") -> Path | None:

    directories = filechooser.choose_dir(
        title=title
    )

    if not directories:
        return None

    directory = Path(directories[0])

    testFile = directory / ".permission_test"

    try:
        testFile.write_text("", encoding="utf-8")
        testFile.unlink()

    except OSError:
        return None

    return directory
