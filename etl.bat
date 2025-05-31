@echo off
setlocal

CALL C:\Users\usuario\anaconda3\Scripts\activate.bat cun_env
cd "C:\Users\usuario\Documents\Prueba Tecnica DS\CUN"

:: Crear log
echo Iniciando ETL... > etl_log.txt
echo. >> etl_log.txt

echo Ejecutando ETL.py... >> etl_log.txt
python ETL.py >nul 2>>etl_log.txt
echo Limpieza de datos completada. >> etl_log.txt
echo. >> etl_log.txt

endlocal