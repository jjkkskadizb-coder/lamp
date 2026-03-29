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
<title>Deepam Jyothi</title>

<style>
body{
    background:#140d07;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    color:white;
    font-family:Arial;
    text-align:center;
}

.container{
    text-align:center;
}

.lamp{
    position:relative;
    width:120px;
    margin:auto;
    cursor:pointer;
}

/* Lamp base */
.base{
    width:120px;
    height:40px;
    background:#8b4513;
    border-radius:50%;
    margin-top:40px;
}

/* Flame */
.flame{
    position:absolute;
    top:-60px;
    left:50%;
    transform:translateX(-50%);
    width:30px;
    height:60px;
    background:orange;
    border-radius:50%;
    animation:flicker 0.2s infinite alternate;
}

/* Glow */
.glow{
    position:absolute;
    top:-80px;
    left:50%;
    transform:translateX(-50%);
    width:80px;
    height:80px;
    background:rgba(255,150,0,0.3);
    border-radius:50%;
    animation:glow 1s infinite alternate;
}

@keyframes flicker{
    from{ transform:translateX(-50%) scaleY(1); }
    to{ transform:translateX(-50%) scaleY(1.2); }
}

@keyframes glow{
    from{ opacity:0.5; }
    to{ opacity:1; }
}
</style>
</head>

<body>

<div class="container">
    <div class="lamp" onclick="boost()">
        <div class="glow" id="glow"></div>
        <div class="flame" id="flame"></div>
        <div class="base"></div>
    </div>

    <h1>🪔 Deepam Jyothi 🪔</h1>
    <p>Click lamp to increase flame</p>
</div>

<script>
function boost(){
    const flame = document.getElementById("flame");
    const glow = document.getElementById("glow");

    flame.style.transform = "translateX(-50%) scale(1.5)";
    glow.style.transform = "translateX(-50%) scale(1.5)";

    setTimeout(()=>{
        flame.style.transform = "translateX(-50%) scale(1)";
        glow.style.transform = "translateX(-50%) scale(1)";
    },500);
}
</script>

</body>
</html>
"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            self.send_response(404)
            self.end_headers()

print("Server running on port", PORT)

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
