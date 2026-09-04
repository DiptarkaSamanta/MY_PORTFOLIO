import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
try:
    from http.server import ThreadingHTTPServer
except ImportError:
    from socketserver import ThreadingMixIn
    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True
from email.message import EmailMessage

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        print(f"do_POST received path: {self.path}", flush=True)
        if self.path == '/upload':
            try:
                content_type = self.headers.get('Content-Type')
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)

                # Parse the multipart form data using standard email parser
                msg = EmailMessage()
                msg['Content-Type'] = content_type
                msg.set_payload(body)

                filename = None
                file_bytes = None

                # Search parts for file attachment
                for part in msg.walk():
                    fn = part.get_filename()
                    if fn:
                        filename = fn
                        file_bytes = part.get_payload(decode=True)
                        break

                if not filename or not file_bytes:
                    self.send_response(400)
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(b'Invalid multipart upload file')
                    return

                # Create song directory if it doesn't exist
                song_dir = os.path.join(DIRECTORY, 'song')
                os.makedirs(song_dir, exist_ok=True)

                # Clean up filename
                filename = os.path.basename(filename)
                filepath = os.path.join(song_dir, filename)

                # Save the file
                with open(filepath, 'wb') as f:
                    f.write(file_bytes)

                # Generate clean title and artist from filename
                title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
                artist = 'Unknown Artist'
                if ' - ' in filename:
                    parts = filename.split(' - ', 1)
                    artist = parts[0].replace('_', ' ').title()
                    title = os.path.splitext(parts[1])[0].replace('_', ' ').title()

                # Send success response with song metadata
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

                import json
                response = {
                    "success": True,
                    "filename": filename,
                    "title": title,
                    "artist": artist,
                    "file": f"song/{filename}"
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
        elif self.path == '/api/chat':
            try:
                print("Received request to /api/chat proxy", flush=True)
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                
                import json
                import urllib.request
                import urllib.error

                payload = json.loads(body.decode('utf-8'))
                messages = payload.get('messages', [])
                
                url = "https://integrate.api.nvidia.com/v1/chat/completions"
                api_key = "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"
                
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                req_data = {
                    "model": "meta/llama-3.1-8b-instruct",
                    "messages": messages,
                    "temperature": 1,
                    "top_p": 0.95,
                    "max_tokens": 16384,
                    "stream": True
                }
                
                req = urllib.request.Request(
                    url,
                    data=json.dumps(req_data).encode('utf-8'),
                    headers=headers,
                    method="POST"
                )
                
                print("Forwarding request to NVIDIA...", flush=True)
                nvidia_response = urllib.request.urlopen(req, timeout=15)
                print("Response received from NVIDIA. Streaming chunks...", flush=True)
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'keep-alive')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                while True:
                    line = nvidia_response.readline()
                    if not line:
                        break
                    self.wfile.write(line)
                    self.wfile.flush()
                print("Streaming complete", flush=True)
                    
            except urllib.error.HTTPError as he:
                print(f"HTTPError forwarding to NVIDIA: {he.code} - {he.reason}", flush=True)
                self.send_response(he.code)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_content = he.read()
                self.wfile.write(error_content)
            except Exception as e:
                print(f"Exception in /api/chat: {e}", flush=True)
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                import json
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Support CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    server = ThreadingHTTPServer(('0.0.0.0', PORT), CustomHTTPRequestHandler)
    print(f"Serving Aethelgard Portfolio at http://localhost:{PORT}")
    server.serve_forever()
