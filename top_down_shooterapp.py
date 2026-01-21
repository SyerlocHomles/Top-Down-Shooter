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
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative; font-family: sans-serif; user-select: none;">
    <div style="display:flex; justify-content: space-between; color:white; font-weight:bold; margin-bottom: 10px;">
        <div id="ui-stage">STAGE: 1-1</div>
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">❤️❤️❤️</div>
    </div>
    
    <div id="item-ui" style="position: absolute; left: 20px; bottom: 20px; text-align: left; pointer-events: none;">
        <div id="energy-status" style="display:none; color:#4deaff; font-size:12px; font-weight:bold; margin-bottom:5px;">⚡ SPEED BOOST: <span id="energy-timer">0.0</span>s</div>
        <div id="triple-status" style="display:none; color:#ffff4d; font-size:12px; font-weight:bold;">Ⅲ TRIPLE SHOT: <span id="triple-count">0</span></div>
    </div>

    <div style="margin: 0 auto 10px; width: 250px;">
        <div id="ui-skill-text" style="color:{p['col']}; font-size: 11px; font-weight:bold; text-transform: uppercase;">{p['type']} ULTIMATE</div>
        <div style="width:100%; height:12px; background:#333; border-radius:6px; overflow:hidden; border: 1px solid #555;">
            <div id="skill-bar" style="width:0%; height:100%; background: {p['col']}; box-shadow: 0 0 10px {p['col']};"></div>
        </div>
    </div>

    <canvas id="g" width="600" height="400" style="background:#050505; border: 2px solid #333; border-radius:5px; cursor: crosshair;"></canvas>
    
    <div id="stage-transition" style="display:none; position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); background:rgba(0,0,0,0.9); padding:30px 60px; border-radius:15px; border: 3px solid #FFD700; z-index:100;">
        <div id="transition-text" style="font-size:32px; font-weight:bold; color:#FFD700; text-shadow: 0 0 20px #FFD700;"></div>
        <div id="transition-subtitle" style="font-size:16px; color:#FFF; margin-top:10px;"></div>
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
          uBar = document.getElementById('skill-bar'), uStage = document.getElementById('ui-stage');
    const energyUI = document.getElementById('energy-status'), energyTimer = document.getElementById('energy-timer');
    const tripleUI = document.getElementById('triple-status'), tripleCount = document.getElementById('triple-count');
    const rBtn = document.getElementById('restart-btn');
    const transitionEl = document.getElementById('stage-transition');
    const transitionText = document.getElementById('transition-text');
    const transitionSubtitle = document.getElementById('transition-subtitle');

    let score = 0, health = {p['hp']}, gameOver = false;
    let keys = {{}}, bullets = [], enemies = [], particles = [], bosses = [], items = [];
    
    // STAGE SYSTEM
    let chapter = 1, stage = 1; // 1-1, 1-2, 1-3
    let stageState = 'combat'; // 'combat', 'transition', 'boss'
    let transitionTimer = 0;
    let nextStageScore = 1000;
    
    let player = {{
        x: 300, y: 200, r: 12, speed: {p['spd']}, baseSpeed: {p['spd']},
        type: '{p['type']}', color: '{p['col']}',
        sT: 0, sM: 100, shield: false,
        dmg: 5, inv: 0, kills: 0, 
        tripleShot: 0, energyTime: 0
    }};

    function spawnExplosion(x, y, color, count=15) {{
        for(let i=0; i<count; i++) particles.push({{
            x, y, vx: (Math.random()-0.5)*15, vy: (Math.random()-0.5)*15, life: Math.random()*30+10, c: color
        }});
    }}

    function spawnItem(x, y) {{
        let r = Math.random();
        if(r < 0.3) {{
            let type = Math.random();
            if(type < 0.3) items.push({{ x, y, type: 'medkit', c: '#ff4d4d', label: '✚' }});
            else if(type < 0.6) items.push({{ x, y, type: 'energy', c: '#4deaff', label: '⚡' }});
            else items.push({{ x, y, type: 'triple', c: '#ffff4d', label: 'Ⅲ' }});
        }}
    }}

    function triggerRespawn() {{
        health--;
        spawnExplosion(player.x, player.y, "#ffffff");
        player.inv = 180;
        if(health <= 0) {{ gameOver = true; rBtn.style.display = "block"; }}
    }}

    function drawHexagon(x, y, size, color, outline=false) {{
        ctx.fillStyle = color; 
        if(outline) {{ ctx.strokeStyle = outline; ctx.lineWidth = 3; }}
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {{ 
            ctx.lineTo(x + size * Math.cos(i * Math.PI / 3), y + size * Math.sin(i * Math.PI / 3)); 
        }}
        ctx.closePath(); 
        ctx.fill();
        if(outline) ctx.stroke();
    }}

    function showTransition(title, subtitle, duration=180) {{
        transitionEl.style.display = 'block';
        transitionText.innerText = title;
        transitionSubtitle.innerText = subtitle;
        transitionTimer = duration;
        player.inv = duration;
        enemies = [];
        bullets = bullets.filter(b => b.p); // Clear enemy bullets
    }}

    function spawnMiniBoss(enhanced=false) {{
        let hp = enhanced ? 1200 : 800;
        let speed = enhanced ? 1.3 : 1.0;
        let type = enhanced ? 'enhanced' : 'basic';
        
        bosses.push({{
            x: 300, y: -50, s: 35, hp: hp, mH: hp, 
            c: '#9b59b6', sp: speed, 
            shieldActive: false, shieldTimer: 0, nextShield: 600,
            fireRate: enhanced ? 30 : 60, fireTimer: 0,
            dashTimer: enhanced ? 600 : 0, dashCooldown: enhanced ? 600 : 0,
            type: 'mini', variant: type,
            summonTimer: 0
        }});
    }}

    function spawnMainBoss() {{
        bosses.push({{
            x: 300, y: -50, s: 60, hp: 3000, mH: 3000,
            c: '#8B0000', sp: 0.8,
            shieldActive: false, shieldTimer: 0, nextShield: 800,
            fireRate: 40, fireTimer: 0,
            summonTimer: 300, summonCooldown: 600,
            type: 'main', phase: 1,
            glowPhase: 0
        }});
    }}

    function advanceStage() {{
        stage++;
        if(stage > 3) {{
            stage = 1;
            chapter++;
            showTransition(`CHAPTER ${{chapter}}`, 'NEW WORLD UNLOCKED!', 240);
        }} else {{
            if(stage === 3) {{
                showTransition(`⚠️ STAGE ${{chapter}}-${{stage}} ⚠️`, 'BOSS INCOMING!', 240);
            }} else {{
                showTransition(`STAGE ${{chapter}}-${{stage}}`, 'GET READY!', 180);
            }}
        }}
        
        // Stage completion rewards
        if(stage === 1) {{ 
            health = Math.min(health + 3, 10); 
            spawnItem(300, 200);
        }} else {{
            health = Math.min(health + 1, 10);
        }}
        
        nextStageScore = score + 1000;
        stageState = 'transition';
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
                for(let a=0; a<Math.PI*2; a+=Math.PI/6) fire(player.x, player.y, a, false, true, 80); 
                shots++; if(shots >= 3) clearInterval(interval);
            }}, 500);
            setTimeout(() => player.shield = false, 10000);
        }} 
        else if(type === 'scout') {{
            if(bosses.length > 0) {{
                let boss = bosses[0];
                let angleToBoss = Math.atan2(boss.y - player.y, boss.x - player.x);
                player.x = boss.x + Math.cos(angleToBoss) * 40; 
                player.y = boss.y + Math.sin(angleToBoss) * 40;
                player.inv = 120; 
                if(!boss.shieldActive) boss.hp -= 400; 
                spawnExplosion(boss.x, boss.y, "#00ff00", 40);
            }} else {{
                let a = Math.atan2(my-player.y, mx-player.x);
                player.x += Math.cos(a)*150; player.y += Math.sin(a)*150;
                player.inv = 60; spawnExplosion(player.x, player.y, player.color);
            }}
        }}
        else if(type === 'bomber') {{
            let radius = 350; 
            spawnExplosion(player.x, player.y, "#ffff00", 150); 
            enemies.forEach(e => {{ if(Math.hypot(e.x-player.x, e.y-player.y) < radius) e.hp -= 500; }});
            bosses.forEach(b => {{ 
                if(Math.hypot(b.x-player.x, b.y-player.y) < radius && !b.shieldActive) b.hp -= 800; 
            }});
        }}
        else if(type === 'roket') {{
            for(let i=0; i<6; i++) {{
                let startAngle = (Math.PI * 2 / 6) * i;
                bullets.push({{ 
                    x: player.x, y: player.y, 
                    vx: Math.cos(startAngle)*5, vy: Math.sin(startAngle)*5, 
                    r: 10, c: '#ffa500', p: true, rk: true, target: null, life: 300, d: 150 
                }});
            }}
        }}
        else if(type === 'assault') {{
            for(let i=0; i<15; i++) 
                setTimeout(()=>fire(player.x, player.y, Math.atan2(my-player.y, mx-player.x), true, true, 40), i*80);
        }}
        else if(type === 'joker') {{
            const pool = ['tank', 'scout', 'bomber', 'roket', 'assault'];
            useUlt(pool[Math.floor(Math.random()*pool.length)]);
        }}
    }}

    canvas.onmousedown = () => {{ 
        if(gameOver) return;
        let a = Math.atan2(my-player.y, mx-player.x);
        fire(player.x, player.y, a, false, true, player.dmg);
        if(player.tripleShot > 0) {{
            fire(player.x, player.y, a + 0.2, false, true, player.dmg);
            fire(player.x, player.y, a - 0.2, false, true, player.dmg);
            player.tripleShot--;
        }}
    }};

    function fire(x, y, a, isSpecial, isPlayer, damageValue) {{
        let ox = x + Math.cos(a) * 20, oy = y + Math.sin(a) * 20;
        bullets.push({{ 
            x:ox, y:oy, 
            vx: Math.cos(a)*(isSpecial?18:15), vy: Math.sin(a)*(isSpecial?18:15), 
            r: isSpecial?8:4, c: isPlayer?player.color:'#F00', 
            p: isPlayer, rk: false, d: damageValue || player.dmg 
        }});
    }}

    function update() {{
        if(gameOver) return;
        
        // Transition State
        if(stageState === 'transition') {{
            transitionTimer--;
            if(transitionTimer <= 0) {{
                transitionEl.style.display = 'none';
                stageState = 'combat';
                
                // Spawn boss based on stage
                if(stage === 1 || stage === 2) {{
                    spawnMiniBoss(stage === 2);
                }} else if(stage === 3) {{
                    spawnMainBoss();
                }}
            }}
            return;
        }}
        
        // Update Energy Item Duration
        if(player.energyTime > 0) {{
            player.energyTime--;
            player.speed = player.baseSpeed * 1.5;
            energyUI.style.display = "block";
            energyTimer.innerText = (player.energyTime / 60).toFixed(1);
        }} else {{
            player.speed = player.baseSpeed;
            energyUI.style.display = "none";
        }}

        // Update Triple Shot UI
        if(player.tripleShot > 0) {{
            tripleUI.style.display = "block";
            tripleCount.innerText = player.tripleShot;
        }} else {{
            tripleUI.style.display = "none";
        }}

        let s = player.speed, nx=player.x, ny=player.y;
        if(keys['KeyW']) ny-=s; if(keys['KeyS']) ny+=s;
        if(keys['KeyA']) nx-=s; if(keys['KeyD']) nx+=s;
        if(nx > player.r && nx < 600-player.r) player.x=nx; 
        if(ny > player.r && ny < 400-player.r) player.y=ny;

        // Skill Charging Logic
        if(player.type === 'roket' && bosses.length > 0) 
            player.sT = Math.min(100, player.sT + (100 / (5 * 60)));
        else if(player.type === 'roket') 
            player.sT = (player.kills/8)*100;
        else if(player.type === 'tank' || player.type === 'bomber') 
            player.sT = Math.min(100, player.sT + (100/(15*60)));
        else if(player.type === 'scout') 
            player.sT = Math.min(100, player.sT + (bosses.length > 0 ? 100/(6*60) : 100/(10*60)));
        else if(player.type === 'joker') 
            player.sT = (player.kills/15)*100;
        else if(player.type === 'assault') 
            player.sT = Math.min(100, player.sT + 0.1);

        uBar.style.width = Math.min(100, player.sT) + '%';

        // Items Logic
        for(let i=items.length-1; i>=0; i--) {{
            let it = items[i];
            if(Math.hypot(player.x-it.x, player.y-it.y) < player.r + 15) {{
                if(it.type === 'medkit') health = Math.min(health + 1, 10);
                else if(it.type === 'energy') player.energyTime += 300;
                else if(it.type === 'triple') player.tripleShot += 20;
                items.splice(i, 1);
            }}
        }}

        // Bullets Logic
        bullets = bullets.filter(b => {{
            if(b.rk) {{
                if(!b.target || b.target.hp <= 0) {{
                    let candidates = [...bosses, ...enemies]; 
                    let minDist = Infinity; b.target = null;
                    candidates.forEach(e => {{ 
                        let d = Math.hypot(e.x-b.x, e.y-b.y); 
                        if(d < minDist) {{ minDist=d; b.target=e; }} 
                    }});
                }}
                if(b.target) {{ 
                    let a = Math.atan2(b.target.y-b.y, b.target.x-b.x); 
                    b.vx += Math.cos(a)*1.2; b.vy += Math.sin(a)*1.2; 
                }}
                let speed = Math.hypot(b.vx, b.vy); 
                if(speed > 10) {{ b.vx=(b.vx/speed)*10; b.vy=(b.vy/speed)*10; }}
            }}
            b.x += b.vx; b.y += b.vy;
            
            if(b.p) {{
                // Hit bosses
                for(let i=bosses.length-1; i>=0; i--) {{
                    let boss = bosses[i];
                    if(Math.hypot(boss.x-b.x, boss.y-b.y) < boss.s+b.r) {{ 
                        if(!boss.shieldActive) boss.hp -= b.d;
                        spawnExplosion(b.x, b.y, '#fff', 5);
                        return false; 
                    }}
                }}
                
                // Hit enemies
                for(let i=enemies.length-1; i>=0; i--) {{
                    let e = enemies[i];
                    if(Math.hypot(e.x-b.x, e.y-b.y) < e.s/2+b.r) {{ 
                        e.hp -= b.d; 
                        if(e.hp<=0) {{ 
                            player.kills++; 
                            score += e.val; 
                            spawnExplosion(e.x, e.y, e.c, 15); 
                            spawnItem(e.x, e.y);
                            enemies.splice(i, 1); 
                        }} 
                        return false; 
                    }}
                }}
            }} else {{
                // Enemy bullets hit player
                if(Math.hypot(player.x-b.x, player.y-b.y) < player.r+b.r) {{
                    if(player.inv<=0 && !player.shield) triggerRespawn(); 
                    return false;
                }}
            }}
            return b.x>-100 && b.x<700 && b.y>-100 && b.y<500;
        }});

        // Boss Logic
        for(let i=bosses.length-1; i>=0; i--) {{
            let boss = bosses[i];
            
            // Movement
            let a = Math.atan2(player.y-boss.y, player.x-boss.x); 
            boss.x += Math.cos(a)*boss.sp; 
            boss.y += Math.sin(a)*boss.sp;
            
            // Collision with player
            if(Math.hypot(player.x-boss.x, player.y-boss.y) < player.r+boss.s && player.inv<=0 && !player.shield) 
                triggerRespawn();
            
            // Shield mechanic
            boss.nextShield--; 
            if(boss.nextShield <= 0 && !boss.shieldActive) {{ 
                boss.shieldActive = true; 
                boss.shieldTimer = 180; 
            }}
            if(boss.shieldActive) {{ 
                boss.shieldTimer--; 
                boss.hp = Math.min(boss.mH, boss.hp + 0.5); 
                if(boss.shieldTimer <= 0) {{ 
                    boss.shieldActive = false; 
                    boss.nextShield = 600 + Math.random()*200; 
                }} 
            }}
            
            // Shooting
            boss.fireTimer++;
            if(boss.fireTimer >= boss.fireRate) {{
                boss.fireTimer = 0;
                if(boss.variant === 'enhanced') {{
                    // Burst fire (3 bullets)
                    for(let j=0; j<3; j++) {{
                        fire(boss.x, boss.y, a + (j-1)*0.15, false, false, 1);
                    }}
                }} else {{
                    fire(boss.x, boss.y, a, false, false, 1);
                }}
            }}
            
            // Dash (enhanced mini boss only)
            if(boss.variant === 'enhanced' && boss.dashTimer > 0) {{
                boss.dashTimer--;
                if(boss.dashTimer === 0) {{
                    boss.dashCooldown = 600;
                    let dashAngle = Math.atan2(player.y-boss.y, player.x-boss.x);
                    boss.x += Math.cos(dashAngle) * 100;
                    boss.y += Math.sin(dashAngle) * 100;
                    spawnExplosion(boss.x, boss.y, boss.c, 20);
                }}
            }} else if(boss.variant === 'enhanced' && boss.dashCooldown > 0) {{
                boss.dashCooldown--;
                if(boss.dashCooldown === 0) boss.dashTimer = 30;
            }}
            
            // Main Boss Summoning
            if(boss.type === 'main') {{
                boss.summonTimer--;
                if(boss.summonTimer <= 0) {{
                    let summonCount = boss.phase === 2 ? 2 : 1;
                    for(let k=0; k<summonCount; k++) {{
                        let angle = (Math.PI * 2 / summonCount) * k;
                        let summonX = boss.x + Math.cos(angle) * 80;
                        let summonY = boss.y + Math.sin(angle) * 80;
                        bosses.push({{
                            x: summonX, y: summonY, s: 30, hp: 600, mH: 600,
                            c: 'rgba(155, 89, 182, 0.7)', sp: 1.1,
                            shieldActive: false, shieldTimer: 0, nextShield: 999999,
                            fireRate: 80, fireTimer: 0,
                            type: 'summon', variant: 'summoned'
                        }});
                    }}
                    boss.summonTimer = boss.summonCooldown;
                    
                    // Spawn some normal enemies too
                    for(let m=0; m<3; m++) {{
                        let ex = Math.random() * 600;
                        let ey = Math.random() * 400;
                        enemies.push({{
                            x: ex, y: ey, s: 22, sp: 1.2, hp: 5, c: '#e74c3c', val: 5
                        }});
                    }}
                }}
                
                // Phase transition
                if(boss.hp <= boss.mH * 0.5 && boss.phase === 1) {{
                    boss.phase = 2;
                    boss.sp = 1.2;
                    boss.fireRate = 25;
                    boss.summonCooldown = 400;
                    spawnExplosion(boss.x, boss.y, '#FFD700', 50);
                }}
                
                boss.glowPhase = (boss.glowPhase + 0.05) % (Math.PI * 2);
            }}
            
            // Boss defeated
            if(boss.hp <= 0) {{
                let bonusScore = boss.type === 'main' ? 1500 : 500;
                score += bonusScore;
                spawnExplosion(boss.x, boss.y, boss.c, boss.type === 'main' ? 100 : 50);
                
                // Drop guaranteed item
                spawnItem(boss.x, boss.y);
                if(boss.type === 'main') {{
                    spawn
