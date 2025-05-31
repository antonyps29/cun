@echo off
setlocal

CALL C:\Users\usuario\anaconda3\Scripts\activate.bat cun_env
cd "C:\Users\usuario\Documents\Prueba Tecnica DS\CUN"

:: Crear log
echo Iniciando entrenamiento del modelo... > modelo_log.txt
echo. >> modelo_log.txt

echo Ejecutando modelo.py... >> modelo_log.txt
python modelo.py >nul 2>>modelo_log.txt
echo Modelo entrenado y predicciones generadas. >> modelo_log.txt
echo. >> modelo_log.txt

endlocal