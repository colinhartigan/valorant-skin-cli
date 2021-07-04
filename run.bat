@echo off

echo NOTE: THIS BATCH SCRIPT CAN ONLY FUNCTION PROPERLY ON WINDOWS 10 AND UP
echo.
timeout /t 1 >NUL 2>NUL

echo "     _   _____   __   ____  ___  ___   _  ________        __    _              ___    "
echo "    | | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/______ / /__ (_)__  ________/ (_)   "
echo "    | |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___(_-</  '_// / _ \/___/ __/ / /    "
echo "    |___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /___/_/\_\/_/_//_/    \__/_/_/     "
echo.
timeout /t 1 >NUL 2>NUL

:DOES_PYTHON_EXIST
python -V | find "Python 3"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
python -V | find /v "Python 3" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
python\python.exe -V | find "Python 3"    >NUL 2>NUL && (goto :PYTHON_PORTABLE_EXIST)
echo No correct Python 3 installation found
echo Downloading Python 3 Portable Package...
curl https://www.python.org/ftp/python/3.9.6/python-3.9.6-embed-amd64.zip > python.zip
echo Extracting Python Portable Package...
mkdir python >NUL 2>NUL
tar -C python -xf python.zip >NUL 2>NUL
echo Python Portable Package Extracted
echo Continuing...
echo.

:PYTHON_PORTABLE_EXIST
echo Installing Pip...
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python\python.exe get-pip.py
echo.
echo Installing Dependencies...
python\python.exe -m pip install -r requirements.txt
echo.
echo Done! Launching Valorant skin manager CLI...
echo.
python\python.exe main.py
goto :EOF

:PYTHON_DOES_EXIST
echo Updating Pip...
python -m pip install --upgrade pip
echo.
echo Installing Dependencies...
python -m pip install -r requirements.txt
echo.
echo Done! Launching Valorant skin manager CLI...
echo.
python main.py
goto :EOF
