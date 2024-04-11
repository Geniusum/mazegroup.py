@echo off

for /d /r %%i in (__pycache__) do (
    echo Suppression du dossier %%i
    rmdir /s /q "%%i"
)