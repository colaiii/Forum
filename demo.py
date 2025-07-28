#!/usr/bin/env python3
"""
演示数据生成脚本
创建一些示例串和回复来展示论坛功能
"""

import os
import sys
import random
from datetime import datetime, timedelta

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.thread import Thread
from app.models.reply import Reply
from app.utils.cookie_manager import CookieManager

def create_demo_data():
    """创建演示数据"""
    app = create_app()
    
    with app.app_context():
        print("🍪 正在创建演示数据...")
        
        # 清除现有数据
        Reply.query.delete()
        Thread.query.delete()
        db.session.commit()
        
        # 示例串标题和内容
        demo_threads = [
            {
                "title": "欢迎来到校园网匿名论坛！",
                "content": "这里是一个模仿A岛风格的匿名论坛，支持饼干系统。\n\n大家可以在这里自由讨论各种话题，请文明发言哦！\n\n主要功能：\n- 🍪 饼干系统（24小时有效）\n- 📝 发串和回复\n- 🖼️ 图片上传\n- 💬 引用回复\n- 📌 置顶功能",
                "is_pinned": True
            },
            {
                "title": "【技术讨论】Python Flask 开发心得",
                "content": "最近在学习Flask框架，感觉很适合快速开发Web应用。\n\n有没有同学一起交流学习经验的？\n\n分享一些学习资源：\n1. Flask官方文档\n2. Miguel Grinberg的Flask教程\n3. 实战项目练习",
                "is_pinned": False
            },
            {
                "title": "【校园生活】食堂新菜品怎么样？",
                "content": "今天去食堂发现有新菜品，尝试了一下味道还不错！\n\n大家有什么推荐的食堂美食吗？\n\n我个人比较喜欢：\n- 红烧肉\n- 宫保鸡丁\n- 酸辣土豆丝",
                "is_pinned": False
            },
            {
                "title": "【学习交流】期末考试复习计划",
                "content": "期末考试快到了，大家都是怎么安排复习的？\n\n我的计划：\n1. 整理笔记\n2. 刷题练习\n3. 小组讨论\n4. 模拟考试\n\n有什么好的复习方法分享吗？",
                "is_pinned": False
            },
            {
                "title": "【闲聊】最近看的好电影推荐",
                "content": "最近有什么好看的电影推荐吗？\n\n我看了几部不错的：\n- 《肖申克的救赎》\n- 《阿甘正传》\n- 《当幸福来敲门》\n\n大家最喜欢什么类型的电影？",
                "is_pinned": False
            }
        ]
        
        # 示例回复内容
        demo_replies = [
            "支持楼主！这个论坛看起来很不错",
            "饼干系统很有趣，确实保护了隐私",
            "界面设计很像A岛，很有意思",
            "Flask确实是个好框架，推荐！",
            "我也在学Python，一起加油！",
            "食堂的红烧肉确实不错",
            "推荐试试二楼的麻辣烫",
            "复习计划很重要，要早做准备",
            "我觉得刷题最有效果",
            "电影推荐很棒，我也要去看看",
            "喜欢科幻片，有推荐吗？",
            "这个论坛功能很完善啊",
            "支持匿名讨论，很自由",
            "希望能多一些技术讨论",
            "期待更多有趣的话题"
        ]
        
        # 创建演示串
        created_threads = []
        for i, thread_data in enumerate(demo_threads):
            cookie_id = CookieManager.generate_cookie_id()
            thread = Thread(
                title=thread_data["title"],
                content=thread_data["content"],
                cookie_id=cookie_id,
                is_pinned=thread_data["is_pinned"],
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48)),
                last_reply_at=datetime.utcnow() - timedelta(minutes=random.randint(1, 60))
            )
            db.session.add(thread)
            created_threads.append(thread)
        
        db.session.commit()
        
        # 为每个串创建一些回复
        for thread in created_threads:
            reply_count = random.randint(2, 8)
            for j in range(reply_count):
                cookie_id = CookieManager.generate_cookie_id()
                reply_content = random.choice(demo_replies)
                
                # 有30%概率引用前面的回复
                quote_id = None
                if j > 0 and random.random() < 0.3:
                    existing_replies = Reply.query.filter_by(thread_id=thread.id).all()
                    if existing_replies:
                        quote_id = random.choice(existing_replies).id
                        reply_content = f">>{quote_id}\n{reply_content}"
                
                reply = Reply(
                    thread_id=thread.id,
                    content=reply_content,
                    cookie_id=cookie_id,
                    quote_id=quote_id,
                    created_at=datetime.utcnow() - timedelta(minutes=random.randint(1, 30))
                )
                db.session.add(reply)
                thread.reply_count += 1
        
        db.session.commit()
        
        print("✅ 演示数据创建完成！")
        print(f"📊 创建了 {len(demo_threads)} 个串")
        print(f"💬 创建了若干回复")
        print("\n🌐 现在可以访问论坛查看演示效果了！")

if __name__ == "__main__":
    create_demo_data() 