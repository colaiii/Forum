# 🍪 校园网匿名论坛

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com)

> 🎯 **专为校园网设计的现代化匿名论坛系统**  
> 基于Flask + PostgreSQL + Redis构建，支持饼干匿名机制、多图片分享、深色模式、实时刷新、板块分类等丰富功能

## ✨ 核心特性

### 🔐 安全匿名系统
- **🍪 饼干机制**: 基于时间戳的临时匿名ID，支持收藏管理和多身份切换
- **🛡️ 频率限制**: 多层次安全防护，防止暴力破解和恶意行为
- **🔒 内容过滤**: 智能审核系统，维护健康讨论环境

### 🏛️ 智能板块分类
- **🏠 时间线**: 全局内容聚合视图
- **📚 学术**: 学术讨论、学习交流、课程分享
- **🍎 生活**: 日常生活、校园生活、美食分享  
- **🎮 游戏**: 游戏讨论、攻略分享、组队交友
- **🎨 创作**: 原创作品、文学创作、艺术分享

### 🚀 现代化功能
- **🔍 智能搜索**: 全文搜索、关键词高亮、板块内搜索
- **🖼️ 多图片分享**: 最多5张图片同时上传，实时预览管理
- **📝 Markdown支持**: 富文本编辑，代码高亮、表格、列表
- **🔄 实时刷新**: 自动检测新内容，无需手动刷新
- **🌙 深色模式**: 智能主题切换，支持系统偏好检测和本地存储
- **📱 响应式设计**: 移动端优化，智能侧边栏和底部弹窗

## 🚀 快速开始

### 环境要求
- Docker 20.10+ & Docker Compose 2.0+
- 8080端口可用

### 一键部署
```bash
# 1. 克隆项目
git clone https://github.com/colaiii/Forum.git
cd Forum

# 2. 构建镜像
docker compose build

# 3. 启动服务
docker compose up -d

# 4. 等待就绪 (约30秒)
docker compose logs -f web

# 5. 生成演示数据 (推荐)
docker compose exec web python demo.py

# 6. 访问论坛
浏览器打开: http://localhost:8080
```

### 🎯 快速体验板块功能
| 板块 | 地址 | 说明 |
|------|------|------|
| 🏠 时间线 | `http://localhost:8080/` | 所有内容聚合 |
| 📚 学术 | `http://localhost:8080/category/academic` | 学习交流 |
| 🍎 生活 | `http://localhost:8080/category/life` | 校园生活 |
| 🎮 游戏 | `http://localhost:8080/category/game` | 游戏讨论 |
| 🎨 创作 | `http://localhost:8080/category/creative` | 原创分享 |

## 🛠️ 技术架构

<details>
<summary>点击展开技术栈详情</summary>

### 后端技术栈
- **Web框架**: Flask 2.3.3 + Gunicorn
- **数据库**: PostgreSQL 15 (主数据) + Redis 7 (缓存/会话)
- **ORM**: SQLAlchemy 3.0
- **图片处理**: Pillow
- **Markdown**: Python-Markdown 3.5

### 前端技术栈
- **模板引擎**: Jinja2
- **样式**: 原生CSS3 (Grid + Flexbox + CSS Variables)
- **主题系统**: CSS变量 + localStorage + 系统偏好检测
- **交互**: 原生JavaScript (ES6+)
- **实时更新**: AJAX + Fetch API

### 部署架构
- **容器编排**: Docker Compose
- **反向代理**: Nginx
- **数据持久化**: Docker Volume

</details>

## 📁 项目结构

```
Forum/
├── app/                      # 核心应用模块
│   ├── models/              # 数据模型 (thread.py, reply.py)
│   ├── routes/              # 路由控制器 (main.py, api.py)
│   ├── utils/               # 工具模块 (cookie_manager.py, categories.py)
│   ├── templates/           # 前端模板
│   └── static/              # 静态资源
├── uploads/                 # 用户上传文件
├── admin_tools.py          # 管理工具脚本
├── demo.py                 # 演示数据生成器
├── docker-compose.yml      # 容器编排配置
└── requirements.txt        # Python依赖
```

## 📖 使用指南

### 🍪 饼干系统

<details>
<summary>饼干管理操作</summary>

1. **打开管理器**: 点击导航栏"🍪 饼干管理"
2. **收藏饼干**: 点击"收藏此饼干"并输入自定义名称
3. **切换身份**: 在收藏列表中点击"使用"按钮
4. **生成新饼干**: 点击"生成新饼干"获得全新身份
5. **导入饼干**: 输入16位饼干ID手动导入

**安全限制**:
- 🚫 每分钟最多导入3次
- 📝 每分钟最多发3串
- 💬 每分钟最多回复5次

</details>

### 🌙 深色模式

<details>
<summary>主题切换功能</summary>

**切换方式**:
- 点击导航栏右侧的🌙/☀️主题切换按钮
- 自动跟随系统深色模式偏好设置

**智能特性**:
- **🧠 自动检测**: 首次访问时自动检测系统主题偏好
- **💾 本地存储**: 用户选择的主题偏好保存在浏览器本地
- **🔄 实时切换**: 主题切换即时生效，支持平滑过渡动画
- **📱 全兼容**: 所有页面元素完美适配深色/浅色主题


</details>

### 🏛️ 板块分类

<details>
<summary>板块操作指南</summary>

**浏览板块**:
- 使用左侧板块导航栏切换不同主题
- 📱 移动端: 点击汉堡菜单展开折叠式侧边栏

**发串选择板块**:
- 从板块页面发串会自动选择当前板块
- 可在下拉框中手动切换板块分类

**搜索功能**:
- 支持全文搜索、仅标题、仅内容三种模式
- 关键词高亮显示，支持板块内搜索

</details>

### 🖼️ 多图片上传

<details>
<summary>图片分享功能</summary>

**支持格式**: PNG, JPG, GIF, WebP  
**数量限制**: 最多5张图片  
**大小限制**: 单张最大16MB

**操作流程**:
1. 选择图片文件（支持多选）
2. 实时预览显示缩略图和文件信息
3. 单独管理每张图片（独立移除按钮）
4. 发布后在详情页网格展示

</details>

## 🛠️ 管理工具

### 基本操作

```bash
# 查看统计信息
docker compose exec web python admin_tools.py stats

# 列出最新串
docker compose exec web python admin_tools.py list

# 删除指定串
docker compose exec web python admin_tools.py delete --id 5

# 设置置顶串
docker compose exec web python admin_tools.py pin --id 1
```

### 批量操作

```bash
# 批量删除
docker compose exec web python admin_tools.py batch --ids 1,2,3,4

# 批量置顶
docker compose exec web python admin_tools.py batch-pin --ids 1,2,3

# 清理旧串
docker compose exec web python admin_tools.py cleanup --days 30
```

## 🔧 开发指南

### 本地开发环境

<details>
<summary>开发环境搭建</summary>

#### 使用Docker（推荐）
```bash
# 构建开发镜像
docker compose build

# 启动开发环境
docker compose up -d

# 查看日志
docker compose logs -f web
```

#### 本地Python环境
```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export FLASK_APP=wsgi.py
export DATABASE_URL=postgresql://user:pass@localhost/dbname
export REDIS_URL=redis://localhost:6379

# 启动服务器
python wsgi.py
```

</details>

### 常用Docker命令

```bash
# 重新构建镜像
docker compose build --no-cache

# 查看服务状态
docker compose ps

# 进入容器调试
docker compose exec web bash

# 清理所有容器
docker compose down --rmi all --volumes
```

## 🔄 API文档

### 自动刷新接口

<details>
<summary>API接口说明</summary>

#### 获取最新串 `/api/threads/latest`
```json
{
  "success": true,
  "has_new_content": true,
  "latest_thread_id": 25,
  "normal_threads": [...],
  "pinned_threads": [...]
}
```

#### 获取最新回复 `/api/threads/<id>/replies/latest`
```json
{
  "success": true,
  "has_new_content": true,
  "latest_reply_id": 50,
  "total_replies": 8,
  "replies": [...]
}
```

</details>

## 🚀 生产部署

### 部署到生产环境

```bash
# 1. 修改配置
# - 更新 nginx.conf 中的 server_name
# - 配置SSL证书
# - 调整 docker-compose.yml 端口映射

# 2. 构建生产镜像
docker compose build --no-cache

# 3. 启动服务
docker compose up -d

# 4. 查看状态
docker compose ps
```

### 性能优化建议
- ✅ 启用Nginx Gzip压缩
- ✅ 配置静态文件缓存
- ✅ 调整Gunicorn worker数量
- ✅ 设置Redis内存限制

## 🤝 贡献指南

1. **Fork** 本项目
2. **创建** 功能分支: `git checkout -b feature/新功能`
3. **提交** 更改: `git commit -am '添加新功能'`
4. **推送** 分支: `git push origin feature/新功能`
5. **提交** Pull Request

## 📊 版本历史

| 版本 | 主要功能 | 发布时间 |
|------|----------|----------|
| v2.1.0 | 🌙 **深色模式主题系统** | 2025.01 |
| v2.0.0 | 🖼️ **多图片分享系统** | 2025.01 |
| v1.9.0 | 📱 移动端重大优化 | 2024.12 |
| v1.8.0 | 🏛️ 板块分类系统 | 2024.11 |
| v1.7.0 | 📌 置顶管理功能 | 2024.10 |
| v1.6.0 | 🔄 实时自动刷新 | 2024.09 |

## 📄 许可证

本项目采用 **MIT许可证** - 详情请参阅 [LICENSE](LICENSE) 文件

## 📞 支持与反馈

- 🌟 **项目地址**: [GitHub Repository](https://github.com/colaiii/Forum)
- 🐛 **问题反馈**: [Issues页面](https://github.com/colaiii/Forum/issues)
- 💬 **开发团队**: Campus Forum Team

---

<div align="center">

**⚠️ 重要提示**: 本项目仅供学习交流使用，请遵守相关法律法规，文明使用论坛功能。

**© 2025 校园网匿名论坛** | 基于Flask开发 | 包含完整的安全防护体系

</div> 