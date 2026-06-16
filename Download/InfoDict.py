
from typing import (
    TypedDict,
    Optional,
    List,
    Union,
    Dict,
    Any,
    Literal,
    Set
)

from Download.DownloadJob import DownloadJob

class Fragment(TypedDict, total=False):
    """Fragment of a fragmented media."""
    url: str                          # fragment's URL
    path: str                         # fragment's path relative to fragment_base_url
    duration: Optional[Union[int, float]]  # fragment duration
    filesize: Optional[int]           # fragment size in bytes

class Thumbnail(TypedDict, total=False):
    """Thumbnail image information."""
    id: Optional[str]                 # Thumbnail format ID
    url: str                          # Thumbnail URL
    ext: Optional[str]                # Image extension
    preference: Optional[int]         # Quality of the image
    width: Optional[int]              # Width in pixels
    height: Optional[int]             # Height in pixels
    resolution: Optional[str]         # "{width}x{height}" (deprecated)
    filesize: Optional[int]           # Size in bytes
    http_headers: Optional[Dict[str, str]]  # HTTP headers for the request

class HLSAES(TypedDict, total=False):
    """HLS AES-128 decryption information."""
    uri: str                          # URI to download the key from
    key: str                          # Key as hex to decrypt fragments
    iv: str                           # IV as hex to decrypt fragments

class Format(TypedDict, total=False):
    """Video/audio format information."""
    # Required fields
    url: str                          # Mandatory URL representing the media
    
    # Common fields
    format_id: str                    # Short description of the format
    ext: str                          # File extension (calculated from URL if missing)
    vcodec: str                       # Name of the video codec in use
    acodec: str                       # Name of the audio codec in use
    protocol: str                     # Protocol for download (http, https, rtmp, etc.)
    
    # Video metadata
    width: Optional[int]              # Width of the video in pixels
    height: Optional[int]             # Height of the video in pixels
    resolution: Optional[str]         # Textual description of width and height
    aspect_ratio: Optional[float]     # Aspect ratio (calculated from width/height)
    fps: Optional[int]                # Frame rate
    dynamic_range: Optional[Literal['SDR', 'HDR10', 'HDR10+', 'HDR12', 'HLG', 'DV']]
    stretched_ratio: Optional[float]  # Pixel aspect ratio (if not square)
    
    # Bitrate information
    tbr: Optional[float]              # Total bitrate (audio+video) in kbps
    vbr: Optional[float]              # Video bitrate in kbps
    abr: Optional[float]              # Audio bitrate in kbps
    
    # Audio metadata
    asr: Optional[int]                # Audio sampling rate in Hertz
    audio_channels: Optional[int]     # Number of audio channels
    
    # File information
    filesize: Optional[int]           # File size in bytes (if known in advance)
    filesize_approx: Optional[int]    # Estimated file size in bytes
    container: Optional[str]          # Name of the container format
    
    # Format description
    format: Optional[str]             # Human-readable description
    format_note: Optional[str]        # Additional info (e.g., "3D", "DASH video")
    
    # Fragmented media
    fragment_base_url: Optional[str]  # Base URL for fragments
    fragments: Optional[List[Fragment]]  # List of fragments
    is_from_start: Optional[bool]     # Live format downloadable from start
    manifest_url: Optional[str]       # URL of the manifest file
    manifest_stream_number: Optional[int]  # Index of stream in manifest (internal)
    hls_media_playlist_data: Optional[str]  # M3U8 playlist data as string
    
    # HLS AES-128 decryption
    hls_aes: Optional[HLSAES]         # HLS decryption information
    extra_param_to_segment_url: Optional[str]  # Query string for segment URLs
    extra_param_to_key_url: Optional[str]      # Query string for key URL
    
    # Request/network
    request_data: Optional[bytes]     # POST data to send
    http_headers: Optional[Dict[str, str]]  # Additional HTTP headers
    player_url: Optional[str]         # SWF Player URL (for rtmpdump)
    no_resume: Optional[bool]         # Server doesn't support resume
    
    # RTMP specific
    page_url: Optional[str]           # Page URL for RTMP
    app: Optional[str]                # RTMP application
    play_path: Optional[str]          # RTMP play path
    tc_url: Optional[str]             # RTMP TC URL
    flash_version: Optional[str]      # Flash version
    rtmp_live: Optional[bool]         # RTMP live stream
    rtmp_conn: Optional[List[str]]    # RTMP connection parameters
    rtmp_protocol: Optional[str]      # RTMP protocol
    rtmp_real_time: Optional[bool]    # RTMP real time
    
    # Preferences and sorting
    preference: Optional[int]         # Order number (-1 default, -2 less than default)
    quality: Optional[int]            # Video quality order (-1 default)
    source_preference: Optional[int]  # Source order (-1 default)
    
    # Language
    language: Optional[str]           # Language code (e.g., "de", "en-US")
    language_preference: Optional[int]  # Language preference (10=exact, -1=default)
    
    # DRM
    has_drm: Optional[Union[bool, Literal['maybe']]]  # Whether format has DRM
    
    # Impersonation
    impersonate: Optional[Any]        # Impersonate target(s)
    
    # Availability
    available_at: Optional[int]       # Unix timestamp when format becomes available
    
    # Downloader options
    downloader_options: Optional[Dict[str, Any]]  # Downloader-specific options
    is_dash_periods: Optional[bool]   # Result of merging multiple DASH periods
    is_from_start: Optional[bool]     # Live format that can be downloaded from start

class Subtitle(TypedDict, total=False):
    """Subtitle information."""
    ext: str                          # File extension
    url: Optional[str]                # URL to subtitles file
    data: Optional[str]               # Subtitles file contents
    name: Optional[str]               # Name or description
    http_headers: Optional[Dict[str, str]]  # HTTP headers
    impersonate: Optional[Any]        # Impersonate target(s)

class Comment(TypedDict, total=False):
    """Comment information."""
    id: str                           # Comment ID
    author: Optional[str]             # Comment author name
    author_id: Optional[str]          # User ID of comment author
    author_thumbnail: Optional[str]   # Author thumbnail URL
    author_url: Optional[str]         # URL to author's page
    author_is_verified: Optional[bool]  # Whether author is verified
    author_is_uploader: Optional[bool]  # Whether author is video uploader
    html: Optional[str]               # Comment as HTML
    text: Optional[str]               # Plain text of comment
    timestamp: Optional[int]          # UNIX timestamp
    parent: Optional[str]             # Parent comment ID ("root" for top-level)
    like_count: Optional[int]         # Positive ratings
    dislike_count: Optional[int]      # Negative ratings
    is_favorited: Optional[bool]      # Marked as favorite by uploader
    is_pinned: Optional[bool]         # Pinned to top

class Chapter(TypedDict, total=False):
    """Chapter information."""
    start_time: float                 # Start time in seconds
    end_time: Optional[float]         # End time in seconds
    title: Optional[str]              # Chapter title

class HeatmapPoint(TypedDict, total=False):
    """Heatmap data point."""
    start_time: float                 # Start time in seconds
    end_time: float                   # End time in seconds
    value: float                      # Normalized value (0-1)

class InfoDict(TypedDict, total=False):
    """Main information dictionary for a video."""
    # Required for video type
    id: str                           # Video identifier
    title: str                        # Video title (empty string if none)
    
    # Either formats or url must be present
    formats: Optional[List[Format]]   # List of formats (worst to best)
    
    # Optional video fields
    ext: Optional[str]                # Video filename extension
    format: Optional[str]             # Video format (defaults to ext)
    player_url: Optional[str]         # SWF Player URL
    direct: Optional[bool]            # True if direct video file (GenericIE only)
    
    # Metadata
    alt_title: Optional[str]          # Secondary title
    display_id: Optional[str]         # Alternative identifier
    thumbnails: Optional[List[Thumbnail]]  # List of thumbnails
    thumbnail: Optional[str]          # Full URL to thumbnail
    description: Optional[str]        # Full video description
    uploader: Optional[str]           # Full name of uploader
    license: Optional[str]            # License name
    creators: Optional[List[str]]     # List of creators
    
    # Dates and timestamps
    timestamp: Optional[int]          # UNIX timestamp of upload
    upload_date: Optional[str]        # Upload date (YYYYMMDD)
    release_timestamp: Optional[int]  # UNIX timestamp of release
    release_date: Optional[str]       # Release date (YYYYMMDD)
    release_year: Optional[int]       # Release year
    modified_timestamp: Optional[int] # Last modified timestamp
    modified_date: Optional[str]      # Last modified date (YYYYMMDD)
    
    # Channel/uploader info
    uploader_id: Optional[str]        # Nickname or ID
    uploader_url: Optional[str]       # URL to personal webpage
    channel: Optional[str]            # Full channel name
    channel_id: Optional[str]         # Channel ID
    channel_url: Optional[str]        # URL to channel webpage
    channel_follower_count: Optional[int]  # Number of followers
    channel_is_verified: Optional[bool]    # Whether channel is verified
    
    # Location
    location: Optional[str]           # Physical location where filmed
    
    # Subtitles and captions
    subtitles: Optional[Dict[str, List[Subtitle]]]  # Available subtitles
    automatic_captions: Optional[Dict[str, List[Subtitle]]]  # Auto-generated captions
    
    # Statistics
    duration: Optional[Union[int, float]]  # Length in seconds
    view_count: Optional[int]         # Number of views
    concurrent_view_count: Optional[int]  # Current viewers
    save_count: Optional[int]         # Times saved/bookmarked
    like_count: Optional[int]         # Positive ratings
    dislike_count: Optional[int]      # Negative ratings
    repost_count: Optional[int]       # Number of reposts
    average_rating: Optional[float]   # Average rating
    comment_count: Optional[int]      # Number of comments
    
    # Comments
    comments: Optional[List[Comment]]  # List of comments
    
    # Content classification
    age_limit: Optional[int]          # Age restriction in years
    categories: Optional[List[str]]   # List of categories
    tags: Optional[List[str]]         # List of tags
    cast: Optional[List[str]]         # List of cast members
    
    # Live status
    is_live: Optional[bool]           # Currently live stream
    was_live: Optional[bool]          # Originally a live stream
    live_status: Optional[Literal['is_live', 'is_upcoming', 'was_live', 'not_live', 'post_live']]
    
    # Time ranges
    start_time: Optional[float]       # Start time in seconds
    end_time: Optional[float]         # End time in seconds
    
    # Chapters and heatmap
    chapters: Optional[List[Chapter]]  # List of chapters
    heatmap: Optional[List[HeatmapPoint]]  # Heatmap data
    
    # Embed and availability
    playable_in_embed: Optional[Union[bool, str]]  # Embed allowed
    availability: Optional[Literal['private', 'premium_only', 'subscriber_only', 'needs_auth', 'unlisted', 'public']]
    media_type: Optional[str]         # Type of media (episode, clip, trailer)
    
    # Series/Episode information
    chapter: Optional[str]            # Chapter name
    chapter_number: Optional[int]     # Chapter number
    chapter_id: Optional[str]         # Chapter ID
    
    series: Optional[str]             # Series title
    series_id: Optional[str]          # Series ID
    season: Optional[str]             # Season title
    season_number: Optional[int]      # Season number
    season_id: Optional[str]          # Season ID
    episode: Optional[str]            # Episode title
    episode_number: Optional[int]     # Episode number
    episode_id: Optional[str]         # Episode ID
    
    # Music/Track information
    track: Optional[str]              # Track title
    track_number: Optional[int]       # Track number
    track_id: Optional[str]           # Track ID
    artists: Optional[List[str]]      # List of artists
    composers: Optional[List[str]]    # List of composers
    genres: Optional[List[str]]       # List of genres
    album: Optional[str]              # Album title
    album_type: Optional[str]         # Album type
    album_artists: Optional[List[str]]  # All artists on album
    disc_number: Optional[int]        # Disc number
    
    # Section cuts
    section_start: Optional[float]    # Start time for clip
    section_end: Optional[float]      # End time for clip
    
    # Storyboard
    rows: Optional[int]               # Rows in storyboard fragment
    columns: Optional[int]            # Columns in storyboard fragment
    
    # Internal/utility
    webpage_url: Optional[str]        # URL to video webpage
    _old_archive_ids: Optional[List[str]]  # Old archive IDs for backward compatibility
    _format_sort_fields: Optional[List[str]]  # Fields for sorting formats
    __post_extractor: Optional[Any]   # Function to call after extraction

def getAvailableVideoExts(infoDict: InfoDict) -> List[str]:

    ALLOWED_VIDEO_EXTS = DownloadJob.ALLOWED_VIDEO_EXTS

    formats = infoDict.get("formats") or []

    exts: Set[str] = set()

    for f in formats:
        ext: str = f.get("ext")
        if ext in ALLOWED_VIDEO_EXTS:
            exts.add(str(ext))

    return sorted(exts)

def getAvailableVideoHeights(infoDict: InfoDict) -> List[str]:

    ALLOWED_VIDEO_HEIGHTS = DownloadJob.ALLOWED_VIDEO_HEIGHTS

    formats = infoDict.get("formats") or []

    heights: Set[int] = set()

    for f in formats:
        height: int = f.get("height")
        strHeight: str = str(height)
        if strHeight in ALLOWED_VIDEO_HEIGHTS:
            heights.add(str(height))

    sortedHeights: list[int] = sorted(heights)

    sortedStrHeights: list[str] = [str(h) for h in sortedHeights]

    return sortedStrHeights

def getAvailableAudioExts(infoDict: InfoDict) -> List[str]:

    ALLOWED_AUDIO_EXTS = DownloadJob.ALLOWED_AUDIO_EXTS

    formats = infoDict.get("formats") or []

    exts: Set[str] = set()

    for f in formats:
        if f.get("acodec") not in (None, "none"):
            ext: str = f.get("ext")
            if ext in ALLOWED_AUDIO_EXTS:
                exts.add(str(ext))

    return sorted(exts)

def getAvailableAudioAbrs(infoDict: InfoDict) -> list[str]:

    ALLOWED_ABRS = DownloadJob.ALLOWED_ABRS

    formats = infoDict.get("formats") or []

    abr_set: Set[str] = set()

    for f in formats:
        abr: float = f.get("abr")
        strAbr: str = str(abr)
        if strAbr in ALLOWED_ABRS:
            abr_set.add(abr)

    sortedAbrs: list[float] = sorted(abr_set)

    sortedStrAbrs: list[str] = [str(a) for a in sortedAbrs]

    return sortedStrAbrs
