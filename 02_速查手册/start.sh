#!/bin/bash
# 一键启动知识库 + 搜索分析服务
# 用法: ./start.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 启动知识库服务..."
echo ""

# 检查 Flask 依赖
if ! python3 -c "import flask" 2>/dev/null; then
  echo "📦 安装 Flask 依赖..."
  pip3 install flask flask-cors
fi

# 启动 Flask 分析服务 (后台)
echo "📊 启动搜索分析服务 (端口 5111)..."
python3 analytics_server.py &
FLASK_PID=$!
echo "   PID: $FLASK_PID"

# 等待 Flask 启动
sleep 1

# 启动 MkDocs (前台)
echo "📚 启动 MkDocs 知识库 (端口 8000)..."
echo ""
echo "========================================="
echo "  🌐 知识库: http://127.0.0.1:8000"
echo "  📊 看板:   http://127.0.0.1:8000/dashboard.html"
echo "  📡 API:    http://127.0.0.1:5111"
echo "========================================="
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 捕获退出信号，同时关闭 Flask
cleanup() {
  echo ""
  echo "🛑 正在关闭服务..."
  kill $FLASK_PID 2>/dev/null
  echo "✅ 已关闭"
}
trap cleanup EXIT INT TERM

# 启动 MkDocs (前台运行，Ctrl+C 触发 cleanup)
mkdocs serve
