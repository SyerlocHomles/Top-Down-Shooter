import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Ultra Stable", layout="centered")
st.title("🛡️ Island.io: Fix Stuck & Ghost Bullets")

# Inisialisasi Karakter
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
    st.info("Pilih Class untuk bermain!")
    st.stop()

# Kode Game - Menggunakan raw string dan pengamanan kurung kurawal
game_html = f"""
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif;">
    <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
        <div id="ui-lvl">LEVEL: 1</div>
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">❤️</div>
    </div>
    
    <div id="ui-skill-container" style="width: 200px; margin: 0 auto 10px;">
        <div id="ui-skill-text" style="color:#00e5ff; font-size: 10px;">ULTIMATE CHARGING</div>
        <div style="width:100%; height:6px; background:#333; border-radius:3px; overflow:hidden;">
            <div id="skill-bar" style="width:0%; height:100%; background:#00e5ff; transition: width 0.1s;"></div>
        </div>
    </div>

    <div id="buff-ui" style="color:#f1c40f; font-size:12px; font-weight:bold; min-height:15px; margin-bottom:5px;"></div>

    <div id="upgrade-menu" style="display:none; position:absolute; width:100%; height:100%; top:0; left:0; background:rgba(0,0,0,0.9); z-index:1000; border-radius:11px;">
        <h2 style="color:white; margin-top:100px;">LEVEL UP!</h2>
        <button onclick="applyUp('hp')" style="padding:10px; background:#2ecc71; color:white; border:none; margin:5px; border-radius:5px; cursor:pointer;">+1 Darah</button>
        <button onclick="applyUp('atk')" style="padding:10px; background:#e74c3c; color:white; border:none; margin:5px; border-radius:5px; cursor:pointer;">+3 Damage</button>
    </div>

    <canvas id="g" width="600" height="400" style="background:#000; border: 2px solid #333; cursor: crosshair;"></canvas>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uLvl = document.getElementById('ui-lvl'), uBar = document.getElementById('skill-bar'),
          uBuff = document.getElementById('buff-ui'), uMenu = document.getElementById('upgrade-menu');

    let score = 0, health = {st.session_state.char['hp']}, level = 1, gameOver = false;
    let keys = {{}}, bullets = [], enemies = [], walls = [], items = [], boss = null;
    
    let player = {{
        x: 300, y: 200, radius: 12, speed: {st.session_state.char['spd']},
        type: '{st.session_state.char['type']}', color: '{st.session_state.char['col']}',
        skillTimer: 0, skillMax: 500, shield: false,
        buffs: {{ speed: 0, triple: 0 }},
        dmg: 5, inv: 0
    }};

    window.applyUp = (type) => {{
        if(type==='hp') health++;
        if(type==='atk') player.dmg += 3;
        uMenu.style.display = 'none';
        level++;
        initWalls();
        requestAnimationFrame(loop);
    }};

    function initWalls() {{
        walls = [];
        for(let i=0; i<4; i++) {{
            let w = 40+Math.random()*60, h = 40+Math.random()*60;
            let x = 50+Math.random()*450, y = 50+Math.random()*250;
            // Jangan taruh tembok di tempat player spawn
            if(Math.abs(x-300) > 80 && Math.abs(y-200) > 80) walls.push({{x,y,w,h}});
        }}
    }}

    function collide(x, y, r, target) {{
        return x + r > target.x && x - r < target.x + target.w &&
               y + r > target.y && y - r < target.y + target.h;
    }}

    function isBlocked(x, y, r) {{
        for(let w of walls) if(collide(x, y, r, w)) return true;
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
        fireBullet(player.x, player.y, Math.atan2(my - player.y, mx - player.x), false);
        if(player.buffs.triple > 0) {{
            fireBullet(player.x, player.y, Math.atan2(my - player.y, mx - player.x) + 0.2, false);
            fireBullet(player.x, player.y, Math.atan2(my - player.y, mx - player.x) - 0.2, false);
        }}
    }};

    function fireBullet(x, y, angle, isRocket) {{
        bullets.push({{
            x, y, vx: Math.cos(angle)*(isRocket?15:10), vy: Math.sin(angle)*(isRocket?15:10),
            r: isRocket?8:4, color: isRocket?'#ff4500':'#f1c40f', rocket: isRocket
        }});
    }}

    function update() {{
        if(gameOver || uMenu.style.display === 'block') return;

        // Buff Timers
        if(player.buffs.speed > 0) player.buffs.speed--;
        if(player.buffs.triple > 0) player.buffs.triple--;
        
        // Skill Charging
        if(player.skillTimer < player.skillMax) player.skillTimer++;
        uBar.style.width = (player.skillTimer/player.skillMax*100) + '%';
        if(keys['Space'] && player.skillTimer >= player.skillMax) {{
            player.skillTimer = 0;
            if(player.type==='assault') {{
                for(let i=0; i<10; i++) setTimeout(() => fireBullet(player.x, player.y, Math.atan2(my-player.y, mx-player.x)+(Math.random()-0.5)*0.3, true), i*80);
            }} else if(player.type==='tank') {{
                player.shield = true; setTimeout(()=>player.shield=false, 5000);
            }} else if(player.type==='scout') {{
                let a = Math.atan2(my-player.y, mx-player.x);
                let jumpX = player.x + Math.cos(a)*150, jumpY = player.y + Math.sin(a)*150;
                if(!isBlocked(jumpX, jumpY, player.radius)) {{ player.x = jumpX; player.y = jumpY; }}
            }}
        }}

        // Movement
        let s = (player.buffs.speed > 0) ? player.speed * 1.7 : player.speed;
        let nx = player.x, ny = player.y;
        if(keys['KeyW']) ny -= s; if(keys['KeyS']) ny += s;
        if(keys['KeyA']) nx -= s; if(keys['KeyD']) nx += s;
        if(!isBlocked(nx, player.y, player.radius)) player.x = nx;
        if(!isBlocked(player.x, ny, player.radius)) player.y = ny;

        // Bullets
        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(isBlocked(b.x, b.y, b.r)) return false;
            
            for(let e of enemies) {{
                let dist = Math.hypot(e.x - b.x, e.y - b.y);
                if(dist < e.size/2 + b.r) {{
                    e.hp -= b.rocket ? player.dmg*3 : player.dmg;
                    return false;
                }}
            }}
            
            if(boss) {{
                if(b.x > boss.x && b.x < boss.x+boss.w && b.y > boss.y && b.y < boss.y+boss.h) {{
                    boss.hp -= b.rocket ? player.dmg*3 : player.dmg;
                    return false;
                }}
            }}
            return b.x > 0 && b.x < 600 && b.y > 0 && b.y < 400;
        }});

        // Enemies & Boss
        enemies.forEach((e, i) => {{
            let angle = Math.atan2(player.y - e.y, player.x - e.x);
            let vx = Math.cos(angle)*e.speed, vy = Math.sin(angle)*e.speed;
            
            if(!isBlocked(e.x + vx, e.y + vy, e.size/2)) {{
                e.x += vx; e.y += vy;
            }} else {{
                // Anti-Stuck Slide
                if(!isBlocked(e.x + vy, e.y - vx, e.size/2)) {{ e.x += vy; e.y -= vx; }}
                else if(!isBlocked(e.x - vy, e.y + vx, e.size/2)) {{ e.x -= vy; e.y += vx; }}
            }}

            if(Math.hypot(player.x - e.x, player.y - e.y) < player.radius + e.size/2) {{
                if(player.inv <= 0 && !player.shield) {{ health--; player.inv = 60; }}
            }}
            if(e.hp <= 0) {{ score += e.val; enemies.splice(i, 1); }}
        }});

        if(boss) {{
            let angle = Math.atan2(player.y - (boss.y+boss.h/2), player.x - (boss.x+boss.w/2));
            boss.x += Math.cos(angle)*1.2; boss.y += Math.sin(angle)*1.2;
            if(player.x > boss.x && player.x < boss.x+boss.w && player.y > boss.y && player.y < boss.y+boss.h) {{
                if(player.inv <= 0 && !player.shield) {{ health--; player.inv = 60; }}
            }}
            if(boss.hp <= 0) {{ score += 500; boss = null; uMenu.style.display = 'block'; }}
        }}

        // Items
        items = items.filter(it => {{
            if(Math.hypot(player.x - it.x, player.y - it.y) < player.radius + 15) {{
                if(it.type === 'speed') player.buffs.speed = 400;
                else player.buffs.triple = 400;
                return false;
            }}
            return true;
        }});

        if(player.inv > 0) player.inv--;
        if(health <= 0) gameOver = true;

        // Spawn
        if(enemies.length < 2 + level) {{
            let ex = Math.random()*600, ey = Math.random()*400;
            if(Math.hypot(player.x-ex, player.y-ey) > 150 && !isBlocked(ex, ey, 15)) {{
                let r = Math.random();
                let type = r < 0.6 ? {{c:'#e74c3c', s:20, sp:1.5, h:5, v:10}} : 
                           r < 0.85 ? {{c:'#2ecc71', s:30, sp:0.8, h:15, v:20}} : 
                                      {{c:'#9b59b6', s:18, sp:2.5, h:3, v:25}};
                enemies.push({{x:ex, y:ey, color:type.c, size:type.s, speed:type.sp, hp:type.h, val:type.v}});
            }}
        }}

        if(score >= level*400 && !boss) {{
            boss = {{x: 100, y: -100, w: 80, h: 80, hp: 300+(level*200), maxHp: 300+(level*200)}};
        }}

        // UI Updates
        uScore.innerText = "Skor: " + score;
        uHP.innerText = "❤️".repeat(health);
        uLvl.innerText = "LEVEL: " + level;
        let bText = [];
        if(player.buffs.speed > 0) bText.push("⚡ SPEED (" + Math.ceil(player.buffs.speed/60) + "s)");
        if(player.buffs.triple > 0) bText.push("🔫 TRIPLE (" + Math.ceil(player.buffs.triple/60) + "s)");
        uBuff.innerText = bText.join(" | ");
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        
        walls.forEach(w => {{ ctx.fillStyle='#444'; ctx.fillRect(w.x, w.y, w.w, w.h); }});
        items.forEach(it => {{ ctx.fillStyle=it.type==='speed'?'#f1c40f':'#3498db'; ctx.beginPath(); ctx.arc(it.x, it.y, 10, 0, 7); ctx.fill(); }});
        bullets.forEach(b => {{ ctx.fillStyle=b.color; ctx.beginPath(); ctx.arc(b.x, b.y, b.r, 0, 7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.color; ctx.fillRect(e.x-e.size/2, e.y-e.size/2, e.size, e.size); }});
        
        if(boss) {{
            ctx.fillStyle = '#e74c3c'; ctx.fillRect(boss.x, boss.y, boss.w, boss.h);
            ctx.fillStyle = '#f00'; ctx.fillRect(boss.x, boss.y-15, (boss.hp/boss.maxHp)*boss.w, 8);
        }}

        if(player.inv % 10 < 5) {{
            ctx.fillStyle = player.color; ctx.beginPath(); ctx.arc(player.x, player.y, player.radius, 0, 7); ctx.fill();
            if(player.shield) {{
                ctx.strokeStyle = '#00e5ff'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(player.x, player.y, player.radius+5, 0, 7); ctx.stroke();
            }}
        }}

        if(gameOver) {{
            ctx.fillStyle = 'white'; ctx.font = '40px Arial'; ctx.textAlign = 'center';
            ctx.fillText("GAME OVER", 300, 200);
        }}
    }}

    function loop() {{
        update();
        draw();
        if(!gameOver && uMenu.style.display !== 'block') requestAnimationFrame(loop);
    }}

    initWalls();
    setInterval(() => {{
        if(items.length < 2) items.push({{x: 50+Math.random()*500, y: 50+Math.random()*300, type: Math.random()>0.5?'speed':'triple'}});
    }}, 5000);
    loop();
}})();
</script>
"""

cp.html(game_html, height=600)
