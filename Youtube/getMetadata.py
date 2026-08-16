
from dataclasses import dataclass

import requests

import helpers

@dataclass
class YoutubeVideoMetadata:
    title: str
    author_name: str
    author_url: str
    type: str
    height: int
    width: int
    version: str
    provider_name: str
    provider_url: str
    thumbnail_height: int
    thumbnail_width: int
    thumbnail_url: str

def getMetadata(youtubeVideoLink: str) -> YoutubeVideoMetadata | None:

    if not helpers.isUrlValid(youtubeVideoLink):
        print("Url is invalid, returning None")
        return None

    try:
        response = requests.get(
            "https://www.youtube.com/oembed",
            params={
                "url": youtubeVideoLink,
                "format": "json"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return YoutubeVideoMetadata(
            title=data["title"],
            author_name=data["author_name"],
            author_url=data["author_url"],
            type=data["type"],
            height=data["height"],
            width=data["width"],
            version=data["version"],
            provider_name=data["provider_name"],
            provider_url=data["provider_url"],
            thumbnail_height=data["thumbnail_height"],
            thumbnail_width=data["thumbnail_width"],
            thumbnail_url=data["thumbnail_url"]
        )

    except requests.exceptions.RequestException:
        print("An error occured while requesting metadata, returning None")
        return None
