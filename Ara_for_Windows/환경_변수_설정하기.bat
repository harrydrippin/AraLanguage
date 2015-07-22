@echo off
set dir=

echo Python의 환경 변수를 설정합니다.

:REDO
set /p dir=Python의 설치 경로를 입력해주세요(예 : C:\Python34) : 
if "%dir%" == "" goto REDO

setx PATH "%PATH%;%dir%"
echo 환경 변수가 설정되었습니다.
pause