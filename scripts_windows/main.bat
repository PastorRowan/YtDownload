
pushd "%CD%"

call .\activate_venv.bat

cd /d %~dp0\..

python main.py

popd
