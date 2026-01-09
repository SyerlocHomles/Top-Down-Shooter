import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Tactical Pro Evolution", layout="centered")
st.title("⚔️ Island.io: Tactical Pro Evolution")

if "char" not in st.session_state:
    st.session_state.char = None

cols = st.columns(3)
classes = [
    ("🔵 Assault (Rocket)", "#00a2e8", 3, 4.5, "assault"),
    ("🟢 Tank (Shield)", "#2ecc71", 6, 3.0, "tank"),
    ("🟡 Scout (Dash)", "#f1c40f", 2, 6.8, "scout")
]

for i, (name, col, hp, spd, t) in enumerate(classes):
    with cols[i]:
        if st.button(name):
            st.session_state.char = {"hp": hp, "spd": spd, "col": col, "type": t}

if not st.session_state.char:
    st.info("Pilih Class untuk bertarung!")
    st.stop()

game_html = f"""
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; user-select: none;">
    <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
        <div id="ui-lvl">LEVEL: 1</div>
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">❤️❤️❤️</div>
    </div>
    
    <div style="margin: 0 auto 10px; width: 250px;">
        <div id="ui-skill-text" style="color:#00e5ff; font-size: 11px; font-weight:bold;">ULTIMATE READY (SPACE)</div>
        <div style="width:100%; height:12px; background:#333; border-radius:6px; overflow:hidden; border: 1px solid #555;">
            <div id="skill-bar" style="width:0%; height:100%; background: linear-gradient(90deg, #009dff, #00e5ff);"></div>
        </div>
    </div>
    <div id="buff-ui" style="color:#f1c40f; font-size:12px; font-weight:bold; min-height:15px; margin-bottom:5px;"></div>

    <div id="upgrade-menu" style="display:none; position:absolute; width:100%; height:100%; top:0; left:0; background:rgba(0,0,0,0.95); z-index:1000; border-radius:11px;">
        <h2 style="color:white; margin-top:100px;">⬆️ BOSS DEFEATED!</h2>
        <p style="color:#2ecc71;">Map Ter-shuffle & Dinding Berkurang!</p>
        <button onclick="window.applyUpgrade('hp')" style="padding:12px 24px; background:#2ecc71; color:white; border:none; margin:10px; border-radius:8px; cursor:pointer; font-weight:bold;">+1 NYAWA</button>
        <button onclick="window.applyUpgrade('dmg')" style="padding:12px 24px; background:#e74c3c; color:white; border:none; margin:10px; border-radius:8px; cursor:pointer; font-weight:bold;">+1 DAMAGE</button>
    </div>

    <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uLvl = document.getElementById('ui-lvl'), uBar = document.getElementById('skill-bar'),
          uBuff = document.getElementById('buff-ui'), uMenu = document.getElementById('upgrade-menu');

    let score = 0, health = {st.session_state.char['hp']}, level = 1, gameOver = false;
    let keys = {{}}, bullets = [], eBullets = [], enemies = [], walls = [], items = [], particles = [], boss = null;
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {st.session_state.char['spd']},
        type: '{st.session_state.char['type']}', color: '{st.session_state.char['col']}',
        sT: 0, sM: 500, shield: false,
        buffs: {{ speed: 0, triple: 0 }},
        dmg: 5, inv: 0
    }};

    window.applyUpgrade = (type) => {{
        if(type==='hp') health++; else player.dmg++;
        level++; score = 0;
        initWalls();
        uMenu.style.display = 'none';
        requestAnimationFrame(loop);
    }};

    // PERBAIKAN: Memberikan jarak antar dinding agar kroco bisa lewat
    function initWalls() {{
        walls = [];
        let count = Math.max(12 - (level * 2), 4);
        let attempts = 0;
        while(walls.length < count && attempts < 100) {{
            attempts++;
            let w = 40, h = 40;
            let x = 50 + Math.floor(Math.random() * 10) * 50;
            let y = 50 + Math.floor(Math.random() * 6) * 50;
            
            // Cek apakah terlalu dekat dengan karakter
            if(Math.hypot(x+w/2-300, y+h/2-200) < 80) continue;
            
            // Cek apakah menempel dengan dinding lain (jarak min 20px)
            let tooClose = false;
            for(let wall of walls) {{
                if(x < wall.x + wall.w + 25 && x + w + 25 > wall.x &&
                   y < wall.y + wall.h + 25 && y + h + 25 > wall.y) {{
                    tooClose = true; break;
                }}
            }}
            if(!tooClose) walls.push({{x,y,w,h}});
        }}
    }}

    function isInsideWall(x, y, r) {{
        for(let w of walls) {{
            if(x + r > w.x && x - r < w.x + w.w && y + r > w.y && y - r < w.y + w.h) return true;
        }}
        return x < r || x > 600-r || y < r || y > 400-r;
    }}

    function spawnExplosion(x, y, color) {{
        for(let i=0; i<15; i++) particles.push({{x,y,vx:(Math.random()-0.5)*10, vy:(Math.random()-0.5)*10, life:25, c:color}});
    }}

    function triggerRespawn() {{
        health--;
        spawnExplosion(player.x, player.y, "#ff0000");
        player.inv = 180; // 3 detik kedap kedip
        if(health <= 0) gameOver = true;
    }}

    window.onkeydown = e => {{ keys[e.code] = true; if(e.code==='Space') useUlt(); }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    let mx=0, my=0;
    canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

    function useUlt() {{
        if(player.sT < player.sM || gameOver || player.inv > 0) return;
        player.sT = 0;
        if(player.type==='assault') {{
            for(let i=0; i<12; i++) setTimeout(()=>fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), true, true), i*100);
        }} else if(player.type==='tank') {{
            player.shield=true; setTimeout(()=>player.shield=false, 6000);
        }} else if(player.type==='scout') {{
            let a = Math.atan2(my-player.y, mx-player.x);
            let tx = player.x + Math.cos(a)*180, ty = player.y + Math.sin(a)*180;
            if(!isInsideWall(tx, ty, player.r)) {{ player.x=tx; player.y=ty; spawnExplosion(tx,ty,player.color); }}
        }}
    }}

    canvas.onmousedown = () => {{
        if(gameOver || uMenu.style.display === 'block') return;
        let a = Math.atan2(my-player.y, mx-player.x);
        fire(player.x, player.y, a, false, true);
        if(player.buffs.triple > 0) {{ fire(player.x, player.y, a+0.25, false, true); fire(player.x, player.y, a-0.25, false, true); }}
    }};

    function fire(x, y, a, isRocket, isPlayer) {{
        bullets.push({{ x, y, vx: Math.cos(a)*(isRocket?14:10), vy: Math.sin(a)*(isRocket?14:10), r: isRocket?8:4, c: isPlayer?'#FFF':'#F00', p: isPlayer, rk: isRocket }});
    }}

    function update() {{
        if(gameOver || uMenu.style.display === 'block') return;
        
        let s = player.buffs.speed > 0 ? player.speed*1.7 : player.speed;
        let nx=player.x, ny=player.y;
        if(keys['KeyW']) ny-=s; if(keys['KeyS']) ny+=s;
        if(keys['KeyA']) nx-=s; if(keys['KeyD']) nx+=s;
        if(!isInsideWall(nx, player.y, player.r)) player.x=nx;
        if(!isInsideWall(player.x, ny, player.r)) player.y=ny;

        if(player.sT < player.sM) player.sT += 1.5;
        uBar.style.width = Math.min(100, (player.sT/player.sM*100)) + '%';

        if(player.buffs.speed > 0) player.buffs.speed--;
        if(player.buffs.triple > 0) player.buffs.triple--;

        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(isInsideWall(b.x, b.y, b.r)) return false;
            if(b.p) {{
                for(let e of enemies) {{
                    if(Math.hypot(e.x-b.x, e.y-b.y) < e.s/2+b.r) {{
                        e.hp -= b.rk?player.dmg*4:player.dmg;
                        if(e.hp<=0) {{ 
                            if(!boss) {{
                                if(e.color==='#9b59b6') score+=10;
                                else if(e.color==='#e74c3c') score+=5;
                                else score+=3;
                            }}
                            enemies.splice(enemies.indexOf(e), 1); 
                        }}
                        return false;
                    }}
                }}
                if(boss && b.x > boss.x && b.x < boss.x+boss.w && b.y > boss.y && b.y < boss.y+boss.h) {{
                    if(boss.sh) boss.hp = Math.min(boss.mH, boss.hp + (level>=5?2:1));
                    else boss.hp -= player.dmg;
                    return false;
                }}
            }} else {{
                if(Math.hypot(player.x-b.x, player.y-b.y) < player.r+b.r) {{
                    if(player.inv<=0 && !player.shield) triggerRespawn();
                    return false;
                }}
            }}
            return b.x>0 && b.x<600 && b.y>0 && b.y<400;
        }});

        enemies.forEach(e => {{
            let a = Math.atan2(player.y-e.y, player.x-e.x);
            let vx=Math.cos(a)*e.sp, vy=Math.sin(a)*e.sp;
            if(!isInsideWall(e.x+vx, e.y+vy, e.s/2)) {{ e.x+=vx; e.y+=vy; }}
            else {{
                if(!isInsideWall(e.x+vy, e.y-vx, e.s/2)) {{ e.x+=vy; e.y-=vx; }}
                else if(!isInsideWall(e.x-vy, e.y+vx, e.s/2)) {{ e.x-=vy; e.y+=vx; }}
            }}
            e.fT++;
            if(e.fT > 300) {{
                if((e.color==='#e74c3c' && level>=2) || (e.color==='#2ecc71' && level>=3)) fire(e.x, e.y, a, false, false);
                e.fT = 0;
            }}
            if(Math.hypot(player.x-e.x, player.y-e.y) < player.r+e.s/2 && player.inv<=0 && !player.shield) triggerRespawn();
        }});

        if(score >= 500 && !boss) {{
            boss = {{x:250, y:-100, w:90, h:90, hp:600*level, mH:600*level, fT:0, uT:0, sh:false}};
        }}
        if(boss) {{
            let a = Math.atan2(player.y-(boss.y+boss.h/2), player.x-(boss.x+boss.w/2));
            let bvx=Math.cos(a)*1.1, bvy=Math.sin(a)*1.1;
            if(!isInsideWall(boss.x+bvx+boss.w/2, boss.y+bvy+boss.h/2, boss.w/2)) {{ boss.x+=bvx; boss.y+=bvy; }}
            boss.fT++;
            if(boss.fT > 120) {{
                let shots = level>=4?3:level>=2?2:1;
                for(let i=0; i<shots; i++) fire(boss.x+boss.w/2, boss.y+boss.h/2, a+(i*0.25-0.12), false, false);
                boss.fT = 0;
            }}
            boss.sh = boss.hp < boss.mH*0.4;
            if(boss.hp <= 0) {{ boss=null; uMenu.style.display='block'; }}
        }}

        // PERBAIKAN: Respawn kroco minimal jarak 150px dari player
        if(enemies.length < 5) {{
            let ex, ey, dist;
            do {{
                ex = 50 + Math.random() * 500;
                ey = 50 + Math.random() * 300;
                dist = Math.hypot(player.x - ex, player.y - ey);
            }} while (isInsideWall(ex, ey, 25) || dist < 150);

            let r = Math.random();
            let t = r<0.4 ? {{c:'#e74c3c', s:20, sp:1.4, h:5}} : r<0.7 ? {{c:'#2ecc71', s:28, sp:0.7, h:12}} : {{c:'#9b59b6', s:18, sp:2.2, h:4}};
            enemies.push({{x:ex, y:ey, color:t.c, s:t.s, sp:t.sp, hp:t.h, fT:0}});
        }}

        particles.forEach((p,i)=>{{ p.x+=p.vx; p.y+=p.vy; p.life--; if(p.life<=0) particles.splice(i,1); }});
        items = items.filter(it => {{
            if(Math.hypot(player.x-it.x, player.y-it.y) < player.r+15) {{
                if(it.t==='speed') player.buffs.speed=480; else player.buffs.triple=480;
                return false;
            }}
            return true;
        }});

        if(player.inv > 0) player.inv--;
        uScore.innerText = "Skor: " + score;
        uHP.innerText = "❤️".repeat(Math.max(0,health));
        let bt = [];
        if(player.buffs.speed>0) bt.push("⚡ SPEED: " + Math.ceil(player.buffs.speed/60) + "s");
        if(player.buffs.triple>0) bt.push("🔫 TRIPLE: " + Math.ceil(player.buffs.triple/60) + "s");
        uBuff.innerText = bt.join(" | ");
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        walls.forEach(w => {{ ctx.fillStyle='#444'; ctx.fillRect(w.x, w.y, w.w, w.h); ctx.strokeStyle='#555'; ctx.strokeRect(w.x,w.y,w.w,w.h); }});
        items.forEach(it => {{ ctx.fillStyle=it.t==='speed'?'#3498db':'#f1c40f'; ctx.beginPath(); ctx.arc(it.x,it.y,10,0,7); ctx.fill(); }});
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.color; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        particles.forEach(p => {{ ctx.fillStyle=p.c; ctx.globalAlpha=p.life/25; ctx.fillRect(p.x,p.y,3,3); ctx.globalAlpha=1; }});
        if(boss) {{
            ctx.fillStyle=boss.sh?'#00e5ff':'#ff4d4d'; ctx.fillRect(boss.x, boss.y, boss.w, boss.h);
            ctx.fillStyle='#f00'; ctx.fillRect(boss.x, boss.y-12, (boss.hp/boss.mH)*boss.w, 8);
        }}
        if(player.inv <= 0 || (player.inv % 10 < 5)) {{
            ctx.fillStyle=player.color; ctx.beginPath(); ctx.arc(player.x,player.y,player.r,0,7); ctx.fill();
            if(player.shield) {{ ctx.strokeStyle='#00e5ff'; ctx.lineWidth=4; ctx.beginPath(); ctx.arc(player.x,player.y,player.r+6,0,7); ctx.stroke(); }}
        }}
        if(gameOver) {{ ctx.fillStyle='white'; ctx.font='40px Arial'; ctx.textAlign='center'; ctx.fillText("GAME OVER", 300, 200); }}
    }}

    function loop() {{ update(); draw(); if(!gameOver && uMenu.style.display!=='block') requestAnimationFrame(loop); }}
    initWalls();
    setInterval(()=>{{
        if(items.length<2) {{
            let ix=50+Math.random()*500, iy=50+Math.random()*300;
            if(!isInsideWall(ix,iy,15)) items.push({{x:ix, y:iy, t:Math.random()>0.5?'speed':'triple'}});
        }}
    }}, 4000);
    loop();
}})();
</script>
"""

cp.html(game_html, height=600)
