
# Install Linux binaries

## 1. Download FFmpeg and FFprobe

Download the `LINUX X64` FFmpeg build from the [yt-dlp FFmpeg Builds repository](https://github.com/yt-dlp/FFmpeg-Builds).

Copy the files into this directory:

```
libs/linux/
├── ffmpeg
└── ffprobe
```

## 2. Download QuickJS

Download `qjs-linux-x86_64` from [quickjs-ng/quickjs/releases](https://github.com/quickjs-ng/quickjs/releases)

Rename the file to `qjs`

Copy the file into this directory:

```
libs/linux/
└── qjs
```

## 3. Make binaries executable:

Run these commands to make the binaries executable

### 3.1 Navigate to the binary directory

From the project root:
```
cd libs/linux
```

### 3.2 Give the binaries execute permission

Run:
```
chmod +x ffmpeg ffprobe qjs
```

The binaries can now be executed by YtDownload.

# Final Directory Structure

The final folder structure should look like this:

```
libs/linux/
├── ffmpeg
├── ffprobe
├── qjs
└── README.MD
```
