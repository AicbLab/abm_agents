"""
ABM 仿真前端服务启动脚本
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # 添加 CORS 头，允许本地访问
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_server():
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 ABM 仿真前端服务已启动")
        print(f"📍 访问地址：http://localhost:{PORT}")
        print(f"📁 目录：{DIRECTORY}")
        print(f"💡 按 Ctrl+C 停止服务\n")
        
        # 自动打开浏览器
        webbrowser.open(f"http://localhost:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️  服务已停止")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()
