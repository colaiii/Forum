from app import db
from datetime import datetime

class Thread(db.Model):
    __tablename__ = 'threads'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cookie_id = db.Column(db.String(32), nullable=False)  # 饼干ID
    image_url = db.Column(db.String(255), nullable=True)  # 图片URL
    category = db.Column(db.String(20), nullable=False, default='timeline')  # 板块分类
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_reply_at = db.Column(db.DateTime, default=datetime.utcnow)
    reply_count = db.Column(db.Integer, default=0)
    is_pinned = db.Column(db.Boolean, default=False)
    
    # 关联回复
    replies = db.relationship('Reply', backref='thread', lazy=True, 
                            cascade='all, delete-orphan',
                            order_by='Reply.created_at')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'cookie_id': self.cookie_id,
            'image_url': self.image_url,
            'category': self.category,
            'created_at': self.created_at.isoformat(),
            'last_reply_at': self.last_reply_at.isoformat(),
            'reply_count': self.reply_count,
            'is_pinned': self.is_pinned
        }
    
    def __repr__(self):
        return f'<Thread {self.id}: {self.title}>' 