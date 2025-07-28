import hashlib
import random
import string
import time
import json
from datetime import datetime, timedelta
from app import redis_client

class CookieManager:
    """饼干系统管理器"""
    
    COOKIE_EXPIRY = 86400 * 7  # 7天
    
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
            cookie_data_raw = redis_client.get(f"cookie:{cookie_id}")
            if not cookie_data_raw:
                return False
            
            # 尝试解析JSON数据
            try:
                cookie_data = json.loads(cookie_data_raw)
                # 检查饼干是否过期
                expires_at = datetime.fromisoformat(cookie_data['expires_at'])
                return datetime.utcnow() < expires_at and cookie_data.get('status') == 'active'
            except (json.JSONDecodeError, KeyError, ValueError):
                # 如果是旧格式数据，仍然认为有效
                return True
        except:
            return True
    
    @staticmethod
    def store_cookie(cookie_id):
        """存储饼干到Redis"""
        if not redis_client:
            return
        
        try:
            # 存储饼干的详细信息
            cookie_data = {
                'id': cookie_id,
                'created_at': datetime.utcnow().isoformat(),
                'expires_at': (datetime.utcnow() + timedelta(seconds=CookieManager.COOKIE_EXPIRY)).isoformat(),
                'status': 'active'
            }
            
            # 将饼干数据序列化为JSON存储
            redis_client.setex(f"cookie:{cookie_id}", CookieManager.COOKIE_EXPIRY, json.dumps(cookie_data))
            
            # 同时在饼干注册表中记录
            redis_client.sadd("registered_cookies", cookie_id)
            
        except Exception as e:
            print(f"Error storing cookie: {e}")
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
    
    @staticmethod
    def is_cookie_registered(cookie_id):
        """检查饼干是否在系统中注册"""
        if not redis_client:
            return True  # 如果Redis不可用，默认允许
        
        try:
            return redis_client.sismember("registered_cookies", cookie_id)
        except:
            return True
    
    @staticmethod
    def get_cookie_info(cookie_id):
        """获取饼干的详细信息"""
        if not redis_client:
            return None
        
        try:
            cookie_data_raw = redis_client.get(f"cookie:{cookie_id}")
            if not cookie_data_raw:
                return None
            
            try:
                return json.loads(cookie_data_raw)
            except json.JSONDecodeError:
                # 旧格式数据，返回基本信息
                return {
                    'id': cookie_id,
                    'created_at': 'unknown',
                    'expires_at': 'unknown',
                    'status': 'active'
                }
        except:
            return None
    
    @staticmethod
    def get_registered_cookies_count():
        """获取已注册饼干总数"""
        if not redis_client:
            return 0
        
        try:
            return redis_client.scard("registered_cookies")
        except:
            return 0