import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Power-Up Edition", layout="centered")
st.title("🌟 Island.io: Power-Up Chaos")
st.write("Ambil item! ⚡ = Cepat, 🔫 = Triple Shot")

game_html = """
<div style="text-align: center; position: relative;">
    <h2 id="stats">Skor: 0 | Nyawa: ❤️❤️❤️</h2>
    <canvas id="gC" width="600" height="400" style="border:5px solid #2c3e50; background:#ecf0f1; border-radius:10px; cursor:crosshair;"></canvas>
    <div id="gO" style="display:none; position:absolute; top:100px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.9); color:white; padding:30px; border-radius:15px; border:3px solid red; z-index:100;">
        <h1>GAME OVER! 💀</h1>
        <button onclick="location.reload()" style="padding:10px 20px; font-size:18px; cursor:pointer; background:#27ae60; color:white; border:none; border-radius:5px;">MAIN LAGI 🔄</button>
    </div>
</div>
<script>
    const cvs = document.getElementById("gC"), ctx = cvs.getContext("2d");
    const stats = document.getElementById("stats"), gOS = document.getElementById("gO");
    let score = 0, lives = 3, isGO = false, keys = {}, mX = 0, mY = 0;
    let ply = { x: 300, y: 200, s: 12, c: "#00a2e8", spd: 4, inv: 0, pwr: null, pTimer: 0 };
    let bullets = [], enemies = [], walls = [], items = [];

    window.onkeydown = (e) => keys[e.code] = true;
    window.onkeyup = (e) => keys[e.code] = false;
    cvs.onmousemove = (e) => { const r = cvs.getBoundingClientRect(); mX = e.clientX - r.left; mY = e.clientY - r.top; };
    
    cvs.onmousedown = () => {
        if(isGO) return;
        let a = Math.atan2(mY-ply.y, mX-ply.x);
        const shoot = (ang) => bullets.push({x:ply.x, y:ply.y, vx:Math.cos(ang)*10, vy:Math.sin(ang)*10});
        
        shoot(a);
        if(ply.pwr === 'triple') {
            shoot(a + 0.2); shoot(a - 0.2);
        }
    };

    function col(x, y, s, ws) { for(let w of ws){ if(x > w.x-s && x < w.x+w.w+s && y > w.y-s && y < w.y+w.h+s) return true; } return false;
