@echo off
rem Сборка расширения: загрузка в тестовую базу, проверка модулей, выгрузка .cfe.
rem Использование: build_extension.bat <ИмяРасширения> <КаталогИсходников> <ВыходнойCfe> [КаталогФайловойБазы]
rem Пример:        build_extension.bat WarehouseTablet out\ext_ws WarehouseTablet.cfe D:\work\test_base
chcp 65001 >nul
setlocal
set PLAT=C:\Program Files (x86)\1cv8\8.3.27.2214\bin\1cv8.exe
set EXT=%~1
set SRC=%~2
set OUT=%~3
set BASE=%~4
if "%BASE%"=="" set BASE=%~dp0test_base
if "%EXT%"=="" (echo Usage: build_extension.bat ExtName SourceDir OutCfe [BaseDir] & exit /b 1)
set L=%~dp0build_log
echo User name of the 1C infobase user:
set /p IBUSER=
echo Password (typed on screen, not stored anywhere):
set /p IBPWD=
del "%L%_*.txt" 2>nul
echo === load
"%PLAT%" DESIGNER /F "%BASE%" /N"%IBUSER%" /P"%IBPWD%" /LoadConfigFromFiles "%SRC%" -Extension %EXT% /UpdateDBCfg /Out "%L%_01_load.txt"
echo === check modules
"%PLAT%" DESIGNER /F "%BASE%" /N"%IBUSER%" /P"%IBPWD%" /CheckModules -Server -ExternalConnection -Extension %EXT% /Out "%L%_02_check.txt"
echo === dump cfe
del "%OUT%" 2>nul
"%PLAT%" DESIGNER /F "%BASE%" /N"%IBUSER%" /P"%IBPWD%" /DumpCfg "%OUT%" -Extension %EXT% /Out "%L%_03_dump.txt"
echo DONE. Logs: %L%_*.txt
endlocal
