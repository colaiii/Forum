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
        
        # 检查发串频率限制
        is_allowed, current_attempts, wait_time = CookieManager.check_thread_rate_limit(cookie_id)
        
        if not is_allowed:
            return jsonify({
                'error': f'发串过于频繁，请等待 {wait_time} 秒后再试（1分钟内最多发3串）',
                'rate_limit': {
                    'exceeded': True,
                    'current_attempts': current_attempts,
                    'max_attempts': CookieManager.THREAD_RATE_LIMIT,
                    'wait_time': wait_time,
                    'window_minutes': CookieManager.THREAD_RATE_WINDOW // 60
                }
            }), 429  # Too Many Requests
        
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
        
        # 记录发串行为（在成功创建后）
        CookieManager.record_thread_creation(cookie_id)
        
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
        
        # 检查回复频率限制
        is_allowed, current_attempts, wait_time = CookieManager.check_reply_rate_limit(cookie_id)
        
        if not is_allowed:
            return jsonify({
                'error': f'回复过于频繁，请等待 {wait_time} 秒后再试（1分钟内最多回复5次）',
                'rate_limit': {
                    'exceeded': True,
                    'current_attempts': current_attempts,
                    'max_attempts': CookieManager.REPLY_RATE_LIMIT,
                    'wait_time': wait_time,
                    'window_minutes': CookieManager.REPLY_RATE_WINDOW // 60
                }
            }), 429  # Too Many Requests
        
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
        
        # 记录回复行为（在成功创建后）
        CookieManager.record_reply_creation(cookie_id)
        
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

@api_bp.route('/cookie/set', methods=['POST'])
def set_cookie():
    """设置指定的饼干"""
    try:
        data = request.get_json()
        cookie_id = data.get('cookie_id', '').strip()
        
        if not cookie_id:
            return jsonify({'error': '饼干ID不能为空'}), 400
        
        if len(cookie_id) != 16:
            return jsonify({'error': '饼干ID必须是16位'}), 400
        
        # 验证饼干ID格式（只允许字母数字）
        import re
        if not re.match(r'^[a-fA-F0-9]{16}$', cookie_id):
            return jsonify({'error': '饼干ID格式无效'}), 400
        
        # 设置饼干到Redis（如果Redis可用）
        CookieManager.store_cookie(cookie_id)
        
        return jsonify({
            'success': True,
            'cookie_id': cookie_id,
            'message': '饼干设置成功'
        })
        
    except Exception as e:
        return jsonify({'error': f'设置失败: {str(e)}'}), 500

@api_bp.route('/cookie/new', methods=['POST'])
def generate_new_cookie():
    """生成新的饼干"""
    try:
        # 生成新饼干
        new_cookie = CookieManager.generate_cookie_id()
        CookieManager.store_cookie(new_cookie)
        
        return jsonify({
            'success': True,
            'cookie_id': new_cookie,
            'message': '新饼干生成成功'
        })
        
    except Exception as e:
        return jsonify({'error': f'生成失败: {str(e)}'}), 500

@api_bp.route('/cookie/validate', methods=['POST'])
def validate_cookie():
    """验证饼干是否有效"""
    try:
        data = request.get_json()
        cookie_id = data.get('cookie_id', '').strip()
        
        if not cookie_id:
            return jsonify({'error': '饼干ID不能为空'}), 400
        
        is_valid = CookieManager.is_valid_cookie(cookie_id)
        is_registered = CookieManager.is_cookie_registered(cookie_id)
        cookie_info = CookieManager.get_cookie_info(cookie_id)
        
        return jsonify({
            'success': True,
            'cookie_id': cookie_id,
            'is_valid': is_valid,
            'is_registered': is_registered,
            'cookie_info': cookie_info,
            'message': '验证完成'
        })
        
    except Exception as e:
        return jsonify({'error': f'验证失败: {str(e)}'}), 500

@api_bp.route('/cookie/check_registration', methods=['POST'])
def check_cookie_registration():
    """检查饼干是否在系统中注册"""
    try:
        # 获取客户端IP
        client_ip = request.environ.get('HTTP_X_REAL_IP', request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))
        if ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        # 检查速率限制
        is_allowed, current_attempts, wait_time = CookieManager.check_import_rate_limit(client_ip)
        
        if not is_allowed:
            return jsonify({
                'success': False,
                'error': f'导入尝试过于频繁，请等待 {wait_time} 秒后再试',
                'rate_limit': {
                    'exceeded': True,
                    'current_attempts': current_attempts,
                    'max_attempts': CookieManager.IMPORT_RATE_LIMIT,
                    'wait_time': wait_time,
                    'window_minutes': CookieManager.IMPORT_RATE_WINDOW // 60
                }
            }), 429  # Too Many Requests
        
        data = request.get_json()
        cookie_id = data.get('cookie_id', '').strip()
        
        if not cookie_id:
            return jsonify({'error': '饼干ID不能为空'}), 400
        
        if len(cookie_id) != 16:
            return jsonify({'error': '饼干ID必须是16位'}), 400
        
        # 验证饼干ID格式
        import re
        if not re.match(r'^[a-fA-F0-9]{16}$', cookie_id):
            return jsonify({'error': '饼干ID格式无效'}), 400
        
        # 记录这次尝试（在验证格式后）
        CookieManager.record_import_attempt(client_ip)
        
        is_registered = CookieManager.is_cookie_registered(cookie_id)
        is_valid = CookieManager.is_valid_cookie(cookie_id) if is_registered else False
        cookie_info = CookieManager.get_cookie_info(cookie_id) if is_registered else None
        
        # 获取更新后的速率限制信息
        rate_info = CookieManager.get_import_attempts_info(client_ip)
        
        if not is_registered:
            return jsonify({
                'success': False,
                'error': '此饼干未在系统中注册，无法导入',
                'rate_limit': rate_info
            }), 400
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': '此饼干已过期或无效，无法导入',
                'rate_limit': rate_info
            }), 400
        
        return jsonify({
            'success': True,
            'cookie_id': cookie_id,
            'is_registered': is_registered,
            'is_valid': is_valid,
            'cookie_info': cookie_info,
            'message': '饼干验证通过，可以导入',
            'rate_limit': rate_info
        })
        
    except Exception as e:
        return jsonify({'error': f'检查失败: {str(e)}'}), 500

@api_bp.route('/cookie/import_rate_info', methods=['GET'])
def get_import_rate_info():
    """获取导入饼干的速率限制信息"""
    try:
        # 获取客户端IP
        client_ip = request.environ.get('HTTP_X_REAL_IP', request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))
        if ',' in client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        # 获取速率限制信息
        rate_info = CookieManager.get_import_attempts_info(client_ip)
        
        return jsonify({
            'success': True,
            'rate_limit': rate_info
        })
        
    except Exception as e:
        return jsonify({'error': f'获取信息失败: {str(e)}'}), 500

@api_bp.route('/cookie/thread_rate_info', methods=['GET'])
def get_thread_rate_info():
    """获取发串频率限制信息"""
    try:
        # 获取饼干ID
        cookie_id = CookieManager.get_or_create_cookie(request)
        
        # 获取发串频率限制信息
        rate_info = CookieManager.get_thread_rate_info(cookie_id)
        
        return jsonify({
            'success': True,
            'rate_limit': rate_info
        })
        
    except Exception as e:
        return jsonify({'error': f'获取信息失败: {str(e)}'}), 500

@api_bp.route('/cookie/reply_rate_info', methods=['GET'])
def get_reply_rate_info():
    """获取回复频率限制信息"""
    try:
        # 获取饼干ID
        cookie_id = CookieManager.get_or_create_cookie(request)
        
        # 获取回复频率限制信息
        rate_info = CookieManager.get_reply_rate_info(cookie_id)
        
        return jsonify({
            'success': True,
            'rate_limit': rate_info
        })
        
    except Exception as e:
        return jsonify({'error': f'获取信息失败: {str(e)}'}), 500

@api_bp.route('/cookie/stats', methods=['GET'])
def get_cookie_stats():
    """获取饼干系统统计信息"""
    try:
        total_registered = CookieManager.get_registered_cookies_count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_registered_cookies': total_registered,
                'message': f'系统中共有 {total_registered} 个已注册的饼干'
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'获取统计失败: {str(e)}'}), 500 