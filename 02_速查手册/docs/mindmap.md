# 🧠 思维导图工作台

<style>
/* 隐藏 MkDocs 侧边栏，给思维导图腾出更多空间 */
.md-sidebar { display: none !important; }
.md-content { max-width: 100% !important; margin: 0 !important; }
.md-main__inner { max-width: 100% !important; }

/* 思维导图编辑器样式 */
#mindmap-toolbar {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: var(--md-code-bg-color, #1e1e2e);
    border-radius: 8px;
    margin-bottom: 12px;
    flex-wrap: wrap;
    border: 1px solid var(--md-default-fg-color--lightest, #333);
    position: sticky;
    top: 0;
    z-index: 100;
}
#mindmap-toolbar select,
#mindmap-toolbar input,
#mindmap-toolbar button {
    font-size: 14px;
    padding: 6px 12px;
    border-radius: 6px;
    border: 1px solid var(--md-default-fg-color--lightest, #555);
    background: var(--md-default-bg-color, #181825);
    color: var(--md-default-fg-color, #cdd6f4);
}
#mindmap-toolbar button {
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;
}
#mindmap-toolbar button:hover {
    filter: brightness(1.2);
}
.btn-primary { background: #3b82f6 !important; color: #fff !important; border-color: #2563eb !important; }
.btn-success { background: #10b981 !important; color: #fff !important; border-color: #059669 !important; }
.btn-warning { background: #f59e0b !important; color: #fff !important; border-color: #d97706 !important; }
.btn-danger  { background: #ef4444 !important; color: #fff !important; border-color: #dc2626 !important; }
.btn-info    { background: #6366f1 !important; color: #fff !important; border-color: #4f46e5 !important; }
.btn-dark    { background: #334155 !important; color: #fff !important; border-color: #475569 !important; }
#mindmap-container {
    width: 100%;
    height: calc(100vh - 200px);
    min-height: 500px;
    border: 2px solid var(--md-default-fg-color--lightest, #333);
    border-radius: 8px;
    background: var(--md-code-bg-color, #1e1e2e);
    overflow: hidden;
}

/* 全屏模式 */
#mindmap-container.fullscreen {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 9999 !important;
    border-radius: 0 !important;
    border: none !important;
}
#mindmap-toolbar.fullscreen-toolbar {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 10000 !important;
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 2px solid #333 !important;
}

#mindmap-status {
    padding: 8px 16px;
    margin-top: 8px;
    font-size: 13px;
    color: var(--md-default-fg-color--light, #999);
    display: flex;
    justify-content: space-between;
}
#mindmap-help {
    margin-top: 16px;
    padding: 16px;
    background: var(--md-code-bg-color, #1e1e2e);
    border-radius: 8px;
    border: 1px solid var(--md-default-fg-color--lightest, #333);
}
#mindmap-help kbd {
    background: var(--md-default-bg-color, #181825);
    border: 1px solid var(--md-default-fg-color--lightest, #555);
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 12px;
}
</style>

<!-- 工具栏 -->
<div id="mindmap-toolbar">
    <select id="map-selector" title="选择思维导图">
        <option value="">-- 选择已有导图 --</option>
    </select>
    <button class="btn-primary" onclick="loadSelected()" title="加载选中的导图">📂 加载</button>
    <span style="color:#555">|</span>
    <input id="new-map-name" type="text" placeholder="新导图名称 (英文)" style="width:160px" />
    <button class="btn-info" onclick="createNew()" title="创建新的空白导图">✨ 新建</button>
    <span style="color:#555">|</span>
    <button class="btn-success" onclick="saveCurrentMap()" title="保存当前导图到服务器">💾 保存</button>
    <button class="btn-warning" onclick="addChildNode()" title="在选中节点下添加子节点">➕ 添加子节点</button>
    <button class="btn-danger" onclick="removeNode()" title="删除选中的节点">🗑️ 删除节点</button>
    <span style="color:#555">|</span>
    <button class="btn-dark" onclick="toggleFullscreen()" id="btn-fullscreen" title="全屏编辑">⛶ 全屏</button>
</div>

<!-- 思维导图画布 -->
<div id="mindmap-container"></div>

<!-- 状态栏 -->
<div id="mindmap-status">
    <span id="status-text">💡 请从上方选择一个导图，或创建新导图</span>
    <span id="status-map-id"></span>
</div>

<!-- 快捷键帮助 -->
<div id="mindmap-help">

**⌨️ 快捷键：**
<kbd>Tab</kbd> 添加子节点 · <kbd>Enter</kbd> 添加兄弟节点 · <kbd>F2</kbd> 编辑节点文字 · <kbd>Delete</kbd> 删除节点 · <kbd>Space</kbd> 折叠/展开 · **双击** 编辑节点

**📝 使用方式：**

1. 从下拉列表选择已有导图并点击「📂 加载」，或在输入框输入名称点击「✨ 新建」
2. 在画布中**双击节点**编辑文字，使用快捷键或工具栏按钮添加/删除节点
3. **拖拽节点**可以调整位置和层级关系
4. 编辑完成后点击「💾 保存」——数据会保存为 JSON 文件，Agent 也可以直接编辑该文件

</div>

<!-- 加载 jsMind 库 -->
<link rel="stylesheet" href="stylesheets/jsmind.css" />
<script src="javascripts/jsmind.js"></script>
<script src="javascripts/jsmind.draggable-node.js"></script>
<script src="javascripts/mindmap_manager.js"></script>

<script>
// ========== 全局状态 ==========
let currentJm = null;
let currentMapId = null;

// ========== 页面初始化 ==========
document.addEventListener('DOMContentLoaded', async () => {
    await refreshMapList();
});

// 刷新导图列表
async function refreshMapList() {
    const selector = document.getElementById('map-selector');
    const maps = await listMindMaps();
    // 清空已有选项（保留第一个占位符）
    while (selector.options.length > 1) selector.remove(1);
    maps.forEach(m => {
        const opt = document.createElement('option');
        opt.value = m.id;
        opt.textContent = m.id;
        selector.appendChild(opt);
    });
}

// 加载选中的导图
async function loadSelected() {
    const selector = document.getElementById('map-selector');
    const mapId = selector.value;
    if (!mapId) {
        setStatus('⚠️ 请先选择一个导图', '');
        return;
    }
    await loadMap(mapId);
}

// 加载指定导图
async function loadMap(mapId) {
    try {
        currentMapId = mapId;
        currentJm = await initMindMap('mindmap-container', mapId, {
            editable: true,
            theme: 'dark'
        });
        setStatus(`✅ 已加载「${mapId}」`, `📄 ${mapId}.json`);
    } catch (e) {
        setStatus(`❌ 加载失败: ${e.message}`, '');
    }
}

// 创建新导图
async function createNew() {
    const input = document.getElementById('new-map-name');
    const name = input.value.trim().replace(/[^a-zA-Z0-9_\-]/g, '_');
    if (!name) {
        setStatus('⚠️ 请输入导图名称（英文+下划线）', '');
        return;
    }
    currentMapId = name;

    // 创建空白导图数据
    const emptyData = {
        meta: { name: name, author: 'Catherine', version: '1.0' },
        format: 'node_tree',
        data: { id: 'root', topic: name.replace(/_/g, ' '), children: [] }
    };

    // 先保存到服务器
    try {
        await fetch(`${MINDMAP_API_BASE}/${name}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(emptyData)
        });
    } catch (e) {
        // 即使保存失败也继续（本地先展示）
    }

    // 初始化编辑器
    currentJm = await initMindMap('mindmap-container', name, {
        editable: true,
        theme: 'dark'
    });

    // 刷新列表
    await refreshMapList();
    document.getElementById('map-selector').value = name;
    input.value = '';
    setStatus(`✅ 新导图「${name}」已创建，开始编辑吧！`, `📄 ${name}.json`);
}

// 保存当前导图
async function saveCurrentMap() {
    if (!currentJm || !currentMapId) {
        setStatus('⚠️ 没有正在编辑的导图', '');
        return;
    }
    try {
        const result = await saveMindMap(currentJm, currentMapId);
        setStatus(`💾 已保存「${currentMapId}」 ✅`, `📄 ${currentMapId}.json`);
    } catch (e) {
        setStatus(`❌ 保存失败: ${e.message}`, '');
    }
}

// 添加子节点
function addChildNode() {
    if (!currentJm) return;
    const selected = currentJm.get_selected_node();
    if (!selected) {
        setStatus('⚠️ 请先点击选择一个节点', '');
        return;
    }
    const nodeId = 'node_' + Date.now();
    currentJm.add_node(selected, nodeId, '新节点');
}

// 删除节点
function removeNode() {
    if (!currentJm) return;
    const selected = currentJm.get_selected_node();
    if (!selected) {
        setStatus('⚠️ 请先点击选择一个节点', '');
        return;
    }
    if (selected.id === 'root') {
        setStatus('⚠️ 不能删除根节点', '');
        return;
    }
    currentJm.remove_node(selected);
}

// 更新状态栏
function setStatus(text, mapInfo) {
    document.getElementById('status-text').textContent = text;
    document.getElementById('status-map-id').textContent = mapInfo;
}

// 全屏切换
let isFullscreen = false;
function toggleFullscreen() {
    const container = document.getElementById('mindmap-container');
    const toolbar = document.getElementById('mindmap-toolbar');
    const btn = document.getElementById('btn-fullscreen');
    
    isFullscreen = !isFullscreen;
    
    if (isFullscreen) {
        container.classList.add('fullscreen');
        toolbar.classList.add('fullscreen-toolbar');
        btn.textContent = '✕ 退出全屏';
        // 全屏后调整画布位置，避免被工具栏遮挡
        container.style.paddingTop = '60px';
    } else {
        container.classList.remove('fullscreen');
        toolbar.classList.remove('fullscreen-toolbar');
        btn.textContent = '⛶ 全屏';
        container.style.paddingTop = '';
    }
    
    // 触发 jsMind 重新计算布局
    if (currentJm) {
        setTimeout(() => currentJm.resize(), 100);
    }
}

// ESC 键退出全屏
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isFullscreen) {
        toggleFullscreen();
    }
});
</script>
