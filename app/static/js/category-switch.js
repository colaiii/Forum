// 板块切换功能 - 无刷新加载
class CategorySwitcher {
    constructor() {
        this.currentCategory = null;
        this.isLoading = false;
        this.init();
    }
    
    init() {
        // 获取当前分类
        this.currentCategory = this.getCurrentCategoryFromURL();
        
        // 绑定事件
        this.bindEvents();
        
        // 监听浏览器前进后退
        window.addEventListener('popstate', this.handlePopState.bind(this));
    }
    
    getCurrentCategoryFromURL() {
        const path = window.location.pathname;
        const match = path.match(/\/category\/([^/?]+)/);
        return match ? match[1] : 'timeline';
    }
    
    bindEvents() {
        // 等待DOM完全加载后绑定事件
        const initEvents = () => {
            // 移除所有分类链接的onclick属性并绑定新事件
            const categoryItems = document.querySelectorAll('.category-item');
            categoryItems.forEach(item => {
                // 移除原有的onclick属性
                item.removeAttribute('onclick');
                
                // 添加新的点击事件监听器
                item.addEventListener('click', (event) => {
                    this.handleCategoryClick(event, item);
                });
            });
        };
        
        // 如果DOM已经加载完成，立即执行
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initEvents);
        } else {
            initEvents();
        }
    }
    
    handleCategoryClick(event, element) {
        event.preventDefault();
        
        if (this.isLoading) {
            return false;
        }
        
        // 获取目标分类
        const href = element.href;
        const categoryMatch = href.match(/\/category\/([^/?]+)/);
        const newCategory = categoryMatch ? categoryMatch[1] : 'timeline';
        
        // 如果是当前分类，不需要切换
        if (newCategory === this.currentCategory) {
            return false;
        }
        
        this.switchToCategory(newCategory);
        return false;
    }
    
    switchToCategory(category) {
        this.isLoading = true;
        
        // 停止自动刷新
        if (window.stopAutoRefresh) {
            window.stopAutoRefresh();
        }
        
        // 显示加载状态
        this.showLoading(true);
        
        // 加载新内容
        this.loadCategoryContent(category)
            .then((data) => {
                // 更新页面内容
                this.updatePageContent(data, category);
                
                // 更新URL
                const newUrl = category === 'timeline' ? '/' : '/category/' + category;
                history.pushState({category: category}, '', newUrl);
                
                // 更新当前分类
                this.currentCategory = category;
                
                // 隐藏加载状态
                this.showLoading(false);
                
                // 重新启动自动刷新
                setTimeout(() => {
                    if (window.startAutoRefresh) {
                        window.startAutoRefresh();
                    }
                }, 1000);
            })
            .catch((error) => {
                console.error('切换分类失败:', error);
                this.showError('切换分类失败');
                this.showLoading(false);
                
                // 降级为页面跳转
                setTimeout(() => {
                    const newUrl = category === 'timeline' ? '/' : '/category/' + category;
                    window.location.href = newUrl;
                }, 1000);
            })
            .finally(() => {
                this.isLoading = false;
            });
    }
    
    async loadCategoryContent(category) {
        const response = await fetch('/api/threads/latest?category=' + category + '&page=1');
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || '获取数据失败');
        }
        
        return data;
    }
    
    updatePageContent(data, category) {
        // 获取分类信息
        const categoryInfo = this.getCategoryInfo(category);
        
        // 更新页面标题
        this.updatePageTitle(categoryInfo);
        
        // 更新置顶串列表
        this.updatePinnedThreads(data.pinned_threads, category);
        
        // 更新普通串列表
        this.updateNormalThreads(data.normal_threads, category);
        
        // 更新分页
        this.updatePagination(data.pagination, category);
        
        // 更新搜索表单
        this.updateSearchForm(category);
        
        // 更新侧边栏激活状态
        this.updateSidebarActiveState(category);
    }
    
    getCategoryInfo(category) {
        const categories = {
            'timeline': { icon: '🏠', name: '首页', description: '最新的串和讨论' },
            'academic': { icon: '📚', name: '学术版', description: '学习、研究和学术讨论' },
            'life': { icon: '🌟', name: '生活版', description: '日常生活、分享和交流' },
            'game': { icon: '🎮', name: '游戏版', description: '游戏相关的讨论和分享' },
            'creative': { icon: '🎨', name: '创意版', description: '创意作品和艺术分享' }
        };
        return categories[category] || categories['timeline'];
    }
    
    updatePageTitle(categoryInfo) {
        const pageTitle = document.querySelector('.page-title h2');
        const pageDescription = document.querySelector('.page-description');
        
        if (pageTitle) {
            pageTitle.textContent = categoryInfo.icon + ' ' + categoryInfo.name;
        }
        if (pageDescription) {
            pageDescription.textContent = categoryInfo.description;
        }
    }
    
    updatePinnedThreads(pinnedThreads, currentCategory) {
        const pinnedSection = document.getElementById('pinnedSection');
        const pinnedList = document.getElementById('pinnedThreadsList');
        
        if (pinnedThreads.length === 0) {
            if (pinnedSection) {
                pinnedSection.style.display = 'none';
            }
            return;
        }
        
        if (pinnedSection) {
            pinnedSection.style.display = 'block';
        }
        
        if (pinnedList) {
            pinnedList.innerHTML = pinnedThreads.map(thread => 
                this.generateThreadHTML(thread, currentCategory, true)
            ).join('');
        }
    }
    
    updateNormalThreads(normalThreads, currentCategory) {
        const normalList = document.getElementById('normalThreadsList');
        
        if (normalList) {
            normalList.innerHTML = normalThreads.map(thread => 
                this.generateThreadHTML(thread, currentCategory, false)
            ).join('');
        }
    }
    
    generateThreadHTML(thread, currentCategory, isPinned) {
        const categoryTag = currentCategory === 'timeline' ? 
            '<span class="thread-category" style="background-color: rgba(0, 123, 255, 0.1); color: #007bff;">📝 ' + thread.category + '</span>' : '';
        
        const pinIcon = isPinned ? '<span class="thread-pin">📌</span>' : '';
        
        let imagesHtml = '';
        if (thread.image_urls && thread.image_urls.length > 0) {
            const imagesList = thread.image_urls.slice(0, 3).map(url => 
                '<div class="thread-image"><img src="' + url + '" alt="图片" onclick="event.stopPropagation(); showImageModal(\'' + url + '\');"></div>'
            ).join('');
            
            const moreImages = thread.image_urls.length > 3 ? 
                '<div class="more-images">+' + (thread.image_urls.length - 3) + '张图片</div>' : '';
                
            imagesHtml = '<div class="thread-images">' + imagesList + moreImages + '</div>';
        }
        
        return '<div class="thread-item ' + (isPinned ? 'pinned' : '') + '" onclick="goToThread(' + thread.id + ')" style="cursor: pointer;">' +
            '<div class="thread-header">' +
                '<span class="thread-id">No.' + thread.id + '</span>' +
                pinIcon +
                categoryTag +
                '<span class="thread-cookie" style="color: ' + thread.cookie_color + '">' + thread.cookie_display + '</span>' +
                '<span class="thread-time">' + thread.created_at + '</span>' +
            '</div>' +
            '<h4 class="thread-title">' +
                '<a href="/thread/' + thread.id + '" onclick="event.stopPropagation();">' + thread.title + '</a>' +
            '</h4>' +
            '<div class="thread-content">' +
                imagesHtml +
                '<div class="markdown-preview">' + thread.content + '</div>' +
            '</div>' +
            '<div class="thread-stats">' +
                '<span class="reply-count">💬 ' + thread.reply_count + '</span>' +
                '<span class="last-reply">最后回复: ' + thread.last_reply_at + '</span>' +
            '</div>' +
        '</div>';
    }
    
    updatePagination(pagination, category) {
        const paginationContainer = document.querySelector('.pagination');
        
        if (!paginationContainer || pagination.total_pages <= 1) {
            if (paginationContainer) {
                paginationContainer.style.display = 'none';
            }
            return;
        }
        
        paginationContainer.style.display = 'flex';
        
        let paginationHTML = '';
        
        // 上一页
        if (pagination.has_prev) {
            paginationHTML += '<a href="javascript:void(0)" class="page-btn" data-page="' + pagination.prev_num + '" data-category="' + category + '">« 上一页</a>';
        }
        
        // 页码
        for (let i = 1; i <= pagination.total_pages; i++) {
            if (i === pagination.current_page) {
                paginationHTML += '<span class="page-btn current">' + i + '</span>';
            } else {
                paginationHTML += '<a href="javascript:void(0)" class="page-btn" data-page="' + i + '" data-category="' + category + '">' + i + '</a>';
            }
        }
        
        // 下一页
        if (pagination.has_next) {
            paginationHTML += '<a href="javascript:void(0)" class="page-btn" data-page="' + pagination.next_num + '" data-category="' + category + '">下一页 »</a>';
        }
        
        paginationContainer.innerHTML = paginationHTML;
        
        // 为分页链接绑定事件
        const pageLinks = paginationContainer.querySelectorAll('.page-btn[data-page]');
        pageLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const page = parseInt(link.getAttribute('data-page'));
                const cat = link.getAttribute('data-category');
                this.loadPage(cat, page);
            });
        });
    }
    
    loadPage(category, page) {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.showLoading(true);
        
        fetch('/api/threads/latest?category=' + category + '&page=' + page)
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    throw new Error(data.error || '获取数据失败');
                }
                
                // 只更新内容区域，不更新标题和侧边栏
                this.updatePinnedThreads(data.pinned_threads, category);
                this.updateNormalThreads(data.normal_threads, category);
                this.updatePagination(data.pagination, category);
                
                // 更新URL
                const newUrl = category === 'timeline' ? 
                    '/?page=' + page : 
                    '/category/' + category + '?page=' + page;
                history.pushState({category: category, page: page}, '', newUrl);
                
                // 滚动到顶部
                window.scrollTo(0, 0);
                
                this.showLoading(false);
            })
            .catch(error => {
                console.error('加载页面失败:', error);
                this.showError('加载页面失败');
                this.showLoading(false);
            })
            .finally(() => {
                this.isLoading = false;
            });
    }
    
    updateSearchForm(category) {
        const categoryInput = document.querySelector('input[name="category"]');
        const searchInput = document.querySelector('.search-input');
        
        if (categoryInput) {
            categoryInput.value = category;
        }
        
        if (searchInput) {
            const categoryInfo = this.getCategoryInfo(category);
            searchInput.placeholder = '在' + categoryInfo.name + '中搜索...';
        }
    }
    
    updateSidebarActiveState(category) {
        // 移除所有激活状态
        document.querySelectorAll('.category-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // 添加新的激活状态
        const activeItem = document.querySelector('.category-item.category-' + category);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }
    
    showLoading(show) {
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        
        if (show) {
            sidebar.style.opacity = '0.7';
            sidebar.style.pointerEvents = 'none';
            mainContent.style.opacity = '0.7';
            this.showStatus('🔄 正在切换板块...');
        } else {
            sidebar.style.opacity = '1';
            sidebar.style.pointerEvents = 'auto';
            mainContent.style.opacity = '1';
        }
    }
    
    showStatus(message) {
        if (window.showRefreshStatus) {
            window.showRefreshStatus(message);
        }
    }
    
    showError(message) {
        if (window.showRefreshStatus) {
            window.showRefreshStatus('❌ ' + message);
        }
    }
    
    handlePopState(event) {
        if (event.state && event.state.category) {
            const category = event.state.category;
            const page = event.state.page || 1;
            
            if (page === 1) {
                this.switchToCategory(category);
            } else {
                this.loadPage(category, page);
            }
        }
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('CategorySwitcher: DOM加载完成，开始初始化');
    
    // 立即移除所有分类链接的onclick属性
    const categoryItems = document.querySelectorAll('.category-item');
    console.log('CategorySwitcher: 找到', categoryItems.length, '个分类链接');
    
    categoryItems.forEach(item => {
        if (item.hasAttribute('onclick')) {
            console.log('CategorySwitcher: 移除onclick属性:', item.className);
            item.removeAttribute('onclick');
        }
    });
    
    // 延迟初始化CategorySwitcher，确保事件绑定正确
    setTimeout(() => {
        console.log('CategorySwitcher: 开始初始化类');
        window.categorySwitcher = new CategorySwitcher();
    }, 100);
});

// 全局函数供HTML调用
function handleCategorySwitch(event, element) {
    // 这个函数现在由CategorySwitcher类处理，直接阻止默认行为
    console.log('CategorySwitcher: 旧的handleCategorySwitch被调用，阻止默认行为');
    event.preventDefault();
    event.stopPropagation();
    return false;
} 