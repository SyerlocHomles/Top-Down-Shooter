import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="IO Style Shooter", layout="centered")

st.title("🏹 Island.io Shooter")
st.write("Misi: Tembak kotak merah! Gunakan **WASD** dan **SPASI**.")

game_html = """
<div style="text-align: center;">
    <h2 id="scoreBoard">Skor: 0</h2>
    <canvas id="gameCanvas" width="600" height="400" style="border:5px solid #2c3e50; background: #ecf0f1; border-radius: 10px;"></canvas>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreBoard = document.getElementById("scoreBoard");

    let score = 0;
    let player = { x: 300, y: 200, size: 15, color: "#00a2e8", speed: 4 };
    let bullets = [];
    let enemies = [
        { x: 50, y: 50, size: 25 },
        { x: 550, y: 350, size: 25 }
    ];
    let walls = [
        { x: 100, y: 100, w: 150, h: 20 },
        { x: 350, y: 250, w: 20, h: 100 }
    ];
    let keys = {};

    window.addEventListener("keydown", (e) => keys[e.code] = true);
    window.addEventListener("keyup", (e) => keys[e.code] = false);

    function update() {
        let nextX = player.x;
        let nextY = player.y;

        if (keys["KeyW"]) nextY -= player.speed;
        if (keys["KeyS"]) nextY += player.speed;
        if (keys["KeyA"]) nextX -= player.speed;
        if (keys["KeyD"]) nextX += player.speed;
        
        // Tembak Peluru
        if (keys["Space"]) {
            bullets.push({ x: player.x, y: player.y, speed: 8 });
            keys["Space"] = false; 
        }

        // Cek Tabrakan Tembok
        let hitWall = false;
        walls.forEach(w => {
            if (nextX > w.x - 15 && nextX < w.x + w.w + 15 &&
                nextY > w.y - 15 && nextY < w.y + w.h + 15) {
                hitWall = true;
            }
        });

        if (!hitWall) {
            player.x = Math.max(15, Math.min(585, nextX));
            player.y = Math.max(15, Math.min(385, nextY));
        }

        // Update Peluru & Cek Hit Musuh
        bullets.forEach((b, bi) => {
            b.x += b.speed;
            enemies.forEach((e, ei) => {
                if (b.x > e.x && b.x < e.x + e.size && b.y > e.y && b.y < e.y + e.size) {
                    bullets.splice(bi, 1);
                    enemies.splice(ei, 1);
                    score += 10;
                    scoreBoard.innerText = "Skor: " + score;
                    // Munculkan musuh baru (Spawn)
                    enemies.push({ x: Math.random()*500, y: Math.random()*300, size: 25 });
                }
            });
            if (b.x > 600) bullets.splice(bi, 1);
        });

        // Musuh Mengejar Player
        enemies.forEach(e => {
            if (e.x < player.x) e.x += 0.5;
            else e.x -= 0.5;
            if (e.y < player.y) e.y += 0.5;
            else e.y -= 0.5;
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Gambar Tembok
        ctx.fillStyle = "#34495e";
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));

        // Gambar Musuh
        ctx.fillStyle = "#e74c3c";
        enemies.forEach(e => ctx.fillRect(e.x, e.y, e.size, e.size));

        // Gambar Peluru
        ctx.fillStyle = "#f1c40f";
        bullets.forEach(b => {
            ctx.beginPath();
            ctx.arc(b.x, b.y, 5, 0, Math.PI*2);
            ctx.fill();
        });

        // Gambar Player
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.arc(player.x, player.y, player.size, 0, Math.PI*2);
        ctx.fill();

        update();
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""

components.html(game_html, height=500)
