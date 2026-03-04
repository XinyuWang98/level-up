// MathJax 配置 (必须在 MathJax 库之前加载)
// 来源: MkDocs Material 官方文档
// https://squidfunk.github.io/mkdocs-material/setup/extensions/python-markdown-extensions/#arithmatex
window.MathJax = {
    tex: {
        inlineMath: [["\\(", "\\)"]],
        displayMath: [["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true
    },
    options: {
        ignoreHtmlClass: ".*|",
        processHtmlClass: "arithmatex"
    }
};

// 兼容 MkDocs Material 的 navigation.instant (SPA 即时导航)
// 页面通过 instant navigation 切换时需要重新触发 MathJax 渲染
document$.subscribe(() => {
    MathJax.startup.output.clearCache()
    MathJax.typesetClear()
    MathJax.texReset()
    MathJax.typesetPromise()
})
