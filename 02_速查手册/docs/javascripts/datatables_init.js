/**
 * DataTables 初始化脚本
 * 用于投递追踪表格的排序、搜索和筛选功能
 */
document.addEventListener('DOMContentLoaded', function () {
    // 查找带有 datatables 标记的表格
    const tables = document.querySelectorAll('table.datatables');

    if (tables.length === 0) return;

    // 等待 jQuery 和 DataTables 加载完成
    const MAX_RETRY = 50;
    const RETRY_INTERVAL_MS = 100;
    let retryCount = 0;

    function initDataTables() {
        if (typeof jQuery === 'undefined' || typeof jQuery.fn.DataTable === 'undefined') {
            retryCount++;
            if (retryCount < MAX_RETRY) {
                setTimeout(initDataTables, RETRY_INTERVAL_MS);
            }
            return;
        }

        tables.forEach(function (table) {
            // 避免重复初始化
            if (jQuery.fn.DataTable.isDataTable(table)) return;

            jQuery(table).DataTable({
                // 中文语言包
                language: {
                    search: "🔍 搜索：",
                    lengthMenu: "显示 _MENU_ 条",
                    info: "共 _TOTAL_ 条，当前 _START_ - _END_",
                    infoEmpty: "暂无数据",
                    infoFiltered: "（从 _MAX_ 条中筛选）",
                    zeroRecords: "未找到匹配记录",
                    paginate: {
                        first: "首页",
                        previous: "上一页",
                        next: "下一页",
                        last: "末页"
                    }
                },
                // 配置
                pageLength: 50,
                paging: false,
                ordering: true,
                searching: true,
                info: true,
                autoWidth: false,
                responsive: true,
                order: [[0, 'asc']],
                columnDefs: [
                    { orderable: true, targets: '_all' },
                    { width: '30px', targets: 0 },
                    { width: '60px', targets: 1 },
                ]
            });

            // 为每个 DataTables wrapper 添加全屏按钮
            var wrapper = jQuery(table).closest('.dataTables_wrapper');
            if (wrapper.find('.dt-fullscreen-btn').length === 0) {
                var btn = jQuery('<button class="dt-fullscreen-btn" title="全屏查看">⛶ 全屏</button>');
                wrapper.prepend(btn);

                btn.on('click', function () {
                    var isFullscreen = wrapper.hasClass('dt-fullscreen');
                    if (isFullscreen) {
                        wrapper.removeClass('dt-fullscreen');
                        btn.text('⛶ 全屏');
                        document.body.style.overflow = '';
                    } else {
                        wrapper.addClass('dt-fullscreen');
                        btn.text('✕ 退出全屏');
                        document.body.style.overflow = 'hidden';
                    }
                });
            }
        });

        // ESC 键退出全屏
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                jQuery('.dataTables_wrapper.dt-fullscreen').each(function () {
                    jQuery(this).removeClass('dt-fullscreen');
                    jQuery(this).find('.dt-fullscreen-btn').text('⛶ 全屏');
                    document.body.style.overflow = '';
                });
            }
        });
    }

    // 启动初始化
    initDataTables();
});
