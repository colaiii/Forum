from app import db
from datetime import datetime

class Reply(db.Model):
    __tablename__ = 'replies'
    
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cookie_id = db.Column(db.String(32), nullable=False)  # 饼干ID
    image_url = db.Column(db.String(255), nullable=True)  # 图片URL
    quote_id = db.Column(db.Integer, db.ForeignKey('replies.id'), nullable=True)  # 引用的回复ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 自引用关系 - 引用的回复
    quoted_reply = db.relationship('Reply', remote_side=[id], backref='quotes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'thread_id': self.thread_id,
            'content': self.content,
            'cookie_id': self.cookie_id,
            'image_url': self.image_url,
            'quote_id': self.quote_id,
            'created_at': self.created_at.isoformat(),
            'quoted_reply': self.quoted_reply.to_dict() if self.quoted_reply else None
        }
    
    def __repr__(self):
        return f'<Reply {self.id} to Thread {self.thread_id}>' 