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

# --- MENU PILIH KARAKTER ---
if not st.session_state.char:
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
            st.markdown(f"<div style='text-align: center; color: {cls['col']}; font-weight: bold;'>{cls['n']}</div>", unsafe_allow_html=True)
            if st.button("Pilih " + cls['n'].split()[1], key=cls['t']):
                st.session_state.char = {"hp": cls["hp"], "spd": cls["spd"], "col": cls["col"], "type": cls["t"]}
                st.rerun()

# --- GAMEPLAY DENGAN PERBAIKAN DOUBLE BRACKET {{ }} ---
p = st.session_state.char
if p:
    game_html = f"""
    <div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; user-select: none;">
        <div id="up-ov" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:1000; border-radius:11px; flex-direction:column; justify-content:center; align-items:center;">
            <h2 style="color:#ffd700;">LEVEL UP!</h2>
            <button onclick="applyUp('speed')" style="width:200px; padding:12px; margin:5px; background:#4deaff; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">⚡ SPEED +0.5</button>
            <button onclick="applyUp('flank')" style="width:200px; padding:12px; margin:5px; background:#ff4d4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🛡️ FLANK GUARD</button>
            <button onclick="applyUp('pet')" style="width:200px; padding:12px; margin:5px; background:#ffff4d; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">🤖 DRONE PET</button>
        </div>

        <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
            <div id="ui-lvl">LEVEL: 1</div><div id="ui-score">Skor: 0</div><div id="ui-hp">❤️❤️❤️</div>
        </div>
        <div style="margin: 0 auto 10px; width: 250px;">
            <div style="width:100%; height:12px; background:#333; border-radius:6px; overflow:hidden; border: 1px solid #555;">
                <div id="skill-bar" style="width:0%; height:100%; background: {p['col']};"></div>
            </div>
        </div>
        <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333;"></canvas>
        <div id="restart-btn" style="display:none; position:absolute; top:50%; left:50%; transform:translate(-50%, -50%);">
            <button onclick="parent.window.location.reload()" style="padding:15px; background:#e74c3c; color:white; border:none; border-radius:10px; cursor:pointer;">KEMBALI KE MENU</button>
        </div>
    </div>

    <script>
    (function() {{
        const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
        const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'), uBar = document.getElementById('skill-bar'), upOv = document.getElementById('up-ov');

        let score = 0, health = {p['hp']}, gameOver = false, isPaused = false;
        let keys = {{}}, bullets = [], enemies = [], particles = [], items = [], boss = null;
        let lastUpgradeScore = 0, lastBossThreshold = 0;

        let player = {{
            x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
            type: '{p['type']}', color: '{p['col']}', sT: 0, sM: 100, kills: 0, inv: 0,
            hasFlank: false, hasPet: false, petAngle: 0
        }};

        window.applyUp = function(t) {{
            if(t==='speed') player.baseSpeed += 0.5;
            if(t==='flank') player.hasFlank = true;
            if(t==='pet') player.hasPet = true;
            upOv.style.display = 'none'; isPaused = false; requestAnimationFrame(loop);
        }};

        function spawnExplosion(x,y,c,count=15) {{ for(let i=0;i<count;i++) particles.push({{x,y,vx:(Math.random()-0.5)*10,vy:(Math.random()-0.5)*10,life:30,c}}); }}
        
        function spawnItem(x, y) {{
            if(Math.random() < 0.25) {{
                let r = Math.random();
                items.push({{ x, y, type: r<0.3?'med':'boost', c: r<0.3?'#ff4d4d':'#4deaff', label: r<0.3?'✚':'⚡' }});
            }}
        }}

        window.onkeydown = e => keys[e.code] = true;
        window.onkeyup = e => keys[e.code] = false;
        let mx=0, my=0; canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};
        
        canvas.onmousedown = () => {{ 
            if(!isPaused && !gameOver) fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), true, 5); 
            if(player.hasFlank && !isPaused && !gameOver) fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x)+Math.PI, true, 5); 
        }};

        function fire(x,y,a,p,d,rk=false) {{ bullets.push({{x,y,vx:Math.cos(a)*12,vy:Math.sin(a)*12,r:rk?10:4,c:p?player.color:'#F00',p,d,rk,target:null}}); }}

        function useUlt() {{
            if(player.sT < player.sM || isPaused) return;
            player.sT = 0; player.kills = 0;
            if(player.type === 'roket') {{ for(let i=0; i<6; i++) fire(player.x, player.y, (Math.PI*2/6)*i, true, 150, true); }}
            else if(player.type === 'bomber') {{ enemies.forEach(e => {{ if(Math.hypot(e.x-player.x, e.y-player.y)<300) e.hp-=500; }}); spawnExplosion(player.x, player.y, '#ff0', 50); }}
        }}
        window.addEventListener('keydown', e => {{ if(e.code==='Space') useUlt(); }});

        function update() {{
            if(gameOver || isPaused) return;

            if(score >= lastUpgradeScore + 1000) {{ isPaused = true; lastUpgradeScore += 1000; upOv.style.display='flex'; return; }}

            let s = player.baseSpeed;
            if(keys['KeyW'] && player.y > 15) player.y -= s;
            if(keys['KeyS'] && player.y < 385) player.y += s;
            if(keys['KeyA'] && player.x > 15) player.x -= s;
            if(keys['KeyD'] && player.x < 585) player.x += s;

            if(player.type === 'roket') player.sT = (player.kills/8)*100;
            else player.sT = Math.min(100, player.sT + 0.2);
            uBar.style.width = player.sT + "%";

            if(player.hasPet) {{ player.petAngle += 0.05; if(Math.random()<0.03) fire(player.x+Math.cos(player.petAngle)*35, player.y+Math.sin(player.petAngle)*35, player.petAngle, true, 5); }}

            items = items.filter(it => {{
                if(Math.hypot(player.x-it.x, player.y-it.y) < 25) {{ if(it.type==='med') health=Math.min(10,health+1); return false; }}
                return true;
            }});

            bullets = bullets.filter(b => {{
                b.x += b.vx; b.y += b.vy;
                if(b.rk) {{ 
                    let t = boss || enemies[0]; 
                    if(t){{ let a=Math.atan2(t.y-b.y, t.x-b.x); b.vx+=Math.cos(a)*0.8; b.vy+=Math.sin(a)*0.8; }} 
                }}
                if(b.p) {{
                    if(boss && Math.hypot(b.x-boss.x, b.y-boss.y)<boss.s){{ boss.hp-=b.d; return false; }}
                    for(let i=enemies.length-1; i>=0; i--) {{
                        let e = enemies[i];
                        if(Math.hypot(b.x-e.x, b.y-e.y)<e.s) {{ 
                            e.hp-=b.d; 
                            if(e.hp<=0){{ player.kills++; score+=e.val; spawnItem(e.x,e.y); spawnExplosion(e.x,e.y,e.c); enemies.splice(i,1); }}
                            return false;
                        }}
                    }}
                }} else {{
                    if(Math.hypot(b.x-player.x, b.y-player.y)<player.r && player.inv<=0){{ health--; player.inv=120; if(health<=0) gameOver=true; return false; }}
                }}
                return b.x>0 && b.x<600 && b.y>0 && b.y<400;
            }});

            if(!boss && enemies.length < 8) {{
                let ex, ey; do {{ ex=Math.random()*600; ey=Math.random()*400; }} while(Math.hypot(ex-player.x, ey-player.y)<200);
                let r=Math.random();
                let type = r<0.2?{{c:'#2ecc71',hp:15,val:15,sp:0.6,s:30}}: (r<0.5?{{c:'#9b59b6',hp:5,val:10,sp:1.8,s:15}}:{{c:'#e74c3c',hp:5,val:5,sp:1.2,s:22}});
                enemies.push({{x:ex, y:ey, ...type}});
            }}
            enemies.forEach(e => {{
                let a = Math.atan2(player.y-e.y, player.x-e.x);
                e.x += Math.cos(a)*e.sp; e.y += Math.sin(a)*e.sp;
                if(Math.hypot(player.x-e.x, player.y-e.y)<player.r+e.s/2 && player.inv<=0){{ health--; player.inv=120; if(health<=0) gameOver=true; }}
            }});

            if(score>=lastBossThreshold+1000 && !boss) boss={{x:300,y:-50,s:50,hp:2000,mH:2000,c:'#800000',sp:1}};
            if(boss){{ 
                let a=Math.atan2(player.y-boss.y, player.x-boss.x); boss.x+=Math.cos(a)*boss.sp; boss.y+=Math.sin(a)*boss.sp;
                if(boss.hp<=0){{ score+=500; lastBossThreshold+=1000; boss=null; }}
            }}

            particles.forEach((p,i) => {{ p.life--; if(p.life<=0) particles.splice(i,1); }});
            if(player.inv>0) player.inv--;
            uScore.innerText = "Skor: " + score; uHP.innerText = "❤️".repeat(health);
            if(gameOver) document.getElementById('restart-btn').style.display='block';
        }}

        function draw() {{
            ctx.clearRect(0,0,600,400);
            items.forEach(it=>{{ ctx.fillStyle=it.c; ctx.beginPath(); ctx.arc(it.x,it.y,8,0,7); ctx.fill(); }});
            bullets.forEach(b=>{{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
            enemies.forEach(e=>{{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
            if(boss){{ ctx.fillStyle=boss.c; ctx.beginPath(); ctx.arc(boss.x,boss.y,boss.s,0,7); ctx.fill(); }}
            if(player.hasPet){{ ctx.fillStyle='#ffff4d'; ctx.beginPath(); ctx.arc(player.x+Math.cos(player.petAngle)*35, player.y+Math.sin(player.petAngle)*35, 6,0,7); ctx.fill(); }}
            particles.forEach(p=>{{ ctx.fillStyle=p.c; ctx.globalAlpha=p.life/30; ctx.fillRect(p.x,p.y,3,3); ctx.globalAlpha=1; }});
            
            if(player.inv<=0 || player.inv%10<5){{
                ctx.save(); ctx.translate(player.x, player.y); ctx.rotate(Math.atan2(my-player.y, mx-player.x));
                ctx.fillStyle=player.color; ctx.beginPath(); ctx.moveTo(18,0); ctx.lineTo(-12,-12); ctx.lineTo(-7,0); ctx.lineTo(-12,12); ctx.fill();
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
