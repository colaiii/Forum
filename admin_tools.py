#!/usr/bin/env python3
"""
论坛管理工具脚本
用于清理和管理串的后台脚本

使用方法:
    python admin_tools.py list                    # 列出所有串
    python admin_tools.py delete --id 5          # 删除串ID为5的串
    python admin_tools.py delete-user --cookie abc123    # 删除用户所有串
    python admin_tools.py cleanup --days 30      # 清理30天前的串
    python admin_tools.py stats                  # 查看统计信息
    python admin_tools.py pin --id 5             # 设置串ID为5的串为置顶
    python admin_tools.py unpin --id 5           # 取消串ID为5的串的置顶
    python admin_tools.py list-pinned            # 列出所有置顶串
    python admin_tools.py batch-pin --ids 1,2,3  # 批量设置置顶串
    python admin_tools.py batch-unpin --ids 1,2,3 # 批量取消置顶串
"""

import os
import sys
import argparse
from datetime import datetime, timedelta

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.thread import Thread
from app.models.reply import Reply

def confirm_action(message):
    """确认操作"""
    response = input(f"{message} (输入 'yes' 确认): ").strip().lower()
    return response == 'yes'

def delete_thread_by_id(thread_id, force=False):
    """根据ID删除串"""
    app = create_app()
    with app.app_context():
        thread = Thread.query.get(thread_id)
        if not thread:
            print(f"❌ 串 {thread_id} 不存在")
            return False
        
        reply_count = thread.reply_count
        title = thread.title
        has_image = bool(thread.image_url)
        
        print(f"🎯 准备删除串:")
        print(f"   ID: {thread_id}")
        print(f"   标题: {title}")
        print(f"   回复数: {reply_count}")
        print(f"   有图片: {'是' if has_image else '否'}")
        print(f"   创建时间: {thread.created_at}")
        
        if not force and not confirm_action("⚠️  确认删除此串及其所有回复？"):
            print("❌ 操作已取消")
            return False
        
        # 删除关联的图片文件
        if thread.image_url:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                    os.path.basename(thread.image_url))
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"🗑️  删除图片文件: {os.path.basename(image_path)}")
        
        # 删除串（会级联删除所有回复）
        db.session.delete(thread)
        db.session.commit()
        print(f"✅ 成功删除串 {thread_id}: {title} (含 {reply_count} 个回复)")
        return True

def delete_threads_by_cookie(cookie_id, force=False):
    """删除特定饼干的所有串"""
    app = create_app()
    with app.app_context():
        threads = Thread.query.filter_by(cookie_id=cookie_id).all()
        
        if not threads:
            print(f"❌ 未找到饼干 {cookie_id} 的串")
            return 0
        
        total_replies = sum(thread.reply_count for thread in threads)
        print(f"🎯 准备删除饼干 {cookie_id} 的所有串:")
        print(f"   串数量: {len(threads)}")
        print(f"   总回复数: {total_replies}")
        
        if not force and not confirm_action("⚠️  确认删除此用户的所有串？"):
            print("❌ 操作已取消")
            return 0
        
        deleted_count = 0
        for thread in threads:
            # 删除关联的图片文件
            if thread.image_url:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                        os.path.basename(thread.image_url))
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            print(f"🗑️  删除串: {thread.id} - {thread.title}")
            db.session.delete(thread)
            deleted_count += 1
        
        db.session.commit()
        print(f"✅ 成功删除 {deleted_count} 个串")
        return deleted_count

def cleanup_old_threads(days_old=30, force=False):
    """清理指定天数之前的串"""
    app = create_app()
    with app.app_context():
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        old_threads = Thread.query.filter(Thread.created_at < cutoff_date).all()
        
        if not old_threads:
            print(f"❌ 没有找到 {days_old} 天前的串")
            return 0
        
        total_replies = sum(thread.reply_count for thread in old_threads)
        print(f"🎯 准备清理 {days_old} 天前的串:")
        print(f"   截止日期: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   串数量: {len(old_threads)}")
        print(f"   总回复数: {total_replies}")
        
        if not force and not confirm_action(f"⚠️  确认清理 {days_old} 天前的所有串？"):
            print("❌ 操作已取消")
            return 0
        
        deleted_count = 0
        for thread in old_threads:
            # 删除关联的图片文件
            if thread.image_url:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                        os.path.basename(thread.image_url))
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            print(f"🗑️  删除旧串: {thread.id} - {thread.title} ({thread.created_at.strftime('%Y-%m-%d')})")
            db.session.delete(thread)
            deleted_count += 1
        
        db.session.commit()
        print(f"✅ 成功清理 {deleted_count} 个 {days_old} 天前的串")
        return deleted_count

def list_threads(limit=20, show_all=False):
    """列出串"""
    app = create_app()
    with app.app_context():
        query = Thread.query.order_by(Thread.created_at.desc())
        
        if not show_all:
            threads = query.limit(limit).all()
        else:
            threads = query.all()
        
        total = Thread.query.count()
        
        print(f"📊 共有 {total} 个串" + (f"，显示最新 {len(threads)} 个:" if not show_all else ":"))
        print("-" * 95)
        print(f"{'ID':>3} | {'标题':30} | {'回复':>4} | {'创建时间':16} | {'饼干ID':12}")
        print("-" * 95)
        
        for thread in threads:
            cookie_short = thread.cookie_id[:8] + "..." if len(thread.cookie_id) > 8 else thread.cookie_id
            title_short = thread.title[:28] + "..." if len(thread.title) > 28 else thread.title
            print(f"{thread.id:3d} | {title_short:30} | {thread.reply_count:4d} | {thread.created_at.strftime('%Y-%m-%d %H:%M')} | {cookie_short}")

def show_stats():
    """显示统计信息"""
    app = create_app()
    with app.app_context():
        total_threads = Thread.query.count()
        total_replies = Reply.query.count()
        
        # 最近7天的串数
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_threads = Thread.query.filter(Thread.created_at >= week_ago).count()
        
        # 最活跃的串
        most_active = Thread.query.order_by(Thread.reply_count.desc()).first()
        
        # 最新的串
        latest_thread = Thread.query.order_by(Thread.created_at.desc()).first()
        
        print("📊 论坛统计信息")
        print("=" * 50)
        print(f"总串数: {total_threads}")
        print(f"总回复数: {total_replies}")
        print(f"最近7天新串: {recent_threads}")
        print(f"平均每串回复数: {total_replies/total_threads:.1f}" if total_threads > 0 else "平均每串回复数: 0")
        
        if most_active:
            print(f"最活跃串: #{most_active.id} \"{most_active.title[:20]}...\" ({most_active.reply_count} 回复)")
        
        if latest_thread:
            print(f"最新串: #{latest_thread.id} \"{latest_thread.title[:20]}...\" ({latest_thread.created_at.strftime('%Y-%m-%d %H:%M')})")

def batch_delete_threads(thread_ids, force=False):
    """批量删除串"""
    app = create_app()
    with app.app_context():
        threads = Thread.query.filter(Thread.id.in_(thread_ids)).all()
        
        if not threads:
            print("❌ 未找到要删除的串")
            return 0
        
        found_ids = [t.id for t in threads]
        missing_ids = [tid for tid in thread_ids if tid not in found_ids]
        
        if missing_ids:
            print(f"⚠️  以下串ID不存在: {missing_ids}")
        
        total_replies = sum(thread.reply_count for thread in threads)
        print(f"🎯 准备批量删除 {len(threads)} 个串:")
        for thread in threads:
            print(f"   #{thread.id}: {thread.title} ({thread.reply_count} 回复)")
        print(f"   总回复数: {total_replies}")
        
        if not force and not confirm_action("⚠️  确认批量删除这些串？"):
            print("❌ 操作已取消")
            return 0
        
        deleted_count = 0
        for thread in threads:
            # 删除关联的图片文件
            if thread.image_url:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], 
                                        os.path.basename(thread.image_url))
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            print(f"🗑️  删除串: {thread.id} - {thread.title}")
            db.session.delete(thread)
            deleted_count += 1
        
        db.session.commit()
        print(f"✅ 成功删除 {deleted_count} 个串")
        return deleted_count

def pin_thread(thread_id, force=False):
    """设置串为置顶"""
    app = create_app()
    with app.app_context():
        thread = Thread.query.get(thread_id)
        if not thread:
            print(f"❌ 串 {thread_id} 不存在")
            return False
        
        if thread.is_pinned:
            print(f"⚠️  串 {thread_id} 已经是置顶状态")
            return False
        
        print(f"📌 准备设置置顶串:")
        print(f"   ID: {thread_id}")
        print(f"   标题: {thread.title}")
        print(f"   回复数: {thread.reply_count}")
        print(f"   创建时间: {thread.created_at}")
        
        if not force and not confirm_action("⚠️  确认设置此串为置顶？"):
            print("❌ 操作已取消")
            return False
        
        thread.is_pinned = True
        db.session.commit()
        print(f"✅ 成功设置串 {thread_id}: {thread.title} 为置顶")
        return True

def unpin_thread(thread_id, force=False):
    """取消串的置顶状态"""
    app = create_app()
    with app.app_context():
        thread = Thread.query.get(thread_id)
        if not thread:
            print(f"❌ 串 {thread_id} 不存在")
            return False
        
        if not thread.is_pinned:
            print(f"⚠️  串 {thread_id} 不是置顶状态")
            return False
        
        print(f"📌 准备取消置顶串:")
        print(f"   ID: {thread_id}")
        print(f"   标题: {thread.title}")
        print(f"   回复数: {thread.reply_count}")
        print(f"   创建时间: {thread.created_at}")
        
        if not force and not confirm_action("⚠️  确认取消此串的置顶状态？"):
            print("❌ 操作已取消")
            return False
        
        thread.is_pinned = False
        db.session.commit()
        print(f"✅ 成功取消串 {thread_id}: {thread.title} 的置顶状态")
        return True

def list_pinned_threads():
    """列出所有置顶串"""
    app = create_app()
    with app.app_context():
        pinned_threads = Thread.query.filter_by(is_pinned=True).order_by(Thread.created_at.desc()).all()
        
        if not pinned_threads:
            print("📌 当前没有置顶串")
            return
        
        print(f"📌 共有 {len(pinned_threads)} 个置顶串:")
        print("-" * 95)
        print(f"{'ID':>3} | {'标题':30} | {'回复':>4} | {'创建时间':16} | {'饼干ID':12}")
        print("-" * 95)
        
        for thread in pinned_threads:
            cookie_short = thread.cookie_id[:8] + "..." if len(thread.cookie_id) > 8 else thread.cookie_id
            title_short = thread.title[:28] + "..." if len(thread.title) > 28 else thread.title
            print(f"{thread.id:3d} | {title_short:30} | {thread.reply_count:4d} | {thread.created_at.strftime('%Y-%m-%d %H:%M')} | {cookie_short}")

def batch_pin_threads(thread_ids, force=False):
    """批量设置置顶串"""
    app = create_app()
    with app.app_context():
        threads = Thread.query.filter(Thread.id.in_(thread_ids)).all()
        
        if not threads:
            print("❌ 未找到要设置置顶的串")
            return 0
        
        found_ids = [t.id for t in threads]
        missing_ids = [tid for tid in thread_ids if tid not in found_ids]
        
        if missing_ids:
            print(f"⚠️  以下串ID不存在: {missing_ids}")
        
        # 筛选出非置顶串
        non_pinned_threads = [t for t in threads if not t.is_pinned]
        already_pinned = [t for t in threads if t.is_pinned]
        
        if already_pinned:
            print(f"⚠️  以下串已经是置顶状态: {[t.id for t in already_pinned]}")
        
        if not non_pinned_threads:
            print("❌ 没有需要设置置顶的串")
            return 0
        
        print(f"📌 准备批量设置 {len(non_pinned_threads)} 个串为置顶:")
        for thread in non_pinned_threads:
            print(f"   #{thread.id}: {thread.title} ({thread.reply_count} 回复)")
        
        if not force and not confirm_action("⚠️  确认批量设置这些串为置顶？"):
            print("❌ 操作已取消")
            return 0
        
        pinned_count = 0
        for thread in non_pinned_threads:
            thread.is_pinned = True
            print(f"📌 设置置顶: {thread.id} - {thread.title}")
            pinned_count += 1
        
        db.session.commit()
        print(f"✅ 成功设置 {pinned_count} 个串为置顶")
        return pinned_count

def batch_unpin_threads(thread_ids, force=False):
    """批量取消置顶串"""
    app = create_app()
    with app.app_context():
        threads = Thread.query.filter(Thread.id.in_(thread_ids)).all()
        
        if not threads:
            print("❌ 未找到要取消置顶的串")
            return 0
        
        found_ids = [t.id for t in threads]
        missing_ids = [tid for tid in thread_ids if tid not in found_ids]
        
        if missing_ids:
            print(f"⚠️  以下串ID不存在: {missing_ids}")
        
        # 筛选出置顶串
        pinned_threads = [t for t in threads if t.is_pinned]
        not_pinned = [t for t in threads if not t.is_pinned]
        
        if not_pinned:
            print(f"⚠️  以下串不是置顶状态: {[t.id for t in not_pinned]}")
        
        if not pinned_threads:
            print("❌ 没有需要取消置顶的串")
            return 0
        
        print(f"📌 准备批量取消 {len(pinned_threads)} 个串的置顶状态:")
        for thread in pinned_threads:
            print(f"   #{thread.id}: {thread.title} ({thread.reply_count} 回复)")
        
        if not force and not confirm_action("⚠️  确认批量取消这些串的置顶状态？"):
            print("❌ 操作已取消")
            return 0
        
        unpinned_count = 0
        for thread in pinned_threads:
            thread.is_pinned = False
            print(f"📌 取消置顶: {thread.id} - {thread.title}")
            unpinned_count += 1
        
        db.session.commit()
        print(f"✅ 成功取消 {unpinned_count} 个串的置顶状态")
        return unpinned_count

def main():
    parser = argparse.ArgumentParser(description='论坛管理工具', 
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   epilog="""
使用示例:
  python admin_tools.py list                    # 列出最新20个串
  python admin_tools.py list --all              # 列出所有串
  python admin_tools.py delete --id 5           # 删除串ID为5的串
  python admin_tools.py delete-user --cookie abc123    # 删除用户所有串
  python admin_tools.py cleanup --days 30       # 清理30天前的串
  python admin_tools.py batch --ids 1,2,3       # 批量删除串
  python admin_tools.py stats                   # 查看统计信息
  python admin_tools.py pin --id 5              # 设置串ID为5的串为置顶
  python admin_tools.py unpin --id 5            # 取消串ID为5的串的置顶
  python admin_tools.py list-pinned             # 列出所有置顶串
  python admin_tools.py batch-pin --ids 1,2,3   # 批量设置置顶串
  python admin_tools.py batch-unpin --ids 1,2,3 # 批量取消置顶串
""")
    
    parser.add_argument('action', 
                       choices=['list', 'delete', 'delete-user', 'cleanup', 'stats', 'batch', 
                               'pin', 'unpin', 'list-pinned', 'batch-pin', 'batch-unpin'], 
                       help='要执行的操作')
    
    parser.add_argument('--id', type=int, help='串ID')
    parser.add_argument('--cookie', type=str, help='饼干ID')
    parser.add_argument('--days', type=int, default=30, help='清理多少天前的串 (默认30天)')
    parser.add_argument('--ids', type=str, help='批量操作的串ID列表，用逗号分隔，如: 1,2,3')
    parser.add_argument('--all', action='store_true', help='显示所有串（仅用于list）')
    parser.add_argument('--force', action='store_true', help='强制执行，跳过确认')
    
    args = parser.parse_args()
    
    print("🛠️  论坛管理工具")
    print("=" * 50)
    
    try:
        if args.action == 'list':
            list_threads(show_all=args.all)
        
        elif args.action == 'delete':
            if not args.id:
                print("❌ 请提供串ID: --id <thread_id>")
                return 1
            delete_thread_by_id(args.id, args.force)
        
        elif args.action == 'delete-user':
            if not args.cookie:
                print("❌ 请提供饼干ID: --cookie <cookie_id>")
                return 1
            delete_threads_by_cookie(args.cookie, args.force)
        
        elif args.action == 'cleanup':
            cleanup_old_threads(args.days, args.force)
        
        elif args.action == 'batch':
            if not args.ids:
                print("❌ 请提供串ID列表: --ids 1,2,3")
                return 1
            try:
                thread_ids = [int(x.strip()) for x in args.ids.split(',')]
                batch_delete_threads(thread_ids, args.force)
            except ValueError:
                print("❌ 串ID格式错误，请使用逗号分隔的数字，如: 1,2,3")
                return 1
        
        elif args.action == 'stats':
            show_stats()
        
        elif args.action == 'pin':
            if not args.id:
                print("❌ 请提供串ID: --id <thread_id>")
                return 1
            pin_thread(args.id, args.force)
        
        elif args.action == 'unpin':
            if not args.id:
                print("❌ 请提供串ID: --id <thread_id>")
                return 1
            unpin_thread(args.id, args.force)
        
        elif args.action == 'list-pinned':
            list_pinned_threads()
        
        elif args.action == 'batch-pin':
            if not args.ids:
                print("❌ 请提供串ID列表: --ids 1,2,3")
                return 1
            try:
                thread_ids = [int(x.strip()) for x in args.ids.split(',')]
                batch_pin_threads(thread_ids, args.force)
            except ValueError:
                print("❌ 串ID格式错误，请使用逗号分隔的数字，如: 1,2,3")
                return 1
        
        elif args.action == 'batch-unpin':
            if not args.ids:
                print("❌ 请提供串ID列表: --ids 1,2,3")
                return 1
            try:
                thread_ids = [int(x.strip()) for x in args.ids.split(',')]
                batch_unpin_threads(thread_ids, args.force)
            except ValueError:
                print("❌ 串ID格式错误，请使用逗号分隔的数字，如: 1,2,3")
                return 1
        
        print("\n✨ 操作完成！")
        return 0
        
    except Exception as e:
        print(f"\n💥 操作失败: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 