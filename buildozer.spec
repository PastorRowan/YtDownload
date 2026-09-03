
[app]

title = YtDownload
package.name = ytdownload
package.domain = ytdownload.ytdownload

version = 1.0.0

p4a.branch = develop

source.dir = .
source.include_exts = py,kv,json
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so
source.exclude_dirs = Scripts_android,scripts_android,scripts_windows,scripts,screenshots

requirements = python3,kivy,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor==3.0.3,materialshapes,pycairo,pillow,exceptiongroup,asyncgui,asynckivy,android,yt-dlp,plyer,requests
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.archs = arm64-v8a

# android.add_src = android/src

# android.

android.api = 34
android.minapi = 24

orientation = portrait

fullscreen = 0
