@echo off
rem === 批处理所在目录 ===
set "BASEDIR=%~dp0"
cd /d "%BASEDIR%"

rem === 端口号、脚本名、VENV 目录 ===
set "PORT=6626"
set "PYFILE=gateway.py"
set "VENV_BIN=venv\Scripts"

rem === 激活虚拟环境 ===
call "%VENV_BIN%\activate.bat"

rem === 检测并关闭占用端口的 python 进程 ===
for /f "tokens=5" %%p in ('netstat -ano ^| find ":%PORT% " ^| find "LISTENING"') do (
    echo [INFO] 发现端口 %PORT% 已被进程 %%p 占用，尝试结束…
    tasklist /fi "PID eq %%p" | find "python.exe" >nul && (
        taskkill /f /pid %%p >nul
        echo [INFO] 已终止进程 %%p
    )
)

rem === 启动服务（无窗口后台运行）===
start "" "%VENV_BIN%\pythonw.exe" "%PYFILE%"
echo [OK] smart_search_gateway 已启动/重启
exit /b 0
