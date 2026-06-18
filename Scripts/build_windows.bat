
pushd "%CD%"

cd /d "%~dp0"

call activate_venv.bat

cd /d "%~dp0.."

pyinstaller ^
  --onefile ^
  --distpath dist/windows ^
  --add-binary "bin/windows/ffmpeg.exe;bin" ^
  --add-binary "bin/windows/ffprobe.exe;bin" ^
  --add-binary "bin/windows/qjs.exe;bin" ^
  main.py

popd
