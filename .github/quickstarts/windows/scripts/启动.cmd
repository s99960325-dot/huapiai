@REM ...

@ECHO OFF

@CHCP 65001

TITLE [Huapir] AI 系统正在启动...

SET PATH=%cd%\WPy64-31320\python;%cd%\ffmpeg\bin;%PATH%

IF NOT EXIST data\venv (

    ECHO 虚拟环境不存在，正在创建...

    python -m venv --system-site-packages data\venv

    ECHO 虚拟环境创建完成
    
)

TITLE [Huapir] AI 系统正在运行...

ECHO 正在启动 Huapir...

call data\venv\Scripts\activate.bat

python -m huapir

TITLE [Huapir] AI 系统已停止运行

ECHO 程序已停止运行。

PAUSE