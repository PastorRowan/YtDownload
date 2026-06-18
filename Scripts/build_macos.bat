
pushd "%CD%"

cd /d "%~dp0"

call activate_venv.bat

cd /d "%~dp0.."

pyinstaller ^
  --onefile ^
  --distpath dist/macos ^
  --add-binary "bin/macos/ffmpeg;bin" ^
  --add-binary "bin/macos/ffprobe;bin" ^
  --add-binary "bin/macos/qjs;bin" ^
  main.py

popd
 