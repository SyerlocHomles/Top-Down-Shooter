import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Boss Evolution", layout="centered")
st.title("🛡️ Island.io: White Bullets & Boss Heal")

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
        <div id="ui-hp">❤️❤️❤️</div>
    </div>
    
    <div style="margin: 0 auto 10px; width: 250px;">
        <div id="ui-skill-text" style="color:#00e5ff; font-size: 11px; font-weight:bold;">ULTIMATE READY</div>
        <div style="width:100%; height:8px; background:#333; border-radius:4px; overflow:hidden; border: 1px solid #555;">
            <div id="skill-bar" style="width:0%; height:100%; background:#00e5ff;"></div>
        </div>
    </div>
    <div id="buff-ui" style="color:#f1c40f; font-size:12px; font-weight:bold; height:15px; margin-bottom:5px;"></div>

    <div id="upgrade-menu" style="display:none; position:absolute; width:100%; height:100%; top:0; left:0; background:rgba(0,0,0,0.9); z-index:1000; border-radius:11px;">
        <h2 style="color:white; margin-top:120px;">⬆️ LEVEL UP!</h2>
        <button onclick="applyUp('hp')" style="padding:12px; background:#2ecc71; color:white; border:none; margin:10px; border-radius:5px; cursor:pointer; font-weight:bold;">+1 NYAWA</button>
        <button onclick="applyUp('atk')" style="padding:12px; background:#e74c3c; color:white; border:none; margin:10px; border-radius:5px; cursor:pointer; font-weight:bold;">+3 DAMAGE</button>
    </div>

    <canvas id="g" width="600" height="400" style="background:#080808; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
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
        if(type==='atk') player.dmg += 3;
        uMenu.style.display = 'none';
        level++; initWalls(); requestAnimationFrame(loop);
    }};

    function initWalls() {{
        walls = [];
        for(let i=0; i<4; i++) {{
            let w = 50+Math.random()*60, h = 50+Math.random()*60;
            let x = 60+Math.random()*440, y = 60+Math.random()*240;
            if(Math.hypot(x+w/2-300, y+h/2-200) > 120) walls.push({{x,y,w,h}});
        }}
    }}

    function isInsideWall(x, y, r) {{
        for(let w of walls) {{
            if(x + r > w.x - 2 && x - r < w.x + w.w + 2 && y + r > w.y - 2 && y - r < w.y + w.h + 2) return true;
        }}
        return x < r || x > 600-r || y < r || y > 400-r;
    }}

    window.onkeydown = e => {{ keys[e.code] = true; }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    
    let mx = 0, my = 0;
    canvas.onmousemove = e => {{
        const r = canvas.getBoundingClientRect();
        mx = e.clientX - r.left; my = e.clientY - r.top;
    }};

    canvas.onmousedown = () => {{
        if(gameOver || uMenu.style.display === 'block') return;
        const angle = Math.atan2(my - player.y, mx - player.x);
        fire(player.x, player.y, angle, false, true);
        if(player.buffs.triple > 0) {{
            fire(player.x, player.y, angle + 0.25, false, true);
            fire(player.x, player.y, angle - 0.25, false, true);
        }}
    }};

    function fire(x, y, a, isRocket, isPlayer) {{
        const b = {{ 
            x: x, y: y, 
            vx: Math.cos(a)*(isRocket?14:11), 
            vy: Math.sin(a)*(isRocket?14:11), 
            r: isRocket?8:4, 
            c: isPlayer?'#FFFFFF':'#FF0000', // PELURU PLAYER PUTIH
            rocket: isRocket 
        }};
        if(isPlayer) bullets.push(b); else eBullets.push(b);
    }}

    function update() {{
        if(gameOver || uMenu.style.display === 'block') return;

        if(player.buffs.speed > 0) player.buffs.speed--;
        if(player.buffs.triple > 0) player.buffs.triple--;
        if(player.sT < player.sM) player.sT++;
        uBar.style.width = (player.sT/player.sM*100) + '%';

        // Movement
        let s = (player.buffs.speed > 0) ? player.speed * 1.8 : player.speed;
        let nx = player.x, ny = player.y;
        if(keys['KeyW']) ny -= s; if(keys['KeyS']) ny += s;
        if(keys['KeyA']) nx -= s; if(keys['KeyD']) nx += s;
        if(!isInsideWall(nx, player.y, player.r)) player.x = nx;
        if(!isInsideWall(player.x, ny, player.r)) player.y = ny;

        // Projectiles
        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(isInsideWall(b.x, b.y, b.r)) return false;
            for(let e of enemies) {{
                if(Math.hypot(e.x - b.x, e.y - b.y) < e.s/2 + b.r) {{ e.hp -= b.rocket?player.dmg*4:player.dmg; return false; }}
            }}
            if(boss && b.x > boss.x && b.x < boss.x+boss.w && b.y > boss.y && b.y < boss.y+boss.h) {{
                if(!boss.sh) boss.hp -= b.rocket?player.dmg*4:player.dmg; return false;
            }}
            return b.x > 0 && b.x < 600 && b.y > 0 && b.y < 400;
        }});

        eBullets = eBullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(isInsideWall(b.x, b.y, b.r)) return false;
            if(Math.hypot(player.x - b.x, player.y - b.y) < player.r + b.r) {{
                if(player.inv <= 0 && !player.shield) {{ health--; player.inv = 60; }}
                return false;
            }}
            return true;
        }});

        // Kroco AI
        enemies.forEach((e, i) => {{
            let a = Math.atan2(player.y - e.y, player.x - e.x);
            let vx = Math.cos(a)*e.sp, vy = Math.sin(a)*e.sp;
            if(!isInsideWall(e.x + vx, e.y + vy, e.s/2)) {{
                e.x += vx; e.y += vy;
            }} else {{
                if(!isInsideWall(e.x + vy*1.5, e.y - vx*1.5, e.s/2)) {{ e.x += vy; e.y -= vx; }}
                else if(!isInsideWall(e.x - vy*1.5, e.y + vx*1.5, e.s/2)) {{ e.x -= vy; e.y += vx; }}
            }}
            if(e.hp <= 0) {{ score += e.v; enemies.splice(i, 1); }}
        }});

        // Boss AI with HEAL
        if(boss) {{
            let a = Math.atan2(player.y - (boss.y+boss.h/2), player.x - (boss.x+boss.w/2));
            let bvx = Math.cos(a)*1.4, bvy = Math.sin(a)*1.4;
            if(!isInsideWall(boss.x + bvx + boss.w/2, boss.y + bvy + boss.h/2, boss.w/2)) {{
                boss.x += bvx; boss.y += bvy;
            }}

            boss.fT++;
            if(boss.fT > 120) {{ fire(boss.x+boss.w/2, boss.y+boss.h/2, a, false, false); boss.fT = 0; }}
            
            boss.uT++;
            if(boss.uT > 300) {{
                for(let i=0; i<12; i++) fire(boss.x+boss.w/2, boss.y+boss.h/2, (i/12)*Math.PI*2, false, false);
                boss.uT = 0;
            }}

            // DEFENSE SKILL: HEAL & SHIELD
            if(boss.hp < boss.mH * 0.4) {{
                boss.sh = true;
                if(boss.hp < boss.mH) boss.hp += 0.25; // Healing perlahan
            }} else {{
                boss.sh = false;
            }}

            if(boss.hp <= 0) {{ score += 1000; boss = null; uMenu.style.display = 'block'; }}
        }}

        // Items logic
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

        if(enemies.length < (boss ? 2 : 4) + level) {{
            let ex = Math.random()*540+30, ey = Math.random()*340+30;
            if(!isInsideWall(ex, ey, 20) && Math.hypot(player.x-ex, player.y-ey) > 150) {{
                let r = Math.random();
                let t = r < 0.6 ? {{c:'#e74c3c', s:20, sp:1.6, h:5, v:10}} : 
                        r < 0.85 ? {{c:'#2ecc71', s:30, sp:0.8, h:15, v:20}} : {{c:'#9b59b6', s:18, sp:2.8, h:3, v:25}};
                enemies.push({{x:ex, y:ey, color:t.c, s:t.s, sp:t.sp, hp:t.h, v:t.v}});
            }}
        }}

        if(score >= level*500 && !boss) {{
            boss = {{x: 250, y: -90, w: 85, h: 85, hp: 500+(level*300), mH: 500+(level*300), fT: 0, uT: 0, sh: false}};
        }}

        uScore.innerText = "Skor: " + score;
        uHP.innerText = "❤️".repeat(health);
        uLvl.innerText = "LEVEL: " + level;
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        walls.forEach(w => {{ ctx.fillStyle='#444'; ctx.fillRect(w.x, w.y, w.w, w.h); }});
        
        items.forEach(it => {{ 
            ctx.fillStyle = (it.t === 'speed' ? '#3498db' : '#f1c40f'); // Biru=Speed, Kuning=Triple
            ctx.beginPath(); ctx.arc(it.x, it.y, 10, 0, 7); ctx.fill(); 
            ctx.strokeStyle='white'; ctx.stroke();
        }});

        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, 7); ctx.fill(); }});
        eBullets.forEach(b => {{ ctx.fillStyle='#ff0000'; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, 7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.color; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        
        if(boss) {{
            ctx.fillStyle = boss.sh ? '#00e5ff' : '#ff4d4d'; // Berubah warna saat perisai aktif
            ctx.fillRect(boss.x, boss.y, boss.w, boss.h);
            ctx.fillStyle = '#f00'; ctx.fillRect(boss.x, boss.y-15, (boss.hp/boss.mH)*boss.w, 10);
            if(boss.sh) {{ 
                ctx.strokeStyle = '#FFFFFF'; ctx.lineWidth = 3; ctx.strokeRect(boss.x-5, boss.y-5, boss.w+10, boss.h+10); 
                ctx.fillStyle = '#00e5ff'; ctx.font = 'bold 10px Arial'; ctx.fillText("HEALING...", boss.x, boss.y-20);
            }}
        }}

        if(player.inv % 10 < 5) {{
            ctx.fillStyle = player.color; ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, 7); ctx.fill();
            if(player.shield) {{ ctx.strokeStyle='#00e5ff'; ctx.lineWidth=4; ctx.beginPath(); ctx.arc(player.x, player.y, player.r+6, 0, 7); ctx.stroke(); }}
        }}
        if(gameOver) {{ ctx.fillStyle='white'; ctx.font='bold 40px Arial'; ctx.textAlign='center'; ctx.fillText("GAME OVER", 300, 200); }}
    }}

    function loop() {{
        update(); draw();
        if(!gameOver && uMenu.style.display !== 'block') requestAnimationFrame(loop);
    }}

    initWalls();
    setInterval(() => {{
        if(items.length < 2) {{
            let ix = 60+Math.random()*480, iy = 60+Math.random()*280;
            if(!isInsideWall(ix, iy, 15)) items.push({{x: ix, y: iy, t: Math.random()>0.5?'speed':'triple'}});
        }}
    }}, 4000);
    loop();
}})();
</script>
"""

cp.html(game_html, height=600)
