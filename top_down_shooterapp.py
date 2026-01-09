import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Shuffle Edition", layout="centered")

st.title("🎲 Island.io: Shuffle & Survive")
st.write("Dinding sekarang **Solid bagi semua**! Klik 'MAINKAN LAGI' untuk acak peta.")

game_html = """
<div style="text-align: center;">
    <h2 id="scoreBoard">Skor: 0</h2>
    <canvas id="gameCanvas" width="600" height="400" style="border:5px solid #2c3e50; background: #ecf0f1; border-radius: 10px; cursor: crosshair;"></canvas>
    <div id="gameOverScreen" style="display:none; position: absolute; top: 150px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.9); color: white; padding: 30px; border-radius: 15px; border: 2px solid red; z-index: 100;">
        <h1>DIHANTAM MUSUH! 💀</h1>
        <button onclick="location.reload()" style="padding: 10px 20px; font-size: 18px; cursor: pointer; background: #27ae60; color: white; border: none; border-radius: 5px;">SHUFFLE & MAIN LAGI 🔄</button>
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
    let keys = {};
    let mouseX = 0; let mouseY = 0;

    // --- LOGIKA SHUFFLE MAP ---
    let walls = [];
    function generateShuffleMap() {
        walls = [];
        for (let i = 0; i < 6; i++) {
            let w = Math.random() * 100 + 30;
            let h = Math.random() * 100 + 30;
            let x = Math.random() * (500 - w) + 50;
            let y = Math.random() * (300 - h) + 50;
            // Pastikan tidak menimpa posisi awal player
            if (!(x < 400 && x + w > 200 && y > 300)) {
                walls.push({ x, y, w, h });
            }
        }
    }
    generateShuffleMap();

    // Spawn Musuh di tempat acak yang aman
    let enemies = [];
    for(let i=0; i<3; i++) {
        enemies.push({ x: Math.random()*550, y: 20, size: 22 });
    }

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
        bullets.push({ x: player.x, y: player.y, vx: Math.cos(angle) * 10, vy: Math.sin(angle) * 10 });
    });

    function checkCollision(objX, objY, size, wallList) {
        for (let w of wallList) {
            if (objX > w.x - size && objX < w.x + w.w + size &&
                objY > w.y - size && objY < w.y + w.h + size) {
                return true;
            }
        }
        return false;
    }

    function update() {
        if (isGameOver) return;

        // Update Player
        let nextPX = player.x; let nextPY = player.y;
        if (keys["KeyW"]) nextPY -= player.speed;
        if (keys["KeyS"]) nextPY += player.speed;
        if (keys["KeyA"]) nextPX -= player.speed;
        if (keys["KeyD"]) nextPX += player.speed;

        if (!checkCollision(nextPX, nextPY, player.size, walls)) {
            player.x = Math.max(player.size, Math.min(600 - player.size, nextPX));
            player.y = Math.max(player.size, Math.min(400 - player.size, nextPY));
        }

        // Update Peluru
        bullets.forEach((b, bi) => {
            b.x += b.vx; b.y += b.vy;
            if (checkCollision(b.x, b.y, 2, walls) || b.x < 0 || b.x > 600 || b.y < 0 || b.y > 400) {
                bullets.splice(bi, 1);
            }
            enemies.forEach((e, ei) => {
                if (b.x > e.x && b.x < e.x + e.size && b.y > e.y && b.y < e.y + e.size) {
                    bullets.splice(bi, 1); enemies.splice(ei, 1);
                    score += 10; scoreBoard.innerText = "Skor: " + score;
                    enemies.push({ x: Math.random()*550, y: 20, size: 22 });
                }
            });
        });

        // Update Musuh (Solid Enemy Logic)
        enemies.forEach(e => {
            let nextEX = e.x; let nextEY = e.y;
            if (e.x < player.x) nextEX += 1.2; else nextEX -= 1.2;
            if (e.y < player.y) nextEY += 1.2; else nextEY -= 1.2;

            // Musuh juga mentok dinding!
            if (!checkCollision(nextEX + e.size/2, nextEY + e.size/2, e.size/2, walls)) {
                e.x = nextEX; e.y = nextEY;
            }

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
        ctx.fillStyle = "#34495e";
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));
        ctx.fillStyle = "#e74c3c";
        enemies.forEach(e => ctx.fillRect(e.x, e.y, e.size, e.size));
        ctx.fillStyle = "#f39c12";
        bullets.forEach(b => { ctx.beginPath(); ctx.arc(b.x, b.y, 4, 0, Math.PI*2); ctx.fill(); });
        ctx.fillStyle = player.color;
        ctx.beginPath(); ctx.arc(player.x, player.y, player.size, 0, Math.PI*2); ctx.fill();
        
        update();
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

components.html(game_html, height=580)
