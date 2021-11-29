cp ./../code/mrpc.py ./
pyinstaller --onefile mrpc.py
cp ./dist/mrpc.exe ./../release/
rm mrpc.py
rm -rf dist
rm -rf build
rm -rf __pycache__
rm mrpc.spec