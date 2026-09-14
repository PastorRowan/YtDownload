
# Install Windows binaries

## 1. Download FFmpeg and FFprobe

Download the `WINDOWS X64` FFmpeg build from the [yt-dlp FFmpeg Builds repository](https://github.com/yt-dlp/FFmpeg-Builds).

Copy the files into this directory:

```
libs/windows/
├── ffmpeg.exe
└── ffprobe.exe
```

## 2. Download QuickJS

Download `qjs.exe` from the [PastorRowan/binaries branch](https://github.com/PastorRowan/binaries/tree/main)

If `qjs.exe` cannot be found there then downdload `qjs-windows-x86_64.exe` from here https://github.com/quickjs-ng/quickjs/releases and rename the file to `qjs.exe`

Copy the file into this directory:

```
libs/windows/
└── qjs.exe
```

# Final Directory Structure

The final folder structure should look like this:

```
libs/windows/
├── ffmpeg.exe
├── ffprobe.exe
├── qjs.exe
└── README.MD
```
