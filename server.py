import http.server
import socketserver
import json
import os
import sys

PORT = 18889
DATA_FILE = 'project_cards.json'

class ProjectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/cards':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, 'r', encoding='utf-8') as f:
                        data = f.read()
                        if not data: data = '[]'
                        self.wfile.write(data.encode('utf-8'))
                except Exception as e:
                    print(f"Error reading file: {e}")
                    self.wfile.write(b'[]')
            else:
                self.wfile.write(b'[]')
            return
        
        # Serve static files
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/cards':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Verify JSON validity
                json_data = json.loads(post_data)
                
                # Write to file
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "count": len(json_data)}).encode('utf-8'))
                print(f"Successfully saved {len(json_data)} cards.")
                
            except Exception as e:
                print(f"Error saving data: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
            return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"启动服务中... 请在浏览器访问 http://localhost:{PORT}")
print(f"数据文件: {os.path.abspath(DATA_FILE)}")
print("按 Ctrl+C 停止服务")

with socketserver.TCPServer(("", PORT), ProjectHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
