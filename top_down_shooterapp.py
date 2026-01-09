import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island Shooter: Mouse Aim", layout="centered")

st.title("🏹 Island.io: Target & Survive")
st.write("Gunakan **WASD** untuk gerak, **Klik Mouse** untuk menembak ke arah kursor!")

game_html = """
<div style="text-align: center;">
    <h2 id="scoreBoard">Skor: 0</h2>
    <canvas id="gameCanvas" width="600" height="400" style="border:5px solid #2c3e50; background: #ecf0f1; border-radius: 10px; cursor: crosshair;"></canvas>
    <div id="gameOverScreen" style="display:none; position: absolute; top: 150px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.8); color: white; padding: 20px; border-radius: 10px;">
        <h1>DIHANTAM MUSUH! 💀</h1>
        <button onclick="location.reload()" style="padding: 10px 20px; font-size: 18px; cursor: pointer;">MAINKAN LAGI 🔄</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const scoreBoard = document.getElementById("scoreBoard");
    const gameOverScreen = document.getElementById("gameOverScreen");

    let score = 0;
    let isGameOver = false;
    let player = { x: 300, y: 200, size: 15, color: "#00a2e8", speed: 4 };
    let bullets = [];
    let enemies = [
        { x: 50, y: 50, size: 25 },
        { x: 550, y: 350, size: 25 }
    ];
    let walls = [
        { x: 100, y: 100, w: 150, h: 20 },
        { x: 430, y: 250, w: 20, h: 100 }
    ];
    let keys = {};
    let mouseX = 0;
    let mouseY = 0;

    window.addEventListener("keydown", (e) => keys[e.code] = true);
    window.addEventListener("keyup", (e) => keys[e.code] = false);
    
    // Track Mouse Position
    canvas.addEventListener("mousemove", (e) => {
        const rect = canvas.getBoundingClientRect();
        mouseX = e.clientX - rect.left;
        mouseY = e.clientY - rect.top;
    });

    // Shooting with Click
    canvas.addEventListener("mousedown", () => {
        if (isGameOver) return;
        // Hitung sudut dari player ke mouse
        let angle = Math.atan2(mouseY - player.y, mouseX - player.x);
        bullets.push({ 
            x: player.x, 
            y: player.y, 
            vx: Math.cos(angle) * 7, 
            vy: Math.sin(angle) * 7 
        });
    });

    function update() {
        if (isGameOver) return;

        let nextX = player.x;
        let nextY = player.y;

        if (keys["KeyW"]) nextY -= player.speed;
        if (keys["KeyS"]) nextY += player.speed;
        if (keys["KeyA"]) nextX -= player.speed;
        if (keys["KeyD"]) nextX += player.speed
