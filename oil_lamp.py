#!/usr/bin/env python3
import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8000))

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indian Oil Lamp - Diya</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{min-height:100vh;background:linear-gradient(145deg,#1a0f0a,#2d1a10);display:flex;justify-content:center;align-items:center;font-family:'Segoe UI',Arial,sans-serif;overflow:hidden;}
        .container{text-align:center;z-index:10;}
        .lamp{position:relative;width:400px;height:450px;display:flex;flex-direction:column;align-items:center;cursor:pointer;}
        .oil-base{position:relative;width:220px;height:60px;background:radial-gradient(ellipse at 50% 30%,#b87333,#8b4513);border-radius:50%;margin-top:auto;margin-bottom:10px;}
        .diya-body{position:relative;width:200px;height:70px;background:linear-gradient(165deg,#c97e2a,#a05518);border-radius:50% 50% 45% 45%;}
        .wick{position:absolute;width:8px;height:32px;background:#3e2a1a;border-radius:4px;top:-40px;left:50%;transform:translateX(-50%);}
        .flame{position:absolute;width:30px;height:60px;background:radial-gradient(circle at 50% 20%,#ffdd77,#ff6600);border-radius:50% 50% 40% 40%;top:-80px;left:50%;transform:translateX(-50%);filter:blur(2px);animation:flicker 0.15s infinite alternate;}
        .flame-inner{position:absolute;width:16px;height:38px;background:radial-gradient(circle at 50% 20%,#fff5cc,#ffaa33);border-radius:50%;top:12px;left:50%;transform:translateX(-50%);}
        .glow{position:absolute;width:140px;height:140px;background:radial-gradient(circle,rgba(255,140,0,0.25),transparent 70%);border-radius:50%;top:-100px;left:50%;transform:translateX(-50%);animation:pulseGlow 1.5s infinite alternate;}
        .title{margin-top:30px;font-size:2rem;color:#ffdd99;text-shadow:0 2px 8px #b85c1a;}
        .subtitle{color:#e6bc84;margin-top:8px;font-style:italic;}
        .instruction{margin-top:30px;color:#c9924b;background:rgba(0,0,0,0.4);padding:8px 18px;border-radius:40px;}
        @keyframes flicker{
            0%{transform:translateX(-50%) scaleY(1);}
            100%{transform:translateX(-48%) scaleY(1.08);}
        }
        @keyframes pulseGlow{
            0%{opacity:0.5;transform:translateX(-50%) scale(0.9);}
            100%{opacity:1;transform:translateX(-50%) scale(1.2);}
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="lamp" id="lamp">
            <div class="glow"></div>
            <div class="flame"><div class="flame-inner"></div></div>
            <div class="wick"></div>
            <div class="diya-body"></div>
            <div class="oil-base"></div>
        </div>
        <div class="title">🪔 Deepam Jyothi 🪔</div>
        <div class="subtitle">Traditional Indian Oil Lamp (Diya)</div>
        <div class="instruction">✨ Click on the lamp to increase the flame glow! ✨</div>
    </div>
    <script>
        const lamp=document.getElementById('lamp');
        const flame=document.querySelector('.flame');
        const glow=document.querySelector('.glow');
        let intensity=1;
        lamp.addEventListener('click',()=>{
            intensity=Math.min(intensity+0.3,2);
            flame.style.transform=`translateX(-50%) scale(${0.8+intensity*0.2})`;
            flame.style.boxShadow=`0 0 ${25*intensity}px rgba(255,80,0,0.9)`;
            glow.style.transform=`translateX(-50%) scale(${0.8+intensity*0.2})`;
            setTimeout(()=>{
                if(intensity>1){
                    intensity=Math.max(1,intensity-0.2);
                    flame.style.transform=`translateX(-50%) scale(${0.8+intensity*0.2})`;
                    glow.style.transform=`translateX(-50%) scale(${0.8+intensity*0.2})`;
                }
            },1500);
        });
    </script>
</body>
</html>"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode())

print(f"Server running on port {PORT}")
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
