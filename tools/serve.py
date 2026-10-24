"""맥미니 미리 보기용 로컬 서버 (영상 구간 요청 지원, Safari에서도 영상 재생).
사용: python3 tools/serve.py        → http://localhost:8090
     python3 tools/serve.py 8091   → 다른 포트"""
import http.server, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def translate_path(self, path):
        p = super().translate_path(path)
        if not os.path.exists(p) and os.path.isfile(p.rstrip("/") + ".html"):
            return p.rstrip("/") + ".html"
        return p

    def send_head(self):
        rng = self.headers.get("Range")
        path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path):
            return super().send_head()
        m = re.match(r"bytes=(\d*)-(\d*)", rng)
        size = os.path.getsize(path)
        start = int(m.group(1)) if m and m.group(1) else 0
        end = int(m.group(2)) if m and m.group(2) else size - 1
        end = min(end, size - 1)
        if start > end:
            self.send_error(416); return None
        f = open(path, "rb"); f.seek(start)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()
        self._remain = end - start + 1
        return f

    def copyfile(self, src, out):
        n = getattr(self, "_remain", None)
        if n is None:
            return super().copyfile(src, out)
        while n > 0:
            buf = src.read(min(65536, n))
            if not buf: break
            out.write(buf); n -= len(buf)
        self._remain = None


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
print(f"http://localhost:{port}  (끄려면 Ctrl+C)")
http.server.ThreadingHTTPServer(("", port), H).serve_forever()
