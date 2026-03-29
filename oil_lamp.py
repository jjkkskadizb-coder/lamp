#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Indian Oil Lamp</title>
<style>
body{
    background:#1a0f0a;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    color:white;
    font-family:Arial;
    text-align:center;
}
.flame{
    width:40px;
    height:80px;
    background:orange;
    border-radius:50%;
    margin:auto;
    animation:flicker 0.2s infinite alternate;
}
@keyframes flicker{
    from{ transform:scaleY(1); opacity:0.8; }
    to{ transform:scaleY(1.2); opacity:1; }
}
.lamp{ cursor:pointer; }
</style>
</head>

<body>
<div class="lamp" onclick="boost()">
    <div class="flame" id="flame"></div>
    <h1>🪔 Deepam Jyothi 🪔</h1>
    <p>Click lamp to increase flame</p>
</div>

<script>
function boost(){
    const flame = document.getElementById("flame");
    flame.style.transform = "scale(1.5)";
    setTimeout(()=>{
        flame.style.transform = "scale(1)";
    },500);
}
</script>
</body>
</html>
"""

class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        return  # hide logs

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

print("Server running on port", PORT)

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
