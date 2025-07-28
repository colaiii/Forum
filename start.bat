@echo off
chcp 65001 >nul
echo 🍪 校园网匿名论坛 - Windows启动脚本
echo ================================

REM 检查Docker是否安装
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker未安装，请先安装Docker Desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker Compose未安装，请先安装Docker Compose
    pause
    exit /b 1
)

REM 创建环境变量文件
if not exist .env (
    echo 📝 创建环境变量文件...
    copy env_template.txt .env
    echo ✅ 已创建 .env 文件，请根据需要修改配置
)

REM 创建上传目录
if not exist uploads mkdir uploads

echo 🚀 启动服务...
echo 数据库: PostgreSQL
echo 缓存: Redis
echo Web: Flask + Gunicorn
echo 代理: Nginx
echo.

REM 启动所有服务
docker-compose up -d

echo.
echo ⏳ 等待服务启动...
timeout /t 10 /nobreak >nul

REM 检查服务状态
echo 📊 检查服务状态...
docker-compose ps

echo.
echo 🎉 论坛启动完成！
echo.
echo 📱 访问地址:
echo   - 论坛首页: http://localhost
echo   - 直接访问: http://localhost:8080
echo.
echo 🔧 管理命令:
echo   - 查看日志: docker-compose logs -f
echo   - 停止服务: docker-compose down
echo   - 重启服务: docker-compose restart
echo.
echo 📋 服务信息:
echo   - PostgreSQL: localhost:5432 (postgres/password)
echo   - Redis: localhost:6379
echo   - 上传目录: ./uploads
echo.
pause 