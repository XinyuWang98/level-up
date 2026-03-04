/**
 * 知识库搜索追踪器 (Search Analytics Tracker)
 * 
 * 功能：
 * 1. 监听 MkDocs Material 搜索框输入，记录搜索查询
 * 2. 记录页面访问事件
 * 3. 双写持久化：localStorage + Flask 微服务
 */

(function () {
    'use strict';

    // ========== 常量定义 ==========
    const STORAGE_KEY = 'mkdocs_search_log';
    const API_BASE = 'http://127.0.0.1:5112';
    const DEBOUNCE_MS = 1500;          // 搜索防抖间隔
    const MAX_LOCAL_RECORDS = 500;     // localStorage 最大记录数
    const MIN_QUERY_LENGTH = 2;        // 最短查询长度

    // ========== 工具函数 ==========

    /** 获取当前 ISO 时间戳 */
    function now() {
        return new Date().toISOString();
    }

    /** 防抖函数 */
    function debounce(fn, delay) {
        let timer = null;
        return function () {
            const args = arguments;
            if (timer) clearTimeout(timer);
            timer = setTimeout(function () { fn.apply(null, args); }, delay);
        };
    }

    /** 从 URL 提取页面名称（去掉 .html 和路径） */
    function getPageName() {
        var path = window.location.pathname;
        var name = path.split('/').pop() || 'index.html';
        return name.replace('.html', '');
    }

    // ========== localStorage 操作 ==========

    /** 读取本地日志 */
    function getLocalLog() {
        try {
            var data = localStorage.getItem(STORAGE_KEY);
            return data ? JSON.parse(data) : [];
        } catch (e) {
            return [];
        }
    }

    /** 写入本地日志（自动裁剪） */
    function saveLocalLog(log) {
        try {
            // 超出上限时保留最新的记录
            if (log.length > MAX_LOCAL_RECORDS) {
                log = log.slice(log.length - MAX_LOCAL_RECORDS);
            }
            localStorage.setItem(STORAGE_KEY, JSON.stringify(log));
        } catch (e) {
            // localStorage 满了或不可用，静默失败
        }
    }

    /** 添加一条记录到本地 */
    function addLocalRecord(record) {
        var log = getLocalLog();
        log.push(record);
        saveLocalLog(log);
    }

    // ========== 远程 API 操作 ==========

    /** 发送事件到 Flask 微服务 */
    function sendToServer(record) {
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', API_BASE + '/api/log', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(record));
            // 不关心响应，静默发送
        } catch (e) {
            // 服务不可用时静默失败
        }
    }

    // ========== 事件记录 ==========

    /** 记录一个事件（双写） */
    function logEvent(type, data) {
        var record = {
            type: type,
            timestamp: now(),
            page: getPageName()
        };
        // 合并额外数据
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                record[key] = data[key];
            }
        }
        addLocalRecord(record);
        sendToServer(record);
    }

    // ========== 搜索追踪 ==========

    /** 上一次记录的查询词（避免重复记录） */
    var lastQuery = '';

    /** 处理搜索输入（防抖后） */
    function handleSearchInput(query) {
        query = query.trim().toLowerCase();
        if (query.length < MIN_QUERY_LENGTH) return;
        if (query === lastQuery) return;
        lastQuery = query;
        logEvent('search', { query: query });
    }

    var debouncedSearch = debounce(handleSearchInput, DEBOUNCE_MS);

    /** 初始化搜索监听 */
    function initSearchTracker() {
        // MkDocs Material 的搜索输入框
        var observer = new MutationObserver(function () {
            var searchInput = document.querySelector('input.md-search__input');
            if (searchInput && !searchInput.dataset.tracked) {
                searchInput.dataset.tracked = 'true';
                searchInput.addEventListener('input', function () {
                    debouncedSearch(this.value);
                });
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });

        // 也直接尝试绑定（页面已加载完的情况）
        var searchInput = document.querySelector('input.md-search__input');
        if (searchInput && !searchInput.dataset.tracked) {
            searchInput.dataset.tracked = 'true';
            searchInput.addEventListener('input', function () {
                debouncedSearch(this.value);
            });
        }
    }

    // ========== 页面访问追踪 ==========

    /** 记录页面访问 */
    function logPageVisit() {
        var page = getPageName();
        // 不记录 dashboard 页面本身的访问
        if (page === 'dashboard') return;
        logEvent('visit', { title: document.title });
    }

    /** 初始化页面访问监听 */
    function initPageTracker() {
        // 首次加载
        logPageVisit();

        // MkDocs Material 的 navigation.instant 会用 History API 导航
        // 监听 URL 变化
        var lastUrl = window.location.href;
        var urlObserver = new MutationObserver(function () {
            if (window.location.href !== lastUrl) {
                lastUrl = window.location.href;
                logPageVisit();
            }
        });
        urlObserver.observe(document.body, { childList: true, subtree: true });
    }

    // ========== 初始化 ==========

    function init() {
        initSearchTracker();
        initPageTracker();
    }

    // DOM 加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
