#!/usr/bin/env python3
"""Heath local preview server.
Serves this folder at http://localhost:8000, reloads the page in your browser whenever a file here changes,
and saves waitlist signups to waitlist.csv.
Run:  python3 server.py   (or double-click start.command on a Mac)
"""
import csv, json, os, re, sys, webbrowser, threading
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8000
CSV = os.path.join(ROOT, "waitlist.csv")
EMAIL = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
WATCH = (".html", ".css", ".js", ".svg", ".jpg", ".webp", ".png", ".json")
RELOAD = b"""
<script>(function(){var v=null;function t(){fetch('/__v',{cache:'no-store'}).then(function(r){return r.text()}).then(function(x){if(v===null)v=x;else if(x!==v)location.reload();setTimeout(t,700)}).catch(function(){setTimeout(t,2000)})}t()})();</script>
"""

def version():
    m = 0
    for dp, dn, fn in os.walk(ROOT):
        for f in fn:
            if f.endswith(WATCH):
                try: m = max(m, os.stat(os.path.join(dp, f)).st_mtime_ns)
                except OSError: pass
    return str(m)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/__v":
            return self.send(200, "text/plain", version().encode())
        if path == "/": path = "/index.html"
        if path.endswith(".html"):
            fp = os.path.join(ROOT, path.lstrip("/"))
            if os.path.isfile(fp):
                with open(fp, "rb") as f: body = f.read()
                return self.send(200, "text/html; charset=utf-8", body + RELOAD)
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/waitlist":
            self.send_error(404); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            email = json.loads(self.rfile.read(min(n, 2048)) or b"{}").get("email", "").strip().lower()
        except Exception:
            email = ""
        if not EMAIL.match(email):
            self.send_error(400, "Invalid email"); return
        new = not os.path.exists(CSV)
        with open(CSV, "a", newline="") as f:
            w = csv.writer(f)
            if new: w.writerow(["email", "joined_at"])
            w.writerow([email, datetime.now(timezone.utc).isoformat(timespec="seconds")])
        self.send(200, "application/json", b'{"ok":true}')

    def log_message(self, fmt, *args):
        if self.command == "POST": sys.stderr.write("waitlist signup saved\n")

if __name__ == "__main__":
    url = f"http://localhost:{PORT}"
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Heath is running at {url}  (auto-reloads on save; press Ctrl+C to stop)")
    if "--no-open" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\nStopped.")
