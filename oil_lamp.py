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
<title>🪔 Deepam Jyothi</title>

<style>
body{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:radial-gradient(circle,#1a0f0a,#000);
    font-family:Arial;
    color:white;
    text-align:center;
}

/* Container */
.container{
    display:flex;
    flex-direction:column;
    align-items:center;
}

/* Lamp */
.lamp{
    position:relative;
    width:200px;
    height:200px;
    cursor:pointer;
}

/* Diya bowl */
.bowl{
    position:absolute;
    bottom:0;
    width:160px;
    height:70px;
    background:linear-gradient(#c97e2a,#8b4513);
    border-radius:50% 50% 40% 40%;
    left:50%;
    transform:translateX(-50%);
}

/* Oil shine */
.bowl::after{
    content:'';
    position:absolute;
    top:10px;
    left:20px;
    width:120px;
    height:20px;
    background:rgba(255,255,255,0.2);
    border-radius:50%;
}

/* Wick */
.wick{
    position:absolute;
    bottom:60px;
    left:50%;
    transform:translateX(-50%);
    width:6px;
    height:30px;
    background:#2b1b0f;
    border-radius:3px;
}

/* Flame */
.flame{
    position:absolute;
    bottom:90px;
    left:50%;
    transform:translateX(-50%);
    width:30px;
    height:60px;
    background:radial-gradient(circle at 50% 20%, #fff3b0, #ff6a00);
    border-radius:50% 50% 40% 40%;
    animation:flicker 0.15s infinite alternate;
}

/* Inner flame */
.flame::after{
    content:'';
    position:absolute;
    top:10px;
    left:50%;
    transform:translateX(-50%);
    width:15px;
    height:35px;
    background:radial-gradient(circle,#fff,#ffaa33);
    border-radius:50%;
}

/* Glow */
.glow{
    position:absolute;
    bottom:80px;
    left:50%;
    transform:translateX(-50%);
    width:120px;
    height:120px;
    background:radial-gradient(circle,rgba(255,150,0,0.4),transparent);
    border-radius:50%;
    animation:glow 1.5s infinite alternate;
}

/* Animations */
@keyframes flicker{
    from{ transform:translateX(-50%) scaleY(1); }
    to{ transform:translateX(-48%) scaleY(1.15); }
}

@keyframes glow{
    from{ opacity:0.6; transform:translateX(-50%) scale(0.9); }
    to{ opacity:1; transform:translateX(-50%) scale(1.2); }
}

/* Text */
h1{ margin-top:20px; }
p{ color:#ccc; }
</style>
</head>

<body>

<div class="container">
    <div class="lamp" onclick="boost()">
        <div class="glow" id="glow"></div>
        <div class="flame" id="flame"></div>
        <div class="wick"></div>
        <div class="bowl"></div>
    </div>

    <h1>🪔 Deepam Jyothi 🪔</h1>
    <p>Click lamp to increase brightness</p>
</div>

<script>
function boost(){
    const flame = document.getElementById("flame");
    const glow = document.getElementById("glow");

    flame.style.transform = "translateX(-50%) scale(1.4)";
    glow.style.transform = "translateX(-50%) scale(1.5)";

    setTimeout(()=>{
        flame.style.transform = "translateX(-50%) scale(1)";
        glow.style.transform = "translateX(-50%) scale(1)";
    },600);
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

print("🔥 Diya server running on port", PORT)

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
