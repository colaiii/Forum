import hashlib
import random
import string
import time
from datetime import datetime, timedelta
from app import redis_client

class CookieManager:
    """饼干系统管理器"""
    
    COOKIE_EXPIRY = 86400  # 24小时
    
    @staticmethod
    def generate_cookie_id():
        """生成新的饼干ID"""
        timestamp = str(int(time.time()))
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        raw_str = f"{timestamp}{random_str}"
        return hashlib.md5(raw_str.encode()).hexdigest()[:16]
    
    @staticmethod
    def get_or_create_cookie(request):
        """获取或创建用户饼干"""
        # 尝试从请求中获取饼干
        cookie_id = request.cookies.get('forum_cookie')
        
        if cookie_id and CookieManager.is_valid_cookie(cookie_id):
            # 延长饼干有效期
            CookieManager.extend_cookie(cookie_id)
            return cookie_id
        
        # 创建新饼干
        new_cookie = CookieManager.generate_cookie_id()
        CookieManager.store_cookie(new_cookie)
        return new_cookie
    
    @staticmethod
    def is_valid_cookie(cookie_id):
        """检查饼干是否有效"""
        if not redis_client:
            return True  # 如果Redis不可用，默认有效
        
        try:
            return redis_client.exists(f"cookie:{cookie_id}")
        except:
            return True
    
    @staticmethod
    def store_cookie(cookie_id):
        """存储饼干到Redis"""
        if not redis_client:
            return
        
        try:
            redis_client.setex(f"cookie:{cookie_id}", CookieManager.COOKIE_EXPIRY, "1")
        except:
            pass
    
    @staticmethod
    def extend_cookie(cookie_id):
        """延长饼干有效期"""
        if not redis_client:
            return
        
        try:
            redis_client.expire(f"cookie:{cookie_id}", CookieManager.COOKIE_EXPIRY)
        except:
            pass
    
    @staticmethod
    def get_cookie_color(cookie_id):
        """为饼干生成颜色(用于显示区分)"""
        colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
            '#BB8FCE', '#85C1E9', '#82E0AA', '#F8C471'
        ]
        # 使用饼干ID的哈希值来选择颜色
        hash_val = int(hashlib.md5(cookie_id.encode()).hexdigest()[:8], 16)
        return colors[hash_val % len(colors)]
    
    @staticmethod
    def format_cookie_display(cookie_id):
        """格式化饼干显示ID"""
        return f"ID:{cookie_id[:8]}" 