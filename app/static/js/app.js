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

// 键盘事件处理
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        hideImageModal();
        hideRulesModal();
        
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