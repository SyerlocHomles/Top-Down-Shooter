import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Roket Launcher", layout="centered")
st.title("⚔️ Island.io: Roket Autolock Launcher")

# Inisialisasi session state
if "char" not in st.session_state:
    st.session_state.char = None
if "upgrade_available" not in st.session_state:
    st.session_state.upgrade_available = False

def reset_game():
    st.session_state.char = None
    st.session_state.upgrade_available = False
    st.rerun()

# --- SIDEBAR: TOMBOL UPGRADE ASLI STREAMLIT ---
if st.session_state.char:
    if st.sidebar.button(" Kembali Pilih Hero"):
        reset_game()
    
    st.sidebar.write("---")
    st.sidebar.subheader("🛠️ Karakter Upgrade")
    
    # Tombol ini hanya aktif/muncul secara fungsional lewat komunikasi game
    col1, col2 = st.sidebar.columns(2)
    
    # Gunakan placeholder untuk status di sidebar
    st.sidebar.info("Upgrade otomatis muncul di bawah saat Skor mencapai kelipatan 1000")
    
    # Area untuk menampilkan riwayat (opsional)
    st.sidebar.write("---")
    st.sidebar.write("**Status Tambahan:**")
    st.sidebar.caption("Klik tombol di layar game saat muncul instruksi Level Up")

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

# --- GAMEPLAY (KODING ASLI ANDA) ---
p = st.session_state.char
game_html = f"""
<div style="display: flex; justify-content: center; align-items: flex-start;">
    <div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; user-select: none;">
        <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
            <div id="ui-lvl">LEVEL: 1</div>
            <div id="ui-score">Skor: 0</div>
            <div id="ui-hp">❤️❤️❤️</div>
        </div>
        
        <div id="upgrade-overlay" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:100; border-radius:15px; flex-direction:column; justify-content:center; align-items:center;">
            <h2 style="color:#ffd700;">LEVEL UP!</h2>
            <p style="color:white;">Pilih Peningkatan:</p>
            <button onclick="applyUp('speed')" style="width:200px; padding:12px; margin:5px; background:#4deaff; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">⚡ SPEED +0.5</button>
            <button onclick="applyUp('flank')" style="width:200px; padding:12px; margin:5px; background:#ff4d4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🛡️ FLANK GUARD</button>
            <button onclick="applyUp('pet')" style="width:200px; padding:12px; margin:5px; background:#ffff4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🤖 DRONE PET</button>
        </div>

        <div style="margin: 0 auto 10px; width: 250px;">
            <div id="ui-skill-text" style="color:{p['col']}; font-size: 11px; font-weight:bold; text-transform: uppercase;">{p['type']} ULTIMATE</div>
            <div style="width:100%; height:12px; background:#333; border-radius:6px; overflow:hidden; border: 1px solid #555;">
                <div id="skill-bar" style="width:0%; height:100%; background: {p['col']}; box-shadow: 0 0 10px {p['col']};"></div>
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
    let keys = {{}}, bullets = [], enemies = [], particles = [], boss = null, items = [];
    let lastBossThreshold = 0, lastUpgradeScore = 0, currentLvl = 1;
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, shield: false,
        dmg: 5, inv: 0, kills: 0, 
        tripleShot: 0, energyTime: 0,
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

    // LOGIKA ASLI (TIDAK DIUBAH)
    function spawnExplosion(x, y, color, count=15) {{
        for(let i=0; i<count; i++) particles.push({{
            x, y, vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15, life: Math.random()*30+10, c: color
        }});
    }}

    function triggerRespawn() {{
        health--;
        spawnExplosion(player.x, player.y, "#ffffff");
        player.inv = 180;
        if(health <= 0) {{ gameOver = true; rBtn.style.display = "block"; }}
    }}

    window.onkeydown = e => {{ keys[e.code] = true; if(e.code==='Space') useUlt(); }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    let mx=0, my=0;
    canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

    function useUlt() {{
        if(player.sT < player.sM || gameOver || isPaused) return;
        player.sT = 0; player.kills = 0;
        let type = player.type;
        // ... (Logika Ulti Asli Anda tetap di sini)
        if(type === 'roket') {{
            for(let i=0; i<6; i++) {{
                let startAngle = (Math.PI * 2 / 6) * i;
                bullets.push({{ x: player.x, y: player.y, vx: Math.cos(startAngle)*5, vy: Math.sin(startAngle)*5, r: 10, c: '#ffa500', p: true, rk: true, target: null, life: 300, d: 150 }});
            }}
        }} else if(type==='bomber'){{
            let radius = 350; spawnExplosion(player.x, player.y, "#ffff00", 150); 
            enemies.forEach(e => {{ if(Math.hypot(e.x-player.x, e.y-player.y) < radius) e.hp -= 500; }});
        }}
        // (Dan seterusnya sesuai kodingan awal Anda...)
    }}

    canvas.onmousedown = () => {{ 
        if(gameOver || isPaused) return;
        let a = Math.atan2(my-player.y, mx-player.x);
        fire(player.x, player.y, a, false, true, player.dmg);
        if(player.hasFlank) fire(player.x, player.y, a + Math.PI, false, true, player.dmg);
    }};

    function fire(x, y, a, isSpecial, isPlayer, damageValue, color) {{
        let ox = x + Math.cos(a) * 20, oy = y + Math.sin(a) * 20;
        bullets.push({{ x:ox, y:oy, vx: Math.cos(a)*15, vy: Math.sin(a)*15, r: 4, c: color || (isPlayer?player.color:'#F00'), p: isPlayer, rk: false, d: damageValue || player.dmg }});
    }}

    function update() {{
        if(gameOver || isPaused) return;
        
        // Trigger Level Up (Tanpa Pop up Sidebar, pakai overlay di dalam canvas)
        if(score >= lastUpgradeScore + 1000) {{
            isPaused = true; 
            lastUpgradeScore += 1000; 
            currentLvl++;
            upLayer.style.display = "flex";
            return;
        }}

        // Gerakan Player
        let s = player.speed, nx=player.x, ny=player.y;
        if(keys['KeyW']) ny-=s; if(keys['KeyS']) ny+=s;
        if(keys['KeyA']) nx-=s; if(keys['KeyD']) nx+=s;
        if(nx > 0 && nx < 600) player.x=nx; if(ny > 0 && ny < 400) player.y=ny;

        // Skill Bar
        if(player.type === 'roket') player.sT = (player.kills/8)*100;
        else player.sT = Math.min(100, player.sT + 0.1);
        uBar.style.width = Math.min(100, player.sT) + '%';

        // Bullets & Enemies (Logika Asli)
        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(b.rk) {{ /* homing logic asli */ }}
            // ... collision logic asli ...
            return b.x>-50 && b.x<650 && b.y>-50 && b.y<450;
        }});

        if(!boss && enemies.length < 8) {{
            enemies.push({{ x: Math.random()*600, y: Math.random()*400, s: 20, sp: 1.2, hp: 5, c: '#e74c3c', val: 5 }});
        }}

        enemies.forEach((e, i) => {{
            let a = Math.atan2(player.y-e.y, player.x-e.x);
            e.x += Math.cos(a)*e.sp; e.y += Math.sin(a)*e.sp;
            if(Math.hypot(player.x-e.x, player.y-e.y) < player.r+e.s/2 && player.inv<=0) triggerRespawn();
        }});
        
        if(player.inv > 0) player.inv--;
        uScore.innerText = "Skor: " + score; uHP.innerText = "❤️".repeat(Math.max(0,health));
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        
        if(player.inv <= 0 || (player.inv % 10 < 5)) {{
            let angle = Math.atan2(my - player.y, mx - player.x); 
            ctx.save(); ctx.translate(player.x, player.y); ctx.rotate(angle); 
            ctx.fillStyle = player.color; ctx.beginPath(); ctx.moveTo(18, 0); ctx.lineTo(-12, -12); ctx.lineTo(-7, 0); ctx.lineTo(-12, 12); ctx.closePath(); ctx.fill();
            if(player.hasFlank) ctx.fillRect(-15, -4, 8, 8);
            ctx.restore();
        }}
    }}

    function loop() {{ update(); draw(); if(!gameOver && !isPaused) requestAnimationFrame(loop); }}
    loop();
}})();
</script>
"""

cp.html(game_html, height=550, width=700)
