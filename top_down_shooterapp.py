import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: 6 Classes", layout="centered")
st.title("⚔️ Island.io: Arrow Glow - 6 Classes")

if "char" not in st.session_state:
    st.session_state.char = None

# Grid untuk 6 Karakter
st.write("### Pilih Hero Anda:")
c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

# Karakter dipercepat: spd dinaikkan secara signifikan
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
        if st.button(cls["n"]):
            st.session_state.char = {"hp": cls["hp"], "spd": cls["spd"], "col": cls["col"], "type": cls["t"]}

if not st.session_state.char:
    st.info("Pilih Class untuk bertarung!")
    st.stop()

# Masukkan logika game ke HTML/JavaScript
p = st.session_state.char
game_html = f"""
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
    <div id="buff-ui" style="color:#f1c40f; font-size:12px; font-weight:bold; min-height:15px; margin-bottom:5px;"></div>

    <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
</div>

<script>
(function() {{
    const canvas = document.getElementById('g'), ctx = canvas.getContext('2d');
    const uScore = document.getElementById('ui-score'), uHP = document.getElementById('ui-hp'),
          uBar = document.getElementById('skill-bar'), uBuff = document.getElementById('buff-ui');

    let score = 0, health = {p['hp']}, level = 1, gameOver = false;
    let keys = {{}}, bullets = [], enemies = [], walls = [], particles = [], boss = null;
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, shield: false,
        dmg: 5, inv: 0, kills: 0
    }};

    function spawnExplosion(x, y, color, count=15) {{
        for(let i=0; i<count; i++) particles.push({{x,y,vx:(Math.random()-0.5)*10, vy:(Math.random()-0.5)*10, life:25, c:color}});
    }}

    function triggerRespawn() {{
        health--;
        spawnExplosion(player.x, player.y, "#ffffff");
        player.inv = 180;
        if(health <= 0) gameOver = true;
    }}

    window.onkeydown = e => {{ keys[e.code] = true; if(e.code==='Space') useUlt(); }};
    window.onkeyup = e => {{ keys[e.code] = false; }};
    let mx=0, my=0;
    canvas.onmousemove = e => {{ const r = canvas.getBoundingClientRect(); mx=e.clientX-r.left; my=e.clientY-r.top; }};

    function useUlt(forcedType = null) {{
        let type = forcedType || player.type;
        if(!forcedType && (player.sT < player.sM || gameOver)) return;
        
        if(!forcedType) {{ player.sT = 0; player.kills = 0; }}

        if(type === 'tank') {{
            player.shield = true;
            let shots = 0;
            let interval = setInterval(() => {{
                for(let a=0; a<Math.PI*2; a+=Math.PI/6) fire(player.x, player.y, a, false, true);
                shots++;
                if(shots >= 3) clearInterval(interval);
            }}, 500);
            setTimeout(() => player.shield = false, 10000);
        }} 
        else if(type === 'scout') {{
            let a = Math.atan2(my-player.y, mx-player.x);
            player.x += Math.cos(a)*150; player.y += Math.sin(a)*150;
            player.inv = 180; 
            spawnExplosion(player.x, player.y, player.color);
        }}
        else if(type === 'bomber') {{
            spawnExplosion(player.x, player.y, "#ffff00", 60);
            enemies.forEach(e => {{
                if(Math.hypot(e.x-player.x, e.y-player.y) < 180) e.hp -= 200;
            }});
            if(boss && Math.hypot((boss.x+40)-player.x, (boss.y+40)-player.y) < 180) boss.hp -= 500;
        }}
        else if(type === 'roket') {{
            for(let i=0; i<5; i++) {{
                let target = enemies.length > 0 ? enemies[Math.floor(Math.random()*enemies.length)] : null;
                bullets.push({{ x: player.x, y: player.y, vx: 0, vy: 0, r: 8, c: '#ff0000', p: true, rk: true, target: target, life: 200 }});
            }}
        }}
        else if(type === 'assault') {{
            for(let i=0; i<15; i++) setTimeout(()=>fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), true, true), i*80);
        }}
        else if(type === 'joker') {{
            const pool = ['tank', 'scout', 'bomber', 'roket', 'assault'];
            useUlt(pool[Math.floor(Math.random()*pool.length)]);
        }}
    }}

    canvas.onmousedown = () => {{
        if(gameOver) return;
        fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), false, true);
    }};

    function fire(x, y, a, isRocket, isPlayer) {{
        let ox = x + Math.cos(a) * 20;
        let oy = y + Math.sin(a) * 20;
        // Peluru dipercepat: multiplier dinaikkan (dari 12:9 ke 18:15)
        bullets.push({{ x:ox, y:oy, vx: Math.cos(a)*(isRocket?18:15), vy: Math.sin(a)*(isRocket?18:15), r: isRocket?8:4, c: isPlayer?player.color:'#F00', p: isPlayer, rk: isRocket }});
    }}

    function update() {{
        if(gameOver) return;
        
        let s = player.speed;
        let nx=player.x, ny=player.y;
        if(keys['KeyW']) ny-=s; if(keys['KeyS']) ny+=s;
        if(keys['KeyA']) nx-=s; if(keys['KeyD']) nx+=s;
        if(nx > 0 && nx < 600) player.x=nx;
        if(ny > 0 && ny < 400) player.y=ny;

        if(player.type === 'tank' || player.type === 'bomber') player.sT = Math.min(100, player.sT + (100/(15*60)));
        else if(player.type === 'scout') player.sT = Math.min(100, player.sT + (100/(10*60)));
        else if(player.type === 'roket') player.sT = (player.kills/10)*100;
        else if(player.type === 'joker') player.sT = (player.kills/15)*100;
        else if(player.type === 'assault') player.sT = Math.min(100, player.sT + 0.1);

        uBar.style.width = Math.min(100, player.sT) + '%';

        bullets = bullets.filter(b => {{
            if(b.target && b.target.hp > 0) {{
                let a = Math.atan2(b.target.y-b.y, b.target.x-b.x);
                b.vx = Math.cos(a)*10; b.vy = Math.sin(a)*10;
            }}
            b.x += b.vx; b.y += b.vy;
            
            if(b.p) {{
                for(let e of enemies) {{
                    if(Math.hypot(e.x-b.x, e.y-b.y) < e.s/2+b.r) {{
                        e.hp -= b.rk?100:player.dmg;
                        if(e.hp<=0) {{ 
                            player.kills++; score += 10;
                            enemies.splice(enemies.indexOf(e), 1); 
                        }}
                        return false;
                    }}
                }}
                if(boss && b.x > boss.x && b.x < boss.x+boss.w && b.y > boss.y && b.y < boss.y+boss.h) {{
                    boss.hp -= player.dmg; return false;
                }}
            }} else {{
                if(Math.hypot(player.x-b.x, player.y-b.y) < player.r+b.r) {{
                    if(player.inv<=0 && !player.shield) triggerRespawn();
                    return false;
                }}
            }}
            return b.x>0 && b.x<600 && b.y>0 && b.y<400;
        }});

        enemies.forEach(e => {{
            let a = Math.atan2(player.y-e.y, player.x-e.x);
            e.x += Math.cos(a)*e.sp; e.y += Math.sin(a)*e.sp;
            if(Math.hypot(player.x-e.x, player.y-e.y) < player.r+e.s/2 && player.inv<=0 && !player.shield) triggerRespawn();
        }});

        if(score >= 300 && !boss) boss = {{x:250, y:50, w:80, h:80, hp:1000, mH:1000}};

        if(enemies.length < 6) {{
            enemies.push({{x:Math.random()*600, y:Math.random()*400, s:20, sp:1.2, hp:10}});
        }}

        particles.forEach((p,i)=>{{ p.x+=p.vx; p.y+=p.vy; p.life--; if(p.life<=0) particles.splice(i,1); }});
        if(player.inv > 0) player.inv--;
        uScore.innerText = "Skor: " + score;
        uHP.innerText = "❤️".repeat(Math.max(0,health));
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        bullets.forEach(b => {{ ctx.fillStyle=b.c; ctx.beginPath(); ctx.arc(b.x,b.y,b.r,0,7); ctx.fill(); }});
        enemies.forEach(e => {{ ctx.fillStyle='#e74c3c'; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); }});
        particles.forEach(p => {{ ctx.fillStyle=p.c; ctx.globalAlpha=p.life/25; ctx.fillRect(p.x,p.y,3,3); ctx.globalAlpha=1; }});
        if(boss) {{
            ctx.fillStyle='#ff4d4d'; ctx.fillRect(boss.x, boss.y, boss.w, boss.h);
            ctx.fillStyle='#f00'; ctx.fillRect(boss.x, boss.y-12, (boss.hp/boss.mH)*boss.w, 8);
        }}
        
        if(player.inv <= 0 || (player.inv % 10 < 5)) {{
            let angle = Math.atan2(my - player.y, mx - player.x);
            ctx.save();
            ctx.translate(player.x, player.y);
            ctx.rotate(angle);
            ctx.shadowBlur = 15; ctx.shadowColor = player.color; ctx.fillStyle = player.color;
            ctx.beginPath();
            ctx.moveTo(18, 0); ctx.lineTo(-12, -12); ctx.lineTo(-7, 0); ctx.lineTo(-12, 12);
            ctx.closePath(); ctx.fill();
            ctx.restore();
            if(player.shield) {{ 
                ctx.strokeStyle='#00e5ff'; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(player.x,player.y,25,0,7); ctx.stroke();
            }}
        }}
        if(gameOver) {{ ctx.fillStyle='white'; ctx.font='40px Arial'; ctx.textAlign='center'; ctx.fillText("GAME OVER", 300, 200); }}
    }}

    function loop() {{ update(); draw(); if(!gameOver) requestAnimationFrame(loop); }}
    loop();
}})();
</script>
"""

cp.html(game_html, height=600)
