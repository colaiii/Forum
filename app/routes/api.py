from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.models.thread import Thread
from app.models.reply import Reply
from app.utils.cookie_manager import CookieManager
from app import db
import os
import uuid
from PIL import Image
from datetime import datetime

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(file_path):
    """处理上传的图片"""
    try:
        with Image.open(file_path) as img:
            # 限制图片大小
            max_size = (800, 600)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 转换为RGB模式(如果是RGBA)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # 保存处理后的图片
            img.save(file_path, 'JPEG', quality=85, optimize=True)
            return True
    except Exception as e:
        print(f"Image processing error: {e}")
        return False

@api_bp.route('/threads', methods=['POST'])
def create_thread():
    """创建新串"""
    try:
        # 获取饼干ID
        cookie_id = CookieManager.get_or_create_cookie(request)
        
        # 获取表单数据
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        if not title or not content:
            return jsonify({'error': '标题和内容不能为空'}), 400
        
        if len(title) > 100:
            return jsonify({'error': '标题过长'}), 400
        
        # 处理图片上传
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # 生成唯一文件名
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{file_ext}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                # 保存文件
                file.save(file_path)
                
                # 处理图片
                if process_image(file_path):
                    image_url = f"/uploads/{filename}"
                else:
                    os.remove(file_path)  # 删除处理失败的文件
        
        # 创建串
        thread = Thread(
            title=title,
            content=content,
            cookie_id=cookie_id,
            image_url=image_url
        )
        
        db.session.add(thread)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'thread_id': thread.id,
            'message': '串创建成功！'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建失败: {str(e)}'}), 500

@api_bp.route('/threads/<int:thread_id>/replies', methods=['POST'])
def create_reply(thread_id):
    """创建回复"""
    try:
        thread = Thread.query.get_or_404(thread_id)
        
        # 获取饼干ID
        cookie_id = CookieManager.get_or_create_cookie(request)
        
        # 获取表单数据
        content = request.form.get('content', '').strip()
        quote_id = request.form.get('quote_id', type=int)
        
        if not content:
            return jsonify({'error': '回复内容不能为空'}), 400
        
        # 处理图片上传
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # 生成唯一文件名
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{file_ext}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                
                # 保存文件
                file.save(file_path)
                
                # 处理图片
                if process_image(file_path):
                    image_url = f"/uploads/{filename}"
                else:
                    os.remove(file_path)
        
        # 创建回复
        reply = Reply(
            thread_id=thread_id,
            content=content,
            cookie_id=cookie_id,
            image_url=image_url,
            quote_id=quote_id
        )
        
        db.session.add(reply)
        
        # 更新串的回复计数和最后回复时间
        thread.reply_count += 1
        thread.last_reply_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'reply_id': reply.id,
            'message': '回复成功！'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'回复失败: {str(e)}'}), 500

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    """单独的图片上传接口"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # 生成唯一文件名
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # 保存文件
        file.save(file_path)
        
        # 处理图片
        if process_image(file_path):
            return jsonify({
                'success': True,
                'url': f"/uploads/{filename}"
            })
        else:
            os.remove(file_path)
            return jsonify({'error': '图片处理失败'}), 500
            
    except Exception as e:
        return jsonify({'error': f'上传失败: {str(e)}'}), 500 