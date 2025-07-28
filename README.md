# 校园网匿名论坛

一个专为校园网用户设计的匿名论坛系统，提供安全、便捷的匿名交流平台。支持饼干(Cookie)匿名机制、饼干收藏管理、Markdown格式、图片分享等丰富功能。

## ✨ 核心特性

- 🍪 **饼干匿名系统**: 基于时间戳的临时匿名ID，支持收藏管理和多身份切换
- 💾 **饼干收藏管理**: 本地存储多个饼干身份，一键切换，智能限制防滥用
- 🧵 **串与回复**: 完整的话题讨论系统，支持嵌套回复和引用
- 📝 **Markdown支持**: 支持富文本编辑，包括代码高亮、表格、列表等
- 🖼️ **图片分享**: 支持多种格式图片上传，自动压缩优化
- 🎨 **响应式界面**: 适配桌面和移动设备的现代化UI
- 🔒 **内容过滤**: 智能内容审核，维护健康讨论环境
- 🐳 **容器化部署**: 基于Docker的一键部署方案

## 🛠️ 技术架构

### 后端技术栈
- **Web框架**: Flask 2.3.3 + Gunicorn
- **数据库**: PostgreSQL 15 (主数据) + Redis 7 (缓存/会话)
- **ORM**: SQLAlchemy 3.0
- **图片处理**: Pillow
- **Markdown**: Python-Markdown 3.5

### 前端技术栈
- **模板引擎**: Jinja2
- **样式**: 原生CSS3 (Grid + Flexbox)
- **交互**: 原生JavaScript (ES6+)
- **响应式**: 移动端优先设计

### 部署架构
- **容器编排**: Docker Compose
- **反向代理**: Nginx
- **健康检查**: 内置服务监控
- **数据持久化**: Docker Volume

## 🚀 快速开始

### 环境要求
- Docker 20.10+
- Docker Compose 2.0+
- 8080端口可用

### 一键部署
```bash
# 1. 克隆项目
git clone https://github.com/colaiii/Forum.git
cd Forum

# 2. 启动服务
docker-compose up -d

# 3. 等待服务就绪 (约30秒)
docker-compose logs -f web

# 4. 访问论坛
浏览器打开: http://localhost:8080
```

### 开发环境搭建
```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 配置环境变量
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export DATABASE_URL=postgresql://user:pass@localhost/dbname
export REDIS_URL=redis://localhost:6379

# 3. 初始化数据库
python -c "from app import create_app, db; app=create_app(); app.app_context().do(db.create_all())"

# 4. 启动开发服务器
python wsgi.py
```

## 📁 项目结构

```
Forum/
├── app/                      # 核心应用模块
│   ├── __init__.py          # 应用工厂和配置
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── thread.py        # 串模型
│   │   └── reply.py         # 回复模型
│   ├── routes/              # 路由控制器
│   │   ├── __init__.py
│   │   └── main.py          # 主要路由
│   ├── utils/               # 工具模块
│   │   ├── __init__.py
│   │   └── cookie_manager.py # 饼干管理
│   ├── templates/           # 前端模板
│   │   ├── base.html        # 基础模板
│   │   ├── index.html       # 首页
│   │   ├── thread.html      # 串详情
│   │   └── new_thread.html  # 发串页
│   └── static/              # 静态资源
│       ├── css/style.css    # 样式文件
│       └── js/app.js        # 交互脚本
├── uploads/                 # 用户上传文件
├── nginx.conf              # Nginx配置
├── docker-compose.yml      # 容器编排
├── Dockerfile             # 应用镜像
├── requirements.txt       # Python依赖
└── wsgi.py               # 应用入口
```

## 🍪 饼干系统详解

### 工作原理
饼干(Cookie)是本论坛独特的匿名机制：

1. **自动分配**: 首次访问时自动生成16位哈希ID
2. **时效性**: 默认7天有效期，可自动延期
3. **一致性**: 同一饼干在所有串中保持统一标识
4. **隐私保护**: 不收集真实身份信息，完全匿名
5. **视觉识别**: 不同饼干显示不同颜色，便于区分

### 技术实现
```python
# 饼干生成算法
timestamp = str(int(time.time()))
random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
cookie_id = hashlib.md5(f"{timestamp}{random_str}".encode()).hexdigest()[:16]
```

### 🆕 饼干管理功能

#### 收藏系统
- **多身份管理**: 用户可收藏最多3个不同的饼干身份
- **本地存储**: 所有收藏数据仅保存在用户浏览器本地，保护隐私
- **快速切换**: 一键切换到已收藏的任意饼干身份
- **自定义名称**: 为每个饼干添加个性化备注名称
- **导入导出**: 支持手动输入16位饼干ID进行恢复

#### 使用限制
- **收藏限制**: 每个用户最多收藏3个饼干身份
- **生成限制**: 24小时内最多生成3个新饼干
- **时间跟踪**: 自动记录生成时间，显示剩余等待时间
- **防滥用**: 超出限制时自动禁用相关功能并提示

#### 管理界面
- **饼干管理器**: 专门的管理弹窗界面
- **实时状态**: 显示当前饼干信息和使用统计
- **颜色标识**: 每个饼干都有独特的颜色标识
- **操作记录**: 显示收藏时间和使用状态

#### 技术特性
```javascript
// 本地存储结构
localStorage.setItem('forum_saved_cookies', JSON.stringify([
    {
        id: "饼干16位ID",
        name: "用户自定义名称", 
        color: "#颜色值",
        savedAt: "保存时间戳"
    }
]));

// 生成限制检查
localStorage.setItem('forum_cookie_generations', JSON.stringify([
    {
        cookieId: "生成的饼干ID",
        timestamp: "生成时间戳"
    }
]));
```

## 📝 使用指南

### 🍪 饼干管理操作
1. **打开管理器**: 点击导航栏"🍪 饼干管理"按钮
2. **收藏当前饼干**: 点击"收藏此饼干"并输入自定义名称
3. **切换饼干身份**: 在收藏列表中点击"使用"按钮切换
4. **生成新饼干**: 点击"生成新饼干"获得全新身份
5. **导入饼干**: 输入16位饼干ID手动导入已知饼干
6. **管理收藏**: 支持重命名、删除已收藏的饼干

### 发串操作
1. 点击"发串"按钮
2. 填写标题(最多100字符)
3. 编写内容(支持Markdown语法)
4. 可选择上传图片(PNG/JPG/GIF/WebP, 最大16MB)
5. 点击发布

### Markdown语法支持
```markdown
# 标题
**粗体** *斜体*
- 列表项
> 引用文本
[链接](https://example.com)
`代码` 或 ```代码块```
| 表格 | 支持 |
|------|------|
```

### 回复与引用
- 直接回复：在串详情页填写回复内容
- 引用回复：使用 `>>编号` 格式引用其他回复
- 图片回复：支持上传图片配合文字回复

## 🔧 配置说明

### 环境变量
```bash
FLASK_ENV=production          # 运行环境
DATABASE_URL=postgresql://... # 数据库连接
REDIS_URL=redis://...        # Redis连接
SECRET_KEY=...               # 会话密钥
UPLOAD_FOLDER=/app/uploads   # 上传目录
```

### Docker Compose配置
- `web`: Flask应用服务 (端口5000)
- `postgres`: PostgreSQL数据库 (端口5432)
- `redis`: Redis缓存服务 (端口6379)
- `nginx`: 反向代理服务 (端口8080)

## 🚀 部署到生产环境

### 域名配置
1. 修改 `nginx.conf` 中的 `server_name`
2. 配置SSL证书（推荐Let's Encrypt）
3. 更新 `docker-compose.yml` 端口映射

### 性能优化
1. 启用Nginx Gzip压缩
2. 配置静态文件缓存
3. 调整Gunicorn worker数量
4. 设置Redis内存限制

### 监控与日志
```bash
# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 资源使用情况
docker stats
```

## 🤝 贡献指南

1. Fork本项目
2. 创建功能分支: `git checkout -b feature/新功能`
3. 提交更改: `git commit -am '添加新功能'`
4. 推送分支: `git push origin feature/新功能`
5. 提交Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 📞 支持与反馈

- 项目地址: [GitHub Repository]
- 问题反馈: [Issues页面]
- 开发团队: Campus Forum Team

---

**注意**: 本项目仅供学习交流使用，请遵守相关法律法规，文明使用论坛功能。

© 2025 校园网匿名论坛 | 基于Flask开发 