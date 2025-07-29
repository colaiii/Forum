# -*- coding: utf-8 -*-
"""
板块分类配置和工具函数
"""

# 板块配置
CATEGORIES = {
    'timeline': {
        'name': '时间线',
        'description': '展示所有板块的串',
        'icon': '🏠',
        'color': '#007bff'
    },
    'academic': {
        'name': '学术',
        'description': '学术讨论、学习交流、课程分享',
        'icon': '📚',
        'color': '#28a745'
    },
    'life': {
        'name': '生活',
        'description': '日常生活、校园生活、美食分享',
        'icon': '🍎',
        'color': '#fd7e14'
    },
    'game': {
        'name': '游戏',
        'description': '游戏讨论、攻略分享、组队交友',
        'icon': '🎮',
        'color': '#e83e8c'
    },
    'creative': {
        'name': '创作',
        'description': '原创作品、文学创作、艺术分享',
        'icon': '🎨',
        'color': '#6f42c1'
    }
}

# 板块顺序
CATEGORY_ORDER = ['timeline', 'academic', 'life', 'game', 'creative']

def get_category_info(category_key):
    """获取板块信息"""
    return CATEGORIES.get(category_key, CATEGORIES['timeline'])

def get_category_name(category_key):
    """获取板块名称"""
    return get_category_info(category_key)['name']

def get_category_icon(category_key):
    """获取板块图标"""
    return get_category_info(category_key)['icon']

def get_category_color(category_key):
    """获取板块颜色"""
    return get_category_info(category_key)['color']

def get_category_list():
    """获取所有板块列表"""
    return [(key, CATEGORIES[key]) for key in CATEGORY_ORDER]

def is_valid_category(category_key):
    """检查是否是有效的板块"""
    return category_key in CATEGORIES 