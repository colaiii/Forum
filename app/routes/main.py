from flask import Blueprint, render_template, request, make_response, redirect, url_for, flash
from app.models.thread import Thread
from app.models.reply import Reply
from app.utils.cookie_manager import CookieManager
from app.utils.categories import get_category_list, get_category_info, is_valid_category
from app import db
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/category/<category>')
def index(category='timeline'):
    """首页 - 显示串（支持板块筛选）"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 验证板块
    if not is_valid_category(category):
        category = 'timeline'
    
    # 获取或创建饼干
    cookie_id = CookieManager.get_or_create_cookie(request)
    
    # 根据板块筛选
    if category == 'timeline':
        # 时间线显示所有板块的串
        pinned_threads = Thread.query.filter_by(is_pinned=True).order_by(Thread.last_reply_at.desc()).all()
        normal_threads = Thread.query.filter_by(is_pinned=False).order_by(Thread.last_reply_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    else:
        # 特定板块只显示该板块的串
        pinned_threads = Thread.query.filter_by(is_pinned=True, category=category).order_by(Thread.last_reply_at.desc()).all()
        normal_threads = Thread.query.filter_by(is_pinned=False, category=category).order_by(Thread.last_reply_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    response = make_response(render_template('index.html', 
                                           pinned_threads=pinned_threads,
                                           threads=normal_threads,
                                           cookie_manager=CookieManager,
                                           current_category=category,
                                           category_info=get_category_info(category),
                                           categories=get_category_list()))
    
    # 设置饼干到浏览器
    response.set_cookie('forum_cookie', cookie_id, max_age=CookieManager.COOKIE_EXPIRY)
    
    return response

@main_bp.route('/thread/<int:thread_id>')
def view_thread(thread_id):
    """查看串详情"""
    thread = Thread.query.get(thread_id)
    if not thread:
        from flask import abort
        abort(404)
    
    # 获取或创建饼干
    cookie_id = CookieManager.get_or_create_cookie(request)
    
    # 获取回复
    replies = Reply.query.filter_by(thread_id=thread_id).order_by(Reply.created_at.asc()).all()
    
    response = make_response(render_template('thread.html', 
                                           thread=thread, 
                                           replies=replies,
                                           cookie_manager=CookieManager,
                                           category_info=get_category_info(thread.category),
                                           categories=get_category_list()))
    
    # 设置饼干到浏览器
    response.set_cookie('forum_cookie', cookie_id, max_age=CookieManager.COOKIE_EXPIRY)
    
    return response

@main_bp.route('/new')
@main_bp.route('/new/<category>')
def new_thread(category='timeline'):
    """新建串页面"""
    # 验证板块
    if not is_valid_category(category):
        category = 'timeline'
    
    cookie_id = CookieManager.get_or_create_cookie(request)
    
    response = make_response(render_template('new_thread.html', 
                                           cookie_manager=CookieManager,
                                           current_category=category,
                                           categories=get_category_list()))
    response.set_cookie('forum_cookie', cookie_id, max_age=CookieManager.COOKIE_EXPIRY)
    
    return response 

@main_bp.route('/search')
def search():
    """搜索串"""
    query = request.args.get('q', '').strip()
    search_type = request.args.get('type', 'all')
    category = request.args.get('category', 'timeline')
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 验证板块
    if not is_valid_category(category):
        category = 'timeline'
    
    # 获取或创建饼干
    cookie_id = CookieManager.get_or_create_cookie(request)
    
    results = None
    
    if query:
        # 构建搜索查询
        if search_type == 'title':
            # 仅搜索标题
            search_query = Thread.query.filter(
                Thread.title.contains(query)
            )
        elif search_type == 'content':
            # 仅搜索内容
            search_query = Thread.query.filter(
                Thread.content.contains(query)
            )
        else:
            # 搜索标题和内容
            search_query = Thread.query.filter(
                or_(
                    Thread.title.contains(query),
                    Thread.content.contains(query)
                )
            )
        
        # 如果不是时间线，添加板块筛选
        if category != 'timeline':
            search_query = search_query.filter(Thread.category == category)
        
        # 按照最后回复时间排序并分页
        results = search_query.order_by(Thread.last_reply_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
    
    response = make_response(render_template('search_results.html',
                                           query=query,
                                           search_type=search_type,
                                           results=results,
                                           cookie_manager=CookieManager,
                                           current_category=category,
                                           categories=get_category_list()))
    
    # 设置饼干到浏览器
    response.set_cookie('forum_cookie', cookie_id, max_age=CookieManager.COOKIE_EXPIRY)
    
    return response 