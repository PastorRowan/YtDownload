
pushd "%CD%"

cd /d %~dp0\..

call .\venv\Scripts\activate.bat

popd
