/**
 * 思维导图管理器 - jsMind 封装
 * 提供创建、加载、保存、嵌入思维导图的统一接口。
 * 依赖: jsmind.js, jsmind.draggable-node.js
 */

const MINDMAP_API_BASE = 'http://127.0.0.1:5112/api/mindmaps';

/**
 * 初始化一个可编辑的思维导图编辑器
 * @param {string} containerId - 容器 DOM 元素的 ID
 * @param {string} mapId - 思维导图的 ID（对应 JSON 文件名，不含 .json）
 * @param {object} options - 可选配置
 * @param {boolean} options.editable - 是否可编辑（默认 true）
 * @param {string} options.theme - 主题（默认 'dark'）
 */
async function initMindMap(containerId, mapId, options = {}) {
    const editable = options.editable !== false;
    const theme = options.theme || 'dark';

    // 🔧 关键修复：每次初始化前清空容器，防止多实例叠加
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = '';
    }

    // jsMind 配置
    const jmOptions = {
        container: containerId,
        editable: editable,
        theme: theme,
        view: {
            engine: 'canvas',
            hmargin: 120,
            vmargin: 60,
            line_width: 2,
            line_color: '#64748b'
        },
        layout: {
            hspace: 40,
            vspace: 25,
            pspace: 15
        },
        shortcut: {
            enable: editable,
            handles: {},
            mapping: {
                addchild: [45, 9],    // Insert 或 Tab 添加子节点
                addbrother: 13,       // Enter 添加兄弟节点
                editnode: 113,        // F2 编辑节点
                delnode: 46,          // Delete 删除节点
                toggle: 32,           // Space 折叠/展开
                left: 37,
                up: 38,
                right: 39,
                down: 40,
            }
        }
    };

    const jm = new jsMind(jmOptions);

    // 尝试从服务器加载数据
    let mindData = null;
    try {
        const response = await fetch(`${MINDMAP_API_BASE}/${mapId}`);
        if (response.ok) {
            mindData = await response.json();
        }
    } catch (e) {
        console.warn(`加载思维导图 ${mapId} 失败:`, e);
    }

    // 如果没有已有数据，创建一个空白导图
    if (!mindData) {
        mindData = {
            meta: { name: mapId, author: 'Catherine', version: '1.0' },
            format: 'node_tree',
            data: { id: 'root', topic: '新思维导图', children: [] }
        };
    }

    jm.show(mindData);

    // 启用拖拽
    if (editable && typeof jsMind.draggable !== 'undefined') {
        // draggable 插件会自动注册
    }

    return jm;
}

/**
 * 保存思维导图到服务器
 * @param {jsMind} jm - jsMind 实例
 * @param {string} mapId - 思维导图 ID
 */
async function saveMindMap(jm, mapId) {
    const data = jm.get_data('node_tree');
    // 包装成完整的 jsMind 格式
    const payload = {
        meta: { name: mapId, author: 'Catherine', version: '1.0' },
        format: 'node_tree',
        data: data.data
    };

    try {
        const response = await fetch(`${MINDMAP_API_BASE}/${mapId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        return result;
    } catch (e) {
        console.error('保存失败:', e);
        throw e;
    }
}

/**
 * 获取所有思维导图列表
 */
async function listMindMaps() {
    try {
        const response = await fetch(MINDMAP_API_BASE);
        return await response.json();
    } catch (e) {
        console.error('获取列表失败:', e);
        return [];
    }
}
