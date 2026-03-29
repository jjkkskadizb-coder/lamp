#!/usr/bin/env python3
"""
Indian Style Animated Oil Lamp (Diya) - Local Web Server
Run this script and open http://localhost:8000 in your browser
"""

import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8000

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indian Oil Lamp (Diya) - Animated</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: none;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(145deg, #1a0f0a 0%, #2d1a10 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', 'Poppins', 'Arial', sans-serif;
            overflow: hidden;
        }

        /* Decorative rangoli background */
        .rangoli {
            position: fixed;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }

        .rangoli-pattern {
            position: absolute;
            width: 600px;
            height: 600px;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: radial-gradient(circle, rgba(255,140,0,0.08) 0%, rgba(255,80,0,0.04) 50%, transparent 70%);
        }

        .container {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        /* Main lamp container */
        .lamp {
            position: relative;
            width: 400px;
            height: 450px;
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));
            transition: transform 0.3s ease;
        }

        .lamp:hover {
            transform: scale(1.02);
        }

        /* Oil pool / Pancha (base) */
        .oil-base {
            position: relative;
            width: 220px;
            height: 60px;
            background: radial-gradient(ellipse at 50% 30%, #b87333, #8b4513);
            border-radius: 50%;
            box-shadow: 0 8px 15px rgba(0,0,0,0.4), inset 0 2px 5px rgba(255,215,140,0.5);
            margin-top: auto;
            margin-bottom: 10px;
        }

        .oil-base::before {
            content: "";
            position: absolute;
            top: -12px;
            left: 10%;
            width: 80%;
            height: 25px;
            background: radial-gradient(ellipse, #d4943a, #a05a1a);
            border-radius: 50%;
        }

        /* Oil surface */
        .oil-surface {
            position: absolute;
            width: 85%;
            height: 30px;
            background: radial-gradient(ellipse, #ffc966, #e6a017);
            border-radius: 50%;
            top: -8px;
            left: 7.5%;
            box-shadow: inset 0 1px 3px rgba(255,255,200,0.8), 0 0 10px rgba(255,100,0,0.3);
        }

        /* Main body of diya (bowl) */
        .diya-body {
            position: relative;
            width: 200px;
            height: 70px;
            background: linear-gradient(165deg, #c97e2a, #a05518);
            border-radius: 50% 50% 45% 45%;
            box-shadow: inset 0 -5px 0 #6b3a10, 0 5px 12px rgba(0,0,0,0.3);
        }

        .diya-body::after {
            content: "";
            position: absolute;
            top: -18px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 22px;
            background: #e0a030;
            border-radius: 20px 20px 10px 10px;
        }

        /* Spout (nozzle for wick) */
        .spout {
            position: absolute;
            width: 45px;
            height: 18px;
            background: #8b5a2b;
            top: -20px;
            right: 30px;
            border-radius: 10px 8px 5px 5px;
            transform: rotate(-15deg);
        }

        /* Decorative rim patterns */
        .decor {
            position: absolute;
            width: 220px;
            height: 15px;
            bottom: -5px;
            left: -10px;
            background: repeating-linear-gradient(90deg, #ffd966, #ffd966 8px, #ffaa33 8px, #ffaa33 16px);
            border-radius: 0 0 20px 20px;
        }

        /* === WICK === */
        .wick {
            position: absolute;
            width: 8px;
            height: 32px;
            background: linear-gradient(90deg, #3e2a1a, #5c3d1e);
            border-radius: 4px;
            top: -40px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 2;
        }

        .wick::before {
            content: "";
            position: absolute;
            width: 10px;
            height: 10px;
            background: #f5a623;
            border-radius: 50%;
            top: -4px;
            left: -1px;
            filter: blur(2px);
        }

        /* === FLAME ANIMATION === */
        .flame {
            position: absolute;
            width: 30px;
            height: 60px;
            background: radial-gradient(circle at 50% 20%, #ffdd77, #ff6600);
            border-radius: 50% 50% 40% 40%;
            top: -80px;
            left: 50%;
            transform: translateX(-50%);
            filter: blur(2px);
            box-shadow: 0 0 25px rgba(255, 80, 0, 0.8), 0 0 45px rgba(255, 150, 0, 0.5);
            animation: flicker 0.15s infinite alternate;
            z-index: 3;
        }

        /* Inner flame */
        .flame-inner {
            position: absolute;
            width: 16px;
            height: 38px;
            background: radial-gradient(circle at 50% 20%, #fff5cc, #ffaa33);
            border-radius: 50%;
            top: 12px;
            left: 50%;
            transform: translateX(-50%);
            filter: blur(1px);
            animation: flickerInner 0.12s infinite alternate;
        }

        @keyframes flicker {
            0% {
                transform: translateX(-50%) scaleY(1) scaleX(1);
                box-shadow: 0 0 20px #ff8000, 0 0 40px #ff5500;
            }
            25% {
                transform: translateX(-48%) scaleY(1.08) scaleX(0.96);
                box-shadow: 0 0 28px #ffaa33, 0 0 50px #ff6600;
            }
            50% {
                transform: translateX(-52%) scaleY(0.94) scaleX(1.05);
                box-shadow: 0 0 22px #ff9933, 0 0 44px #ff4400;
            }
            75% {
                transform: translateX(-49%) scaleY(1.03) scaleX(0.98);
                box-shadow: 0 0 26px #ffaa44, 0 0 48px #ff7700;
            }
            100% {
                transform: translateX(-51%) scaleY(0.97) scaleX(1.02);
                box-shadow: 0 0 24px #ff8811, 0 0 42px #ff5500;
            }
        }

        @keyframes flickerInner {
            0% {
                transform: translateX(-50%) scaleY(1);
                opacity: 0.9;
            }
            100% {
                transform: translateX(-48%) scaleY(0.92);
                opacity: 1;
            }
        }

        /* Glow effect around lamp */
        .glow {
            position: absolute;
            width: 140px;
            height: 140px;
            background: radial-gradient(circle, rgba(255,140,0,0.25), transparent 70%);
            border-radius: 50%;
            top: -100px;
            left: 50%;
            transform: translateX(-50%);
            pointer-events: none;
            animation: pulseGlow 1.5s infinite alternate;
        }

        @keyframes pulseGlow {
            0% {
                opacity: 0.5;
                transform: translateX(-50%) scale(0.9);
            }
            100% {
                opacity: 1;
                transform: translateX(-50%) scale(1.2);
            }
        }

        /* Smoke particles (optional indian touch) */
        .smoke {
            position: absolute;
            width: 4px;
            height: 4px;
            background: rgba(180, 120, 70, 0.3);
            border-radius: 50%;
            top: -110px;
            left: 50%;
            pointer-events: none;
            animation: smokeRise 2.5s infinite ease-out;
        }

        @keyframes smokeRise {
            0% {
                transform: translateX(-50%) translateY(0) scale(1);
                opacity: 0.4;
            }
            100% {
                transform: translateX(calc(-50% + 15px)) translateY(-80px) scale(3);
                opacity: 0;
            }
        }

        /* Title and text */
        .title {
            margin-top: 30px;
            font-size: 2rem;
            color: #ffdd99;
            text-shadow: 0 2px 8px #b85c1a, 0 0 5px #ffaa44;
            letter-spacing: 2px;
            font-weight: 500;
        }

        .subtitle {
            color: #e6bc84;
            font-size: 1rem;
            margin-top: 8px;
            text-shadow: 0 1px 3px #3a1e0a;
            font-style: italic;
        }

        .instruction {
            margin-top: 30px;
            color: #c9924b;
            font-size: 0.85rem;
            background: rgba(0,0,0,0.4);
            padding: 8px 18px;
            border-radius: 40px;
            backdrop-filter: blur(4px);
        }

        /* Small decorative dots (Indian motif) */
        .dots {
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 12px;
        }
        .dot {
            width: 8px;
            height: 8px;
            background: #ffb347;
            border-radius: 50%;
            opacity: 0.7;
            animation: twinkle 1.2s infinite alternate;
        }
        .dot:nth-child(2) { animation-delay: 0.3s; }
        .dot:nth-child(3) { animation-delay: 0.6s; }
        @keyframes twinkle {
            0% { opacity: 0.3; transform: scale(0.8);}
            100% { opacity: 1; transform: scale(1.2);}
        }

        /* Responsive */
        @media (max-width: 550px) {
            .lamp { transform: scale(0.85); }
            .title { font-size: 1.5rem; }
        }
    </style>
</head>
<body>
    <div class="rangoli">
        <div class="rangoli-pattern"></div>
    </div>
    <div class="container">
        <div class="lamp" id="lamp">
            <!-- Glow effect -->
            <div class="glow"></div>
            
            <!-- Smoke particles (multiple) -->
            <div class="smoke" style="animation-delay: 0s;"></div>
            <div class="smoke" style="animation-delay: 0.8s; left: 48%;"></div>
            <div class="smoke" style="animation-delay: 1.5s; left: 52%;"></div>
            
            <!-- Flame -->
            <div class="flame">
                <div class="flame-inner"></div>
            </div>
            
            <!-- Wick -->
            <div class="wick"></div>
            
            <!-- Diya body with spout -->
            <div class="diya-body">
                <div class="spout"></div>
                <div class="decor"></div>
            </div>
            
            <!-- Oil base -->
            <div class="oil-base">
                <div class="oil-surface"></div>
            </div>
            
            <!-- Decorative dots at bottom -->
            <div class="dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
        
        <div class="title">
            🪔 Deepam Jyothi 🪔
        </div>
        <div class="subtitle">
            Traditional Indian Oil Lamp (Diya)
        </div>
        <div class="instruction">
            ✨ Click on the lamp to increase the flame glow! ✨
        </div>
    </div>

    <script>
        const lamp = document.getElementById('lamp');
        const flame = document.querySelector('.flame');
        const glow = document.querySelector('.glow');
        let intensity = 1;
        
        // Click to increase brightness and flame size (Indian tradition: light the lamp)
        lamp.addEventListener('click', () => {
            intensity = Math.min(intensity + 0.2, 2.2);
            updateFlame();
            // reset after 3 seconds back to normal slowly
            setTimeout(() => {
                if(intensity > 1) {
                    intensity = Math.max(1, intensity - 0.15);
                    updateFlame();
                }
            }, 2000);
        });
        
        function updateFlame() {
            const scaleVal = 0.8 + (intensity * 0.2);
            const blurVal = Math.max(2, 6 - intensity);
            flame.style.transform = `translateX(-50%) scale(${scaleVal})`;
            flame.style.filter = `blur(${blurVal * 0.6}px)`;
            flame.style.boxShadow = `0 0 ${25 * intensity}px rgba(255,80,0,0.9), 0 0 ${50 * intensity}px rgba(255,150,0,0.6)`;
            glow.style.transform = `translateX(-50%) scale(${0.8 + intensity * 0.2})`;
            glow.style.opacity = 0.5 + intensity * 0.2;
        }
        
        // Additional random subtle flame flicker variations via js (enhance)
        setInterval(() => {
            if(Math.random() > 0.7) {
                const randScale = 0.98 + Math.random() * 0.07;
                flame.style.transform = `translateX(-50%) scale(${randScale})`;
                setTimeout(() => {
                    if(Math.random() > 0.5)
                        flame.style.transform = `translateX(-50%) scale(${0.8 + intensity * 0.2})`;
                }, 80);
            }
        }, 120);
        
        // Add floating diya sound effect metaphor (console only, but adds charm)
        console.log("%c✨ Shubh Deepavali! The lamp of knowledge burns bright ✨", "color: #ffaa33; font-size: 16px; font-style: italic;");
    </script>
</body>
</html>
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve our HTML content"""
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Page Not Found')

def open_browser():
    """Open browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{PORT}')

def main():
    """Start the HTTP server"""
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"\n{'='*50}")
        print(f"🪔 INDIAN OIL LAMP (DEEPAM) 🪔")
        print(f"{'='*50}")
        print(f"✨ Server running at: http://localhost:{PORT}")
        print(f"✨ Press Ctrl+C to stop the server")
        print(f"✨ Click on the lamp to make the flame brighter!")
        print(f"{'='*50}\n")
        
        # Open browser automatically
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🪔 Server stopped. The light within continues to shine! 🪔\n")

if __name__ == "__main__":
    main()
