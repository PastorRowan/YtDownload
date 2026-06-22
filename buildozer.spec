
[app]

title = YtDownload
package.name = ytdownload
package.domain = ytdownload.ytdownload

version = 1.0.0

source.dir = .
source.include_exts = py,kv,json
source.include_patterns = bin/android/*
source.exclude_dirs = Scripts_android,scripts_android,scripts_windows,scripts,screenshots

requirements = python3,kivy,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,materialshapes,pycairo,pillow,exceptiongroup,asyncgui,asynckivy,yt-dlp
orientation = portrait

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 34
android.minapi = 24

fullscreen = 0
