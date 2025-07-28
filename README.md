# 校园网匿名论坛

一个校园网匿名论坛系统，支持饼干功能、串发布、回复等核心功能。

## 功能特点

- 🍪 **饼干系统**: 临时匿名ID，无需注册
- 🧵 **串发布**: 创建讨论话题
- 💬 **回复功能**: 支持回复引用
- 🖼️ **图片上传**: 支持图片分享
- 🎨 **简洁界面**: 简洁的界面设计
- 🐳 **Docker部署**: 容器化部署

## 技术栈

- 后端: Python Flask + SQLAlchemy + Redis
- 前端: HTML + CSS + JavaScript
- 数据库: PostgreSQL
- 部署: Docker + Docker Compose

## 快速启动

```bash
# 克隆项目
git clone <your-repo>
cd competition

# 使用Docker启动
docker-compose up -d

# 访问论坛
http://localhost:8080
```

## 开发环境

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python wsgi.py
```

## 项目结构

```
├── app/                 # 主应用
│   ├── models/         # 数据模型
│   ├── routes/         # 路由处理
│   ├── templates/      # 前端模板
│   └── static/         # 静态资源
├── uploads/            # 上传文件
├── docker-compose.yml  # Docker配置
├── Dockerfile         # Docker镜像
└── requirements.txt   # Python依赖
```

## 饼干系统说明

饼干(Cookie)是本论坛的核心匿名机制:
- 每个访客自动分配临时ID
- 同一饼干在同一串内保持一致
- 饼干有效期为24小时
- 通过饼干可识别同一用户的回复 