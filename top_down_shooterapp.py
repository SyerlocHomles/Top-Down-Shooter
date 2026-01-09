import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Chaos", layout="centered")
st.title("🌪️ Island.io: Random Chaos")
st.write("Musuh spawn acak! WASD untuk gerak, Klik Mouse untuk nembak.")

game_html = """
<div style="text-align: center; position: relative;">
    <h2 id="scB">Skor: 0</h2>
    <canvas id="gC" width="600" height="400" style="border:5px solid #2c3; background:#ecf0f1; border-radius:10px; cursor:crosshair;"></canvas>
    <div id="gO" style="display:none; position:absolute; top:100px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.9); color:white; padding:30px; border-radius:15px; border:3px solid red; z-index:100;">
        <h1>DIHANTAM MUSUH! 💀</h1>
        <button onclick="location.reload()" style="padding:10px 20px; font-size:18px; cursor:pointer; background:#27ae60; color:white; border:none; border-radius:5px;">MAIN LAGI 🔄</button>
    </div>
</div>
<script>
    const cvs = document.getElementById("gC"), ctx = cvs.getContext("2d");
    const scB = document.getElementById("scB"), gOS = document.getElementById("gO");
    let score = 0, isGO = false, keys = {}, mX = 0, mY = 0;
    let ply = { x: 300, y: 200, s: 12, c: "#00a2e8", spd: 4 };
    let bullets = [], enemies = [], walls = [];

    window.onkeydown = (e) => keys[e.code] = true;
    window.onkeyup = (e) => keys[e.code] = false;
    cvs.onmousemove = (e) => { const r = cvs.getBoundingClientRect(); mX = e.clientX - r.left; mY = e.clientY - r.top; };
    cvs.onmousedown = () => { if(!isGO){ let a = Math.atan2(mY-ply.y, mX-ply.x); bullets.push({x:ply.x, y:ply.y, vx:Math.cos(a)*10, vy:Math.sin(a)*10}); }};

    function col(x, y, s, ws) { for(let w of ws){ if(x > w.x-s && x < w.x+w.w+s && y > w.y-s && y < w.y+w.h+s) return true; } return false; }

    function spawnE() {
        let ok = false; while(!ok){
            let rx = Math.random()*560+20, ry = Math.random()*360+20;
            let d = Math.sqrt((rx-ply.x)**2 + (ry-ply.y)**2);
            if(!col(rx, ry, 15, walls) && d > 150){ enemies.push({x:rx, y:ry, s:22}); ok = true; }
        }
    }

    function init() {
        walls = []; for(let i=0; i<6; i++){
            let w=Math.random()*80+40, h=Math.random()*80+40, x=Math.random()*500+50, y=Math.random()*300+50;
            if(!(x<350 && x+w>250 && y<250 && y+h>150)) walls.push({x,y,w,h});
        }
        for(let i=0; i<4; i++) spawnE();
    }

    function update() {
        if(isGO) return;
        let nx = ply.x, ny = ply.y;
        if(keys["KeyW"]) ny -= ply.spd; if(keys["KeyS"]) ny += ply.spd;
        if(keys["KeyA"]) nx -= ply.spd; if(keys["KeyD"]) nx += ply.spd;
        if(!col(nx, ny, ply.s, walls)){ ply.x = Math.max(ply.s, Math.min(588, nx)); ply.y = Math.max(ply.s, Math.min(388, ny)); }

        bullets.forEach((b, i) => {
            b.x += b.vx; b.y += b.vy;
            if(col(b.x, b.y, 2, walls) || b.x<0 || b.x>600 || b.y<0 || b.y>400) bullets.splice(i, 1);
            enemies.forEach((e, ei) => {
                if(b.x > e.x && b.x < e.x+e.s && b.y > e.y && b.y < e.y+e.s){
                    bullets.splice(i,1); enemies.splice(ei,1); score+=10; scB.innerText="Skor: "+score; spawnE();
                }
            });
        });

        enemies.forEach(e => {
            let nex = e.x, ney = e.y;
            if(e.x < ply.x) nex += 1.3; else nex -= 1.3;
            if(e
