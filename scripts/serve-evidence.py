"""Read-only loopback evidence viewer. Never serves the repository directory."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]
files = {
    "/evidence": (root / "presentation/evidence.html", "text/html; charset=utf-8"),
    "/before.json": (root / "artifacts/stagingguard-before.json", "application/json"),
    "/after.json": (root / "artifacts/stagingguard-after.json", "application/json"),
}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        entry = files.get(urlsplit(self.path).path)
        if not entry or not entry[0].is_file():
            self.send_error(404)
            return
        data = entry[0].read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", entry[1])
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    print("Read-only evidence viewer: http://127.0.0.1:8890/evidence", flush=True)
    ThreadingHTTPServer(("127.0.0.1", 8890), Handler).serve_forever()
