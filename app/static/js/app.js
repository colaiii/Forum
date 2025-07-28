// 图片弹窗功能
function showImageModal(src) {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    
    if (modal && modalImg) {
        modal.style.display = 'block';
        modalImg.src = src;
        
        // 防止事件冒泡
        event.stopPropagation();
    }
}

function hideImageModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// 规则弹窗功能
function showRulesModal() {
    const modal = document.getElementById('rulesModal');
    if (modal) {
        modal.style.display = 'block';
        // 防止页面滚动
        document.body.style.overflow = 'hidden';
    }
}

function hideRulesModal() {
    const modal = document.getElementById('rulesModal');
    if (modal) {
        modal.style.display = 'none';
        // 恢复页面滚动
        document.body.style.overflow = 'auto';
    }
}

// 饼干管理功能
class CookieManager {
    static STORAGE_KEY = 'forum_saved_cookies';
    static GENERATION_KEY = 'forum_cookie_generations';
    static MAX_SAVED_COOKIES = 3;  // 最多收藏3个饼干
    static MAX_DAILY_GENERATIONS = 3;  // 24小时内最多生成3个饼干
    
    // 显示饼干管理器
    static show() {
        const modal = document.getElementById('cookieManagerModal');
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
            this.loadCookieData();
        }
    }
    
    // 隐藏饼干管理器
    static hide() {
        const modal = document.getElementById('cookieManagerModal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }
    
    // 获取当前饼干
    static getCurrentCookie() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'forum_cookie') {
                return value;
            }
        }
        return null;
    }
    
    // 生成饼干颜色
    static generateCookieColor(cookieId) {
        const colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', 
            '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
            '#BB8FCE', '#85C1E9', '#82E0AA', '#F8C471'
        ];
        
        // 简单的哈希算法
        let hash = 0;
        for (let i = 0; i < cookieId.length; i++) {
            hash = ((hash << 5) - hash + cookieId.charCodeAt(i)) & 0xffffffff;
        }
        return colors[Math.abs(hash) % colors.length];
    }
    
    // 获取保存的饼干列表
    static getSavedCookies() {
        try {
            const saved = localStorage.getItem(this.STORAGE_KEY);
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            console.error('获取保存的饼干失败:', e);
            return [];
        }
    }
    
    // 获取饼干生成记录
    static getCookieGenerations() {
        try {
            const generations = localStorage.getItem(this.GENERATION_KEY);
            return generations ? JSON.parse(generations) : [];
        } catch (e) {
            console.error('获取饼干生成记录失败:', e);
            return [];
        }
    }
    
    // 保存饼干生成记录
    static setCookieGenerations(generations) {
        try {
            localStorage.setItem(this.GENERATION_KEY, JSON.stringify(generations));
        } catch (e) {
            console.error('保存饼干生成记录失败:', e);
        }
    }
    
    // 检查今日生成次数
    static getTodayGenerationCount() {
        const generations = this.getCookieGenerations();
        const today = new Date();
        const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000);
        
        // 过滤出24小时内的生成记录
        const recentGenerations = generations.filter(gen => {
            const genTime = new Date(gen.timestamp);
            return genTime > yesterday;
        });
        
        // 清理过期记录
        if (recentGenerations.length !== generations.length) {
            this.setCookieGenerations(recentGenerations);
        }
        
        return recentGenerations.length;
    }
    
    // 记录饼干生成
    static recordCookieGeneration(cookieId) {
        const generations = this.getCookieGenerations();
        generations.push({
            cookieId: cookieId,
            timestamp: new Date().toISOString()
        });
        this.setCookieGenerations(generations);
    }
    
    // 检查是否可以生成新饼干
    static canGenerateNewCookie() {
        return this.getTodayGenerationCount() < this.MAX_DAILY_GENERATIONS;
    }
    
    // 检查是否可以收藏更多饼干
    static canSaveMoreCookies() {
        return this.getSavedCookies().length < this.MAX_SAVED_COOKIES;
    }
    
    // 保存饼干列表
    static setSavedCookies(cookies) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cookies));
        } catch (e) {
            console.error('保存饼干失败:', e);
            showToast('保存失败：浏览器存储空间不足');
        }
    }
    
    // 保存当前饼干
    static saveCurrentCookie() {
        const currentCookie = this.getCurrentCookie();
        if (!currentCookie) {
            showToast('没有找到当前饼干');
            return;
        }
        
        const savedCookies = this.getSavedCookies();
        
        // 检查是否已经保存
        if (savedCookies.find(c => c.id === currentCookie)) {
            showToast('该饼干已经在收藏列表中');
            return;
        }
        
        // 检查收藏数量限制
        if (!this.canSaveMoreCookies()) {
            showToast(`最多只能收藏${this.MAX_SAVED_COOKIES}个饼干，请先删除其他饼干`);
            return;
        }
        
        // 生成默认名称
        const defaultName = `饼干 ${currentCookie.substring(0, 8)}`;
        const name = prompt('给这个饼干起个名字:', defaultName);
        
        if (name === null) return; // 用户取消
        
        const cookieData = {
            id: currentCookie,
            name: name.trim() || defaultName,
            color: this.generateCookieColor(currentCookie),
            savedAt: new Date().toISOString()
        };
        
        savedCookies.push(cookieData);
        this.setSavedCookies(savedCookies);
        this.loadCookieData();
        showToast('饼干已保存到收藏');
    }
    
    // 删除保存的饼干
    static deleteSavedCookie(cookieId) {
        if (!confirm('确定要删除这个饼干吗？')) return;
        
        const savedCookies = this.getSavedCookies();
        const filtered = savedCookies.filter(c => c.id !== cookieId);
        this.setSavedCookies(filtered);
        this.loadCookieData();
        showToast('饼干已删除');
    }
    
    // 使用保存的饼干
    static useSavedCookie(cookieId) {
        if (!confirm('确定要切换到这个饼干吗？页面将刷新。')) return;
        
        // 设置饼干
        const expiry = new Date();
        expiry.setTime(expiry.getTime() + (7 * 24 * 60 * 60 * 1000)); // 7天
        document.cookie = `forum_cookie=${cookieId}; expires=${expiry.toUTCString()}; path=/`;
        
        showToast('饼干已切换，页面即将刷新...');
        setTimeout(() => {
            location.reload();
        }, 1000);
    }
    
    // 生成新饼干
    static generateNewCookie() {
        // 检查生成次数限制
        if (!this.canGenerateNewCookie()) {
            const remainingTime = this.getRemainingTimeForGeneration();
            showToast(`24小时内最多生成${this.MAX_DAILY_GENERATIONS}个饼干，${remainingTime}后可再次生成`);
            return;
        }
        
        if (!confirm('确定要生成新饼干吗？当前饼干将失效，页面将刷新。')) return;
        
        // 记录生成行为（使用临时ID，实际ID由服务器生成）
        this.recordCookieGeneration('temp_' + Date.now());
        
        // 清除当前饼干
        document.cookie = 'forum_cookie=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
        
        showToast('正在生成新饼干，页面即将刷新...');
        setTimeout(() => {
            location.reload();
        }, 1000);
    }
    
    // 获取下次可生成时间
    static getRemainingTimeForGeneration() {
        const generations = this.getCookieGenerations();
        if (generations.length === 0) return '现在';
        
        const oldestGeneration = generations.reduce((oldest, gen) => {
            return new Date(gen.timestamp) < new Date(oldest.timestamp) ? gen : oldest;
        });
        
        const nextGenerationTime = new Date(new Date(oldestGeneration.timestamp).getTime() + 24 * 60 * 60 * 1000);
        const now = new Date();
        
        if (nextGenerationTime <= now) return '现在';
        
        const diffMs = nextGenerationTime - now;
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        
        if (diffHours > 0) {
            return `${diffHours}小时${diffMinutes}分钟`;
        } else {
            return `${diffMinutes}分钟`;
        }
    }
    
    // 导入饼干
    static async importCookie() {
        const cookieId = document.getElementById('importCookieId').value.trim();
        const cookieName = document.getElementById('importCookieName').value.trim();
        
        if (!cookieId) {
            showToast('请输入饼干ID');
            return;
        }
        
        if (cookieId.length !== 16) {
            showToast('饼干ID必须是16位');
            return;
        }
        
        const savedCookies = this.getSavedCookies();
        
        // 检查是否已存在
        if (savedCookies.find(c => c.id === cookieId)) {
            showToast('该饼干已在收藏列表中');
            return;
        }
        
        // 检查收藏数量限制
        if (!this.canSaveMoreCookies()) {
            showToast(`最多只能收藏${this.MAX_SAVED_COOKIES}个饼干，请先删除其他饼干`);
            return;
        }
        
        // 先验证饼干是否在系统中注册
        showToast('正在验证饼干...');
        
        try {
            const response = await fetch('/api/cookie/check_registration', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    cookie_id: cookieId
                })
            });
            
            const result = await response.json();
            
            if (!result.success) {
                showToast(result.error || '饼干验证失败');
                return;
            }
            
            // 验证通过，可以导入
            const defaultName = cookieName || `饼干 ${cookieId.substring(0, 8)}`;
            const cookieData = {
                id: cookieId,
                name: defaultName,
                color: this.generateCookieColor(cookieId),
                savedAt: new Date().toISOString(),
                // 添加服务器返回的饼干信息
                serverInfo: result.cookie_info
            };
            
            savedCookies.push(cookieData);
            this.setSavedCookies(savedCookies);
            
            // 清空表单
            document.getElementById('importCookieId').value = '';
            document.getElementById('importCookieName').value = '';
            
            this.loadCookieData();
            showToast('饼干导入成功');
            
        } catch (error) {
            console.error('验证饼干时出错:', error);
            showToast('网络错误，请检查连接后重试');
        }
    }
    
    // 编辑饼干名称
    static editCookieName(cookieId) {
        const savedCookies = this.getSavedCookies();
        const cookie = savedCookies.find(c => c.id === cookieId);
        
        if (!cookie) return;
        
        const newName = prompt('修改饼干名称:', cookie.name);
        if (newName === null || newName.trim() === '') return;
        
        cookie.name = newName.trim();
        this.setSavedCookies(savedCookies);
        this.loadCookieData();
        showToast('名称已更新');
    }
    
    // 加载饼干数据到界面
    static loadCookieData() {
        const currentCookie = this.getCurrentCookie();
        const savedCookies = this.getSavedCookies();
        
        // 更新当前饼干显示
        const currentCookieId = document.getElementById('currentCookieId');
        const currentCookieColor = document.getElementById('currentCookieColor');
        
        if (currentCookie) {
            currentCookieId.textContent = `ID:${currentCookie.substring(0, 8)}`;
            const color = this.generateCookieColor(currentCookie);
            currentCookieColor.style.cssText = `
                width: 20px; 
                height: 20px; 
                background-color: ${color}; 
                border-radius: 50%; 
                display: inline-block; 
                margin-left: 10px;
                border: 2px solid #fff;
                box-shadow: 0 0 0 1px #ccc;
            `;
        }
        
        // 更新保存的饼干列表
        const savedCookiesList = document.getElementById('savedCookiesList');
        const savedCookieCount = document.getElementById('savedCookieCount');
        
        savedCookieCount.textContent = `(${savedCookies.length}/${this.MAX_SAVED_COOKIES})`;
        
        if (savedCookies.length === 0) {
            savedCookiesList.innerHTML = '<div class="empty-message">暂无收藏的饼干</div>';
        } else {
            savedCookiesList.innerHTML = savedCookies.map(cookie => `
                <div class="cookie-item saved">
                    <div class="cookie-info">
                        <div class="cookie-id">ID:${cookie.id.substring(0, 8)}</div>
                        <div class="cookie-name">${cookie.name}</div>
                        <div class="cookie-color" style="width: 16px; height: 16px; background-color: ${cookie.color}; border-radius: 50%; display: inline-block; margin-left: 8px; border: 1px solid #ccc;"></div>
                        <div class="cookie-date">保存于: ${new Date(cookie.savedAt).toLocaleDateString()}</div>
                    </div>
                    <div class="cookie-actions">
                        <button class="btn btn-primary btn-small" onclick="CookieManager.useSavedCookie('${cookie.id}')">使用</button>
                        <button class="btn btn-secondary btn-small" onclick="CookieManager.editCookieName('${cookie.id}')">重命名</button>
                        <button class="btn btn-back btn-small" onclick="CookieManager.deleteSavedCookie('${cookie.id}')">删除</button>
                    </div>
                </div>
            `).join('');
        }
        
        // 更新生成次数显示和按钮状态
        const generationCount = document.getElementById('generationCount');
        const saveCookieBtn = document.getElementById('saveCookieBtn');
        const newCookieBtn = document.getElementById('newCookieBtn');
        
        const todayGenerations = this.getTodayGenerationCount();
        const canSave = this.canSaveMoreCookies();
        const canGenerate = this.canGenerateNewCookie();
        
        if (generationCount) {
            generationCount.textContent = `${todayGenerations}/${this.MAX_DAILY_GENERATIONS}`;
        }
        
        // 更新收藏按钮状态
        if (saveCookieBtn) {
            if (!canSave) {
                saveCookieBtn.disabled = true;
                saveCookieBtn.textContent = '收藏已满';
                saveCookieBtn.title = `最多只能收藏${this.MAX_SAVED_COOKIES}个饼干`;
            } else if (currentCookie && savedCookies.find(c => c.id === currentCookie)) {
                saveCookieBtn.disabled = true;
                saveCookieBtn.textContent = '已收藏';
                saveCookieBtn.title = '该饼干已在收藏列表中';
            } else {
                saveCookieBtn.disabled = false;
                saveCookieBtn.textContent = '收藏此饼干';
                saveCookieBtn.title = '';
            }
        }
        
        // 更新生成按钮状态
        if (newCookieBtn) {
            if (!canGenerate) {
                newCookieBtn.disabled = true;
                newCookieBtn.textContent = '今日已达上限';
                const remainingTime = this.getRemainingTimeForGeneration();
                newCookieBtn.title = `24小时内最多生成${this.MAX_DAILY_GENERATIONS}个饼干，${remainingTime}后可再次生成`;
            } else {
                newCookieBtn.disabled = false;
                newCookieBtn.textContent = '生成新饼干';
                newCookieBtn.title = '';
            }
        }
    }
}

// 全局函数供HTML调用
function showCookieManager() {
    CookieManager.show();
}

function hideCookieManager() {
    CookieManager.hide();
}

function saveCookie() {
    CookieManager.saveCurrentCookie();
}

function newCookie() {
    CookieManager.generateNewCookie();
}

function importCookie() {
    CookieManager.importCookie();
}

// 键盘事件处理
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        hideImageModal();
        hideRulesModal();
        hideCookieManager();
        
        // 隐藏回复表单
        const replyForm = document.getElementById('replyForm');
        if (replyForm && replyForm.style.display !== 'none') {
            if (typeof hideReplyForm === 'function') {
                hideReplyForm();
            }
        }
    }
});

// 自动调整文本域高度
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// 为所有文本域添加自动调整功能
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
    });
});

// 字符计数功能
function updateCharCount(input, countElement, maxLength) {
    const count = input.value.length;
    countElement.textContent = count;
    
    if (count > maxLength) {
        input.style.borderColor = '#e74c3c';
        countElement.style.color = '#e74c3c';
    } else if (count > maxLength * 0.8) {
        input.style.borderColor = '#f39c12';
        countElement.style.color = '#f39c12';
    } else {
        input.style.borderColor = '';
        countElement.style.color = '';
    }
}

// 图片上传预览
function handleImagePreview(input, previewElement) {
    const file = input.files[0];
    
    if (file) {
        // 检查文件类型
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            alert('不支持的文件格式，请选择 JPG、PNG、GIF 或 WebP 文件');
            input.value = '';
            return;
        }
        
        // 检查文件大小 (16MB)
        if (file.size > 16 * 1024 * 1024) {
            alert('文件大小超过16MB限制');
            input.value = '';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            previewElement.innerHTML = `
                <div class="preview-item">
                    <img src="${e.target.result}" alt="预览" style="max-width: 200px; max-height: 200px;">
                    <div class="preview-info">
                        <div>${file.name}</div>
                        <div>${(file.size / 1024 / 1024).toFixed(2)} MB</div>
                    </div>
                </div>
            `;
        };
        reader.readAsDataURL(file);
    } else {
        previewElement.innerHTML = '';
    }
}

// 时间格式化
function formatTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // 小于1分钟
    if (diff < 60000) {
        return '刚刚';
    }
    
    // 小于1小时
    if (diff < 3600000) {
        return Math.floor(diff / 60000) + '分钟前';
    }
    
    // 小于1天
    if (diff < 86400000) {
        return Math.floor(diff / 3600000) + '小时前';
    }
    
    // 小于7天
    if (diff < 604800000) {
        return Math.floor(diff / 86400000) + '天前';
    }
    
    // 超过7天显示具体日期
    return date.toLocaleDateString('zh-CN');
}

// 内容过滤 (简单的敏感词过滤)
function filterContent(content) {
    const badWords = ['垃圾', '傻逼', '操你妈']; // 示例敏感词
    let filtered = content;
    
    badWords.forEach(word => {
        const regex = new RegExp(word, 'gi');
        filtered = filtered.replace(regex, '*'.repeat(word.length));
    });
    
    return filtered;
}

// 复制功能
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('已复制到剪贴板');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showToast('已复制到剪贴板');
    } catch (err) {
        console.error('复制失败:', err);
        showToast('复制失败');
    }
    
    document.body.removeChild(textArea);
}

// 简单的消息提示
function showToast(message, duration = 3000) {
    // 移除已存在的toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #2c3e50;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 4px;
        z-index: 10000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        animation: slideInRight 0.3s ease;
    `;
    toast.textContent = message;
    
    // 添加CSS动画
    if (!document.querySelector('#toast-styles')) {
        const style = document.createElement('style');
        style.id = 'toast-styles';
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(toast);
    
    // 自动移除
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, duration);
}

// 表单提交防重复
function preventDoubleSubmit(form) {
    let isSubmitting = false;
    
    form.addEventListener('submit', function(e) {
        if (isSubmitting) {
            e.preventDefault();
            return false;
        }
        
        isSubmitting = true;
        
        // 禁用提交按钮
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            const originalText = submitBtn.textContent;
            submitBtn.textContent = '提交中...';
            
            // 5秒后恢复按钮状态
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
                isSubmitting = false;
            }, 5000);
        }
    });
}

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 为所有表单添加防重复提交
    const forms = document.querySelectorAll('form');
    forms.forEach(preventDoubleSubmit);
    
    // 更新相对时间显示
    const timeElements = document.querySelectorAll('.thread-time, .reply-time');
    timeElements.forEach(element => {
        const time = element.textContent;
        if (time && time.includes('-')) {
            // 这里可以添加相对时间显示逻辑
        }
    });
}); 