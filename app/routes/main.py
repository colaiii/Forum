from flask import Blueprint, render_template, request, make_response, redirect, url_for, flash
from app.models.thread import Thread
from app.models.reply import Reply
from app.utils.cookie_manager import CookieManager
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首页 - 显示所有串"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 获取或创建饼干
    cookie_id = CookieManager.get_or_create_cookie(request)
    
    # 获取置顶串和普通串
    pinned_threads = Thread.query.filter_by(is_pinned=True).order_by(Thread.last_reply_at.desc()).all()
    normal_threads = Thread.query.filter_by(is_pinned=False).order_by(Thread.last_reply_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    response = make_response(render_template('index.html', 
                                           pinned_threads=pinned_threads,
                                           threads=normal_threads,
                                           cookie_manager=CookieManager))
    
    # 设置饼干到浏览器
    response.set_cookie('forum_cookie', cookie_id, max_age=CookieManager.COOKIE_EXPIRY)
    
    return response

@main_bp.route('/thread/<int:thread_id>')
def view_thread(thread_id):
    """查看串详情"""
    thread = Thread.query.get_or_404(thread_id)
    
    # 获取或创建饼干
    cookie_id = CookieManager.get_or_create_cookie(request)
    
    # 获取回复
    replies = Reply.query.filter_by(thread_id=thread_id).order_by(Reply.created_at.asc()).all()
    
    response = make_response(render_template('thread.html', 
                                           thread=thread, 
                                           replies=replies,
                                           cookie_manager=CookieManager))
    
    # 设置饼干到浏览器
    response.set_cookie('forum_cookie', cookie_id, max_age=CookieManager.COOKIE_EXPIRY)
    
    return response

@main_bp.route('/new')
def new_thread():
    """新建串页面"""
    cookie_id = CookieManager.get_or_create_cookie(request)
    
    response = make_response(render_template('new_thread.html', cookie_manager=CookieManager))
    response.set_cookie('forum_cookie', cookie_id, max_age=CookieManager.COOKIE_EXPIRY)
    
    return response 