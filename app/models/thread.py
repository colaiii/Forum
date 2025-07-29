from app import db
from datetime import datetime
import json

class Thread(db.Model):
    __tablename__ = 'threads'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cookie_id = db.Column(db.String(32), nullable=False)  # 饼干ID
    image_urls = db.Column(db.Text, nullable=True)  # 图片URL列表（JSON格式）
    category = db.Column(db.String(20), nullable=False, default='timeline')  # 板块分类
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_reply_at = db.Column(db.DateTime, default=datetime.utcnow)
    reply_count = db.Column(db.Integer, default=0)
    is_pinned = db.Column(db.Boolean, default=False)
    
    # 关联回复
    replies = db.relationship('Reply', backref='thread', lazy=True, 
                            cascade='all, delete-orphan',
                            order_by='Reply.created_at')
    
    def get_image_urls(self):
        """获取图片URL列表"""
        if not self.image_urls:
            return []
        try:
            return json.loads(self.image_urls)
        except:
            return []
    
    def set_image_urls(self, urls):
        """设置图片URL列表"""
        if urls:
            self.image_urls = json.dumps(urls)
        else:
            self.image_urls = None
    
    @property
    def image_url(self):
        """向后兼容性：返回第一张图片URL"""
        urls = self.get_image_urls()
        return urls[0] if urls else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'cookie_id': self.cookie_id,
            'image_urls': self.get_image_urls(),
            'image_url': self.image_url,  # 向后兼容
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'last_reply_at': self.last_reply_at.isoformat(),
            'reply_count': self.reply_count,
            'is_pinned': self.is_pinned
        }
    
    def __repr__(self):
        return f'<Thread {self.id}: {self.title}>' 