// 移动端侧边栏控制函数
function toggleMobileSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (sidebar && overlay && menuBtn) {
        const isOpen = sidebar.classList.contains('mobile-open');
        
        if (isOpen) {
            closeMobileSidebar();
        } else {
            openMobileSidebar();
        }
    }
}

function openMobileSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (sidebar && overlay && menuBtn) {
        sidebar.classList.add('mobile-open');
        overlay.style.display = 'block';
        menuBtn.classList.add('active');
        document.body.style.overflow = 'hidden'; // 防止背景滚动
        
        // 延迟显示遮罩层的透明度动画
        setTimeout(() => {
            overlay.classList.add('active');
        }, 10);
    }
}

function closeMobileSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const menuBtn = document.querySelector('.mobile-menu-btn');
    
    if (sidebar && overlay && menuBtn) {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
        menuBtn.classList.remove('active');
        document.body.style.overflow = ''; // 恢复滚动
        
        // 延迟隐藏遮罩层
        setTimeout(() => {
            overlay.style.display = 'none';
        }, 300);
    }
}

// 监听窗口大小变化，在桌面端自动关闭移动端侧边栏
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        closeMobileSidebar();
    }
});

// 移动端按钮状态管理函数
function convertToBackButton(onClickAction) {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    
    if (mobileMenuBtn && window.innerWidth <= 768) {
        // 保存原始状态（如果还没有保存）
        if (!mobileMenuBtn.hasAttribute('data-original-state')) {
            mobileMenuBtn.setAttribute('data-original-state', 'true');
            mobileMenuBtn.setAttribute('data-original-onclick', mobileMenuBtn.getAttribute('onclick') || '');
            mobileMenuBtn.setAttribute('data-original-html', mobileMenuBtn.innerHTML);
        }
        
        // 修改按钮为返回按钮
        mobileMenuBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 12H5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 19L5 12L12 5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        
        // 移除原有事件并设置新的返回功能
        mobileMenuBtn.removeAttribute('onclick');
        
        // 移除现有的事件监听器
        const newBtn = mobileMenuBtn.cloneNode(true);
        mobileMenuBtn.parentNode.replaceChild(newBtn, mobileMenuBtn);
        
        // 设置新的点击事件
        newBtn.addEventListener('click', function() {
            eval(onClickAction);
        });
        
        newBtn.setAttribute('aria-label', '返回');
        newBtn.classList.add('back-btn');
        
        // 设置返回按钮样式
        newBtn.style.background = 'rgba(233, 76, 76, 0.9)';
        newBtn.style.width = '36px';
        newBtn.style.height = '36px';
        newBtn.style.padding = '6px';
        newBtn.style.position = 'absolute';
        newBtn.style.left = '12px';
        newBtn.style.top = '50%';
        newBtn.style.transform = 'translateY(-50%)';
    }
}

function restoreMenuButton() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    
    if (mobileMenuBtn && window.innerWidth <= 768 && mobileMenuBtn.hasAttribute('data-original-state')) {
        // 恢复原始HTML内容
        const originalHtml = mobileMenuBtn.getAttribute('data-original-html');
        const originalOnclick = mobileMenuBtn.getAttribute('data-original-onclick');
        
        mobileMenuBtn.innerHTML = originalHtml;
        
        // 恢复原始事件
        if (originalOnclick) {
            mobileMenuBtn.setAttribute('onclick', originalOnclick);
        } else {
            mobileMenuBtn.removeAttribute('onclick');
            // 重新绑定菜单切换功能
            const newBtn = mobileMenuBtn.cloneNode(true);
            mobileMenuBtn.parentNode.replaceChild(newBtn, mobileMenuBtn);
            newBtn.addEventListener('click', toggleMobileSidebar);
            mobileMenuBtn = newBtn;
        }
        
        mobileMenuBtn.setAttribute('aria-label', '切换菜单');
        mobileMenuBtn.classList.remove('back-btn');
        
        // 恢复原始样式
        mobileMenuBtn.style.background = 'rgba(255, 255, 255, 0.15)';
        mobileMenuBtn.style.width = '32px';
        mobileMenuBtn.style.height = '32px';
        mobileMenuBtn.style.padding = '5px';
        mobileMenuBtn.style.position = 'absolute';
        mobileMenuBtn.style.left = '12px';
        mobileMenuBtn.style.top = '50%';
        mobileMenuBtn.style.transform = 'translateY(-50%)';
        
        // 清除保存的状态
        mobileMenuBtn.removeAttribute('data-original-state');
        mobileMenuBtn.removeAttribute('data-original-onclick');
        mobileMenuBtn.removeAttribute('data-original-html');
    }
}

// 图片弹窗功能
function showImageModal(src) {
    // 先关闭其他弹窗
    const rulesModal = document.getElementById('rulesModal');
    const cookieModal = document.getElementById('cookieManagerModal');
    
    if (rulesModal && rulesModal.style.display === 'block') {
        hideRulesModal();
    }
    if (cookieModal && cookieModal.style.display === 'block') {
        hideCookieManager();
    }
    
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    
    if (modal && modalImg) {
        modal.style.display = 'block';
        modalImg.src = src;
        
        // 在移动端将按钮改为返回按钮
        if (typeof convertToBackButton === 'function') {
            convertToBackButton('hideImageModal()');
        }
        
        // 防止事件冒泡
        event.stopPropagation();
    }
}

function hideImageModal() {
    const modal = document.getElementById('imageModal');
    if (modal) {
        modal.style.display = 'none';
        // 恢复移动端按钮为菜单按钮
        if (typeof restoreMenuButton === 'function') {
            restoreMenuButton();
        }
    }
}

// 规则弹窗功能
function showRulesModal() {
    // 先关闭饼干管理器（如果打开的话）
    const cookieModal = document.getElementById('cookieManagerModal');
    if (cookieModal && cookieModal.style.display === 'block') {
        hideCookieManager();
    }
    
    const modal = document.getElementById('rulesModal');
    if (modal) {
        modal.style.display = 'block';
        // 防止页面滚动
        document.body.style.overflow = 'hidden';
        // 在移动端将按钮改为返回按钮
        convertToBackButton('hideRulesModal()');
    }
}

function hideRulesModal() {
    const modal = document.getElementById('rulesModal');
    if (modal) {
        modal.style.display = 'none';
        // 恢复页面滚动
        document.body.style.overflow = 'auto';
        // 恢复移动端按钮为菜单按钮
        restoreMenuButton();
    }
}

// 自定义确认弹窗
function customConfirm(message, title = '确认操作') {
    return new Promise((resolve) => {
        const modal = document.getElementById('customConfirmModal');
        const titleEl = document.getElementById('confirmTitle');
        const messageEl = document.getElementById('confirmMessage');
        const okBtn = document.getElementById('confirmOk');
        const cancelBtn = document.getElementById('confirmCancel');
        
        if (!modal || !titleEl || !messageEl || !okBtn || !cancelBtn) {
            // 如果自定义弹窗元素不存在，回退到原生confirm
            resolve(confirm(message));
            return;
        }
        
        titleEl.textContent = title;
        messageEl.textContent = message;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // 先关闭其他弹窗
        const rulesModal = document.getElementById('rulesModal');
        const cookieModal = document.getElementById('cookieManagerModal');
        const imageModal = document.getElementById('imageModal');
        
        if (rulesModal && rulesModal.style.display === 'block') {
            hideRulesModal();
        }
        if (cookieModal && cookieModal.style.display === 'block') {
            hideCookieManager();
        }
        if (imageModal && imageModal.style.display === 'block') {
            hideImageModal();
        }
        
        // 在移动端将按钮改为返回按钮
        if (typeof convertToBackButton === 'function') {
            convertToBackButton('document.getElementById("confirmCancel").click()');
        }
        
        const cleanup = () => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            okBtn.removeEventListener('click', handleOk);
            cancelBtn.removeEventListener('click', handleCancel);
            modal.removeEventListener('click', handleBackdrop);
            // 恢复移动端按钮为菜单按钮
            if (typeof restoreMenuButton === 'function') {
                restoreMenuButton();
            }
        };
        
        const handleOk = () => {
            cleanup();
            resolve(true);
        };
        
        const handleCancel = () => {
            cleanup();
            resolve(false);
        };
        
        const handleBackdrop = (e) => {
            if (e.target === modal) {
                handleCancel();
            }
        };
        
        okBtn.addEventListener('click', handleOk);
        cancelBtn.addEventListener('click', handleCancel);
        modal.addEventListener('click', handleBackdrop);
        
        // 自动聚焦到确定按钮
        setTimeout(() => okBtn.focus(), 100);
    });
}

// 自定义输入弹窗
function customPrompt(message, defaultValue = '', title = '输入信息') {
    return new Promise((resolve) => {
        const modal = document.getElementById('customPromptModal');
        const titleEl = document.getElementById('promptTitle');
        const messageEl = document.getElementById('promptMessage');
        const inputEl = document.getElementById('promptInput');
        const okBtn = document.getElementById('promptOk');
        const cancelBtn = document.getElementById('promptCancel');
        
        if (!modal || !titleEl || !messageEl || !inputEl || !okBtn || !cancelBtn) {
            // 如果自定义弹窗元素不存在，回退到原生prompt
            resolve(prompt(message, defaultValue));
            return;
        }
        
        titleEl.textContent = title;
        messageEl.textContent = message;
        inputEl.value = defaultValue;
        inputEl.placeholder = defaultValue;
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        
        // 先关闭其他弹窗
        const rulesModal = document.getElementById('rulesModal');
        const cookieModal = document.getElementById('cookieManagerModal');
        const imageModal = document.getElementById('imageModal');
        const confirmModal = document.getElementById('customConfirmModal');
        
        if (rulesModal && rulesModal.style.display === 'block') {
            hideRulesModal();
        }
        if (cookieModal && cookieModal.style.display === 'block') {
            hideCookieManager();
        }
        if (imageModal && imageModal.style.display === 'block') {
            hideImageModal();
        }
        if (confirmModal && confirmModal.style.display === 'block') {
            document.getElementById('confirmCancel').click();
        }
        
        // 在移动端将按钮改为返回按钮
        if (typeof convertToBackButton === 'function') {
            convertToBackButton('document.getElementById("promptCancel").click()');
        }
        
        const cleanup = () => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            okBtn.removeEventListener('click', handleOk);
            cancelBtn.removeEventListener('click', handleCancel);
            modal.removeEventListener('click', handleBackdrop);
            inputEl.removeEventListener('keydown', handleKeydown);
            // 恢复移动端按钮为菜单按钮
            if (typeof restoreMenuButton === 'function') {
                restoreMenuButton();
            }
        };
        
        const handleOk = () => {
            cleanup();
            resolve(inputEl.value.trim() || null);
        };
        
        const handleCancel = () => {
            cleanup();
            resolve(null);
        };
        
        const handleBackdrop = (e) => {
            if (e.target === modal) {
                handleCancel();
            }
        };
        
        const handleKeydown = (e) => {
            if (e.key === 'Enter') {
                handleOk();
            } else if (e.key === 'Escape') {
                handleCancel();
            }
        };
        
        okBtn.addEventListener('click', handleOk);
        cancelBtn.addEventListener('click', handleCancel);
        modal.addEventListener('click', handleBackdrop);
        inputEl.addEventListener('keydown', handleKeydown);
        
        // 自动聚焦到输入框并选中默认值
        setTimeout(() => {
            inputEl.focus();
            if (defaultValue) {
                inputEl.select();
            }
        }, 100);
    });
}

// 测试自定义弹窗功能
function testCustomModals() {
    console.log('测试自定义弹窗...');
    customConfirm('这是一个测试确认弹窗，文字应该正常显示').then(result => {
        console.log('确认弹窗结果:', result);
        if (result) {
            customPrompt('请输入测试内容:', '默认内容').then(input => {
                console.log('输入弹窗结果:', input);
                showToast('弹窗测试完成');
            });
        }
    });
}

// 饼干管理功能
class CookieManager {
    static STORAGE_KEY = 'forum_saved_cookies';
    static GENERATION_KEY = 'forum_cookie_generations';
    static MAX_SAVED_COOKIES = 3;  // 最多收藏3个饼干
    static MAX_DAILY_GENERATIONS = 3;  // 24小时内最多生成3个饼干
    
    // 显示饼干管理器
    static show() {
        // 先关闭规则弹窗（如果打开的话）
        const rulesModal = document.getElementById('rulesModal');
        if (rulesModal && rulesModal.style.display === 'block') {
            hideRulesModal();
        }
        
        const modal = document.getElementById('cookieManagerModal');
        if (modal) {
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
            this.loadCookieData();
            // 在移动端将按钮改为返回按钮
            if (typeof convertToBackButton === 'function') {
                convertToBackButton('hideCookieManager()');
            }
        }
    }
    
    // 隐藏饼干管理器
    static hide() {
        const modal = document.getElementById('cookieManagerModal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            // 恢复移动端按钮为菜单按钮
            if (typeof restoreMenuButton === 'function') {
                restoreMenuButton();
            }
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
    static async saveCurrentCookie() {
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
        const name = await customPrompt('给这个饼干起个名字:', defaultName);
        
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
    static async deleteSavedCookie(cookieId) {
        const confirmed = await customConfirm('确定要删除这个饼干吗？');
        if (!confirmed) return;
        
        const savedCookies = this.getSavedCookies();
        const filtered = savedCookies.filter(c => c.id !== cookieId);
        this.setSavedCookies(filtered);
        this.loadCookieData();
        showToast('饼干已删除');
    }
    
    // 使用保存的饼干
    static async useSavedCookie(cookieId) {
        const confirmed = await customConfirm('确定要切换到这个饼干吗？页面将刷新。');
        if (!confirmed) return;
        
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
    static async generateNewCookie() {
        // 检查生成次数限制
        if (!this.canGenerateNewCookie()) {
            const remainingTime = this.getRemainingTimeForGeneration();
            showToast(`24小时内最多生成${this.MAX_DAILY_GENERATIONS}个饼干，${remainingTime}后可再次生成`);
            return;
        }
        
        const confirmed = await customConfirm('确定要生成新饼干吗？当前饼干将失效，页面将刷新。');
        if (!confirmed) return;
        
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
            
            // 更新速率限制信息显示
            if (result.rate_limit) {
                this.updateRateLimitDisplay(result.rate_limit);
            }
            
            if (!result.success) {
                // 检查是否是速率限制错误
                if (response.status === 429) {
                    const waitTime = result.rate_limit?.wait_time || 60;
                    showToast(`导入尝试过于频繁，请等待 ${waitTime} 秒后再试`);
                    // 显示倒计时
                    this.showRateLimitCountdown(waitTime);
                } else {
                    showToast(result.error || '饼干验证失败');
                }
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
    
    // 更新速率限制显示
    static updateRateLimitDisplay(rateLimitInfo) {
        const importLimitsEl = document.getElementById('importLimits');
        if (!importLimitsEl) return;
        
        const { current_attempts, max_attempts, remaining_attempts, window_minutes, reset_time } = rateLimitInfo;
        
        let limitText = `导入尝试次数：${current_attempts}/${max_attempts}（${window_minutes}分钟内）`;
        
        // 移除之前的样式类
        importLimitsEl.classList.remove('rate-limited');
        
        if (remaining_attempts === 0) {
            limitText += ' - 已达上限';
            importLimitsEl.classList.add('rate-limited');
            if (reset_time) {
                const resetDate = new Date(reset_time * 1000);
                const now = new Date();
                const waitSeconds = Math.max(0, Math.ceil((resetDate - now) / 1000));
                limitText += `，${waitSeconds}秒后重置`;
            }
            
            // 禁用导入按钮
            const importBtn = document.querySelector('button[onclick="importCookie()"]');
            if (importBtn && !importBtn.disabled) {
                importBtn.disabled = true;
                importBtn.textContent = '已达尝试上限';
            }
        } else {
            limitText += `，还可尝试${remaining_attempts}次`;
            
            // 启用导入按钮
            const importBtn = document.querySelector('button[onclick="importCookie()"]');
            if (importBtn && importBtn.disabled && importBtn.textContent.includes('已达尝试上限')) {
                importBtn.disabled = false;
                importBtn.textContent = '验证并导入';
            }
        }
        
        importLimitsEl.innerHTML = `
            <div class="limit-info">
                <span class="limit-label">${limitText}</span>
            </div>
        `;
    }
    
    // 显示速率限制倒计时
    static showRateLimitCountdown(waitTime) {
        const importBtn = document.querySelector('#importCookie') || document.querySelector('button[onclick="importCookie()"]');
        if (!importBtn) return;
        
        let remaining = waitTime;
        importBtn.disabled = true;
        importBtn.textContent = `等待 ${remaining} 秒`;
        
        const countdown = setInterval(() => {
            remaining--;
            if (remaining <= 0) {
                clearInterval(countdown);
                importBtn.disabled = false;
                importBtn.textContent = '验证并导入';
                // 刷新速率限制信息
                this.loadRateLimitInfo();
            } else {
                importBtn.textContent = `等待 ${remaining} 秒`;
            }
        }, 1000);
    }
    
    // 加载速率限制信息
    static async loadRateLimitInfo() {
        try {
            const response = await fetch('/api/cookie/import_rate_info');
            const result = await response.json();
            
            if (result.success && result.rate_limit) {
                this.updateRateLimitDisplay(result.rate_limit);
            } else {
                // API调用成功但没有返回期望的数据，显示默认信息
                this.showDefaultRateLimitInfo();
            }
        } catch (error) {
            console.error('获取速率限制信息失败:', error);
            // API调用失败，显示默认信息
            this.showDefaultRateLimitInfo();
        }
    }
    
    // 显示默认的速率限制信息
    static showDefaultRateLimitInfo() {
        const importLimitsEl = document.getElementById('importLimits');
        if (importLimitsEl) {
            importLimitsEl.classList.remove('rate-limited');
            importLimitsEl.innerHTML = `
                <div class="limit-info">
                    <span class="limit-label">导入尝试次数：0/3（1分钟内），还可尝试3次</span>
                </div>
            `;
        }
    }
    
    // 编辑饼干名称
    static async editCookieName(cookieId) {
        const savedCookies = this.getSavedCookies();
        const cookie = savedCookies.find(c => c.id === cookieId);
        
        if (!cookie) return;
        
        const newName = await customPrompt('修改饼干名称:', cookie.name);
        if (newName === null || newName.trim() === '') return;
        
        cookie.name = newName.trim();
        this.setSavedCookies(savedCookies);
        this.loadCookieData();
        showToast('名称已更新');
    }
    
    // HTML调用的包装函数
    static deleteSavedCookieWrapper(cookieId) {
        this.deleteSavedCookie(cookieId).catch(error => {
            console.error('删除饼干失败:', error);
            showToast('删除饼干失败，请重试');
        });
    }
    
    static useSavedCookieWrapper(cookieId) {
        this.useSavedCookie(cookieId).catch(error => {
            console.error('切换饼干失败:', error);
            showToast('切换饼干失败，请重试');
        });
    }
    
    static editCookieNameWrapper(cookieId) {
        this.editCookieName(cookieId).catch(error => {
            console.error('编辑饼干名称失败:', error);
            showToast('编辑饼干名称失败，请重试');
        });
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
                        <button class="btn btn-primary btn-small" onclick="CookieManager.useSavedCookieWrapper('${cookie.id}')">使用</button>
                        <button class="btn btn-secondary btn-small" onclick="CookieManager.editCookieNameWrapper('${cookie.id}')">重命名</button>
                        <button class="btn btn-back btn-small" onclick="CookieManager.deleteSavedCookieWrapper('${cookie.id}')">删除</button>
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
        
        // 如果是在饼干管理器中，加载速率限制信息
        const importLimitsEl = document.getElementById('importLimits');
        if (importLimitsEl) {
            this.loadRateLimitInfo();
        }
    }
}

// 全局函数供HTML调用
function showCookieManager() {
    try {
        CookieManager.show();
    } catch (error) {
        console.error('显示饼干管理器失败:', error);
        showToast('饼干管理器加载失败，请刷新页面重试');
    }
}

function hideCookieManager() {
    try {
        CookieManager.hide();
    } catch (error) {
        console.error('隐藏饼干管理器失败:', error);
    }
}

async function saveCookie() {
    try {
        // 防止快速重复点击
        const btn = document.getElementById('saveCookieBtn');
        if (btn && btn.disabled) return;
        
        if (btn) {
            btn.disabled = true;
            setTimeout(() => {
                btn.disabled = false;
            }, 2000);
        }
        
        await CookieManager.saveCurrentCookie();
    } catch (error) {
        console.error('保存饼干失败:', error);
        showToast('保存饼干失败，请重试');
        // 重新启用按钮
        const btn = document.getElementById('saveCookieBtn');
        if (btn) btn.disabled = false;
    }
}

async function newCookie() {
    try {
        // 防止快速重复点击
        const btn = document.getElementById('newCookieBtn');
        if (btn && btn.disabled) return;
        
        if (btn) {
            btn.disabled = true;
            btn.textContent = '生成中...';
        }
        
        await CookieManager.generateNewCookie();
    } catch (error) {
        console.error('生成新饼干失败:', error);
        showToast('生成新饼干失败，请重试');
        // 重新启用按钮
        const btn = document.getElementById('newCookieBtn');
        if (btn) {
            btn.disabled = false;
            btn.textContent = '生成新饼干';
        }
    }
}

function importCookie() {
    try {
        CookieManager.importCookie();
    } catch (error) {
        console.error('导入饼干失败:', error);
        showToast('导入饼干失败，请重试');
    }
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

// 调试用：检查弹窗文字显示
function debugModal() {
    console.log('开始调试弹窗显示...');
    
    // 检查弹窗元素是否存在
    const confirmModal = document.getElementById('customConfirmModal');
    const promptModal = document.getElementById('customPromptModal');
    
    console.log('确认弹窗元素:', confirmModal);
    console.log('输入弹窗元素:', promptModal);
    
    if (confirmModal) {
        const title = document.getElementById('confirmTitle');
        const message = document.getElementById('confirmMessage');
        console.log('确认弹窗标题元素:', title);
        console.log('确认弹窗消息元素:', message);
        
        if (title) {
            console.log('标题样式:', window.getComputedStyle(title));
        }
        if (message) {
            console.log('消息样式:', window.getComputedStyle(message));
        }
    }
    
    // 测试弹窗
    customConfirm('这是测试文字，应该水平显示').then(result => {
        console.log('测试完成，结果:', result);
    });
}

// 全局暴露调试函数
window.debugModal = debugModal;

// ================== 深色模式功能 ==================

/**
 * 深色模式管理器
 */
const ThemeManager = {
    // 主题类型
    THEMES: {
        LIGHT: 'light',
        DARK: 'dark'
    },
    
    // 本地存储键名
    STORAGE_KEY: 'forum_theme_preference',
    
    /**
     * 初始化主题系统
     */
    init() {
        // 从本地存储获取用户偏好
        const savedTheme = this.getSavedTheme();
        
        // 如果没有保存的偏好，检查系统偏好
        const preferredTheme = savedTheme || this.getSystemPreference();
        
        // 应用主题
        this.setTheme(preferredTheme);
        
        // 监听系统主题变化
        this.watchSystemPreference();
        
        console.log('深色模式系统初始化完成，当前主题:', preferredTheme);
    },
    
    /**
     * 获取保存的主题偏好
     */
    getSavedTheme() {
        try {
            return localStorage.getItem(this.STORAGE_KEY);
        } catch (e) {
            console.warn('无法访问localStorage:', e);
            return null;
        }
    },
    
    /**
     * 保存主题偏好
     */
    saveTheme(theme) {
        try {
            localStorage.setItem(this.STORAGE_KEY, theme);
        } catch (e) {
            console.warn('无法保存主题设置:', e);
        }
    },
    
    /**
     * 获取系统主题偏好
     */
    getSystemPreference() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return this.THEMES.DARK;
        }
        return this.THEMES.LIGHT;
    },
    
    /**
     * 监听系统主题变化
     */
    watchSystemPreference() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                // 只有在用户没有手动设置偏好时才跟随系统
                if (!this.getSavedTheme()) {
                    const newTheme = e.matches ? this.THEMES.DARK : this.THEMES.LIGHT;
                    this.setTheme(newTheme);
                }
            });
        }
    },
    
    /**
     * 设置主题
     */
    setTheme(theme) {
        const validTheme = theme === this.THEMES.DARK ? this.THEMES.DARK : this.THEMES.LIGHT;
        
        // 应用到DOM
        document.documentElement.setAttribute('data-theme', validTheme);
        
        // 更新切换按钮图标
        this.updateToggleIcon(validTheme);
        
        // 触发主题变化事件
        this.dispatchThemeChangeEvent(validTheme);
        
        console.log('主题已切换至:', validTheme);
    },
    
    /**
     * 切换主题
     */
    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || this.THEMES.LIGHT;
        const newTheme = currentTheme === this.THEMES.DARK ? this.THEMES.LIGHT : this.THEMES.DARK;
        
        // 设置新主题
        this.setTheme(newTheme);
        
        // 保存用户偏好
        this.saveTheme(newTheme);
        
        // 添加切换动画
        this.addSwitchAnimation();
        
        return newTheme;
    },
    
    /**
     * 更新切换按钮图标
     */
    updateToggleIcon(theme) {
        const lightIcon = document.getElementById('theme-icon-light');
        const darkIcon = document.getElementById('theme-icon-dark');
        
        if (lightIcon && darkIcon) {
            if (theme === this.THEMES.DARK) {
                lightIcon.style.display = 'none';
                darkIcon.style.display = 'block';
            } else {
                lightIcon.style.display = 'block';
                darkIcon.style.display = 'none';
            }
        }
    },
    
    /**
     * 添加切换动画
     */
    addSwitchAnimation() {
        const button = document.querySelector('.theme-toggle');
        if (button) {
            button.style.transform = 'scale(0.9)';
            setTimeout(() => {
                button.style.transform = 'scale(1)';
            }, 150);
        }
    },
    
    /**
     * 触发主题变化事件
     */
    dispatchThemeChangeEvent(theme) {
        const event = new CustomEvent('themechange', {
            detail: { theme }
        });
        document.dispatchEvent(event);
    },
    
    /**
     * 获取当前主题
     */
    getCurrentTheme() {
        return document.documentElement.getAttribute('data-theme') || this.THEMES.LIGHT;
    },
    
    /**
     * 检查是否为深色模式
     */
    isDarkMode() {
        return this.getCurrentTheme() === this.THEMES.DARK;
    }
};

/**
 * 切换主题的全局函数
 */
function toggleTheme() {
    return ThemeManager.toggleTheme();
}

/**
 * 页面加载完成后初始化主题系统
 */
document.addEventListener('DOMContentLoaded', function() {
    ThemeManager.init();
});

/**
 * 监听主题变化事件，可以用于其他功能的主题适配
 */
document.addEventListener('themechange', function(e) {
    console.log('主题已变更为:', e.detail.theme);
    
    // 可以在这里添加其他需要响应主题变化的逻辑
    // 比如更新图表颜色、重新渲染某些组件等
});

// 全局暴露主题管理器
window.ThemeManager = ThemeManager;
window.toggleTheme = toggleTheme;