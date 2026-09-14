
# Install Android arm64-v8a binaries

## 1. Download FFmpeg and FFprobe

Download `libffmpeg.so` and `libffprobe.so` from the [PastorRowan/binaries branch](https://github.com/PastorRowan/binaries/tree/main)

If the files are not available there, download `ffmpeg.so` and `ffprobe.so` from here instead: https://github.com/hzw1199/Android-FFmpeg-Prebuilt.

Rename the files:

ffmpeg.so → libffmpeg.so
ffprobe.so → libffprobe.so

Copy the files into this directory:

```
libs/arm64-v8a/
├── libffmpeg.so
└── libffprobe.so
```

## 2. Download QuickJS

Download `libqjs.so` and from the [PastorRowan/binaries branch](https://github.com/PastorRowan/binaries/tree/main)

Copy the file into this directory:

```
libs/arm64-v8a/
└── libqjs.so
```

# Final Directory Structure

The final folder structure should look like this:

```
libs/arm64-v8a/
├── libffmpeg.so
├── libffprobe.so
├── libqjs.so
└── README.MD
```
