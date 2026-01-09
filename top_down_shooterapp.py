import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: 3 Lives", layout="centered")
st.title("🛡️ Island.io: Survivor")
st.write("Kamu punya **3 Nyawa**! Gunakan WASD dan Klik Mouse untuk bertahan.")

game_html = """
<div style="text-align: center; position: relative;">
    <h2 id="stats">Skor: 0 | Nyawa: ❤️❤️❤️</h2>
    <canvas id="gC" width="600" height="400" style="border:5px solid #2c3e50; background:#ecf0f1; border-radius:10px; cursor:crosshair;"></canvas>
    <div id="gO" style="display:none; position:absolute; top:100px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.9); color:white; padding:30px; border-radius:15px; border:3px solid red; z-index:100;">
        <h1>GAME OVER! 💀</h1>
        <button onclick="location.reload()" style="padding:10px 20px; font-size:18px; cursor:pointer; background:#27ae60; color:white; border:none; border-radius:5px;">COBA LAGI 🔄</button>
    </div>
</div>
<script>
    const cvs = document.getElementById("gC"), ctx = cvs.getContext("2d");
    const stats = document.getElementById("stats"), gOS = document.getElementById("gO");
    let score = 0, lives = 3, isGO = false, keys = {}, mX = 0, mY = 0;
    let ply = { x: 300, y: 200, s: 12, c: "#00a2e8", spd: 4, invuln: 0 };
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
        if(ply.invuln > 0) ply.invuln--;

        bullets.forEach((b, i) => {
            b.x += b.vx; b.y += b.vy;
            if(col(b.x, b.y, 2, walls) || b.x<0 || b.x>600 || b.y<0 || b.y>400) bullets.splice(i, 1);
            enemies.forEach((e, ei) => {
                if(b.x > e.x && b.x < e.x+e.s && b.y > e.y && b.y < e.y+e.s){
                    bullets.splice(i,1); enemies.splice(ei,1); score+=10; spawnE();
                }
            });
        });

        enemies.forEach(e => {
            let nex = e.x, ney = e.y;
            if(e.x < ply.x) nex += 1.3; else nex -= 1.3;
            if(e.y < ply.y) ney += 1.3; else ney -= 1.3;
            if(!col(nex+11, ney+11, 11, walls)){ e.x = nex; e.y = ney; }
            if(ply.invuln <= 0 && Math.sqrt((e.x+11-ply.x)**2 + (e.y+11-ply.y)**2) < (11+ply.s)){
                lives--; ply.invuln = 60; // Kebal selama 1 detik
                if(lives <= 0){ isGO = true; gOS.style.display="block"; }
            }
        });
        stats.innerText = `Skor: ${score} | Nyawa: ${"❤️".repeat(lives)}`;
    }

    function draw() {
        ctx.clearRect(0,0,600,400);
        ctx.fillStyle="#34495e"; walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));
        ctx.fillStyle="#e74c3c"; enemies.forEach(e => ctx.fillRect(e.x, e.y, e.s, e.s));
        ctx.fillStyle="#f39c12"; bullets.forEach(b => { ctx.beginPath(); ctx.arc(b.x, b.y, 4, 0, 7); ctx.fill(); });
        if(ply.invuln % 10 < 5){ ctx.fillStyle=ply.c; ctx.beginPath(); ctx.arc(ply.x, ply.y, ply.s, 0, 7); ctx.fill(); }
        update(); requestAnimationFrame(draw);
    }
    init(); draw();
</script>
"""
components.html(game_html, height=580)
