import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Upgrade Sidebar", layout="centered")
st.title("⚔️ Island.io: Roket Launcher")

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
    {"n": "🔴 Assault", "col": "#ff0000", "hp": 3, "spd": 6.5, "t": "assault", "slot": c1},
    {"n": "🔵 Tank", "col": "#0000ff", "hp": 6, "spd": 4.5, "t": "tank", "slot": c2},
    {"n": "🟢 Scout", "col": "#00ff00", "hp": 2, "spd": 8.5, "t": "scout", "slot": c3},
    {"n": "🟣 Joker", "col": "#800080", "hp": 4, "spd": 6.5, "t": "joker", "slot": c4},
    {"n": "🟡 Bomber", "col": "#ffff00", "hp": 3, "spd": 6.0, "t": "bomber", "slot": c5},
    {"n": "🟠 Roket", "col": "#ffa500", "hp": 3, "spd": 6.5, "t": "roket", "slot": c6}
]

for cls in classes_data:
    with cls["slot"]:
        is_selected = st.session_state.char and st.session_state.char["type"] == cls["t"]
        style = f"text-align: center; color: {cls['col'] if not is_selected else '#444'}; font-weight: bold;"
        if is_selected:
            style += "filter: grayscale(100%); opacity: 0.3;"
            
        st.markdown(f"<div style='{style}'>{cls['n']}</div>", unsafe_allow_html=True)
        if st.button("Pilih", key=cls['t'], disabled=is_selected):
            st.session_state.char = {"hp": cls["hp"], "spd": cls["spd"], "col": cls["col"], "type": cls["t"]}
            st.rerun()

# --- GAME ENGINE ---
if st.session_state.char:
    p = st.session_state.char
    game_html = f"""
    <div id="game-container" style="position:relative; width:650px; margin:auto; font-family:sans-serif;">
        
        <div id="upgrade-history" style="position:absolute; left:-120px; top:50px; width:100px; background:rgba(255,255,255,0.1); border-radius:10px; padding:10px; color:rgba(255,255,255,0.5); font-size:12px; text-align:left; border:1px solid rgba(255,255,255,0.1);">
            <b style="color:rgba(255,255,255,0.8)">UPGRADES:</b><br>
            <div id="hist-list">Belum ada</div>
        </div>

        <div id="sidebar-upgrade" style="display:none; position:absolute; right:-160px; top:0; width:140px; background:#222; border:2px solid #ffd700; border-radius:10px; padding:10px; z-index:1000; box-shadow: 5px 0 15px rgba(0,0,0,0.5);">
            <h4 style="color:#ffd700; margin:0 0 10px 0; font-size:12px; text-align:center;">LEVEL UP!</h4>
            <button onclick="applyUpgrade('Speed', '#4deaff')" style="width:100%; margin-bottom:5px; background:#4deaff; border:none; cursor:pointer; font-weight:bold; border-radius:4px;">⚡ SPEED</button>
            <button onclick="applyUpgrade('Shield', '#ff4d4d')" style="width:100%; margin-bottom:5px; background:#ff4d4d; border:none; cursor:pointer; font-weight:bold; border-radius:4px;">🛡️ SHIELD</button>
            <button onclick="applyUpgrade('Damage', '#ffff4d')" style="width:100%; margin-bottom:10px; background:#ffff4d; border:none; cursor:pointer; font-weight:bold; border-radius:4px;">🔥 DMG</button>
            <hr style="border:0.5px solid #444">
            <button onclick="window.parent.location.reload()" style="width:100%; background:#fff; border:none; cursor:pointer; font-size:10px; border-radius:4px;">🔄 GANTI HERO</button>
        </div>

        <div style="background:#111; padding:15px; border-radius:15px; border: 4px solid #333;">
            <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom:10px;">
                <div id="ui-lvl">LVL: 1</div>
                <div id="ui-score">SKOR: 0</div>
                <div id="ui-hp">❤️❤️❤️</div>
            </div>
            <canvas id="g" width="600" height="400" style="background:#000; border: 1px solid #444;"></canvas>
        </div>
    </div>

    <script>
    (function() {{
        const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
        const upSidebar = document.getElementById('sidebar-upgrade');
        const histList = document.getElementById('hist-list');
        
        let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
        let lastUpgradeScore = 0, currentLvl = 1;
        let upgradesChosen = [];

        let player = {{ x: 300, y: 200, r: 12, speed: {p['spd']}, color: '{p['col']}', inv: 0 }};

        window.applyUpgrade = function(name, color) {{
            upgradesChosen.push(name);
            if(name === 'Speed') player.speed += 1;
            
            // Update Tampilan Transparan di Samping Kiri
            histList.innerHTML = upgradesChosen.map(u => `• ${{u}}`).join('<br>');
            
            upSidebar.style.display = "none";
            isPaused = false;
            requestAnimationFrame(loop);
        }};

        function update() {{
            if(gameOver || isPaused) return;

            // Trigger Level Up ke samping
            if(score >= lastUpgradeScore + 500) {{
                isPaused = true; 
                lastUpgradeScore += 500; 
                currentLvl++;
                upSidebar.style.display = "block";
                return;
            }}

            // Simulasi skor naik otomatis untuk demo
            score += 1;
            
            document.getElementById('ui-score').innerText = "SKOR: " + score;
            document.getElementById('ui-lvl').innerText = "LVL: " + currentLvl;
            document.getElementById('ui-hp').innerText = "❤️".repeat(health);
        }}

        function draw() {{
            ctx.clearRect(0,0,600,400);
            ctx.fillStyle = player.color;
            ctx.beginPath(); ctx.arc(player.x, player.y, player.r, 0, 7); ctx.fill();
            
            if(isPaused) {{
                ctx.fillStyle = "rgba(0,0,0,0.5)";
                ctx.fillRect(0,0,600,400);
                ctx.fillStyle = "white";
                ctx.textAlign = "center";
                ctx.fillText("PILIH UPGRADE DI SAMPING!", 300, 200);
            }}
        }}

        function loop() {{ update(); draw(); if(!gameOver && !isPaused) requestAnimationFrame(loop); }}
        loop();
    }})();
    </script>
    """
    cp.html(game_html, height=500, width=800)
