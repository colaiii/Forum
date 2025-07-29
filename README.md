# 校园网匿名论坛

一个专为校园网用户设计的匿名论坛系统，提供安全、便捷的匿名交流平台。支持饼干(Cookie)匿名机制、饼干收藏管理、置顶管理、Markdown格式、多图片分享等丰富功能。

## ✨ 核心特性

- 🍪 **饼干匿名系统**: 基于时间戳的临时匿名ID，支持收藏管理和多身份切换
- 💾 **饼干收藏管理**: 本地存储多个饼干身份，一键切换，智能限制防滥用
- 🏛️ **板块分类系统**: 五大主题板块分类，支持分板块浏览和发布内容
  - 🏠 **时间线**: 展示所有板块的最新内容，全局视图
  - 📚 **学术**: 学术讨论、学习交流、课程分享
  - 🍎 **生活**: 日常生活、校园生活、美食分享
  - 🎮 **游戏**: 游戏讨论、攻略分享、组队交友
  - 🎨 **创作**: 原创作品、文学创作、艺术分享
- 🔍 **智能搜索系统**: 支持全文搜索、标题搜索、内容搜索，关键词高亮显示，支持板块内搜索
- 🧵 **串与回复**: 完整的话题讨论系统，支持嵌套回复和引用
- 📝 **Markdown支持**: 支持富文本编辑，包括代码高亮、表格、列表等
- 🖼️ **多图片分享**: 支持最多5张图片同时上传，智能预览和管理，自动压缩优化
- 🛡️ **全面安全防护**: 多层次频率限制系统，防止暴力破解和恶意行为
  - 饼干导入限制：每分钟最多3次尝试，防止暴力破解
  - 发串频率限制：每分钟最多发3串，防止内容刷屏
  - 回复频率限制：每分钟最多回复5次，防止恶意刷屏
- 🔄 **实时自动刷新**: 智能检测新内容，无需手动刷新页面
  - 首页自动检测新串：30秒检查一次，发现新串时弹出提示
  - 串详情自动检测新回复：20秒检查一次，实时显示新回复数量
  - 智能暂停机制：页面不可见时自动暂停，节省资源
- 🎨 **响应式界面**: 适配桌面和移动设备的现代化UI
  - **智能侧边栏**: 移动端支持折叠式板块导航，节省屏幕空间
  - **智能返回按钮**: 不同页面自动切换为对应的返回功能
  - **弹窗优化**: 移动端弹窗去除顶栏，采用底部滑出设计
  - **互斥弹窗**: 确保同时只有一个弹窗处于活动状态
  - **友好错误页面**: 自定义404页面，访问不存在的串时显示美观的错误提示
  - **流畅发串体验**: 发表串后自动跳转到详情页，无缝浏览体验
- 🔒 **内容过滤**: 智能内容审核，维护健康讨论环境
- 🛠️ **强大管理工具**: 完整的后台管理脚本，支持串管理、置顶管理、统计分析、批量操作
- 🐳 **容器化部署**: 基于Docker的一键部署方案

## 🛠️ 技术架构

### 后端技术栈
- **Web框架**: Flask 2.3.3 + Gunicorn
- **数据库**: PostgreSQL 15 (主数据) + Redis 7 (缓存/会话)
- **ORM**: SQLAlchemy 3.0
- **图片处理**: Pillow
- **Markdown**: Python-Markdown 3.5
- **管理工具**: 自研Python脚本，提供完整的论坛管理功能

### 前端技术栈
- **模板引擎**: Jinja2
- **样式**: 原生CSS3 (Grid + Flexbox)
- **交互**: 原生JavaScript (ES6+)
- **实时更新**: AJAX + Fetch API，支持无感知自动刷新
- **响应式**: 移动端优先设计
- **移动端优化**: 智能按钮系统、折叠式导航、底部弹窗设计

### 部署架构
- **容器编排**: Docker Compose
- **反向代理**: Nginx
- **健康检查**: 内置服务监控
- **数据持久化**: Docker Volume

## 🚀 快速开始

> 💡 **新用户提示**：首次部署后建议运行 `docker compose exec web python demo.py` 生成演示数据，立即体验完整功能！

### 环境要求
- Docker 20.10+
- Docker Compose 2.0+
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

# 4. 等待服务就绪 (约30秒)
docker compose logs -f web

# 5. 生成演示数据 (可选，推荐首次部署时使用)
docker compose exec web python demo.py

# 6. 访问论坛
浏览器打开: http://localhost:8080

# 快速体验板块功能
http://localhost:8080/                    # 时间线（全部内容）
http://localhost:8080/category/academic   # 学术板块
http://localhost:8080/category/life       # 生活板块  
http://localhost:8080/category/game       # 游戏板块
http://localhost:8080/category/creative   # 创作板块
```

### 🎯 快速体验
如果你想立即体验论坛的完整功能，建议在部署后运行演示数据脚本：

```bash
# 生成丰富的演示内容
docker compose exec web python demo.py
```

**演示数据包含：**
- 📌 1个置顶欢迎串（包含板块分类功能介绍）
- 🧵 10个不同板块的讨论串，涵盖五大主题分类：
  - 📚 **学术板块**: Python Flask开发、算法题讨论、期末考试复习等
  - 🍎 **生活板块**: 食堂美食、宿舍生活小贴士等
  - 🎮 **游戏板块**: 热门游戏推荐、王者荣耀组队等
  - 🎨 **创作板块**: 原创小说连载、手绘作品分享等
- 💬 60+丰富的回复内容和引用关系
- 🎨 Markdown格式化内容展示
- 🍪 多样化的饼干用户身份

**预览效果：**
- ✅ 板块分类导航和切换功能
- ✅ 分板块内容展示和筛选
- ✅ 置顶串功能展示
- ✅ 搜索功能测试（支持板块内搜索）
- ✅ 引用回复机制
- ✅ 饼干系统演示
- ✅ Markdown渲染效果

### 开发环境搭建

#### 使用Docker（推荐）
```bash
# 1. 克隆项目
git clone https://github.com/colaiii/Forum.git
cd Forum

# 2. 构建开发镜像
docker compose build

# 3. 启动开发环境
docker compose up -d

# 4. 查看日志
docker compose logs -f web

# 5. 停止服务
docker compose down
```

#### 本地Python环境
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

#### 常用Docker命令
```bash
# 重新构建镜像（代码更新后）
docker compose build --no-cache

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f [service_name]

# 进入容器调试
docker compose exec web bash

# 清理所有容器和镜像
docker compose down --rmi all --volumes

# 管理工具常用命令
docker compose exec web python demo.py                   # 生成演示数据
docker compose exec web python admin_tools.py stats      # 查看统计
docker compose exec web python admin_tools.py list       # 列出串
docker compose exec web python admin_tools.py cleanup --days 30  # 清理旧串
docker compose exec web python admin_tools.py pin --id 1  # 设置置顶串
docker compose exec web python admin_tools.py list-pinned # 列出置顶串
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
│   │   ├── main.py          # 主要路由（搜索、页面）
│   │   └── api.py           # API路由（串、回复、频率限制、自动刷新）
│   ├── utils/               # 工具模块
│   │   ├── __init__.py
│   │   ├── cookie_manager.py # 饼干管理（包含所有频率限制逻辑）
│   │   └── categories.py    # 板块分类配置和工具函数
│   ├── templates/           # 前端模板
│   │   ├── base.html        # 基础模板（含规则和饼干管理）
│   │   ├── index.html       # 首页（含搜索框）
│   │   ├── search_results.html # 搜索结果页面
│   │   ├── thread.html      # 串详情页面
│   │   ├── new_thread.html  # 发串页面（含多图片上传）
│   │   └── 404.html         # 自定义404错误页面
│   └── static/              # 静态资源
│       ├── css/style.css    # 样式文件（含搜索和限制样式）
│       └── js/app.js        # 交互脚本（含饼干管理和限制处理）
├── uploads/                 # 用户上传文件
├── nginx.conf              # Nginx配置
├── docker-compose.yml      # 容器编排
├── Dockerfile             # 应用镜像
├── requirements.txt       # Python依赖
├── demo.py               # 演示数据生成脚本（创建丰富的示例内容）
├── admin_tools.py        # 论坛管理工具脚本（支持串管理、置顶管理、统计分析）
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
- **导入限制**: 每分钟最多尝试3次导入，防止暴力破解
- **时间跟踪**: 自动记录生成时间，显示剩余等待时间
- **防滥用**: 超出限制时自动禁用相关功能并提示

#### 安全机制
- **饼干导入限制**: 基于IP地址的导入频率限制，每分钟最多3次尝试
  - 使用Redis滚动时间窗口技术
  - 防止暴力破解饼干ID
  - 超出限制时显示等待倒计时
- **发串频率限制**: 基于饼干ID的发串频率控制，每分钟最多3串
  - 防止垃圾内容和恶意刷屏
  - 维护论坛内容质量
- **回复频率限制**: 基于饼干ID的回复频率控制，每分钟最多5次回复
  - 防止恶意刷屏和无意义回复
  - 鼓励理性讨论和有价值的互动
- **注册验证**: 只能导入已在系统中注册且有效的饼干ID
- **自动清理**: 过期的限制记录自动清除，不占用存储空间
- **优雅降级**: Redis不可用时系统自动降级，保证基本功能正常

## 🔍 搜索功能详解

### 功能特性
1. **多种搜索模式**
   - **全部搜索**: 同时搜索标题和内容
   - **仅标题**: 只在串标题中搜索关键词
   - **仅内容**: 只在串内容中搜索关键词

2. **智能显示**
   - **关键词高亮**: 搜索结果中的关键词黄色高亮显示
   - **搜索统计**: 显示搜索关键词、模式和结果数量
   - **分页支持**: 大量搜索结果支持分页浏览

3. **用户体验**
   - **搜索建议**: 无结果时提供搜索优化建议
   - **快速入口**: 主页和导航栏都有搜索入口
   - **条件保持**: 搜索条件在结果页面保持，便于调整
   - **界面优化**: 首次访问时不显示空白统计区域，避免界面混乱
   - **响应式布局**: 移动端友好的搜索体验

### 技术实现
```python
# 搜索查询构建
if search_type == 'title':
    search_query = Thread.query.filter(Thread.title.contains(query))
elif search_type == 'content':
    search_query = Thread.query.filter(Thread.content.contains(query))
else:
    search_query = Thread.query.filter(
        or_(Thread.title.contains(query), Thread.content.contains(query))
    )
```

### 搜索界面
- **响应式设计**: 移动端友好的搜索表单
- **实时反馈**: 搜索过程中的加载提示
- **结果展示**: 清晰的搜索结果布局和样式

## 🏛️ 板块分类系统详解

### 功能特性
1. **五大主题板块**
   - **🏠 时间线**: 展示全部板块内容的聚合视图，提供全局浏览体验
   - **📚 学术**: 专注于学术讨论、学习交流、课程分享等教育相关内容
   - **🍎 生活**: 涵盖日常生活、校园生活、美食分享等生活类话题
   - **🎮 游戏**: 游戏讨论、攻略分享、组队交友等娱乐互动内容
   - **🎨 创作**: 原创作品、文学创作、艺术分享等创意展示平台

2. **智能分类管理**
   - **自动归类**: 发串时选择板块，内容自动归类到对应分区
   - **视觉区分**: 时间线中不同板块内容有颜色标识，便于识别
   - **独立浏览**: 每个板块可独立浏览，专注特定主题内容
   - **搜索集成**: 支持在特定板块内进行精准搜索

3. **用户体验优化**
   - **左侧导航**: 固定侧边栏提供便捷的板块切换功能
   - **智能预选**: 从特定板块页面发串时自动选择对应板块
   - **响应式布局**: 移动端采用折叠式侧边栏设计，点击展开板块选择
   - **状态保持**: 浏览时保持当前板块状态，便于连续使用
   - **触摸优化**: 移动端板块项目支持触摸友好的交互设计

### 技术实现
```python
# 板块配置定义
CATEGORIES = {
    'timeline': {
        'name': '时间线',
        'description': '展示所有板块的串',
        'icon': '🏠',
        'color': '#007bff'
    },
    'academic': {
        'name': '学术',
        'description': '学术讨论、学习交流、课程分享',
        'icon': '📚',
        'color': '#28a745'
    },
    # ... 其他板块配置
}

# 路由支持板块筛选
@main_bp.route('/')
@main_bp.route('/category/<category>')
def index(category='timeline'):
    if category == 'timeline':
        # 显示所有板块内容
        threads = Thread.query.order_by(Thread.last_reply_at.desc())
    else:
        # 显示特定板块内容
        threads = Thread.query.filter_by(category=category)
```

### 数据库设计
- **category字段**: Thread表添加category字段存储板块分类
- **默认值**: 新串默认分类为'timeline'，保证向后兼容
- **索引优化**: category字段建立索引，提高查询性能
- **数据验证**: 只允许有效的板块分类值，确保数据一致性

## 🖼️ 多图片分享系统详解

### 功能特性
1. **多图片支持**
   - **数量限制**: 单次发串最多支持5张图片
   - **格式支持**: PNG, JPG, GIF, WebP 格式
   - **大小限制**: 单张图片最大16MB
   - **智能压缩**: 自动优化图片尺寸和质量

2. **用户交互优化**
   - **批量选择**: 支持一次性选择多张图片
   - **实时预览**: 选择后立即显示缩略图预览
   - **独立管理**: 每张图片独立的移除按钮
   - **文件信息**: 显示图片文件名和大小

3. **智能限制系统**
   - **友好提示**: 超出限制时显示自定义弹窗提醒
   - **解决建议**: 提供具体的操作建议和说明
   - **状态保持**: 限制触发时保持已选择图片的状态

### 技术实现

#### 数据库设计
```sql
-- 支持多图片存储的新字段设计
ALTER TABLE threads ADD COLUMN image_urls TEXT;  -- JSON格式存储多个图片URL

-- 向后兼容性
-- 保留原 image_url 字段，通过属性访问第一张图片
```

#### 前端交互
```javascript
// 多图片选择和预览
const selectedFiles = new DataTransfer();

// 文件数量限制检查
if (selectedFiles.files.length + newFiles.length > 5) {
    showImageLimitModal();  // 显示友好的限制弹窗
    return;
}

// 动态预览更新
function updateImagePreview() {
    // 为每张图片生成预览项
    // 包含缩略图、文件信息、移除按钮
}
```

#### 后端处理
```python
# API支持多图片处理
uploaded_files = request.files.getlist('images')
image_urls = []

for file in uploaded_files:
    if file and allowed_file(file.filename):
        # 处理单张图片
        processed_url = process_and_save_image(file)
        image_urls.append(processed_url)

# 存储为JSON格式
thread.set_image_urls(image_urls)
```

### 用户界面设计

#### 桌面端显示
- **列表页**: 显示前3张图片缩略图，超过时显示"+N张图片"提示
- **详情页**: 显示所有图片，网格布局展示
- **发串页**: 卡片式预览，每张图片独立管理

#### 移动端优化
- **触摸友好**: 移除按钮采用圆形设计，便于点击
- **响应式布局**: 图片预览在移动端垂直排列
- **弹窗适配**: 限制提示弹窗采用底部滑出设计

#### 视觉设计
```css
/* 现代化的移除按钮 */
.image-remove-btn {
    background: #e74c3c;
    border-radius: 50%;
    position: absolute;
    top: -8px;
    right: -8px;
    width: 24px;
    height: 24px;
    transition: all 0.2s ease;
}

/* 移动端适配 */
@media (max-width: 768px) {
    .image-remove-btn {
        width: 28px;
        height: 28px;
    }
}
```

## 📝 使用指南

### 🏛️ 板块分类操作
1. **浏览板块**: 使用左侧板块导航栏切换不同主题板块
   - **🏠 时间线**: 查看所有板块的最新内容，全局浏览模式
   - **📚 学术**: 浏览学术讨论、学习交流、课程分享相关内容
   - **🍎 生活**: 查看日常生活、校园生活、美食分享等话题
   - **🎮 游戏**: 浏览游戏讨论、攻略分享、组队交友内容
   - **🎨 创作**: 查看原创作品、文学创作、艺术分享等创意内容

2. **发串选择板块**: 
   - 点击对应板块页面的"+ 发新串"按钮，自动选择当前板块
   - 在发串页面的"选择板块"下拉框中选择合适的分类
   - 系统会根据选择的板块对内容进行归类展示

3. **板块切换**: 
   - **桌面端**: 左侧固定导航栏显示当前所在板块（高亮显示）
   - **移动端**: 点击汉堡菜单按钮展开折叠式侧边栏进行板块切换
   - 点击任意板块图标即可切换到对应的主题板块
   - **智能收起**: 移动端选择板块后侧边栏自动收起

### 🔍 搜索功能操作
1. **快速搜索**: 在主页搜索框输入关键词，选择搜索类型，点击搜索
2. **搜索类型**:
   - **全部**: 搜索标题和内容中的关键词
   - **仅标题**: 只搜索串标题
   - **仅内容**: 只搜索串内容
3. **板块搜索**: 
   - **时间线搜索**: 在时间线板块中搜索全部板块内容
   - **板块内搜索**: 在特定板块页面搜索时，只搜索当前板块的内容
   - **搜索范围**: 搜索框会显示"在XX中搜索..."提示当前搜索范围
4. **查看结果**: 搜索结果页面显示匹配的串，关键词会高亮显示
5. **调整搜索**: 在结果页面可以修改关键词或搜索类型重新搜索
6. **导航入口**: 可通过导航栏"搜索"链接进入搜索页面

### 📱 移动端导航操作
1. **侧边栏切换**: 
   - **首页/列表页**: 点击左上角汉堡菜单按钮展开板块导航
   - **折叠式设计**: 侧边栏从左侧滑出，不占用主要内容区域
   - **点击关闭**: 点击空白区域或再次点击菜单按钮即可收起
   
2. **智能返回按钮**:
   - **串详情页**: 汉堡菜单自动变为红色返回按钮，点击返回列表页
   - **发新串页**: 按钮变为返回按钮，智能返回到对应板块页面
   - **搜索结果页**: 返回按钮支持返回上一页或首页
   
3. **弹窗状态管理**:
   - **饼干管理/规则界面**: 打开弹窗时按钮自动变为返回按钮
   - **图片预览**: 查看图片时返回按钮用于关闭预览
   - **确认/输入弹窗**: 返回按钮相当于"取消"操作
   - **互斥机制**: 打开新弹窗时自动关闭其他已打开的弹窗
   
4. **移动端弹窗优化**:
   - **去除顶栏**: 饼干管理和规则界面在移动端无顶栏设计
   - **底部滑出**: 弹窗从屏幕底部滑出，采用现代化的底部抽屉设计
   - **圆角设计**: 顶部圆角处理，视觉效果更加现代
   - **内容优化**: 弹窗内容区域经过移动端特别优化，触摸友好

5. **紧凑顶栏设计**:
   - **高度优化**: 移动端顶栏高度从90px优化到70px（小屏幕60px）
   - **按钮精简**: 汉堡菜单和导航按钮尺寸适配移动端
   - **空间利用**: 为内容区域释放更多可视空间

### 🍪 饼干管理操作
1. **打开管理器**: 点击导航栏"🍪 饼干管理"按钮
2. **收藏当前饼干**: 点击"收藏此饼干"并输入自定义名称
3. **切换饼干身份**: 在收藏列表中点击"使用"按钮切换
4. **生成新饼干**: 点击"生成新饼干"获得全新身份
5. **导入饼干**: 输入16位饼干ID手动导入已知饼干
   - ⚠️ **速率限制**: 每分钟最多尝试3次导入
   - 🔒 **安全验证**: 只能导入已注册且有效的饼干
   - ⏱️ **等待提示**: 超出限制时显示等待倒计时
6. **管理收藏**: 支持重命名、删除已收藏的饼干

### 📝 发串操作
1. 点击"+ 发新串"按钮（可从时间线或特定板块页面进入）
2. **选择板块**: 在下拉框中选择合适的主题板块
   - 从特定板块页面进入时会自动选择对应板块
   - 可手动切换到其他板块分类
3. 填写标题(最多100字符)
4. 编写内容(支持Markdown语法)
5. **多图片上传**(PNG/JPG/GIF/WebP格式):
   - 📸 **多选支持**: 一次最多选择5张图片
   - 👀 **实时预览**: 图片选择后立即显示预览，包含文件名和大小
   - 🗑️ **单独管理**: 每张图片都有独立的移除按钮，可随时删除不需要的图片
   - 📏 **智能限制**: 单张图片最大16MB，超出限制时显示友好提示弹窗
   - ⚠️ **数量提醒**: 尝试选择超过5张图片时弹出详细的限制说明
6. 点击发布
   - ⚠️ **频率限制**: 同一饼干1分钟内最多发3串，防止刷屏
   - 📂 **自动归类**: 发布后的串会出现在对应的板块中
   - 🔄 **自动跳转**: 发布成功后自动跳转到新串的详情页面

### 🔄 自动刷新功能
论坛支持智能的自动刷新功能，无需手动刷新页面即可看到最新内容：

#### **首页自动刷新**
- 📈 **自动检测**: 每30秒自动检查是否有新发布的串
- 🔔 **智能提醒**: 发现新串时在页面右上角显示绿色提示框
- 📱 **一键查看**: 点击"立即查看"按钮即可刷新页面显示新内容
- ⏸️ **智能暂停**: 切换到其他标签页时自动暂停检查，回到页面时恢复

#### **串详情页自动刷新**
- 💬 **回复检测**: 每20秒自动检查是否有新的回复
- 📊 **精确统计**: 显示具体的新回复数量（如"有3个新回复"）
- ⚡ **即时更新**: 点击提示可立即查看最新回复
- 🔇 **无干扰**: 不会影响用户正在输入的回复内容

#### **用户体验优化**
- 🎨 **优雅动画**: 提示框采用滑入动画效果
- 📱 **移动端适配**: 在手机端自适应显示位置和大小
- 💾 **资源节省**: 页面不可见时自动暂停检查，节省带宽和电量
- 🔄 **错误处理**: 网络异常时静默处理，不影响正常浏览

### 🖼️ 多图片上传操作
1. **选择图片**: 在发串页面点击"选择文件"，支持一次选择多张图片
2. **格式检查**: 系统自动检查图片格式（支持PNG/JPG/GIF/WebP）
3. **实时预览**: 选择后立即显示图片预览，包含：
   - 📸 图片缩略图（120×120px）
   - 📄 文件名和大小信息
   - 🗑️ 独立的圆形移除按钮
4. **图片管理**: 
   - **添加更多**: 可继续选择图片，直到达到5张上限
   - **单独删除**: 点击任意图片的移除按钮即可删除
   - **重新选择**: 删除后可以选择新的图片替换
5. **智能限制**: 
   - 📏 单张图片超过16MB时显示错误提示
   - 🚫 尝试选择超过5张图片时弹出友好的限制说明弹窗
   - 💡 弹窗提供具体的解决建议
6. **发布展示**: 
   - 🏠 **首页/搜索页**: 显示前3张图片，超过时显示"+N张图片"
   - 📄 **详情页**: 以网格形式展示所有图片
   - 📱 **移动端**: 自动适配响应式布局

### 💬 回复与引用
- **直接回复**: 在串详情页填写回复内容
- **引用回复**: 点击"引用"按钮，系统会自动设置引用关系，无需手动填写格式
- **图片回复**: 支持上传图片配合文字回复
- **频率保护**: 
  - ⚠️ **频率限制**: 同一饼干1分钟内最多回复5次，防止刷屏
  - 🎯 **智能引用**: 点击引用时不会自动填充内容，避免Markdown语法冲突
  - 📝 **自由编辑**: 用户可以自由编写回复内容和格式

### 🚫 错误处理与导航
- **自定义404页面**: 访问不存在的串时显示友好的错误提示
  - 🔍 **错误说明**: 清晰说明可能的错误原因
  - 🏠 **快速导航**: 提供返回首页、返回上一页等便捷操作
  - 💡 **使用建议**: 建议用户浏览最新串、发表新串或使用搜索功能
  - 📱 **响应式设计**: 移动端友好的错误页面布局
- **流畅发串体验**: 发表串后自动跳转到新串的详情页面，无需手动导航

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

### 🛠️ 管理工具

论坛提供了强大的后台管理脚本 `admin_tools.py`，用于串的管理和维护。

#### 基本使用方法
```bash
# 基本命令格式
docker compose exec web python admin_tools.py <操作> [参数]
```

#### 主要功能

##### 📊 查看串统计
```bash
# 查看论坛统计信息
docker compose exec web python admin_tools.py stats

# 列出最新20个串
docker compose exec web python admin_tools.py list

# 列出所有串
docker compose exec web python admin_tools.py list --all
```

##### 🗑️ 删除管理
```bash
# 删除单个串（有确认提示）
docker compose exec web python admin_tools.py delete --id 5

# 删除用户所有串
docker compose exec web python admin_tools.py delete-user --cookie 3c8bd2b2

# 批量删除多个串
docker compose exec web python admin_tools.py batch --ids 1,2,3,4

# 清理30天前的旧串
docker compose exec web python admin_tools.py cleanup --days 30
```

##### 📌 置顶管理
```bash
# 设置单个串为置顶
docker compose exec web python admin_tools.py pin --id 1

# 取消单个串的置顶
docker compose exec web python admin_tools.py unpin --id 1

# 列出所有置顶串
docker compose exec web python admin_tools.py list-pinned

# 批量设置多个串为置顶
docker compose exec web python admin_tools.py batch-pin --ids 1,2,3

# 批量取消多个串的置顶
docker compose exec web python admin_tools.py batch-unpin --ids 1,2,3
```

##### 🚀 高级操作
```bash
# 强制删除（跳过确认）
docker compose exec web python admin_tools.py delete --id 5 --force

# 清理指定天数前的串
docker compose exec web python admin_tools.py cleanup --days 7

# 查看帮助信息
docker compose exec web python admin_tools.py --help
```

#### 安全特性
- **⚠️ 确认机制**: 所有删除操作都有确认提示，防止误操作
- **🗑️ 完整清理**: 自动删除关联的图片文件和所有回复
- **📊 详细信息**: 删除前显示串的详细信息（标题、回复数、创建时间等）
- **🔄 级联删除**: 删除串时自动删除所有相关回复，保持数据一致性
- **💾 事务安全**: 使用数据库事务确保操作的原子性
- **🔒 权限控制**: 只能在Docker容器内执行，确保安全性

#### 实用场景
```bash
# 定期维护：清理旧内容
docker compose exec web python admin_tools.py cleanup --days 30

# 内容管理：删除违规串
docker compose exec web python admin_tools.py delete --id 123

# 用户管理：处理恶意用户
docker compose exec web python admin_tools.py delete-user --cookie abc123

# 监控分析：查看论坛状态
docker compose exec web python admin_tools.py stats

# 置顶管理：设置重要公告
docker compose exec web python admin_tools.py pin --id 1

# 置顶管理：查看当前置顶串
docker compose exec web python admin_tools.py list-pinned
```

### 配置说明

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

## 🛡️ 频率限制系统

为了维护论坛秩序，防止恶意行为和垃圾内容，论坛实施了完善的频率限制机制：

### 🔐 饼干导入限制
- **限制规则**: 每分钟最多尝试3次导入
- **作用范围**: 基于客户端IP地址
- **防护目标**: 防止暴力破解饼干ID
- **技术实现**: Redis有序集合 + 滚动时间窗口
- **用户提示**: 超出限制时显示精确的等待时间

### 📝 发串频率限制  
- **限制规则**: 每分钟最多发布3个串
- **作用范围**: 基于饼干ID
- **防护目标**: 防止内容刷屏和垃圾串
- **错误提示**: `发串过于频繁，请等待 XX 秒后再试（1分钟内最多发3串）`

### 💬 回复频率限制
- **限制规则**: 每分钟最多发布5条回复
- **作用范围**: 基于饼干ID  
- **防护目标**: 防止回复刷屏和恶意灌水
- **错误提示**: `回复过于频繁，请等待 XX 秒后再试（1分钟内最多回复5次）`

### ⚙️ 技术特性
- **Redis存储**: 使用有序集合高效管理时间窗口
- **自动清理**: 过期记录自动删除，节省存储空间
- **优雅降级**: Redis不可用时不影响基本功能
- **精确计时**: 提供秒级精度的等待时间提示
- **状态码**: 使用标准HTTP 429状态码表示频率限制

## 🔄 自动刷新系统

### API接口

#### 获取最新串 `/api/threads/latest`
用于首页自动刷新功能，检测新发布的串：

**请求参数**:
- `last_id` (可选): 最后已知的串ID，只返回比这个ID新的串
- `page` (可选): 页码，默认为1

**响应示例**:
```json
{
  "success": true,
  "has_new_content": true,
  "latest_thread_id": 25,
  "normal_threads": [
    {
      "id": 25,
      "title": "新发布的串",
      "content": "这是最新发布的内容...",
      "cookie_id": "abc123def456",
      "cookie_display": "ID:abc123de",
      "cookie_color": "#F8C471",
      "created_at": "2025-07-28 18:30:00",
      "last_reply_at": "07-28 18:30",
      "reply_count": 0,
      "is_pinned": false
    }
  ],
  "pinned_threads": [...]
}
```

#### 获取最新回复 `/api/threads/<id>/replies/latest`
用于串详情页自动刷新功能，检测新的回复：

**请求参数**:
- `last_id` (可选): 最后已知的回复ID，只返回比这个ID新的回复

**响应示例**:
```json
{
  "success": true,
  "has_new_content": true,
  "latest_reply_id": 50,
  "total_replies": 8,
  "replies": [
    {
      "id": 50,
      "content": "新的回复内容",
      "cookie_id": "def456ghi789",
      "cookie_display": "ID:def456gh",
      "cookie_color": "#85C1E9",
      "quote_id": null,
      "created_at": "2025-07-28 18:35:00",
      "thread_id": 15
    }
  ]
}
```

### 技术特性
- **增量更新**: 只返回新增的内容，减少数据传输
- **智能检测**: 基于ID比较，准确识别新内容
- **性能优化**: 使用索引查询，响应速度快
- **错误处理**: 网络异常时优雅降级，不影响用户体验

### 📊 频率限制API响应示例
```json
{
  "error": "发串过于频繁，请等待 45 秒后再试（1分钟内最多发3串）",
  "rate_limit": {
    "exceeded": true,
    "current_attempts": 3,
    "max_attempts": 3,
    "wait_time": 45,
    "window_minutes": 1
  }
}
```

## 🚀 部署到生产环境

### 域名配置
1. 修改 `nginx.conf` 中的 `server_name`
2. 配置SSL证书（推荐Let's Encrypt）
3. 更新 `docker-compose.yml` 端口映射

### 部署步骤
```bash
# 1. 构建生产镜像
docker compose build --no-cache

# 2. 启动服务
docker compose up -d

# 3. 查看服务状态
docker compose ps
```

### 性能优化
1. 启用Nginx Gzip压缩
2. 配置静态文件缓存
3. 调整Gunicorn worker数量
4. 设置Redis内存限制

### 监控与日志
```bash
# 查看服务状态
docker compose ps

# 查看实时日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f web

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

**更新日志**: 
- 🔍 v1.2.0: 新增搜索功能和关键词高亮
- 🛡️ v1.3.0: 完善安全防护，新增多层次频率限制系统
- 💬 v1.4.0: 优化引用功能，改进用户体验
- 🛠️ v1.5.0: 新增强大的管理工具系统，支持完整的串管理和维护功能
- 🔄 v1.6.0: 新增实时自动刷新系统，支持无感知内容更新和智能页面检测
- 📌 v1.7.0: 新增置顶管理功能，支持串的置顶设置、批量操作和置顶串列表管理
- 🏛️ v1.8.0: 新增板块分类系统，支持五大主题板块分类、分板块浏览、板块内搜索和智能内容归类
- 📱 v1.9.0: 重大移动端优化，新增智能按钮系统、折叠式侧边栏、底部弹窗设计和互斥弹窗机制
- 🖼️ v2.0.0: **多图片分享系统** - 支持一次上传最多5张图片，实时预览管理，现代化移除按钮设计，智能限制弹窗，自动跳转到详情页，自定义404错误页面

© 2025 校园网匿名论坛 | 基于Flask开发 | 包含完整的安全防护体系 