@echo off
setlocal
python "%~dp0artz.py" %*
exit /b %errorlevel%
