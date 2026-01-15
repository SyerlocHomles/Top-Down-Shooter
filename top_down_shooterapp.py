import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Roket Launcher", layout="centered")
st.title("⚔️ Island.io: Roket Autolock Launcher")

# Inisialisasi session state
if "char" not in st.session_state:
    st.session_state.char = None

def reset_game():
    st.session_state.char = None
    st.rerun()

# Tombol reset di sidebar Streamlit
if st.session_state.char:
    if st.sidebar.button("Kembali Pilih Hero"):
        reset_game()

# --- MENU PILIH KARAKTER ---
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
            # EFEK BAYANGAN: Jika hero dipilih, tampilannya abu-abu transparan
            is_picked = st.session_state.get('char_type') == cls['t']
            div_style = f"text-align: center; color: {cls['col']}; font-weight: bold;"
            if is_picked:
                div_style += "filter: grayscale(100%); opacity: 0.3;"

            st.markdown(f"<div style='{div_style}'>{cls['n']}</div>", unsafe_allow_html=True)
            
            if st.button("Pilih " + cls['n'].split()[1], key=cls['t'], disabled=is_picked):
                st.session_state.char = {"hp": cls["hp"], "spd": cls["spd"], "col": cls["col"], "type": cls["t"]}
                st.session_state.char_type = cls['t'] # Simpan untuk efek bayangan
                st.rerun()
            st.caption(cls["stat"])
            st.write("---")
    st.stop()

# --- GAMEPLAY ---
p = st.session_state.char
game_html = f"""
<div style="display: flex; justify-content: center; align-items: flex-start; gap: 20px; font-family: sans-serif; user-select: none;">
    
    <div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; width: 620px;">
        <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
            <div id="ui-lvl">LEVEL: 1</div>
            <div id="ui-score">Skor: 0</div>
            <div id="ui-hp">❤️❤️❤️</div>
        </div>

        <div style="margin: 0 auto 10px; width: 250px;">
            <div id="ui-skill-text" style="color:{p['col']}; font-size: 11px; font-weight:bold; text-transform: uppercase;">{p['type']} ULTIMATE</div>
            <div style="width:100%; height:12px; background:#333; border-radius:6px; overflow:hidden; border: 1px solid #555;">
                <div id="skill-bar" style="width:0%; height:100%; background: {p['col']}; box-shadow: 0 0 10px {p['col']};"></div>
            </div>
        </div>

        <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
        
        <div id="restart-btn" style="display:none; position:absolute; top:50%; left:50%; transform:translate(-50%, -50%);">
            <button onclick="parent.window.location.reload()" style="padding:15px 30px; font-size:18px; font-weight:bold; color:white; background:#e74c3c; border:none; border-radius:10px; cursor:pointer;">
                MAIN LAGI
            </button>
        </div>
    </div>

    <div style="width: 180px; display: flex; flex-direction: column; gap: 10px;">
        
        <div id="upgrade-menu" style="display:none; background:#222; padding:15px; border:3px solid #ffd700; border-radius:12px; box-shadow: 0 5px 20px rgba(0,0,0,0.8);">
            <h3 style="color:#ffd700; margin:0 0 10px 0; font-size:14px; text-align:center;">LEVEL UP!</h3>
            <button onclick="applyUpgrade('speed')" style="width:100%; margin-bottom:8px; padding:8px; background:#4deaff; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">⚡ SPEED</button>
            <button onclick="applyUpgrade('flank')" style="width:100%; margin-bottom:8px; padding:8px; background:#ff4d4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🛡️ FLANK</button>
            <button onclick="applyUpgrade('pet')" style="width:100%; margin-bottom:8px; padding:8px; background:#ffff4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🤖 PET</button>
            <hr style="border:1px solid #444">
            <button onclick="parent.window.location.reload()" style="width:100%; padding:5px; background:#555; color:white; border:none; border-radius:5px; cursor:pointer; font-size:10px;">GANTI HERO</button>
        </div>

        <div id="upgrade-history" style="background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; border: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.4); font-size: 11px;">
            <strong style="color: rgba(255,255,255,0.7);">RIWAYAT UPGRADE:</strong>
            <ul id="history-list" style="padding-left: 15px; margin: 5px 0;">
                <li>Belum ada upgrade</li>
            </ul>
        </div>
    </div>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uBar = document.getElementById('skill-bar'), upMenu = document.getElementById('upgrade-menu'),
          histList = document.getElementById('history-list'), rBtn = document.getElementById('restart-btn');

    let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
    let keys = {{}}, bullets = [], enemies = [], particles = [], items = [], boss = null;
    let lastUpgradeScore = 0, currentLvl = 1, upgrades = [];

    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, shield: false, dmg: 5, inv: 0, kills: 0,
        hasFlank: false, hasPet: false, petAngle: 0
    }};

    window.applyUpgrade = function(type) {{
        if(type === 'speed') {{ player.baseSpeed += 0.5; player.speed = player.baseSpeed; upgrades.push("⚡ Speed Boost"); }}
        if(type === 'flank') {{ player.hasFlank = true; upgrades.push("🛡️ Flank Guard"); }}
        if(type === 'pet') {{ player.hasPet = true; upgrades.push("🤖 Drone Pet"); }}
        
        // Update riwayat transparan
        histList.innerHTML = upgrades.map(item => `<li>${{item}}</li>`).join("");
        
        upMenu.style.display = "none";
        isPaused = false;
        requestAnimationFrame(loop);
    }};

    function spawnExplosion(x, y, color) {{
        for(let i=0; i<10; i++) particles.push({{ x, y, vx:(Math.random()-0.5)*10, vy:(Math.random()-0.5)*10, life:20, c:color }});
    }}

    function triggerRespawn() {{
        health--;
        spawnExplosion(player.x, player.y, "#fff");
        player.inv = 120;
        if(health <= 0) {{ gameOver = true; rBtn.style.display = "block"; }}
    }}

    window.onkeydown = e => {{ keys[e.code] = true; if(e.code==='Space') useUlt(); }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    let mx=0, my=0;
    canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

    function fire(x, y, a, isSpecial, isPlayer, damageValue) {{
        bullets.push({{ x, y, vx: Math.cos(a)*15, vy: Math.sin(a)*15, r: 5, c: isPlayer?player.color:'#F00', p: isPlayer, d: damageValue || 5 }});
    }}

    function update() {{
        if(gameOver || isPaused) return;

        if(score >= lastUpgradeScore + 1000) {{
            isPaused = true; lastUpgradeScore += 1000; currentLvl++;
            upMenu.style.display = "block"; return;
        }}

        // Gerakan Player
        let s = player.speed;
        if(keys['KeyW']) player.y -= s; if(keys['KeyS']) player.y += s;
        if(keys['KeyA']) player.x -= s; if(keys['KeyD']) player.x += s;

        // Skill Charging
        player.sT = Math.min(100, player.sT + 0.1);
        uBar.style.width = player.sT + '%';

        // Bullets
        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(b.p) {{
                enemies.forEach((e, i) => {{
                    if(Math.hypot(e.x-b.x, e.y-b.y) < 20) {{
                        e.hp -= b.d; if(e.hp<=0) {{ score+=100; enemies.splice(i,1); }}
                        return false;
                    }}
                }});
            }} else if(Math.hypot(player.x-b.x, player.y-b.y) < 15 && player.inv <= 0) {{
                triggerRespawn(); return false;
            }}
            return b.x > 0 && b.x < 600 && b.y > 0 && b.y < 400;
        }});

        // Enemies
        if(enemies.length < 5) enemies.push({{ x: Math.random()*600, y: Math.random()*400, hp: 10, c: '#e74c3c' }});
        enemies.forEach(e => {{
            let a = Math.atan2(player.y-e.y, player.x-e.x);
            e.x += Math.cos(a)*1.5; e.y += Math.sin(a)*1.5;
            if(Math.hypot(player.x-e.x, player.y-e.y) < 20 && player.inv <= 0) triggerRespawn();
        }});

        particles.forEach((p,i)=>{{ p.x+=p.vx; p.y+=p.vy; p.life--; if(p.life<=0) particles.splice(i,1); }});
        if(player.inv > 0) player.inv--;
        uScore.innerText = "Skor: " + score; uHP.innerText = "❤️".repeat(Math.max(0,health));
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.c; ctx.fillRect(e.x-10, e.y-10, 20, 20); }});
        particles.forEach(p => {{ ctx.fillStyle=p.c; ctx.fillRect(p.x,p.y,2,2); }});
        
        if(player.inv <= 0 || player.inv % 10 < 5) {{
            ctx.fillStyle = player.color;
            ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, 7); ctx.fill();
        }}
    }}

    canvas.onmousedown = () => {{ if(!isPaused) fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), false, true); }};

    function loop() {{ update(); draw(); if(!gameOver && !isPaused) requestAnimationFrame(loop); }}
    loop();
}})();
</script>
"""

cp.html(game_html, height=550, width=850)
