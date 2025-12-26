import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse

# Default port
PORT = 18889

# Allow port override from command line
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print(f"Invalid port number: {sys.argv[1]}, using default {PORT}")

DATA_FILE = 'project_cards.json'
PROJECTS_FILE = 'projects.json'
CATALOG_FILE = 'data/catalog.json'
USERS_FILE = 'data/users.json'

class ProjectHandler(http.server.SimpleHTTPRequestHandler):
    def handle_data_request(self, file_path, method):
        # Allow read/write for all JSON files
        if method == 'GET':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = f.read()
                        if not data: data = '[]'
                        self.wfile.write(data.encode('utf-8'))
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    self.wfile.write(b'[]')
            else:
                self.wfile.write(b'[]')
                
        elif method == 'POST':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Verify JSON validity
                json_data = json.loads(post_data)
                
                # Write to file
                # Ensure directory exists
                os.makedirs(os.path.dirname(os.path.abspath(file_path)) or '.', exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                # Handle single object (dict) or list
                count = len(json_data) if isinstance(json_data, list) else 1
                self.wfile.write(json.dumps({"status": "success", "count": count}).encode('utf-8'))
                print(f"Successfully saved to {file_path}")
                
            except Exception as e:
                print(f"Error saving data to {file_path}: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/cards':
            return self.handle_data_request(DATA_FILE, 'GET')
        elif path == '/api/projects':
            return self.handle_data_request(PROJECTS_FILE, 'GET')
        elif path == '/api/catalog':
            return self.handle_data_request(CATALOG_FILE, 'GET')
        elif path == '/api/users':
            return self.handle_data_request(USERS_FILE, 'GET')
        
        # Serve static files
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/cards':
            return self.handle_data_request(DATA_FILE, 'POST')
        elif path == '/api/projects':
            return self.handle_data_request(PROJECTS_FILE, 'POST')
        elif path == '/api/catalog':
            return self.handle_data_request(CATALOG_FILE, 'POST')
        elif path == '/api/users':
            return self.handle_data_request(USERS_FILE, 'POST')
        return super().do_POST()

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
