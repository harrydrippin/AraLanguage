@echo off
set dir=

echo Python�� ȯ�� ������ �����մϴ�.

:REDO
set /p dir=Python�� ��ġ ��θ� �Է����ּ���(�� : C:\Python34) : 
if "%dir%" == "" goto REDO

setx PATH "%PATH%;%dir%"
echo ȯ�� ������ �����Ǿ����ϴ�.
pause