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
    IMPORT_RATE_LIMIT = 3  # 每分钟最多尝试3次导入
    IMPORT_RATE_WINDOW = 60  # 速率限制时间窗口(秒)
    THREAD_RATE_LIMIT = 3  # 每分钟最多发3串
    THREAD_RATE_WINDOW = 60  # 发串速率限制时间窗口(秒)
    REPLY_RATE_LIMIT = 5  # 每分钟最多发5条回复
    REPLY_RATE_WINDOW = 60  # 回复速率限制时间窗口(秒)
    
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
    
    @staticmethod
    def check_import_rate_limit(client_ip):
        """检查导入饼干的速率限制"""
        if not redis_client:
            return True, 0, 0  # Redis不可用时不限制
        
        try:
            # 使用IP地址作为限制键
            rate_key = f"import_rate_limit:{client_ip}"
            current_time = int(time.time())
            window_start = current_time - CookieManager.IMPORT_RATE_WINDOW
            
            # 清理过期的尝试记录
            redis_client.zremrangebyscore(rate_key, 0, window_start)
            
            # 获取当前时间窗口内的尝试次数
            attempts = redis_client.zcard(rate_key)
            
            if attempts >= CookieManager.IMPORT_RATE_LIMIT:
                # 计算还需要等待的时间
                oldest_attempt = redis_client.zrange(rate_key, 0, 0, withscores=True)
                if oldest_attempt:
                    wait_time = int(oldest_attempt[0][1]) + CookieManager.IMPORT_RATE_WINDOW - current_time
                    return False, attempts, max(0, wait_time)
                else:
                    return False, attempts, CookieManager.IMPORT_RATE_WINDOW
            
            return True, attempts, 0
            
        except Exception as e:
            print(f"Error checking rate limit: {e}")
            return True, 0, 0  # 发生错误时不限制
    
    @staticmethod
    def record_import_attempt(client_ip):
        """记录一次导入尝试"""
        if not redis_client:
            return
        
        try:
            rate_key = f"import_rate_limit:{client_ip}"
            current_time = int(time.time())
            
            # 记录这次尝试
            redis_client.zadd(rate_key, {str(current_time): current_time})
            
            # 设置键的过期时间，自动清理
            redis_client.expire(rate_key, CookieManager.IMPORT_RATE_WINDOW * 2)
            
        except Exception as e:
            print(f"Error recording import attempt: {e}")
            pass
    
    @staticmethod
    def get_import_attempts_info(client_ip):
        """获取导入尝试信息"""
        if not redis_client:
            return {
                'current_attempts': 0,
                'max_attempts': CookieManager.IMPORT_RATE_LIMIT,
                'window_minutes': CookieManager.IMPORT_RATE_WINDOW // 60,
                'remaining_attempts': CookieManager.IMPORT_RATE_LIMIT,
                'reset_time': None
            }
        
        try:
            rate_key = f"import_rate_limit:{client_ip}"
            current_time = int(time.time())
            window_start = current_time - CookieManager.IMPORT_RATE_WINDOW
            
            # 清理过期记录
            redis_client.zremrangebyscore(rate_key, 0, window_start)
            
            # 获取当前尝试次数
            attempts = redis_client.zcard(rate_key)
            remaining = max(0, CookieManager.IMPORT_RATE_LIMIT - attempts)
            
            # 计算重置时间
            reset_time = None
            if attempts > 0:
                oldest_attempt = redis_client.zrange(rate_key, 0, 0, withscores=True)
                if oldest_attempt:
                    reset_time = int(oldest_attempt[0][1]) + CookieManager.IMPORT_RATE_WINDOW
            
            return {
                'current_attempts': attempts,
                'max_attempts': CookieManager.IMPORT_RATE_LIMIT,
                'window_minutes': CookieManager.IMPORT_RATE_WINDOW // 60,
                'remaining_attempts': remaining,
                'reset_time': reset_time
            }
            
        except Exception as e:
            print(f"Error getting import attempts info: {e}")
            return {
                'current_attempts': 0,
                'max_attempts': CookieManager.IMPORT_RATE_LIMIT,
                'window_minutes': CookieManager.IMPORT_RATE_WINDOW // 60,
                'remaining_attempts': CookieManager.IMPORT_RATE_LIMIT,
                'reset_time': None
            }
    
    @staticmethod
    def check_thread_rate_limit(cookie_id):
        """检查发串的速率限制"""
        if not redis_client:
            return True, 0, 0  # Redis不可用时不限制
        
        try:
            # 使用饼干ID作为限制键
            rate_key = f"thread_rate_limit:{cookie_id}"
            current_time = int(time.time())
            window_start = current_time - CookieManager.THREAD_RATE_WINDOW
            
            # 清理过期的发串记录
            redis_client.zremrangebyscore(rate_key, 0, window_start)
            
            # 获取当前时间窗口内的发串次数
            attempts = redis_client.zcard(rate_key)
            
            if attempts >= CookieManager.THREAD_RATE_LIMIT:
                # 计算还需要等待的时间
                oldest_attempt = redis_client.zrange(rate_key, 0, 0, withscores=True)
                if oldest_attempt:
                    wait_time = int(oldest_attempt[0][1]) + CookieManager.THREAD_RATE_WINDOW - current_time
                    return False, attempts, max(0, wait_time)
                else:
                    return False, attempts, CookieManager.THREAD_RATE_WINDOW
            
            return True, attempts, 0
            
        except Exception as e:
            print(f"Error checking thread rate limit: {e}")
            return True, 0, 0  # 发生错误时不限制
    
    @staticmethod
    def record_thread_creation(cookie_id):
        """记录一次发串行为"""
        if not redis_client:
            return
        
        try:
            rate_key = f"thread_rate_limit:{cookie_id}"
            current_time = int(time.time())
            
            # 记录这次发串
            redis_client.zadd(rate_key, {str(current_time): current_time})
            
            # 设置键的过期时间，自动清理
            redis_client.expire(rate_key, CookieManager.THREAD_RATE_WINDOW * 2)
            
        except Exception as e:
            print(f"Error recording thread creation: {e}")
            pass
    
    @staticmethod
    def get_thread_rate_info(cookie_id):
        """获取发串频率信息"""
        if not redis_client:
            return {
                'current_attempts': 0,
                'max_attempts': CookieManager.THREAD_RATE_LIMIT,
                'window_minutes': CookieManager.THREAD_RATE_WINDOW // 60,
                'remaining_attempts': CookieManager.THREAD_RATE_LIMIT,
                'reset_time': None
            }
        
        try:
            rate_key = f"thread_rate_limit:{cookie_id}"
            current_time = int(time.time())
            window_start = current_time - CookieManager.THREAD_RATE_WINDOW
            
            # 清理过期记录
            redis_client.zremrangebyscore(rate_key, 0, window_start)
            
            # 获取当前发串次数
            attempts = redis_client.zcard(rate_key)
            remaining = max(0, CookieManager.THREAD_RATE_LIMIT - attempts)
            
            # 计算重置时间
            reset_time = None
            if attempts > 0:
                oldest_attempt = redis_client.zrange(rate_key, 0, 0, withscores=True)
                if oldest_attempt:
                    reset_time = int(oldest_attempt[0][1]) + CookieManager.THREAD_RATE_WINDOW
            
            return {
                'current_attempts': attempts,
                'max_attempts': CookieManager.THREAD_RATE_LIMIT,
                'window_minutes': CookieManager.THREAD_RATE_WINDOW // 60,
                'remaining_attempts': remaining,
                'reset_time': reset_time
            }
            
        except Exception as e:
            print(f"Error getting thread rate info: {e}")
            return {
                'current_attempts': 0,
                'max_attempts': CookieManager.THREAD_RATE_LIMIT,
                'window_minutes': CookieManager.THREAD_RATE_WINDOW // 60,
                'remaining_attempts': CookieManager.THREAD_RATE_LIMIT,
                'reset_time': None
            }
    
    @staticmethod
    def check_reply_rate_limit(cookie_id):
        """检查回复的速率限制"""
        if not redis_client:
            return True, 0, 0  # Redis不可用时不限制
        
        try:
            # 使用饼干ID作为限制键
            rate_key = f"reply_rate_limit:{cookie_id}"
            current_time = int(time.time())
            window_start = current_time - CookieManager.REPLY_RATE_WINDOW
            
            # 清理过期的回复记录
            redis_client.zremrangebyscore(rate_key, 0, window_start)
            
            # 获取当前时间窗口内的回复次数
            attempts = redis_client.zcard(rate_key)
            
            if attempts >= CookieManager.REPLY_RATE_LIMIT:
                # 计算还需要等待的时间
                oldest_attempt = redis_client.zrange(rate_key, 0, 0, withscores=True)
                if oldest_attempt:
                    wait_time = int(oldest_attempt[0][1]) + CookieManager.REPLY_RATE_WINDOW - current_time
                    return False, attempts, max(0, wait_time)
                else:
                    return False, attempts, CookieManager.REPLY_RATE_WINDOW
            
            return True, attempts, 0
            
        except Exception as e:
            print(f"Error checking reply rate limit: {e}")
            return True, 0, 0  # 发生错误时不限制
    
    @staticmethod
    def record_reply_creation(cookie_id):
        """记录一次回复行为"""
        if not redis_client:
            return
        
        try:
            rate_key = f"reply_rate_limit:{cookie_id}"
            current_time = int(time.time())
            
            # 记录这次回复
            redis_client.zadd(rate_key, {str(current_time): current_time})
            
            # 设置键的过期时间，自动清理
            redis_client.expire(rate_key, CookieManager.REPLY_RATE_WINDOW * 2)
            
        except Exception as e:
            print(f"Error recording reply creation: {e}")
            pass
    
    @staticmethod
    def get_reply_rate_info(cookie_id):
        """获取回复频率信息"""
        if not redis_client:
            return {
                'current_attempts': 0,
                'max_attempts': CookieManager.REPLY_RATE_LIMIT,
                'window_minutes': CookieManager.REPLY_RATE_WINDOW // 60,
                'remaining_attempts': CookieManager.REPLY_RATE_LIMIT,
                'reset_time': None
            }
        
        try:
            rate_key = f"reply_rate_limit:{cookie_id}"
            current_time = int(time.time())
            window_start = current_time - CookieManager.REPLY_RATE_WINDOW
            
            # 清理过期记录
            redis_client.zremrangebyscore(rate_key, 0, window_start)
            
            # 获取当前回复次数
            attempts = redis_client.zcard(rate_key)
            remaining = max(0, CookieManager.REPLY_RATE_LIMIT - attempts)
            
            # 计算重置时间
            reset_time = None
            if attempts > 0:
                oldest_attempt = redis_client.zrange(rate_key, 0, 0, withscores=True)
                if oldest_attempt:
                    reset_time = int(oldest_attempt[0][1]) + CookieManager.REPLY_RATE_WINDOW
            
            return {
                'current_attempts': attempts,
                'max_attempts': CookieManager.REPLY_RATE_LIMIT,
                'window_minutes': CookieManager.REPLY_RATE_WINDOW // 60,
                'remaining_attempts': remaining,
                'reset_time': reset_time
            }
            
        except Exception as e:
            print(f"Error getting reply rate info: {e}")
            return {
                'current_attempts': 0,
                'max_attempts': CookieManager.REPLY_RATE_LIMIT,
                'window_minutes': CookieManager.REPLY_RATE_WINDOW // 60,
                'remaining_attempts': CookieManager.REPLY_RATE_LIMIT,
                'reset_time': None
            }