import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island Shooter: Solid Walls", layout="centered")

st.title("🛡️ Island.io: Tactical Cover")
st.write("Dinding sekarang **SOLID**! Gunakan untuk berlindung dan bidik musuh dengan kursor.")

game_html = """
<div style="text-align: center;">
    <h2 id="scoreBoard">Skor: 0</h2>
    <canvas id="gameCanvas" width="600" height="400" style="border:5px solid #2c3e50; background: #ecf0f1; border-radius: 10px; cursor: crosshair;"></canvas>
    <div id="gameOverScreen" style="display:none; position: absolute; top: 150px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.9); color: white; padding: 30px; border-radius: 15px; border: 2px solid red; z-index: 10;">
        <h1>DIHANTAM MUSUH! 💀</h1>
        <button onclick="location.reload()" style="padding: 10px 20px; font-size: 18px; cursor: pointer; background: #27ae60; color: white; border: none; border-radius: 5px;">MAINKAN LAGI 🔄</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreBoard = document.getElementById("scoreBoard");
    const gameOverScreen = document.getElementById("gameOverScreen");

    let score = 0;
    let isGameOver = false;
    let player = { x: 300, y: 350, size: 12, color: "#00a2e8", speed: 4 };
    let bullets = [];
    let enemies = [{ x: 50, y: 50, size: 25 }, { x: 550, y: 50, size: 25 }];
    
    let walls = [
        { x: 100, y: 80, w: 150, h: 25 },  // Atas kiri
        { x: 350, y: 80, w: 150, h: 25 },  // Atas kanan
        { x: 280, y: 180, w: 40, h: 40 },  // Tengah (Benteng)
        { x: 50, y: 250, w: 25, h: 100 },  // Bawah kiri vertikal
        { x: 525, y: 250, w: 25, h: 100 }  // Bawah kanan vertikal
    ];
    
    let keys = {};
    let mouseX = 0; let mouseY = 0;

    window.addEventListener("keydown", (e) => keys[e.code] = true);
    window.addEventListener("keyup", (e) => keys[e.code] = false);
    
    canvas.addEventListener("mousemove", (e) => {
        const rect = canvas.getBoundingClientRect();
        mouseX = e.clientX - rect.left;
        mouseY = e.clientY - rect.top;
    });

    canvas.addEventListener("mousedown", () => {
        if (isGameOver) return;
        let angle = Math.atan2(mouseY - player.y, mouseX - player.x);
        bullets.push({ x: player.x, y: player.y, vx: Math.cos(angle) * 9, vy: Math.sin(angle) * 9 });
    });

    function update() {
        if (isGameOver) return;

        let nextX = player.x; let nextY = player.y;
        if (keys["KeyW"]) nextY -= player.speed;
        if (keys["KeyS"]) nextY += player.speed;
        if (keys["KeyA"]) nextX -= player.speed;
        if (keys["KeyD"]) nextX += player.speed;

        let playerHitWall = false;
        walls.forEach(w => {
            if (nextX > w.x - player.size && nextX < w.x + w.w + player.size &&
                nextY > w.y - player.size && nextY < w.y + w.h + player.size) {
                playerHitWall = true;
            }
        });
        if (!playerHitWall) {
            player.x = Math.max(player.size, Math.min(600 - player.size, nextX));
            player.y = Math.max(player.size, Math.min(400 - player.size, nextY));
        }

        bullets.forEach((b, bi) => {
            b.x += b.vx; b.y += b.vy;

            walls.forEach(w => {
                if (b.x > w.x && b.x < w.x + w.w && b.y > w.y && b.y < w.y + w.h) {
                    bullets.splice(bi, 1);
                }
            });

            enemies.forEach((e, ei) => {
                if (b.x > e.x && b.x < e.x + e.size && b.y > e.y && b.y < e.y + e.size) {
                    bullets.splice(bi, 1);
                    enemies.splice(ei, 1);
                    score += 10;
                    scoreBoard.innerText = "Skor: " + score;
                    enemies.push({ x: Math.random()*550, y: 30, size: 25 });
                }
            });

            if (b.x < 0 || b.x > 600 || b.y < 0 || b.y > 400) bullets.splice(bi, 1);
        });

        enemies.forEach(e => {
            if (e.x < player.x) e.x += 1.3; else e.x -= 1.3;
            if (e.y < player.y) e.y += 1.3; else e.y -= 1.3;

            let dx = (e.x + e.size/2) - player.x;
            let dy = (e.y + e.size/2) - player.y;
            if (Math.sqrt(dx*dx + dy*dy) < (e.size/2 + player.size)) {
                isGameOver = true;
                gameOverScreen.style.display = "block";
            }
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#2c3e50";
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));
        ctx.fillStyle = "#e74c3c";
        enemies.forEach(e => ctx.fillRect(e.x, e.y, e.size, e.size));
        ctx.fillStyle = "#f39c12";
        bullets.forEach(b => { ctx.beginPath(); ctx.arc(b.x, b.y, 4, 0, Math.PI*2); ctx.fill(); });
        ctx.fillStyle = player.color;
        ctx.beginPath(); ctx.arc(player.x, player.y, player.size, 0, Math.PI*2); ctx.fill();
        
        ctx.strokeStyle = "rgba(44, 62, 80, 0.15)";
        ctx.setLineDash([5, 5]);
        ctx.beginPath(); ctx.moveTo(player.x, player.y); ctx.lineTo(mouseX, mouseY); ctx.stroke();
        ctx.setLineDash([]);
        
        update();
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

components.html(game_html, height=580)
