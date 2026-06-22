
pushd "%CD%"

cd /d %~dp0\..

python -m venv venv

cd /d %~dp0

call activate_venv.bat

cd /d %~dp0\..

pip install -r requirements.txt

popd
