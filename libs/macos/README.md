
# Install MacOS binaries

## 1. Download FFmpeg and FFprobe

Download the FFmpeg build ZIP archive from https://evermeet.cx/ffmpeg/

Copy the files into this directory:

```
libs/macos/
├── ffmpeg
└── ffprobe
```

## 2. Download QuickJS

Download `qjs-darwin-x86_64` from [quickjs-ng/quickjs/releases](https://github.com/quickjs-ng/quickjs/releases)

Rename the file to `qjs`

Copy the file into this directory:

```
libs/macos/
└── qjs
```

## 3. Make binaries executable:

Run these commands to make the binaries executable

### 3.1 Navigate to the binary directory

From the project root:
```
cd libs/macos
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
libs/macos/
├── ffmpeg
├── ffprobe
├── qjs
└── README.MD
```
