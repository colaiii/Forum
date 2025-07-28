from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import redis
import os
from datetime import timedelta
from markupsafe import Markup

db = SQLAlchemy()
redis_client = None

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/forum')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # 使用绝对路径
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)
    
    # Redis连接
    global redis_client
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    redis_client = redis.from_url(redis_url)
    
    # 注册蓝图
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 添加自定义过滤器
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """将换行符转换为HTML换行标签"""
        if text is None:
            return ''
        # 转义HTML特殊字符，然后替换换行符
        import html
        escaped_text = html.escape(str(text))
        result = escaped_text.replace('\n', '<br>')
        return Markup(result)
    
    # 添加静态文件路由
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        from flask import send_from_directory, abort
        
        # 确保文件存在
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            abort(404)
        
        # 设置正确的Content-Type
        response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        
        # 添加缓存头
        response.headers['Cache-Control'] = 'public, max-age=3600'
        
        return response
    
    # 创建数据库表
    with app.app_context():
        from app.models import Thread, Reply
        db.create_all()
    
    # 创建上传目录
    upload_dir = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    
    # 设置目录权限
    try:
        os.chmod(upload_dir, 0o755)
    except:
        pass
    
    return app 