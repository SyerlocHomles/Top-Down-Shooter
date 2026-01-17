import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Roket Launcher", layout="centered")
st.title("⚔️ Island.io: Roket Autolock Launcher")

if "char" not in st.session_state:
    st.session_state.char = None

def reset_game():
    st.session_state.char = None
    st.rerun()

if st.session_state.char:
    if st.sidebar.button("Kembali Pilih Hero"):
        reset_game()

# --- MENU PILIH KARAKTER (ASLI) ---
if not st.session_state.char:
    st.write("### Pilih Hero Anda:")
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)
    classes_data = [
        {"n": "🔴 Assault", "col": "#ff0000", "hp": 3, "spd": 6.5, "t": "assault", "slot": c1, "stat": "**HP:** ❤️❤️❤️\n\n**SPD:** ⚡⚡\n\n**SKILL:** Rapid Fire"},
        {"n": "🔵 Tank", "col": "#0000ff", "hp": 6, "spd": 4.5, "t": "tank", "slot": c2, "stat": "**HP:** ❤️❤️❤️❤️❤️❤️\n\n**SPD:** ⚡\n\n**SKILL:** Iron Shield"},
        {"n": "🟢 Scout", "col": "#00ff00", "hp": 2, "spd": 8.5, "t": "scout", "slot": c3, "stat": "**HP:** ❤️❤️\n\n**SPD:** ⚡⚡⚡\n\n**SKILL:** Teleport Dash"},
        {"n": "🟣 Joker", "col": "#800080", "hp": 4, "spd": 6.5, "t": "joker", "slot": c4, "stat": "**HP:** ❤️❤️❤️❤️\n\n**SPD:** ⚡⚡\n\n**SKILL:** Random Gamble"},
        {"n": "🟡 Bomber", "col": "#ffff00", "hp": 3, "spd": 6.0, "t": "bomber", "slot": c5, "stat": "**HP:** ❤️❤️❤️\n\n**SPD:** ⚡⚡\n\n**SKILL:** Nuke Blast"},
        {"n": "🟠 Roket", "col": "#ffa500", "hp": 3, "spd": 6.5, "t": "roket", "slot": c6, "stat": "**HP:** ❤️❤️❤️\n\n**SPD:** ⚡⚡\n\n**SKILL:** Homing Missile"}
    ]
    for cls in classes_data:
        with cls["slot"]:
            st.markdown(f"<div style='text-align: center; color: {cls['col']}; font-weight: bold;'>{cls['n']}</div>", unsafe_allow_html=True)
            if st.button("Pilih " + cls['n'].split()[1], key=cls['t']):
                st.session_state.char = {"hp": cls["hp"], "spd": cls["spd"], "col": cls["col"], "type": cls["t"]}
                st.rerun()
            st.caption(cls["stat"])
            st.write("---")
    st.stop()

p = st.session_state.char
game_html = f"""
<div style="display: flex; justify-content: center; align-items: flex-start;">
    <div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; user-select: none;">
        
        <div id="upgrade-overlay" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:1000; border-radius:11px; flex-direction:column; justify-content:center; align-items:center;">
            <h2 style="color:#ffd700; margin-bottom:20px;">LEVEL UP!</h2>
            <button onclick="applyUp('speed')" style="width:220px; padding:15px; margin:10px; background:#4deaff; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">⚡ SPEED +0.5</button>
            <button onclick="applyUp('flank')" style="width:220px; padding:15px; margin:10px; background:#ff4d4d; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">🛡️ FLANK GUARD</button>
            <button onclick="applyUp('pet')" style="width:220px; padding:15px; margin:10px; background:#ffff4d; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">🤖 DRONE PET</button>
        </div>

        <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
            <div id="ui-lvl">LEVEL: 1</div>
            <div id="ui-score">Skor: 0</div>
            <div id="ui-hp">❤️❤️❤️</div>
        </div>
        <div style="margin: 0 auto 10px; width: 250px;">
            <div id="ui-skill-text" style="color:{p['col']}; font-size: 11px; font-weight:bold; text-transform: uppercase;">{p['type']} ULTIMATE</div>
            <div style="width:100%; height:12px; background:#333; border-radius:6px; overflow:hidden; border: 1px solid #555;">
                <div id="skill-bar" style="width:0%; height:100%; background: {p['col']};"></div>
            </div>
        </div>
        <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
        <div id="restart-btn" style="display:none; position:absolute; top:65%; left:50%; transform:translate(-50%, -50%);">
            <button onclick="parent.window.location.reload()" style="padding:15px 30px; font-size:18px; font-weight:bold; color:white; background:#e74c3c; border:none; border-radius:10px; cursor:pointer;">KEMBALI KE MENU</button>
        </div>
    </div>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uBar = document.getElementById('skill-bar'), uLvl = document.getElementById('ui-lvl');
    const rBtn = document.getElementById('restart-btn'), upLayer = document.getElementById('upgrade-overlay');

    let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
    let keys = {{}}, bullets = [], enemies = [], particles = [], boss = null;
    let lastUpgradeScore = 0, lastBossThreshold = 0, currentLvl = 1;

    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, shield: false, inv: 0, kills: 0,
        hasFlank: false, hasPet: false, petAngle: 0
    }};

    window.applyUp = function(type) {{
        if(type === 'speed') player.baseSpeed += 0.5;
        if(type === 'flank') player.hasFlank = true;
        if(type === 'pet') player.hasPet = true;
        upLayer.style.display = "none";
        isPaused = false;
        requestAnimationFrame(loop);
    }};

    function spawnExplosion(x, y, color, count=15) {{
        for(let i=0; i<count; i++) particles.push({{ x, y, vx:(Math.random()-0.5)*15, vy:(Math.random()-0.5)*15, life:Math.random()*30+10, c:color }});
    }}

    function triggerRespawn() {{
        health--; spawnExplosion(player.x, player.y, "#ffffff"); player.inv = 120;
        if(health <= 0) {{ gameOver = true; rBtn.style.display = "block"; }}
    }}

    window.onkeydown = e => {{ keys[e.code] = true; if(e.code==='Space') useUlt(); }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    let mx=0, my=0;
    canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

    function fire(x, y, a, isPlayer, damageValue, isRoket=false) {{
        bullets.push({{ x, y, vx:Math.cos(a)*15, vy:Math.sin(a)*15, r:isRoket?10:4, c:isPlayer?player.color:'#F00', p:isPlayer, rk:isRoket, d:damageValue, target:null }});
    }}

    function useUlt() {{
        if(player.sT < player.sM || isPaused || gameOver) return;
        player.sT = 0; player.kills = 0;
        if(player.type === 'roket') {{
            for(let i=0; i<6; i++) fire(player.x, player.y, (Math.PI*2/6)*i, true, 150, true);
        }} else if(player.type === 'bomber') {{
            spawnExplosion(player.x, player.y, "#ffff00", 100);
            enemies.forEach(e => {{ if(Math.hypot(e.x-player.x, e.y-player.y) < 300) e.hp -= 500; }});
            if(boss && Math.hypot(boss.x-player.x, boss.y-player.y) < 300) boss.hp -= 800;
        }} else if(player.type === 'assault') {{
            for(let i=0; i<10; i++) setTimeout(()=>fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), true, 40), i*100);
        }} // Logika ulti lain disederhanakan agar tidak error
    }}

    canvas.onmousedown = () => {{ 
        if(isPaused || gameOver) return;
        let a = Math.atan2(my-player.y, mx-player.x);
        fire(player.x, player.y, a, true, 5);
        if(player.hasFlank) fire(player.x, player.y, a+Math.PI, true, 5);
    }};

    function update() {{
        if(gameOver || isPaused) return;

        // SISTEM UPGRADE
        if(score >= lastUpgradeScore + 1000) {{
            isPaused = true; lastUpgradeScore += 1000; currentLvl++;
            upLayer.style.display = "flex"; return;
        }}

        // Gerak Player
        let s = player.baseSpeed;
        if(keys['KeyW']) player.y -= s; if(keys['KeyS']) player.y += s;
        if(keys['KeyA']) player.x -= s; if(keys['KeyD']) player.x += s;

        // Skill Bar
        player.sT = Math.min(100, player.sT + 0.2);
        uBar.style.width = player.sT + "%";

        // PET Logic
        if(player.hasPet) {{
            player.petAngle += 0.05;
            if(Math.random()<0.05) fire(player.x+Math.cos(player.petAngle)*35, player.y+Math.sin(player.petAngle)*35, player.petAngle, true, 5);
        }}

        // BULLET Logic (Tabrakan)
        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(b.rk) {{ // Homing
                let t = boss || enemies[0];
                if(t) {{ let a = Math.atan2(t.y-b.y, t.x-b.x); b.vx += Math.cos(a)*1; b.vy += Math.sin(a)*1; }}
            }}
            if(b.p) {{ // Peluru Pemain hit Musuh
                if(boss && Math.hypot(b.x-boss.x, b.y-boss.y) < boss.s) {{ boss.hp -= b.d; return false; }}
                for(let i=enemies.length-1; i>=0; i--) {{
                    let e = enemies[i];
                    if(Math.hypot(b.x-e.x, b.y-e.y) < e.s) {{ 
                        e.hp -= b.d; if(e.hp<=0) {{ score+=e.val; spawnExplosion(e.x, e.y, e.c); enemies.splice(i,1); }}
                        return false; 
                    }}
                }}
            }} else {{ // Peluru Musuh hit Pemain
                if(Math.hypot(b.x-player.x, b.y-player.y) < player.r && player.inv<=0) {{ triggerRespawn(); return false; }}
            }}
            return b.x>0 && b.x<600 && b.y>0 && b.y<400;
        }});

        // MUSUH SPAWN (ASLI)
        if(!boss && enemies.length < 8) {{
            let r = Math.random();
            let type = r < 0.2 ? {{c:'#2ecc71', hp:15, val:15, sp:0.6, s:30}} : (r < 0.5 ? {{c:'#9b59b6', hp:5, val:10, sp:1.8, s:15}} : {{c:'#e74c3c', hp:5, val:5, sp:1.2, s:22}});
            enemies.push({{ x:Math.random()*600, y:Math.random()*400, ...type }});
        }}

        enemies.forEach(e => {{
            let a = Math.atan2(player.y-e.y, player.x-e.x);
            e.x += Math.cos(a)*e.sp; e.y += Math.sin(a)*e.sp;
            if(Math.hypot(player.x-e.x, player.y-e.y) < player.r+e.s/2 && player.inv<=0) triggerRespawn();
        }});

        // BOSS SPAWN
        if(score >= lastBossThreshold + 1000 && !boss) {{
            boss = {{ x:300, y:-50, s:50, hp:2000, mH:2000, c:'#800000', sp:1 }};
        }}
        if(boss) {{
            let a = Math.atan2(player.y-boss.y, player.x-boss.x);
            boss.x += Math.cos(a)*boss.sp; boss.y += Math.sin(a)*boss.sp;
            if(boss.hp <= 0) {{ score+=500; lastBossThreshold+=1000; boss=null; }}
        }}

        particles.forEach((p,i) => {{ p.life--; if(p.life<=0) particles.splice(i,1); }});
        if(player.inv > 0) player.inv--;
        uScore.innerText = "Skor: " + score; uHP.innerText = "❤️".repeat(Math.max(0,health));
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        if(boss) {{ ctx.fillStyle=boss.c; ctx.beginPath(); ctx.arc(boss.x, boss.y, boss.s, 0, 7); ctx.fill(); }}
        if(player.hasPet) {{ ctx.fillStyle='#ffff4d'; ctx.beginPath(); ctx.arc(player.x+Math.cos(player.petAngle)*35, player.y+Math.sin(player.petAngle)*35, 6, 0, 7); ctx.fill(); }}
        
        if(player.inv <= 0 || player.inv % 10 < 5) {{
            let a = Math.atan2(my-player.y, mx-player.x);
            ctx.save(); ctx.translate(player.x, player.y); ctx.rotate(a);
            ctx.fillStyle = player.color; ctx.beginPath(); ctx.moveTo(18,0); ctx.lineTo(-12,-12); ctx.lineTo(-7,0); ctx.lineTo(-12,12); ctx.fill();
            if(player.hasFlank) ctx.fillRect(-15,-4,8,8);
            ctx.restore();
        }}
    }}

    function loop() {{ update(); draw(); if(!gameOver) requestAnimationFrame(loop); }}
    loop();
}})();
</script>
"""

cp.html(game_html, height=580, width=700)
