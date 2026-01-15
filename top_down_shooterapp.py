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

# --- SIDEBAR UNTUK UPGRADE (DIPERBAIKI) ---
if st.session_state.char:
    if st.sidebar.button("Kembali Pilih Hero"):
        reset_game()
    
    st.sidebar.write("---")
    # Bagian ini yang kita taruh di sidebar agar bisa diklik
    st.sidebar.markdown("""
        <div id="sidebar-upgrade-container" style="font-family: sans-serif;">
            <div id="upgrade-menu" style="display:none; background:#1a1a1a; padding:15px; border:2px solid #ffd700; border-radius:10px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); margin-bottom: 20px;">
                <h3 style="color:#ffd700; margin:0 0 10px 0; font-size:16px; text-align:center;">LEVEL UP!</h3>
                <button id="btn-speed" style="width:100%; margin-bottom:8px; padding:10px; background:#4deaff; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">⚡ SPEED +0.5</button>
                <button id="btn-flank" style="width:100%; margin-bottom:8px; padding:10px; background:#ff4d4d; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">🛡️ FLANK GUARD</button>
                <button id="btn-pet" style="width:100%; padding:10px; background:#ffff4d; border:none; border-radius:4px; font-weight:bold; cursor:pointer;">🤖 DRONE PET</button>
            </div>

            <div id="upgrade-history-list" style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); color:rgba(255,255,255,0.6); font-size:13px;">
                <div style="font-weight:bold; margin-bottom:5px;">RIWAYAT UPGRADE:</div>
                <div id="hist-content"><i>Belum ada</i></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
            st.markdown(f"<div style='text-align: center; color: {cls['col']}; font-weight: bold;'>{cls['n']}</div>", unsafe_allow_html=True)
            if st.button("Pilih " + cls['n'].split()[1], key=cls['t']):
                st.session_state.char = {"hp": cls["hp"], "spd": cls["spd"], "col": cls["col"], "type": cls["t"]}
                st.rerun()
            st.caption(cls["stat"])
            st.write("---")
    st.stop()

# --- GAMEPLAY ---
p = st.session_state.char
game_html = f"""
<div style="display: flex; justify-content: center; align-items: flex-start;">
    <div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; user-select: none;">
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
    const rBtn = document.getElementById('restart-btn');

    // AKSES ELEMEN SIDEBAR DARI DALAM IFRAME
    const sideMenu = window.parent.document.getElementById('upgrade-menu');
    const sideHist = window.parent.document.getElementById('hist-content');
    const btnSpeed = window.parent.document.getElementById('btn-speed');
    const btnFlank = window.parent.document.getElementById('btn-flank');
    const btnPet   = window.parent.document.getElementById('btn-pet');

    let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
    let keys = {{}}, bullets = [], enemies = [], particles = [], boss = null, items = [];
    let lastBossThreshold = 0, lastUpgradeScore = 0, currentLvl = 1;
    let upgradesTaken = [];
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, shield: false,
        dmg: 5, inv: 0, kills: 0, 
        tripleShot: 0, energyTime: 0,
        hasFlank: false, hasPet: false, petAngle: 0
    }};

    // FUNGSI UPGRADE YANG DIPERBAIKI (Langsung terhubung ke tombol sidebar)
    function applyUpgrade(type) {{
        if(type === 'speed') {{ player.baseSpeed += 0.5; player.speed = player.baseSpeed; upgradesTaken.push("⚡ Speed"); }}
        if(type === 'flank') {{ player.hasFlank = true; upgradesTaken.push("🛡️ Flank"); }}
        if(type === 'pet') {{ player.hasPet = true; upgradesTaken.push("🤖 Pet"); }}
        
        if(sideHist) sideHist.innerHTML = upgradesTaken.map(u => "• " + u).join("<br>");
        if(sideMenu) sideMenu.style.display = "none";
        isPaused = false;
        requestAnimationFrame(loop);
    }}

    // Event Listener untuk tombol di Sidebar
    if(btnSpeed) btnSpeed.onclick = () => applyUpgrade('speed');
    if(btnFlank) btnFlank.onclick = () => applyUpgrade('flank');
    if(btnPet)   btnPet.onclick   = () => applyUpgrade('pet');

    // --- LOGIKA ASLI GAME (TIDAK DIUBAH) ---
    function spawnExplosion(x, y, color, count=15) {{
        for(let i=0; i<count; i++) particles.push({{
            x, y, vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15, life: Math.random()*30+10, c: color
        }});
    }}

    function spawnItem(x, y) {{
        let r = Math.random();
        if(r < 0.25) {{
            let type = Math.random();
            if(type < 0.3) items.push({{ x, y, type: 'medkit', c: '#ff4d4d', label: '✚' }});
            else if(type < 0.6) items.push({{ x, y, type: 'energy', c: '#4deaff', label: '⚡' }});
            else items.push({{ x, y, type: 'triple', c: '#ffff4d', label: 'Ⅲ' }});
        }}
    }}

    function triggerRespawn() {{
        health--; spawnExplosion(player.x, player.y, "#ffffff"); player.inv = 180;
        if(health <= 0) {{ gameOver = true; rBtn.style.display = "block"; }}
    }}

    function drawHexagon(x, y, size, color) {{
        ctx.fillStyle = color; ctx.beginPath();
        for (let i = 0; i < 6; i++) {{ ctx.lineTo(x + size * Math.cos(i * Math.PI / 3), y + size * Math.sin(i * Math.PI / 3)); }}
        ctx.closePath(); ctx.fill();
    }}

    window.onkeydown = e => {{ keys[e.code] = true; if(e.code==='Space') useUlt(); }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    let mx=0, my=0;
    canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

    function fire(x, y, a, isSpecial, isPlayer, damageValue, color) {{
        let ox = x + Math.cos(a) * 20, oy = y + Math.sin(a) * 20;
        bullets.push({{ x:ox, y:oy, vx: Math.cos(a)*(isSpecial?18:15), vy: Math.sin(a)*(isSpecial?18:15), r: isSpecial?8:4, c: color || (isPlayer?player.color:'#F00'), p: isPlayer, rk: false, d: damageValue || player.dmg }});
    }}

    function useUlt(forcedType = null) {{
        let type = forcedType || player.type;
        if(!forcedType && (player.sT < player.sM || gameOver || isPaused)) return;
        if(!forcedType) {{ player.sT = 0; player.kills = 0; }}
        if(type === 'tank') {{
            player.shield = true; let shots = 0;
            let interval = setInterval(() => {{ for(let a=0; a<Math.PI*2; a+=Math.PI/6) fire(player.x, player.y, a, false, true, 80); shots++; if(shots >= 3) clearInterval(interval); }}, 500);
            setTimeout(() => player.shield = false, 10000);
        }} 
        else if(type === 'scout') {{
            if(boss) {{
                let angleToBoss = Math.atan2(boss.y - player.y, boss.x - player.x);
                player.x = boss.x + Math.cos(angleToBoss) * 40; player.y = boss.y + Math.sin(angleToBoss) * 40;
                player.inv = 120; if(!boss.shieldActive) boss.hp -= 400; 
            }} else {{
                let a = Math.atan2(my-player.y, mx-player.x); player.x += Math.cos(a)*150; player.y += Math.sin(a)*150;
                player.inv = 60; spawnExplosion(player.x, player.y, player.color);
            }}
        }}
        else if(type === 'bomber') {{
            let radius = 350; spawnExplosion(player.x, player.y, "#ffff00", 150); 
            enemies.forEach(e => {{ if(Math.hypot(e.x-player.x, e.y-player.y) < radius) e.hp -= 500; }});
            if(boss && Math.hypot(boss.x-player.x, boss.y-player.y) < radius) {{ if(!boss.shieldActive) boss.hp -= 800; }}
        }}
        else if(type === 'roket') {{
            for(let i=0; i<6; i++) {{
                bullets.push({{ x: player.x, y: player.y, vx: Math.cos((Math.PI*2/6)*i)*5, vy: Math.sin((Math.PI*2/6)*i)*5, r: 10, c: '#ffa500', p: true, rk: true, target: null, life: 300, d: 150 }});
            }}
        }}
        else if(type === 'assault') {{
            for(let i=0; i<15; i++) setTimeout(()=>fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), true, true, 40), i*80);
        }}
        else if(type === 'joker') {{
            const pool = ['tank', 'scout', 'bomber', 'roket', 'assault'];
            useUlt(pool[Math.floor(Math.random()*pool.length)]);
        }}
    }}

    canvas.onmousedown = () => {{ 
        if(gameOver || isPaused) return;
        let a = Math.atan2(my-player.y, mx-player.x);
        fire(player.x, player.y, a, false, true, player.dmg);
        if(player.hasFlank) fire(player.x, player.y, a + Math.PI, false, true, player.dmg);
        if(player.tripleShot > 0) {{ fire(player.x, player.y, a + 0.2, false, true, player.dmg); fire(player.x, player.y, a - 0.2, false, true, player.dmg); player.tripleShot--; }}
    }};

    function update() {{
        if(gameOver || isPaused) return;
        
        // LEVEL UP LOGIC
        if(score >= lastUpgradeScore + 1000) {{
            isPaused = true; lastUpgradeScore += 1000; currentLvl++;
            if(sideMenu) sideMenu.style.display = "block"; return;
        }}

        if(player.hasPet) {{
            player.petAngle += 0.05;
            if(Math.random() < 0.04) {{
                let target = enemies[0] || boss;
                let a = target ? Math.atan2(target.y-player.y, target.x-player.x) : player.petAngle;
                fire(player.x + Math.cos(player.petAngle)*35, player.y + Math.sin(player.petAngle)*35, a, false, true, 4, '#ffff4d');
            }}
        }}

        for(let i = items.length - 1; i >= 0; i--) {{
            let it = items[i]; if(Math.hypot(player.x - it.x, player.y - it.y) < player.r + 10) {{
                if(it.type === 'medkit') health = Math.min(health + 1, 10);
                else if(it.type === 'energy') player.energyTime += 300;
                else if(it.type === 'triple') player.tripleShot += 20;
                items.splice(i, 1);
            }}
        }}

        if(player.energyTime > 0) {{ player.energyTime--; player.speed = player.baseSpeed * 1.5; }} 
        else {{ player.speed = player.baseSpeed; }}

        let s = player.speed, nx=player.x, ny=player.y;
        if(keys['KeyW']) ny-=s; if(keys['KeyS']) ny+=s;
        if(keys['KeyA']) nx-=s; if(keys['KeyD']) nx+=s;
        if(nx > 0 && nx < 600) player.x=nx; if(ny > 0 && ny < 400) player.y=ny;

        // Skill Charge
        if(player.type === 'roket' && boss) player.sT = Math.min(100, player.sT + 0.3);
        else if(player.type === 'roket') player.sT = (player.kills/8)*100;
        else if(player.type === 'tank' || player.type === 'bomber') player.sT = Math.min(100, player.sT + 0.12);
        else player.sT = Math.min(100, player.sT + 0.2);
        uBar.style.width = Math.min(100, player.sT) + '%';

        bullets = bullets.filter(b => {{
            if(b.rk) {{
                let target = boss || enemies[0];
                if(target) {{ let a = Math.atan2(target.y-b.y, target.x-b.x); b.vx += Math.cos(a)*1.2; b.vy += Math.sin(a)*1.2; }}
                let speed = Math.hypot(b.vx, b.vy); if(speed > 10) {{ b.vx=(b.vx/speed)*10; b.vy=(b.vy/speed)*10; }}
            }}
            b.x += b.vx; b.y += b.vy;
            if(b.p) {{
                if(boss && Math.hypot(boss.x-b.x, boss.y-b.y) < boss.s) {{ if(!boss.shieldActive) boss.hp -= b.d; return false; }}
                for(let i=enemies.length-1; i>=0; i--) {{
                    let e = enemies[i]; if(Math.hypot(e.x-b.x, e.y-b.y) < e.s/2+b.r) {{ e.hp -= b.d; if(e.hp<=0) {{ player.kills++; score += e.val; enemies.splice(i, 1); }} return false; }}
                }}
            }} else if(Math.hypot(player.x-b.x, player.y-b.y) < player.r+b.r) {{ if(player.inv<=0 && !player.shield) triggerRespawn(); return false; }}
            return b.x>-50 && b.x<650 && b.y>-50 && b.y<450;
        }});

        if(score >= lastBossThreshold + 1000 && !boss) {{ boss = {{ x: 300, y: -50, s: 50, hp: 2000, mH: 2000, c: '#800000', sp: 1, shieldActive: false, shieldTimer: 0, nextShield: 400 }}; enemies = []; }}
        if(boss) {{
            let a = Math.atan2(player.y-boss.y, player.x-boss.x); boss.x += Math.cos(a)*boss.sp; boss.y += Math.sin(a)*boss.sp;
            if(boss.hp <= 0) {{ score += 500; boss = null; lastBossThreshold += 1000; }}
            if(Math.random() < 0.02) fire(boss.x, boss.y, a + (Math.random()-0.5), false, false, 1);
        }}
        if(!boss && enemies.length < 8) enemies.push({{ x: Math.random()*600, y: Math.random()*400, s: 20, sp: 1.2, hp: 5, c: '#e74c3c', val: 10 }});
        enemies.forEach(e => {{ let a = Math.atan2(player.y-e.y, player.x-e.x); e.x += Math.cos(a)*e.sp; e.y += Math.sin(a)*e.sp; if(Math.hypot(player.x-e.x, player.y-e.y) < player.r+e.s/2 && player.inv<=0 && !player.shield) triggerRespawn(); }});
        particles.forEach((p,i)=>{{ p.life--; if(p.life<=0) particles.splice(i,1); }});
        if(player.inv > 0) player.inv--;
        uScore.innerText = "Skor: " + score; uHP.innerText = "❤️".repeat(Math.max(0,health));
        uLvl.innerText = boss ? "BOSS BATTLE!" : "LEVEL: " + currentLvl;
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        if(boss) drawHexagon(boss.x, boss.y, boss.s, boss.c);
        particles.forEach(p => {{ ctx.fillStyle=p.c; ctx.globalAlpha=p.life/30; ctx.fillRect(p.x,p.y,3,3); ctx.globalAlpha=1; }});
        if(player.hasPet) {{ ctx.fillStyle = '#ffff4d'; ctx.beginPath(); ctx.arc(player.x + Math.cos(player.petAngle)*35, player.y + Math.sin(player.petAngle)*35, 6, 0, 7); ctx.fill(); }}
        if(player.inv <= 0 || (player.inv % 10 < 5)) {{
            let angle = Math.atan2(my - player.y, mx - player.x); ctx.save(); ctx.translate(player.x, player.y); ctx.rotate(angle); ctx.fillStyle = player.color; ctx.beginPath(); ctx.moveTo(18, 0); ctx.lineTo(-12, -12); ctx.lineTo(-12, 12); ctx.closePath(); ctx.fill();
            if(player.hasFlank) ctx.fillRect(-15, -4, 8, 8); ctx.restore();
            if(player.shield) {{ ctx.strokeStyle='#00e5ff'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(player.x,player.y,25,0,7); ctx.stroke(); }}
        }}
        if(gameOver) {{ ctx.fillStyle='white'; ctx.font='40px Arial'; ctx.textAlign='center'; ctx.fillText("GAME OVER", 300, 200); }}
    }}

    function loop() {{ update(); draw(); if(!gameOver && !isPaused) requestAnimationFrame(loop); }}
    loop();
}})();
</script>
"""

cp.html(game_html, height=550, width=700)
