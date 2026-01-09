import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Pro AI", layout="centered")
st.title("🛡️ Island.io: Smart Navigation")
st.write("AI sekarang punya sistem 'Wall Following'. Mereka akan mencari celah!")

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
    let ply = { x: 300, y: 200, s: 12, c: "#00a2e8", spd: 4, inv: 0 };
    let bullets = [], enemies = [], walls = [];

    window.onkeydown = (e) => keys[e.code] = true;
    window.onkeyup = (e) => keys[e.code] = false;
    cvs.onmousemove = (e) => { const r = cvs.getBoundingClientRect(); mX = e.clientX - r.left; mY = e.clientY - r.top; };
    cvs.onmousedown = () => { if(!isGO){ let a = Math.atan2(mY-ply.y, mX-ply.x); bullets.push({x:ply.x, y:ply.y, vx:Math.cos(a)*10, vy:Math.sin(a)*10}); }};

    function col(x, y, s, ws) { for(let w of ws){ if(x > w.x-s && x < w.x+w.w+s && y > w.y-s && y < w.y+w.h+s) return true; } return false; }

    function spawnE() {
        let ok = false; while(!ok){
            let rx = Math.random()*560+20, ry = Math.random()*360+20;
            if(!col(rx, ry, 15, walls) && Math.sqrt((rx-ply.x)**2 + (ry-ply.y)**2) > 150){ 
                // mode: 'seek' (kejar player), 'avoid' (menyusuri dinding)
                enemies.push({x:rx, y:ry, s:22, mode: 'seek', turnTimer: 0, dir: {x:0, y:0}}); 
                ok = true; 
            }
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
        if(ply.inv > 0) ply.inv--;

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
            let spd = 1.3;
            if (e.mode === 'seek') {
                let dx = ply.x - e.x, dy = ply.y - e.y;
                let dist = Math.sqrt(dx*dx + dy*dy);
                let vx = (dx/dist)*spd, vy = (dy/dist)*spd;

                if (!col(e.x + vx + 11, e.y + vy + 11, 11, walls)) {
                    e.x += vx; e.y += vy;
                } else {
                    // Masuk ke mode 'avoid' (belok 90 derajat)
                    e.mode = 'avoid';
                    e.turnTimer = 40 + Math.random()*40; // durasi melipir dinding
                    e.dir = Math.abs(dx) > Math.abs(dy) ? {x:0, y:dy>0?spd:-spd} : {x:dx>0?spd:-spd, y:0};
                }
            } else {
                // Mode Avoid: Paksa gerak ke satu arah menyamping
                if (!col(e.x + e.dir.x + 11, e.y + e.dir.y + 11, 11, walls)) {
                    e.x += e.dir.x; e.y += e.dir.y;
                } else {
                    e.dir.x *= -1; e.dir.y *= -1; // Balik arah kalau mentok lagi
                }
                e.turnTimer--;
                if (e.turnTimer <= 0) e.mode = 'seek';
            }

            if(ply.inv <= 0 && Math.sqrt((e.x+11-ply.x)**2 + (e.y+11-ply.y)**2) < (11+ply.s)){
                lives--; ply.inv = 60;
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
        if(ply.inv % 10 < 5){ ctx.fillStyle=ply.c; ctx.beginPath(); ctx.arc(ply.x, ply.y, ply.s, 0, 7); ctx.fill(); }
        update(); requestAnimationFrame(draw);
    }
    init(); draw();
</script>
"""
components.html(game_html, height=580)
