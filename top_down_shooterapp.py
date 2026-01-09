import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Boss Battle Fix", layout="centered")
st.title("🏹 Island.io: Boss Revenge & Physics Fix")

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
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif;">
    <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
        <div id="ui-lvl">LEVEL: 1</div>
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">❤️</div>
    </div>
    
    <div id="ui-skill-container" style="width: 250px; margin: 0 auto 10px;">
        <div id="ui-skill-text" style="color:#00e5ff; font-size: 11px; font-weight:bold;">ULTIMATE READY</div>
        <div style="width:100%; height:8px; background:#333; border-radius:4px; overflow:hidden; border: 1px solid #555;">
            <div id="skill-bar" style="width:0%; height:100%; background:#00e5ff;"></div>
        </div>
    </div>
    <div id="buff-ui" style="color:#f1c40f; font-size:12px; font-weight:bold; min-height:15px;"></div>

    <div id="upgrade-menu" style="display:none; position:absolute; width:100%; height:100%; top:0; left:0; background:rgba(0,0,0,0.9); z-index:1000; border-radius:11px;">
        <h2 style="color:white; margin-top:120px;">⬆️ LEVEL UP!</h2>
        <button onclick="applyUp('hp')" style="padding:12px; background:#2ecc71; color:white; border:none; margin:10px; border-radius:5px; cursor:pointer;">TAMBAH NYAWA</button>
        <button onclick="applyUp('atk')" style="padding:12px; background:#e74c3c; color:white; border:none; margin:10px; border-radius:5px; cursor:pointer;">TAMBAH DAMAGE</button>
    </div>

    <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px;"></canvas>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uLvl = document.getElementById('ui-lvl'), uBar = document.getElementById('skill-bar'),
          uBuff = document.getElementById('buff-ui'), uMenu = document.getElementById('upgrade-menu');

    let score = 0, health = {st.session_state.char['hp']}, level = 1, gameOver = false;
    let keys = {{}}, bullets = [], eBullets = [], enemies = [], walls = [], items = [], boss = null;
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {st.session_state.char['spd']},
        type: '{st.session_state.char['type']}', color: '{st.session_state.char['col']}',
        sT: 0, sM: 600, shield: false,
        buffs: {{ speed: 0, triple: 0 }},
        dmg: 5, inv: 0
    }};

    window.applyUp = (type) => {{
        if(type==='hp') health++;
        if(type==='atk') player.dmg += 4;
        uMenu.style.display = 'none';
        level++; initWalls(); requestAnimationFrame(loop);
    }};

    function initWalls() {{
        walls = [];
        for(let i=0; i<5; i++) {{
            let w = 50+Math.random()*70, h = 50+Math.random()*70;
            let x = 50+Math.random()*450, y = 50+Math.random()*250;
            if(Math.hypot(x-300, y-200) > 100) walls.push({{x,y,w,h}});
        }}
    }}

    function isInsideWall(x, y, r) {{
        for(let w of walls) {{
            if(x + r > w.x && x - r < w.x + w.w && y + r > w.y && y - r < w.y + w.h) return true;
        }
        return x < r || x > 600-r || y < r || y > 400-r;
    }}

    window.onkeydown = e => keys[e.code] = true;
    window.onkeyup = e => keys[e.code] = false;
    let mx = 0, my = 0;
    canvas.onmousemove = e => {{
        const r = canvas.getBoundingClientRect();
        mx = e.clientX - r.left; my = e.clientY - r.top;
    }};

    canvas.onmousedown = () => {{
        if(gameOver || uMenu.style.display === 'block') return;
        fire(player.x, player.y, Math.atan2(my - player.y, mx - player.x), false, true);
        if(player.buffs.triple > 0) {{
            fire(player.x, player.y, Math.atan2(my - player.y, mx - player.x) + 0.25, false, true);
            fire(player.x, player.y, Math.atan2(my - player.y, mx - player.x) - 0.25, false, true);
        }}
    }};

    function fire(x, y, a, isRocket, isPlayer) {{
        const b = {{ x, y, vx: Math.cos(a)*(isRocket?14:10), vy: Math.sin(a)*(isRocket?14:10), r: isRocket?8:4, c: isPlayer?player.color:'#f00', rocket: isRocket }};
        if(isPlayer) bullets.push(b); else eBullets.push(b);
    }}

    function update() {{
        if(gameOver || uMenu.style.display === 'block') return;

        if(player.buffs.speed > 0) player.buffs.speed--;
        if(player.buffs.triple > 0) player.buffs.triple--;
        if(player.sT < player.sM) player.sT++;
        uBar.style.width = (player.sT/player.sM*100) + '%';

        if(keys['Space'] && player.sT >= player.sM) {{
            player.sT = 0;
            if(player.type==='assault') {{
                for(let i=0; i<12; i++) setTimeout(() => fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x)+(Math.random()-0.5)*0.4, true, true), i*70);
            }} else if(player.type==='tank') {{
                player.shield = true; setTimeout(()=>player.shield=false, 6000);
            }} else if(player.type==='scout') {{
                let a = Math.atan2(my-player.y, mx-player.x);
                let tx = player.x + Math.cos(a)*160, ty = player.y + Math.sin(a)*160;
                if(!isInsideWall(tx, ty, player.r)) {{ player.x = tx; player.y = ty; }}
            }}
        }}

        let s = (player.buffs.speed > 0) ? player.speed * 1.8 : player.speed;
        let nx = player.x, ny = player.y;
        if(keys['KeyW']) ny -= s; if(keys['KeyS']) ny += s;
        if(keys['KeyA']) nx -= s; if(keys['KeyD']) nx += s;
        if(!isInsideWall(nx, player.y, player.r)) player.x = nx;
        if(!isInsideWall(player.x, ny, player.r)) player.y = ny;

        // Player Projectiles
        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(isInsideWall(b.x, b.y, b.r)) return false;
            for(let e of enemies) {{
                if(Math.hypot(e.x - b.x, e.y - b.y) < e.s/2 + b.r) {{ e.hp -= b.rocket?player.dmg*4:player.dmg; return false; }}
            }}
            if(boss) {{
                if(b.x > boss.x && b.x < boss.x+boss.w && b.y > boss.y && b.y < boss.y+boss.h) {{
                    if(!boss.sh) boss.hp -= b.rocket?player.dmg*4:player.dmg; return false;
                }}
            }}
            return b.x > 0 && b.x < 600 && b.y > 0 && b.y < 400;
        }});

        // Enemy Projectiles
        eBullets = eBullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(isInsideWall(b.x, b.y, b.r)) return false;
            if(Math.hypot(player.x - b.x, player.y - b.y) < player.r + b.r) {{
                if(player.inv <= 0 && !player.shield) {{ health--; player.inv = 60; }}
                return false;
            }}
            return true;
        }});

        // Enemy Logic
        enemies.forEach((e, i) => {{
            let a = Math.atan2(player.y - e.y, player.x - e.x);
            let vx = Math.cos(a)*e.sp, vy = Math.sin(a)*e.sp;
            if(!isInsideWall(e.x + vx, e.y + vy, e.s/2)) {{ e.x += vx; e.y += vy; }}
            else {{ // Sliding Anti-Stuck
                if(!isInsideWall(e.x+vy, e.y-vx, e.s/2)) {{ e.x+=vy; e.y-=vx; }}
                else if(!isInsideWall(e.x-vy, e.y+vx, e.s/2)) {{ e.x-=vy; e.y+=vx; }}
            }}
            if(Math.hypot(player.x - e.x, player.y - e.y) < player.r + e.s/2) {{
                if(player.inv <= 0 && !player.shield) {{ health--; player.inv = 60; }}
            }}
            if(e.hp <= 0) {{ score += e.v; enemies.splice(i, 1); }}
        }});

        // Boss AI
        if(boss) {{
            let a = Math.atan2(player.y - (boss.y+boss.h/2), player.x - (boss.x+boss.w/2));
            boss.x += Math.cos(a)*1.3; boss.y += Math.sin(a)*1.3;
            boss.fT++;
            if(boss.fT > 100) {{ fire(boss.x+boss.w/2, boss.y+boss.h/2, a, false, false); boss.fT = 0; }}
            boss.sh = boss.hp < boss.mH * 0.5; // Shield active if HP < 50%
            if(boss.hp <= 0) {{ score += 1000; boss = null; uMenu.style.display = 'block'; }}
        }}

        // Items Spawn & Logic
        items = items.filter(it => {{
            if(Math.hypot(player.x - it.x, player.y - it.y) < player.r + 15) {{
                if(it.t === 'speed') player.buffs.speed = 450;
                else player.buffs.triple = 450;
                return false;
            }}
            return true;
        }});

        if(player.inv > 0) player.inv--;
        if(health <= 0) gameOver = true;

        if(enemies.length < 3 + level && !boss) {{
            let ex = Math.random()*560+20, ey = Math.random()*360+20;
            if(!isInsideWall(ex, ey, 20) && Math.hypot(player.x-ex, player.y-ey) > 150) {{
                let r = Math.random();
                let t = r < 0.6 ? {{c:'#e74c3c', s:22, sp:1.6, h:5, v:10}} : 
                        r < 0.85 ? {{c:'#2ecc71', s:32, sp:0.9, h:16, v:20}} : {{c:'#9b59b6', s:18, sp:2.6, h:3, v:25}};
                enemies.push({{x:ex, y:ey, color:t.c, s:t.s, sp:t.sp, hp:t.h, v:t.v}});
            }}
        }}

        if(score >= level*500 && !boss) {{
            boss = {{x: 250, y: -100, w: 90, h: 90, hp: 400+(level*300), mH: 400+(level*300), fT: 0, sh: false}};
        }}
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        walls.forEach(w => {{ ctx.fillStyle='#333'; ctx.fillRect(w.x, w.y, w.w, w.h); ctx.strokeStyle='#555'; ctx.strokeRect(w.x,w.y,w.w,w.h); }});
        items.forEach(it => {{ ctx.fillStyle=it.t==='speed'?'#f1c40f':'#3498db'; ctx.beginPath(); ctx.arc(it.x, it.y, 10, 0, 7); ctx.fill(); ctx.strokeStyle='white'; ctx.stroke(); }});
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, 7); ctx.fill(); }});
        eBullets.forEach(b => {{ ctx.fillStyle='#ff0000'; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, 7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.color; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        
        if(boss) {{
            ctx.fillStyle = '#ff4d4d'; ctx.fillRect(boss.x, boss.y, boss.w, boss.h);
            ctx.fillStyle = '#f00'; ctx.fillRect(boss.x, boss.y-15, (boss.hp/boss.mH)*boss.w, 10);
            if(boss.sh) {{ ctx.strokeStyle='#00e5ff'; ctx.lineWidth=4; ctx.strokeRect(boss.x-5, boss.y-5, boss.w+10, boss.h+10); }}
        }}

        if(player.inv % 10 < 5) {{
            ctx.fillStyle = player.color; ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, 7); ctx.fill();
            if(player.shield) {{ ctx.strokeStyle = '#00e5ff'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(player.x, player.y, player.r+7, 0, 7); ctx.stroke(); }}
        }}

        if(gameOver) {{ ctx.fillStyle = 'white'; ctx.font = 'bold 45px Arial'; ctx.textAlign = 'center'; ctx.fillText("GAME OVER", 300, 200); }}
    }}

    function loop() {{
        update(); draw();
        if(!gameOver && uMenu.style.display !== 'block') requestAnimationFrame(loop);
    }}

    initWalls();
    setInterval(() => {{
        if(items.length < 2) {{
            let ix = 50+Math.random()*500, iy = 50+Math.random()*300;
            if(!isInsideWall(ix, iy, 15)) items.push({{x: ix, y: iy, t: Math.random()>0.5?'speed':'triple'}});
        }}
    }}, 4000);
    loop();
}})();
</script>
"""

cp.html(game_html, height=600)
