#!/bin/bash

echo "🍪 校园网匿名论坛 - 启动脚本"
echo "================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建环境变量文件
if [ ! -f .env ]; then
    echo "📝 创建环境变量文件..."
    cp env_template.txt .env
    echo "✅ 已创建 .env 文件，请根据需要修改配置"
fi

# 创建上传目录
mkdir -p uploads

echo "🚀 启动服务..."
echo "数据库: PostgreSQL"
echo "缓存: Redis" 
echo "Web: Flask + Gunicorn"
echo "代理: Nginx"
echo ""

# 启动所有服务
docker-compose up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

echo ""
echo "🎉 论坛启动完成！"
echo ""
echo "📱 访问地址:"
echo "  - 论坛首页: http://localhost"
echo "  - 直接访问: http://localhost:8080"
echo ""
echo "🔧 管理命令:"
echo "  - 查看日志: docker-compose logs -f"
echo "  - 停止服务: docker-compose down"
echo "  - 重启服务: docker-compose restart"
echo ""
echo "📋 服务信息:"
echo "  - PostgreSQL: localhost:5432 (postgres/password)"
echo "  - Redis: localhost:6379"
echo "  - 上传目录: ./uploads" 