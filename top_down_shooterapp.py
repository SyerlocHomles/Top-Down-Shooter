import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Roket Launcher", layout="centered")
st.title("⚔️ Island.io: Roket Upgrade System")

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
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: 'Segoe UI', sans-serif; user-select: none; color: white;">
    <div style="display:flex; justify-content: space-between; font-weight:bold; margin-bottom: 10px;">
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
    
    <div id="upgrade-menu" style="display:none; position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); background:rgba(20,20,20,0.95); padding:20px; border:3px solid #ffd700; border-radius:15px; width:300px; z-index:100;">
        <h2 style="color:#ffd700; margin-top:0;">LEVEL UP!</h2>
        <p>Pilih Perk Kamu:</p>
        <button onclick="applyUpgrade('speed')" style="width:100%; padding:10px; margin:5px 0; background:#4deaff; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">⚡ Speed +0.5</button>
        <button onclick="applyUpgrade('flank')" style="width:100%; padding:10px; margin:5px 0; background:#ff4d4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🛡️ Flank Guard</button>
        <button onclick="applyUpgrade('pet')" style="width:100%; padding:10px; margin:5px 0; background:#ffff4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🤖 Drone Pet</button>
    </div>

    <div id="restart-btn" style="display:none; position:absolute; top:65%; left:50%; transform:translate(-50%, -50%);">
        <button onclick="parent.window.location.reload()" style="padding:15px 30px; font-size:18px; font-weight:bold; color:white; background:#e74c3c; border:none; border-radius:10px; cursor:pointer; box-shadow: 0 5px #c0392b;">
            KEMBALI KE MENU
        </button>
    </div>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uBar = document.getElementById('skill-bar'), uLvl = document.getElementById('ui-lvl');
    const upMenu = document.getElementById('upgrade-menu'), rBtn = document.getElementById('restart-btn');

    let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
    let keys = {{}}, bullets = [], enemies = [], particles = [], boss = null, items = [];
    let currentLvl = 1, lastUpgradeScore = 0;
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, shield: false,
        dmg: 5, inv: 0, kills: 0, 
        tripleShot: 0, energyTime: 0,
        // Upgrade Stats
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

    function fire(x, y, a, isSpecial, isPlayer, damageValue, color) {{
        let ox = x + Math.cos(a) * 20, oy = y + Math.sin(a) * 20;
        bullets.push({{ x:ox, y:oy, vx: Math.cos(a)*(isSpecial?18:15), vy: Math.sin(a)*(isSpecial?18:15), r: isSpecial?8:4, c: color || (isPlayer?player.color:'#F00'), p: isPlayer, rk: false, d: damageValue || player.dmg }});
    }}

    function useUlt() {{
        if(player.sT < player.sM || gameOver || isPaused) return;
        player.sT = 0; player.kills = 0;
        if(player.type === 'roket') {{
            for(let i=0; i<6; i++) bullets.push({{ x: player.x, y: player.y, vx: Math.cos(i)*5, vy: Math.sin(i)*5, r: 10, c: '#ffa500', p: true, rk: true, target: null, life: 300, d: 150 }});
        }}
        // ... (Ultimate lainnya disingkat untuk efisiensi koding upgrade)
    }}

    canvas.onmousedown = () => {{ 
        if(gameOver || isPaused) return;
        let a = Math.atan2(my-player.y, mx-player.x);
        fire(player.x, player.y, a, false, true);
        if(player.hasFlank) fire(player.x, player.y, a + Math.PI, false, true); // Tembak belakang
    }};

    function update() {{
        if(gameOver || isPaused) return;
        
        // Cek Level Up
        if(score >= lastUpgradeScore + 1000) {{
            isPaused = true;
            lastUpgradeScore += 1000;
            currentLvl++;
            upMenu.style.display = "block";
            return;
        }}

        // Pet Logic
        if(player.hasPet) {{
            player.petAngle += 0.05;
            if(Math.random() < 0.05) {{ // Pet nembak otomatis
                let target = enemies[0] || boss;
                let a = target ? Math.atan2(target.y-player.y, target.x-player.x) : player.petAngle;
                fire(player.x + Math.cos(player.petAngle)*30, player.y + Math.sin(player.petAngle)*30, a, false, true, 3, '#ffff4d');
            }}
        }}

        let s = player.speed, nx=player.x, ny=player.y;
        if(keys['KeyW']) ny-=s; if(keys['KeyS']) ny+=s;
        if(keys['KeyA']) nx-=s; if(keys['KeyD']) nx+=s;
        if(nx > 0 && nx < 600) player.x=nx; if(ny > 0 && ny < 400) player.y=ny;

        player.sT = Math.min(100, player.sT + 0.2);
        uBar.style.width = player.sT + '%';

        bullets = bullets.filter(b => {{
            b.x += b.vx; b.y += b.vy;
            if(b.p) {{
                enemies.forEach((e, i) => {{
                    if(Math.hypot(e.x-b.x, e.y-b.y) < e.s/2+b.r) {{
                        e.hp -= b.d;
                        if(e.hp<=0) {{ score += 150; spawnExplosion(e.x, e.y, e.c); enemies.splice(i,1); }}
                        b.del = true;
                    }}
                }});
            }} else if(Math.hypot(player.x-b.x, player.y-b.y) < player.r+b.r && player.inv<=0) {{
                triggerRespawn(); return false;
            }}
            return !b.del && b.x>-50 && b.x<650 && b.y>-50 && b.y<450;
        }});

        if(enemies.length < 5) {{
            enemies.push({{ x: Math.random()*600, y: Math.random()*400, s: 20, hp: 10, c: '#e74c3c', sp: 1.2 }});
        }}
        enemies.forEach(e => {{ 
            let a = Math.atan2(player.y-e.y, player.x-e.x); 
            e.x += Math.cos(a)*e.sp; e.y += Math.sin(a)*e.sp; 
            if(Math.hypot(player.x-e.x, player.y-e.y) < player.r+e.s/2 && player.inv<=0) triggerRespawn();
        }});

        particles.forEach((p,i)=>{{ p.x+=p.vx; p.y+=p.vy; p.life--; if(p.life<=0) particles.splice(i,1); }});
        if(player.inv > 0) player.inv--;
        
        uScore.innerText = "Skor: " + score; 
        uHP.innerText = "❤️".repeat(Math.max(0,health));
        uLvl.innerText = "LEVEL: " + currentLvl;
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        particles.forEach(p => {{ ctx.fillStyle=p.c; ctx.globalAlpha=p.life/30; ctx.fillRect(p.x,p.y,3,3); ctx.globalAlpha=1; }});

        // Draw Pet
        if(player.hasPet) {{
            let px = player.x + Math.cos(player.petAngle)*35;
            let py = player.y + Math.sin(player.petAngle)*35;
            ctx.fillStyle = '#ffff4d';
            ctx.beginPath(); ctx.arc(px, py, 6, 0, 7); ctx.fill();
            ctx.strokeStyle = 'white'; ctx.stroke();
        }}

        // Draw Player
        if(player.inv <= 0 || (player.inv % 10 < 5)) {{
            let angle = Math.atan2(my - player.y, mx - player.x);
            ctx.save(); ctx.translate(player.x, player.y); ctx.rotate(angle);
            ctx.fillStyle = player.color;
            ctx.beginPath(); ctx.moveTo(18, 0); ctx.lineTo(-12, -12); ctx.lineTo(-7, 0); ctx.lineTo(-12, 12); ctx.closePath(); ctx.fill();
            // Flank Guard Visual
            if(player.hasFlank) {{
                ctx.fillRect(-15, -5, 10, 10);
            }}
            ctx.restore();
        }}
        if(gameOver) {{ ctx.fillStyle='white'; ctx.font='40px Arial'; ctx.textAlign='center'; ctx.fillText("GAME OVER", 300, 200); }}
    }}

    function loop() {{ 
        update(); 
        draw(); 
        if(!gameOver && !isPaused) requestAnimationFrame(loop); 
    }}
    loop();
}})();
</script>
"""

cp.html(game_html, height=600)
