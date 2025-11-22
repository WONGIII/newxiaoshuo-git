@echo off
chcp 65001 >nul
title 优雅小说网站

echo.
echo ========================================
echo           优雅小说网站启动器
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请先安装Python 3.7或更高版本
    echo.
    echo 安装步骤：
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装Python
    echo 3. 安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

:: 显示Python版本
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [信息] %PYTHON_VERSION%

:: 检查依赖是否安装
echo [信息] 检查依赖包...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 正在安装依赖包...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖包安装失败
        echo 请手动运行：pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo [信息] 依赖包检查通过

:: 创建数据库和超级管理员
echo [信息] 初始化数据库...
python -c "
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    # 检查是否已存在超级管理员
    super_admin = User.query.filter_by(role='super_admin').first()
    if not super_admin:
        admin = User(
            username='admin',
            email='admin@novel.com'
        )
        admin.set_password('admin123')
        admin.role = 'super_admin'
        db.session.add(admin)
        db.session.commit()
        print('超级管理员账户已创建')
        print('用户名: admin')
        print('密码: admin123')
    else:
        print('超级管理员账户已存在')
" >nul 2>&1

if %errorlevel% neq 0 (
    echo [警告] 数据库初始化失败，尝试直接启动...
)

echo.
echo ========================================
echo           网站启动信息
echo ========================================
echo 访问地址: http://127.0.0.1:5000
echo 管理员账户: admin / admin123
echo.
echo [提示] 按 Ctrl+C 停止服务器
echo ========================================
echo.

:: 启动网站
echo [信息] 正在启动网站...
python run.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 网站启动失败
    echo 可能的原因：
    echo 1. 端口5000被占用
    echo 2. 依赖包安装不完整
    echo 3. 文件权限问题
    echo.
    echo 请检查以上问题后重试
    pause
)
