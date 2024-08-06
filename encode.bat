@echo off
@set PATH=%PATH%;%~dp0bin

title Win64 OpenSSL Command Prompt
echo Win64 OpenSSL Command Prompt
echo.
openssl version -a
echo.

%SystemDrive%
cd %UserProfile%

cmd.exe /K

@REM e:
@REM cd E:\OneDrive\Code\tgworker
openssl aes-256-cbc -pbkdf2 -salt -in 27437823session_name.session -out 27437823session_name.session.enc -pass pass:2cd52bc41b1196baab4a32e04c376dcb2cd52bc41b1196baab4a32e04c376dcb
openssl aes-256-cbc -pbkdf2 -salt -in 29614663session_name.session -out 29614663session_name.session.enc -pass pass:2cd52bc41b1196baab4a32e04c376dcb2cd52bc41b1196baab4a32e04c376dcb
