import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island Shooter: Solid Walls", layout="centered")

st.title("🛡️ Island.io: Tactical Cover")
st.write("Dinding sekarang **SOLID**! Gunakan untuk berlindung dari kejaran musuh.")

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
    
    // MENAMBAH LEBIH BANYAK DINDING
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
    
    canvas.addEventListener("mousemove
