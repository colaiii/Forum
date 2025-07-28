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
                "content": "这里是一个校园网匿名论坛，支持饼干系统。\n\n大家可以在这里自由讨论各种话题，请文明发言哦！\n\n**主要功能：**\n- 🍪 饼干系统（7天有效）\n- 📝 发串和回复\n- 🖼️ 图片上传\n- 💬 引用回复\n- 📌 置顶功能\n- 🔍 搜索功能\n\n> 让我们一起建设一个和谐的匿名交流社区！",
                "is_pinned": True
            },
            {
                "title": "【技术讨论】Python Flask 开发心得",
                "content": "最近在学习Flask框架，感觉很适合快速开发Web应用。\n\n有没有同学一起交流学习经验的？\n\n**分享一些学习资源：**\n1. Flask官方文档\n2. Miguel Grinberg的Flask教程\n3. 实战项目练习\n\n```python\nfrom flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return 'Hello, World!'\n```\n\n期待大家的经验分享！",
                "is_pinned": False
            },
            {
                "title": "【校园生活】食堂新菜品怎么样？",
                "content": "今天去食堂发现有新菜品，尝试了一下味道还不错！\n\n大家有什么推荐的食堂美食吗？\n\n**我个人比较喜欢：**\n- 红烧肉\n- 宫保鸡丁\n- 酸辣土豆丝\n\n> 友情提示：二楼新开了一家奶茶店，味道不错哦！",
                "is_pinned": False
            },
            {
                "title": "【学习交流】期末考试复习计划",
                "content": "期末考试快到了，大家都是怎么安排复习的？\n\n**我的计划：**\n1. 整理笔记\n2. 刷题练习\n3. 小组讨论\n4. 模拟考试\n\n有什么好的复习方法分享吗？大家一起加油！💪",
                "is_pinned": False
            },
            {
                "title": "【闲聊】最近看的好电影推荐",
                "content": "最近有什么好看的电影推荐吗？\n\n**我看了几部不错的：**\n- 《肖申克的救赎》⭐⭐⭐⭐⭐\n- 《阿甘正传》⭐⭐⭐⭐⭐\n- 《当幸福来敲门》⭐⭐⭐⭐\n\n大家最喜欢什么类型的电影？欢迎在回复中分享！",
                "is_pinned": False
            },
            {
                "title": "【求助】课程作业问题求解",
                "content": "最近有一道算法题卡住了，有没有大佬能帮忙看看？\n\n**题目描述：**\n给定一个数组，找出其中两个数的和等于目标值的所有组合。\n\n```\n输入: nums = [2,7,11,15], target = 9\n输出: [0,1]\n```\n\n我尝试了暴力解法，但时间复杂度太高了。求指导！🤔",
                "is_pinned": False
            }
        ]
        
        # 丰富的回复内容分类
        positive_replies = [
            "支持楼主！这个论坛看起来很不错",
            "同意楼主的观点，说得很有道理",
            "感谢分享，学到了很多东西",
            "这个想法很棒，值得推广",
            "楼主辛苦了，内容很详细",
            "非常有用的信息，收藏了！",
            "说得太对了，深有同感"
        ]
        
        technical_replies = [
            "Flask确实是个好框架，推荐大家学习",
            "我也在学Python，一起加油！",
            "建议配合SQLAlchemy使用，效果更好",
            "可以试试用Docker部署，很方便",
            "推荐看看官方文档，写得很详细",
            "这种写法很优雅，学习了",
            "有没有考虑过性能优化的问题？"
        ]
        
        campus_life_replies = [
            "食堂的红烧肉确实不错，推荐！",
            "推荐试试二楼的麻辣烫，味道很棒",
            "三楼的盖浇饭也很好吃",
            "图书馆新开的咖啡厅环境不错",
            "最近天气转凉，记得多穿衣服",
            "期末考试加油，大家都能过！",
            "这个活动我也想参加"
        ]
        
        study_replies = [
            "复习计划很重要，要早做准备",
            "我觉得刷题最有效果",
            "建议多做历年真题",
            "小组学习确实效率更高",
            "时间管理很关键",
            "记得劳逸结合，不要太累",
            "有什么不懂的可以问老师"
        ]
        
        entertainment_replies = [
            "电影推荐很棒，我也要去看看",
            "喜欢科幻片，有推荐吗？",
            "最近的新电影质量都不错",
            "这部电影我看过，确实很好",
            "推荐看看悬疑类的电影",
            "动画电影也有很多经典的",
            "期待你的更多推荐"
        ]
        
        help_replies = [
            "这个问题我之前也遇到过",
            "建议用双指针的方法解决",
            "可以先排序再查找",
            "哈希表是个不错的选择",
            "时间复杂度可以优化到O(n)",
            "这种题型在leetcode上有很多",
            "需要的话可以私信交流"
        ]
        
        general_replies = [
            "这个论坛功能很完善啊",
            "支持匿名讨论，很自由",
            "希望能多一些有趣的话题",
            "期待更多精彩内容",
            "界面设计很简洁美观",
            "饼干系统确实保护隐私",
            "感谢管理员的维护"
        ]
        
        # 引用回复内容（不包含>>标记）
        quote_replies = [
            "完全同意这个观点！",
            "说得很有道理，学习了",
            "确实是这样的",
            "你提到的这点很重要",
            "这个建议很实用",
            "感谢详细解释",
            "这个方法我试过，确实有效",
            "补充一点相关信息",
            "我有不同的看法",
            "可以展开讲讲吗？"
        ]
        
        # 创建演示串
        created_threads = []
        for i, thread_data in enumerate(demo_threads):
            cookie_id = CookieManager.generate_cookie_id()
            CookieManager.store_cookie(cookie_id)  # 注册饼干到系统
            
            # 串的创建时间设置为过去的时间
            thread_created_time = datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            
            thread = Thread(
                title=thread_data["title"],
                content=thread_data["content"],
                cookie_id=cookie_id,
                is_pinned=thread_data["is_pinned"],
                created_at=thread_created_time,
                last_reply_at=thread_created_time  # 初始设置为创建时间，后续会被回复更新
            )
            db.session.add(thread)
            created_threads.append(thread)
        
        db.session.commit()
        
        # 为每个串创建一些回复
        for thread_index, thread in enumerate(created_threads):
            reply_count = random.randint(3, 12)
            thread_replies = []
            
            # 根据串的主题选择合适的回复内容
            if "技术" in thread.title or "Python" in thread.title or "算法" in thread.title:
                reply_pool = technical_replies + help_replies + general_replies
            elif "食堂" in thread.title or "校园" in thread.title:
                reply_pool = campus_life_replies + general_replies
            elif "考试" in thread.title or "学习" in thread.title:
                reply_pool = study_replies + general_replies
            elif "电影" in thread.title or "闲聊" in thread.title:
                reply_pool = entertainment_replies + general_replies
            elif "求助" in thread.title:
                reply_pool = help_replies + technical_replies
            else:
                reply_pool = positive_replies + general_replies
            
            # 为了确保时间逻辑正确，先生成所有回复时间，然后排序
            reply_times = []
            for j in range(reply_count):
                # 回复时间在串创建时间之后的随机时间
                min_minutes_after = 1  # 至少1分钟后
                max_minutes_after = min(120, (datetime.utcnow() - thread.created_at).total_seconds() // 60)  # 最多到现在
                if max_minutes_after <= min_minutes_after:
                    max_minutes_after = min_minutes_after + 30
                
                reply_time = thread.created_at + timedelta(minutes=random.randint(min_minutes_after, int(max_minutes_after)))
                reply_times.append(reply_time)
            
            # 按时间排序，确保回复按时间顺序
            reply_times.sort()
            
            for j in range(reply_count):
                cookie_id = CookieManager.generate_cookie_id()
                CookieManager.store_cookie(cookie_id)  # 注册饼干到系统
                
                # 决定是否引用以及引用内容
                quote_id = None
                if j > 2 and random.random() < 0.25:  # 25%概率引用前面的回复
                    if thread_replies:
                        quoted_reply = random.choice(thread_replies)
                        quote_id = quoted_reply.id
                        reply_content = random.choice(quote_replies)
                    else:
                        reply_content = random.choice(reply_pool)
                else:
                    reply_content = random.choice(reply_pool)
                
                reply = Reply(
                    thread_id=thread.id,
                    content=reply_content,
                    cookie_id=cookie_id,
                    quote_id=quote_id,
                    created_at=reply_times[j]  # 使用排序后的时间
                )
                db.session.add(reply)
                thread_replies.append(reply)
                thread.reply_count += 1
            
            # 更新串的最后回复时间为最新回复时间（循环结束后设置）
            if reply_times:
                thread.last_reply_at = reply_times[-1]  # 最后一个（最新的）回复时间
        
        db.session.commit()
        
        # 输出统计信息
        total_threads = len(demo_threads)
        total_replies = Reply.query.count()
        pinned_count = sum(1 for t in demo_threads if t["is_pinned"])
        
        print("✅ 演示数据创建完成！")
        print(f"📊 创建了 {total_threads} 个串 (其中 {pinned_count} 个置顶)")
        print(f"💬 创建了 {total_replies} 个回复")
        print(f"🔗 包含引用关系的回复")
        print(f"🎨 使用了Markdown格式内容")
        print("\n🌐 现在可以访问论坛查看演示效果了！")
        print("💡 提示：演示数据包含了丰富的内容类型和引用关系")

if __name__ == "__main__":
    create_demo_data() 