/**
 * Mermaid 增强工具 (全屏预览 + 高对比度配色)
 * 
 * 功能：
 * 1. 为每个 Mermaid 图表自动注入"全屏"按钮
 * 2. 点击按钮后进入全屏，ESC 退出
 * 3. 后渲染 SVG 颜色替换: 将 Mermaid 默认的低对比度颜色替换为高可见度颜色
 * 4. 兼容 MkDocs Material SPA 模式和 暗色/亮色 主题切换
 */

(function () {
    'use strict';

    // ========== 常量定义 ==========
    const FULLSCREEN_BTN_CLASS = 'mermaid-fullscreen-btn';
    const CONTAINER_CLASS = 'mermaid-container';
    const FULLSCREEN_CLASS = 'mermaid-fullscreen';
    const BTN_TEXT_ENTER = '⛶ 全屏';
    const BTN_TEXT_EXIT = '✕ 退出全屏';

    // 高对比度颜色映射 (Mermaid 默认色 → 替换色)
    // Mermaid dark theme 默认使用低对比暗色, 这里替换为明亮高可见色
    const COLOR_MAP_DARK = {
        // done 状态 → 翡翠绿
        '#0d1117': '#10b981', '#0d1117ff': '#10b981',
        '#1e2228': '#10b981',
        // active 状态 → 琥珀色 
        '#1f2937': '#f59e0b', '#1f2937ff': '#f59e0b',
        // 默认任务 → 天蓝色
        '#2d333b': '#3b82f6', '#2d333bff': '#3b82f6',
    };

    // ========== 全屏功能 ==========

    /** 为单个 mermaid 元素添加全屏按钮 */
    function wrapMermaid(mermaidEl) {
        if (mermaidEl.parentElement && mermaidEl.parentElement.classList.contains(CONTAINER_CLASS)) {
            return;
        }

        var container = document.createElement('div');
        container.className = CONTAINER_CLASS;
        mermaidEl.parentNode.insertBefore(container, mermaidEl);
        container.appendChild(mermaidEl);

        var btn = document.createElement('button');
        btn.className = FULLSCREEN_BTN_CLASS;
        btn.textContent = BTN_TEXT_ENTER;
        btn.setAttribute('aria-label', '全屏预览图表');
        container.appendChild(btn);

        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            toggleFullscreen(container, btn);
        });
    }

    /** 切换全屏状态 */
    function toggleFullscreen(container, btn) {
        var isFullscreen = container.classList.contains(FULLSCREEN_CLASS);
        var svg = container.querySelector('svg');

        if (isFullscreen) {
            // 退出全屏 → 还原 SVG 原始尺寸
            container.classList.remove(FULLSCREEN_CLASS);
            btn.textContent = BTN_TEXT_ENTER;
            document.body.style.overflow = '';
            if (svg) {
                // 还原保存的原始属性
                if (svg.dataset.origWidth) svg.style.width = svg.dataset.origWidth;
                if (svg.dataset.origHeight) svg.style.height = svg.dataset.origHeight;
                if (svg.dataset.origMaxWidth) svg.style.maxWidth = svg.dataset.origMaxWidth;
            }
        } else {
            // 进入全屏 → 强制 SVG 撑满屏幕宽度
            container.classList.add(FULLSCREEN_CLASS);
            btn.textContent = BTN_TEXT_EXIT;
            document.body.style.overflow = 'hidden';
            if (svg) {
                // 保存原始尺寸
                svg.dataset.origWidth = svg.style.width || '';
                svg.dataset.origHeight = svg.style.height || '';
                svg.dataset.origMaxWidth = svg.style.maxWidth || '';
                // 强制拉伸
                svg.style.width = '100%';
                svg.style.maxWidth = '100%';
                svg.style.height = 'auto';
            }
        }
    }

    /** ESC 键退出全屏 */
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            var fullscreenEl = document.querySelector('.' + FULLSCREEN_CLASS);
            if (fullscreenEl) {
                var btn = fullscreenEl.querySelector('.' + FULLSCREEN_BTN_CLASS);
                toggleFullscreen(fullscreenEl, btn);
            }
        }
    });

    // ========== 高对比度 SVG 颜色替换 ==========

    /** 
     * 检测当前是否为暗色模式
     * MkDocs Material 通过 data-md-color-scheme 属性控制主题
     */
    function isDarkMode() {
        var body = document.body;
        var scheme = body.getAttribute('data-md-color-scheme') || '';
        return scheme === 'slate';
    }

    /**
     * 遍历 Mermaid SVG 中的所有元素，根据 Gantt 类名替换颜色
     * Mermaid 9+ 生成的甘特图使用类名如: task, done, active, crit 等
     */
    function recolorMermaidSVGs() {
        document.querySelectorAll('.mermaid svg').forEach(function (svg) {
            if (svg.dataset.recolored) return;
            svg.dataset.recolored = 'true';

            // 甘特图: 根据 class 属性匹配任务类型并设置颜色
            svg.querySelectorAll('rect, polygon, path').forEach(function (el) {
                var cls = el.getAttribute('class') || '';

                if (isDarkMode()) {
                    // done 状态 → 翡翠绿
                    if (cls.match(/\bdone\b/)) {
                        el.style.fill = '#10b981';
                        el.style.stroke = '#059669';
                    }
                    // active 状态 → 琥珀色
                    else if (cls.match(/\bactive\b/)) {
                        el.style.fill = '#f59e0b';
                        el.style.stroke = '#d97706';
                    }
                    // crit (关键路径) → 珊瑚红
                    else if (cls.match(/\bcrit\b/)) {
                        el.style.fill = '#ef4444';
                        el.style.stroke = '#dc2626';
                    }
                } else {
                    // 亮色模式
                    if (cls.match(/\bdone\b/)) {
                        el.style.fill = '#059669';
                        el.style.stroke = '#047857';
                    }
                    else if (cls.match(/\bactive\b/)) {
                        el.style.fill = '#d97706';
                        el.style.stroke = '#b45309';
                    }
                    else if (cls.match(/\bcrit\b/)) {
                        el.style.fill = '#dc2626';
                        el.style.stroke = '#b91c1c';
                    }
                }
            });

            // 甘特图: 文字标签高对比
            svg.querySelectorAll('text').forEach(function (el) {
                var cls = el.getAttribute('class') || '';

                if (isDarkMode()) {
                    // 任务文字 → 白色加粗
                    if (cls.match(/task/i)) {
                        el.style.fill = '#ffffff';
                        el.style.fontWeight = '600';
                    }
                    // 标题 → 亮白
                    if (cls.match(/title/i)) {
                        el.style.fill = '#f1f5f9';
                        el.style.fontWeight = '700';
                        el.style.fontSize = '16px';
                    }
                    // Section 标签 → 浅灰
                    if (cls.match(/section/i)) {
                        el.style.fill = '#e2e8f0';
                        el.style.fontWeight = '700';
                    }
                    // X 轴刻度
                    if (cls.match(/tick/i) || el.closest('.tick')) {
                        el.style.fill = '#94a3b8';
                    }
                }
            });

            // 甘特图: 网格线柔和
            if (isDarkMode()) {
                svg.querySelectorAll('.grid .tick line, .grid line').forEach(function (el) {
                    el.style.stroke = '#475569';
                });
            }
        });
    }

    // ========== 主初始化 ==========

    function initAll() {
        // 1. 全屏按钮
        document.querySelectorAll('.mermaid').forEach(function (el) {
            wrapMermaid(el);
        });
        // 2. 高对比度颜色
        recolorMermaidSVGs();
    }

    function init() {
        initAll();

        // 监听 DOM 变化 — Mermaid 异步渲染 + SPA 页面切换
        var observer = new MutationObserver(function (mutations) {
            var shouldRescan = false;
            mutations.forEach(function (mutation) {
                mutation.addedNodes.forEach(function (node) {
                    if (node.nodeType === 1) {
                        if (node.classList && node.classList.contains('mermaid')) {
                            shouldRescan = true;
                        }
                        if (node.querySelector && node.querySelector('.mermaid')) {
                            shouldRescan = true;
                        }
                        // SVG 被注入到 .mermaid 容器中
                        if (node.tagName === 'svg' && node.closest && node.closest('.mermaid')) {
                            shouldRescan = true;
                        }
                    }
                });
            });
            if (shouldRescan) {
                setTimeout(initAll, 800);
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });

        // 监听主题切换 → 重新着色
        var themeObserver = new MutationObserver(function (mutations) {
            mutations.forEach(function (m) {
                if (m.attributeName === 'data-md-color-scheme') {
                    // 重置已着色标记，重新着色
                    document.querySelectorAll('.mermaid svg').forEach(function (svg) {
                        svg.dataset.recolored = '';
                    });
                    setTimeout(recolorMermaidSVGs, 300);
                }
            });
        });
        themeObserver.observe(document.body, { attributes: true });
    }

    // DOM 准备好后启动 (延迟等 Mermaid 渲染完)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            setTimeout(init, 1500);
        });
    } else {
        setTimeout(init, 1500);
    }

})();
