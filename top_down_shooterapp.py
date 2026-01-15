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

# --- MENU PILIH KARAKTER ---
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
        # Logika Bayangan: Jika hero ini sedang dipilih, buat jadi grayscale
        is_selected = st.session_state.char and st.session_state.char["type"] == cls["t"]
        
        style = f"text-align: center; color: {cls['col'] if not is_selected else '#555'}; font-weight: bold;"
        if is_selected:
            style += "filter: grayscale(100%); opacity: 0.5;"
            
        st.markdown(f"<div style='{style}'>{cls['n']} {'(AKTIF)' if is_selected else ''}</div>", unsafe_allow_html=True)
        
        if st.button("Pilih " + cls['n'].split()[1], key=cls['t'], disabled=is_selected):
            st.session_state.char = {"hp": cls["hp"], "spd": cls["spd"], "col": cls["col"], "type": cls["t"]}
            st.rerun()
            
        st.caption(cls["stat"])
        st.write("---")

# --- GAMEPLAY MODAL (Hanya muncul jika char dipilih) ---
if st.session_state.char:
    p = st.session_state.char
    game_html = f"""
    <div id="game-overlay" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); z-index:9999; display:flex; justify-content:center; align-items:center;">
        <div style="text-align:center; background:#111; padding:20px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; width: 650px;">
            
            <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
                <div id="ui-lvl">LEVEL: 1</div>
                <div id="ui-score">Skor: 0</div>
                <div id="ui-hp">❤️❤️❤️</div>
            </div>

            <div id="upgrade-menu" style="display:none; position:absolute; top:50px; left:50%; transform:translateX(-50%); background:rgba(25,25,25,0.98); padding:15px; border:3px solid #ffd700; border-radius:12px; width:90%; z-index:10000; box-shadow: 0 5px 20px rgba(0,0,0,0.8);">
                <h3 style="color:#ffd700; margin:0 0 10px 0; font-size:16px;">LEVEL UP! PILIH UPGRADE:</h3>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px;">
                    <button onclick="applyUpgrade('speed')" style="padding:10px; background:#4deaff; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">⚡ SPEED +0.5</button>
                    <button onclick="applyUpgrade('flank')" style="padding:10px; background:#ff4d4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🛡️ FLANK GUARD</button>
                    <button onclick="applyUpgrade('pet')" style="padding:10px; background:#ffff4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🤖 DRONE PET</button>
                    <button onclick="window.parent.location.reload()" style="padding:10px; background:#ffffff; color:black; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🔄 GANTI HERO</button>
                </div>
            </div>

            <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
            
            <div id="restart-btn" style="display:none; margin-top:10px;">
                <button onclick="window.parent.location.reload()" style="padding:10px 20px; font-weight:bold; color:white; background:#e74c3c; border:none; border-radius:5px; cursor:pointer;">KEMBALI KE MENU</button>
            </div>
        </div>
    </div>

    <script>
    (function() {{
        const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
        const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'), uLvl = document.getElementById('ui-lvl');
        const upMenu = document.getElementById('upgrade-menu'), rBtn = document.getElementById('restart-btn');

        let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
        let keys = {{}}, bullets = [], enemies = [], particles = [], items = [], boss = null;
        let lastUpgradeScore = 0, currentLvl = 1;
        
        let player = {{
            x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
            type: '{p['type']}', color: '{p['col']}',
            sT: 0, sM: 100, shield: false, dmg: 5, inv: 0, kills: 0, 
            tripleShot: 0, energyTime: 0, hasFlank: false, hasPet: false, petAngle: 0
        }};

        window.applyUpgrade = function(type) {{
            if(type === 'speed') {{ player.baseSpeed += 0.5; player.speed = player.baseSpeed; }}
            if(type === 'flank') {{ player.hasFlank = true; }}
            if(type === 'pet') {{ player.hasPet = true; }}
            upMenu.style.display = "none";
            isPaused = false;
            requestAnimationFrame(loop);
        }};

        function spawnItem(x, y) {{
            if(Math.random() < 0.25) {{
                let r = Math.random();
                if(r < 0.3) items.push({{ x, y, type: 'medkit', c: '#ff4d4d', label: '✚' }});
                else if(r < 0.6) items.push({{ x, y, type: 'energy', c: '#4deaff', label: '⚡' }});
                else items.push({{ x, y, type: 'triple', c: '#ffff4d', label: 'Ⅲ' }});
            }}
        }}

        function triggerRespawn() {{
            health--;
            player.inv = 120;
            if(health <= 0) {{ gameOver = true; rBtn.style.display = "block"; }}
        }}

        window.onkeydown = e => keys[e.code] = true;
        window.onkeyup = e => keys[e.code] = false;
        let mx=0, my=0;
        canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

        canvas.onmousedown = () => {{ 
            if(gameOver || isPaused) return;
            fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), false, true);
        }};

        function fire(x, y, a, isSpecial, isPlayer) {{
            bullets.push({{ x, y, vx: Math.cos(a)*15, vy: Math.sin(a)*15, r: 5, c: isPlayer?player.color:'#F00', p: isPlayer }});
        }}

        function update() {{
            if(gameOver || isPaused) return;
            
            if(score >= lastUpgradeScore + 1000) {{
                isPaused = true; lastUpgradeScore += 1000; currentLvl++;
                upMenu.style.display = "block"; return;
            }}

            // Item Pickup Logic
            for(let i=items.length-1; i>=0; i--) {{
                if(Math.hypot(player.x-items[i].x, player.y-items[i].y) < 25) {{
                    if(items[i].type==='medkit') health++;
                    items.splice(i,1);
                }}
            }}

            let s = player.speed;
            if(keys['KeyW']) player.y-=s; if(keys['KeyS']) player.y+=s;
            if(keys['KeyA']) player.x-=s; if(keys['KeyD']) player.x+=s;

            bullets = bullets.filter(b => {{
                b.x += b.vx; b.y += b.vy;
                if(!b.p && Math.hypot(player.x-b.x, player.y-b.y) < 15 && player.inv <= 0) {{ triggerRespawn(); return false; }}
                if(b.p) {{
                    enemies.forEach((e, ei) => {{
                        if(Math.hypot(e.x-b.x, e.y-b.y) < 20) {{ e.hp -= 5; if(e.hp<=0) {{ score+=20; spawnItem(e.x,e.y); enemies.splice(ei,1); }} }}
                    }});
                }}
                return b.x > 0 && b.x < 600 && b.y > 0 && b.y < 400;
            }});

            if(enemies.length < 5) enemies.push({{ x: Math.random()*600, y: Math.random()*400, hp: 10, c: '#e74c3c' }});
            
            enemies.forEach(e => {{
                let a = Math.atan2(player.y-e.y, player.x-e.x);
                e.x += Math.cos(a)*1.5; e.y += Math.sin(a)*1.5;
                if(Math.hypot(player.x-e.x, player.y-e.y) < 20 && player.inv <= 0) triggerRespawn();
            }});

            if(player.inv > 0) player.inv--;
            uScore.innerText = "Skor: " + score; uHP.innerText = "❤️".repeat(Math.max(0,health));
        }}

        function draw() {{
            ctx.clearRect(0,0,600,400);
            items.forEach(it => {{ ctx.fillStyle=it.c; ctx.beginPath(); ctx.arc(it.x,it.y,8,0,7); ctx.fill(); }});
            bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
            enemies.forEach(e => {{ ctx.fillStyle=e.c; ctx.fillRect(e.x-10, e.y-10, 20, 20); }});
            
            if(player.inv <= 0 || player.inv % 10 < 5) {{
                ctx.fillStyle = player.color;
                ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, 7); ctx.fill();
            }}
            if(gameOver) {{ ctx.fillStyle='white'; ctx.font='30px Arial'; ctx.fillText("GAME OVER", 220, 200); }}
        }}

        function loop() {{ update(); draw(); if(!gameOver && !isPaused) requestAnimationFrame(loop); }}
        loop();
    }})();
    </script>
    """
    cp.html(game_html, height=600)
