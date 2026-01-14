import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Upgrade System", layout="centered")
st.title("⚔️ Island.io: Top Menu Upgrade")

# Inisialisasi session state
if "char" not in st.session_state:
    st.session_state.char = None

def reset_game():
    st.session_state.char = None
    st.rerun()

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
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; user-select: none; color: white; overflow: hidden;">
    
    <div style="display:flex; justify-content: space-between; font-weight:bold; margin-bottom: 10px;">
        <div id="ui-lvl">LEVEL: 1</div>
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">❤️❤️❤️</div>
    </div>

    <div id="upgrade-menu" style="display:none; position:absolute; top:10px; left:50%; transform:translateX(-50%); background:rgba(30,30,30,0.98); padding:15px; border:3px solid #ffd700; border-radius:12px; width:90%; z-index:100; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <h3 style="color:#ffd700; margin:0 0 10px 0; font-size:16px;">PILIH UPGRADE KARAKTER</h3>
        <div style="display:flex; gap:10px; justify-content:center;">
            <button onclick="applyUpgrade('speed')" style="flex:1; padding:12px 5px; background:#4deaff; border:none; border-radius:8px; font-weight:bold; cursor:pointer; font-size:12px;">⚡ SPEED +0.5</button>
            <button onclick="applyUpgrade('flank')" style="flex:1; padding:12px 5px; background:#ff4d4d; border:none; border-radius:8px; font-weight:bold; cursor:pointer; font-size:12px;">🛡️ FLANK GUARD</button>
            <button onclick="applyUpgrade('pet')" style="flex:1; padding:12px 5px; background:#ffff4d; border:none; border-radius:8px; font-weight:bold; cursor:pointer; font-size:12px;">🤖 DRONE PET</button>
        </div>
    </div>

    <div style="margin: 0 auto 10px; width: 250px;">
        <div style="width:100%; height:8px; background:#333; border-radius:4px; overflow:hidden; border: 1px solid #555;">
            <div id="skill-bar" style="width:0%; height:100%; background: {p['col']};"></div>
        </div>
    </div>

    <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
    
    <div id="restart-btn" style="display:none; position:absolute; top:65%; left:50%; transform:translate(-50%, -50%);">
        <button onclick="parent.window.location.reload()" style="padding:15px 30px; background:#e74c3c; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">KEMBALI KE MENU</button>
    </div>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uBar = document.getElementById('skill-bar'), uLvl = document.getElementById('ui-lvl');
    const upMenu = document.getElementById('upgrade-menu'), rBtn = document.getElementById('restart-btn');

    let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
    let keys = {{}}, bullets = [], enemies = [], particles = [];
    let currentLvl = 1, lastUpgradeScore = 0;
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, inv: 0,
        hasFlank: false, hasPet: false, petAngle: 0
    }};

    window.applyUpgrade = function(type) {{
        if(type === 'speed') {{ player.baseSpeed += 0.5; player.speed = player.baseSpeed; }}
        if(type === 'flank') {{ player.hasFlank = true; }}
        if(type === 'pet') {{ player.hasPet = true; }}
        
        upMenu.style.display = "none";
        isPaused = false;
        requestAnimationFrame(loop);
    }};

    function fire(x, y, a, isPlayer, color, dmg) {{
        bullets.push({{ x, y, vx: Math.cos(a)*14, vy: Math.sin(a)*14, r: 4, c: color || player.color, p: isPlayer, d: dmg || 5 }});
    }}

    window.onkeydown = e => {{ keys[e.code] = true; }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    let mx=0, my=0;
    canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

    canvas.onmousedown = () => {{ 
        if(gameOver || isPaused) return;
        let a = Math.atan2(my-player.y, mx-player.x);
        fire(player.x, player.y, a, true);
        if(player.hasFlank) fire(player.x, player.y, a + Math.PI, true);
    }};

    function update() {{
        if(gameOver || isPaused) return;
        
        if(score >= lastUpgradeScore + 1000) {{
            isPaused = true;
            lastUpgradeScore += 1000;
            currentLvl++;
            upMenu.style.display = "block";
            return;
        }}

        if(player.hasPet) {{
            player.petAngle += 0.05;
            if(Math.random() < 0.03) {{
                let a = Math.random() * Math.PI * 2;
                fire(player.x + Math.cos(player.petAngle)*35, player.y + Math.sin(player.petAngle)*35, a, true, '#ffff4d', 2);
            }}
        }}

        let s = player.speed;
        if(keys['KeyW']) player.y -= s; if(keys['KeyS']) player.y += s;
        if(keys['KeyA']) player.x -= s; if(keys['KeyD']) player.x += s;

        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(b.p) {{
                enemies.forEach((e, i) => {{
                    if(Math.hypot(e.x-b.x, e.y-b.y) < e.s/2 + b.r) {{
                        score += 100; enemies.splice(i,1); b.del = true;
                    }}
                }});
            }}
            return !b.del && b.x>-50 && b.x<650 && b.y>-50 && b.y<450;
        }});

        if(enemies.length < 5) enemies.push({{ x: Math.random()*600, y: Math.random()*400, s: 20, c: '#e74c3c', sp: 1.2 }});
        enemies.forEach(e => {{ 
            let a = Math.atan2(player.y-e.y, player.x-e.x); e.x += Math.cos(a)*e.sp; e.y += Math.sin(a)*e.sp; 
            if(Math.hypot(player.x-e.x, player.y-e.y) < player.r+e.s/2 && player.inv<=0) {{ health--; player.inv=120; if(health<=0) gameOver=true; }}
        }});

        if(player.inv > 0) player.inv--;
        uScore.innerText = "Skor: " + score; 
        uHP.innerText = "❤️".repeat(Math.max(0,health));
        uLvl.innerText = "LEVEL: " + currentLvl;
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});

        if(player.hasPet) {{
            ctx.fillStyle = '#ffff4d';
            ctx.beginPath(); ctx.arc(player.x + Math.cos(player.petAngle)*35, player.y + Math.sin(player.petAngle)*35, 6, 0, 7); ctx.fill();
        }}

        if(player.inv <= 0 || (player.inv % 10 < 5)) {{
            let a = Math.atan2(my - player.y, mx - player.x);
            ctx.save(); ctx.translate(player.x, player.y); ctx.rotate(a);
            ctx.fillStyle = player.color;
            ctx.beginPath(); ctx.moveTo(15, 0); ctx.lineTo(-10, -10); ctx.lineTo(-10, 10); ctx.closePath(); ctx.fill();
            if(player.hasFlank) ctx.fillRect(-12, -4, 8, 8);
            ctx.restore();
        }}
        if(gameOver) {{ ctx.fillStyle='white'; ctx.font='40px Arial'; ctx.textAlign='center'; ctx.fillText("GAME OVER", 300, 200); rBtn.style.display="block"; }}
    }}

    function loop() {{ update(); draw(); if(!gameOver && !isPaused) requestAnimationFrame(loop); }}
    loop();
}})();
</script>
"""

cp.html(game_html, height=600)
