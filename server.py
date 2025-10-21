import http.server
import socketserver
import urllib.request
import json

# Port for the MCP server
PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    """Simple HTTP handler that serves weather data at /weather"""
    def do_GET(self):
        if self.path == '/weather':
            # Fetch current weather data for Vancouver, BC using Open-Meteo API
            url = "https://api.open-meteo.com/v1/forecast?latitude=49.25&longitude=-123.1&current_weather=true"
            try:
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode())
                weather = data.get('current_weather', {})
                content = json.dumps(weather).encode()
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                error = {"error": str(e)}
                content = json.dumps(error).encode()
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
