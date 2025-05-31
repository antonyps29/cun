@echo off
setlocal

CALL C:\Users\usuario\anaconda3\Scripts\activate.bat cun_env
cd "C:\Users\usuario\Documents\Prueba Tecnica DS\CUN"

:: Crear log
echo Iniciando carga a base de datos... > load_db_log.txt
echo. >> load_db_log.txt

echo Ejecutando load_db.py... >> load_db_log.txt
python load_db.py >nul 2>>load_db_log.txt
echo Datos subidos a la base de datos y copia generada en Supabase. >> load_db_log.txt
echo. >> load_db_log.txt

endlocal