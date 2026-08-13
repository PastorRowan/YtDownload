
import zipfile
import re
import requests

YT_DLP_VERSION_REGEX = r"__version__\s*=\s*['\"]([^'\"]+)['\"]"

def parse_yt_dlp_version(version: str) -> tuple[int, ...]:
    return tuple(map(int, version.split(".")))

def get_yt_dlp_version_in_version_py(text: str) -> str | None:
    return re.search(
        YT_DLP_VERSION_REGEX,
        text,
    )

def get_current_yt_dlp_version(zip_path: str) -> str | None:

    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            with archive.open("yt_dlp/version.py") as version_file:

                text = version_file.read().decode("utf-8")

                match = get_yt_dlp_version_in_version_py(text)

                return match.group(1) if match else None

    except (
        FileNotFoundError,
        KeyError,
        zipfile.BadZipFile,
    ):
        return None

def get_latest_yt_dlp_version() -> str | None:

    try:

        response = requests.get(
            "https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/yt_dlp/version.py",
            timeout=10,
        )

        response.raise_for_status()

        match = get_yt_dlp_version_in_version_py(response.text)

        return match.group(1) if match else None

    except requests.RequestException:
        return None

def download_yt_zlp(download_path: str) -> None:

    url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"

    response = requests.get(url, stream=True, timeout=30)

    response.raise_for_status()

    with open(download_path, "wb") as file:

        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

def update_yt_dlp(zip_path: str) -> None:

    current_version = get_current_yt_dlp_version(zip_path)

    if current_version is None:
        download_yt_zlp(zip_path)
        return

    latest_version = get_latest_yt_dlp_version()

    if latest_version is None:
        download_yt_zlp(zip_path)
        return

    current = parse_yt_dlp_version(current_version)
    latest = parse_yt_dlp_version(latest_version)

    if current < latest:
        print("Current version is older than the latest version.\nInstalling latest version...")
        download_yt_zlp(zip_path)
    elif current > latest:
        print("Current version is newer than the latest version.")
    else:
        print("yt-dlp is already up to date.")
