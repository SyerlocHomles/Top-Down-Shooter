import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Chaos Edition", layout="centered")

st.title("🌪️ Island.io: Random Chaos")
st.write("Awas! Musuh sekarang bisa muncul di **MANA SAJA**!")

game_html = """
<div style="text-align: center;">
    <h2 id="scoreBoard">Skor: 0</h2>
    <canvas id="gameCanvas" width="600" height="400" style="border:5px solid #2c3e50; background: #ecf0f1; border-radius: 10px; cursor: crosshair;"></canvas>
    <div id="gameOverScreen" style="display:none; position: absolute; top: 150px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.9); color: white; padding: 30px; border-radius: 15px; border: 2px solid red; z-index: 100;">
        <h1>DIHANTAM MUSUH! 💀</h1>
        <button onclick="location.reload()" style="padding: 10px 20px; font-size: 18px; cursor: pointer; background: #27ae60; color: white; border: none; border-radius: 5px;">ACAK ULANG & MAIN 🔄</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreBoard = document.getElementById("scoreBoard");
    const gameOverScreen = document.getElementById("gameOverScreen");

    let score = 0;
    let isGameOver = false;
    let player = { x: 300, y: 200, size: 12, color: "#00a2e8", speed: 4 };
    let bullets = [];
    let enemies = [];
    let walls = [];
    let keys = {};
    let mouseX = 0; let mouseY = 0;

    // --- FUNGSI DETEKSI TABRAKAN ---
    function checkCollision(objX, objY, size, wallList) {
        for (let w of wallList) {
            if (objX > w.x - size && objX < w.x + w.w + size &&
                objY > w.y - size && objY < w.y + w.h + size) {
                return true;
            }
        }
        return false;
    }

    // --- GENERATE MAP ---
    function generateMap() {
        walls = [];
        for (let i = 0; i < 6; i++) {
            let w = Math.random() * 80 + 40;
            let h = Math.random() * 80 + 40;
            let x = Math.random() * (500 - w) + 50;
            let y = Math.random() * (300 - h) + 50;
            // Jangan taruh dinding di tengah (tempat player mulai)
            if (!(x < 350 && x + w > 250 && y < 250 && y + h > 150)) {
                walls.push({ x, y, w, h });
            }
        }
    }

    // --- SPAWN MUSUH (RANDOM DI MANA SAJA) ---
    function spawnEnemy() {
        let spawned = false;
        while (!spawned) {
            let rx = Math.random() * 560 + 20;
            let ry = Math.random() * 360 + 20;
            
            // Cek Jarak dari Player (Biar gak langsung nempel pas spawn)
            let dx = rx - player.x;
            let dy = ry - player.y;
            let distToPlayer = Math.sqrt(dx*dx + dy*dy);

            // Syarat: Tidak di dalam dinding DAN jauh dari player (> 150px)
            if (!checkCollision(rx, ry, 15, walls) && distToPlayer > 150) {
                enemies.push({ x: rx, y: ry, size: 22 });
                spawned = true;
            }
        }
    }

    // Mulai Game
    generateMap();
    for(let i=0; i<3; i++) spawnEnemy();

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

    function update() {
        if (isGameOver) return;

        // Player Move
        let npx = player.x; let npy
