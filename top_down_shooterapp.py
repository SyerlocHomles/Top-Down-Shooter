import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Pro Fix", layout="centered")
st.title("🛡️ Island.io: Precision Update")

if "char" not in st.session_state:
    st.session_state.char = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Assault (Rocket)"):
        st.session_state.char = {"hp": 3, "spd": 4.5, "col": "#00a2e8", "type": "assault"}
with col2:
    if st.button("🟢 Tank (Shield)"):
        st.session_state.char = {"hp": 6, "spd": 3.0, "col": "#2ecc71", "type": "tank"}
with col3:
    if st.button("🟡 Scout (Dash)"):
        st.session_state.char = {"hp": 2, "spd": 6.8, "col": "#f1c40f", "type": "scout"}

if not st.session_state.char:
    st.info("Pilih Class untuk Memulai!")
    st.stop()

game_html = f"""
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444; position:relative;">
    <div style="display:flex; justify-content: space-between; color:white; font-family:Arial; font-weight:bold; padding:0 10px;">
        <div id="ui-lvl">LEVEL: 1</div>
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">❤️❤️❤️</div>
    </div>
    
    <div style="margin: 10px auto; width: 250px;">
        <div id="ui-skill" style="color:#00e5ff; font-size: 11px; font-weight:bold;">CHARGING...</div>
        <div style="width:100%; height:8px; background:#333; border-radius:4px; overflow:hidden; border: 1px solid #555;">
            <div id="skill-fill" style="width:0%; height:100%; background:#00e5ff;"></div>
        </div>
    </div>

    <div id="buff-ui" style="color:#f1c40f; font-size:12px; height:15px; font-weight:bold; margin-bottom:5px;"></div>

    <div id="store" style="display:none; position:absolute; width:95%; height:80%; background:rgba(0,0,0,0.9); z-index:100; color:white; top:10%; left:2.5%; border-radius:10px; padding-top:50px;">
        <h2>⬆️ LEVEL UP!</h2>
        <button onclick="applyUpgrade('hp')" style="padding:10px; margin:5px; cursor:pointer;">+1 HP</button>
        <button onclick="applyUpgrade('atk')" style="padding:10px; margin:5px; cursor:pointer;">ATK Up</button>
        <button onclick="applyUpgrade('buff')" style="padding:10px; margin:5px; cursor:pointer;">Buff +2s</button>
    </div>

    <canvas id="c" width="600" height="400" style="background:#0a0a0a; border-radius:5px; cursor:crosshair;"></canvas>
</div>

<script>
    const cv=document.getElementById("c"), ctx=cv.getContext("2d");
    const uiS=document.getElementById("ui-score"), uiH=document.getElementById("ui-hp"), 
          uiL=document.getElementById("ui-lvl"), uiK=document.getElementById("ui-skill"), 
          uiF=document.getElementById("skill-fill"), uiB=document.getElementById("buff-ui"),
          store=document.getElementById("store");
    
    let sc=0, li={st.session_state.char['hp']}, lvl=1, go=false, ks={{}}, buls=[], ebuls=[], enms=[], wls=[], itms=[], pX=[], boss=null, mX=0, mY=0;
    
    let ply={{
        x:300, y:200, s:12, inv:0, spd:{st.session_state.char['spd']}, col:'{st.session_state.char['col']}', 
        type:'{st.session_state.char['type']}', sRdy:false, sT:0, mST:600, sh:false, bDur:400, dmg:5,
        buffs: {{ speed: 0, triple: 0 }}
    }};

    function applyUpgrade(t) {{
        if(t==='hp') li++; if(t==='atk') ply.dmg += 3; if(t==='buff') ply.bDur += 120;
        store.style.display='none'; lvl++; initMap(); requestAnimationFrame(draw);
    }}

    window.onkeydown=(e)=>{{ ks[e.code]=true; if(e.code==="Space") useSkill(); }};
    window.onkeyup=(e)=>ks[e.code]=false;
    cv.onmousemove=(e)=>{{ let r=cv.getBoundingClientRect(); mX=e.clientX-r.left; mY=e.clientY-r.top; }};

    cv.onmousedown=(e)=>{{
        if(go || store.style.display==='block') return; 
        let a=Math.atan2(mY-ply.y, mX-ply.x);
        fire(ply.x, ply.y, a, 12, "#f1c40f", false);
        if(ply.buffs.triple > 0) {{ 
            fire(ply.x, ply.y, a+0.2, 12, "#f1c40f", false); 
            fire(ply.x, ply.y, a-0.2, 12, "#f1c40f", false); 
        }}
    }};

    function fire(x,y,a,s,c,r) {{ buls.push({{x,y,vx:Math.cos(a)*s, vy:Math.sin(a)*s, col:c, r}}); }}

    // FIX DETEKSI TEMBOK (Lebih Akurat)
    function checkWall(x, y, size) {{
        for(let w of wls) {{
            if(x + size > w.x && x - size < w.x + w.w &&
               y + size > w.y && y - size < w.y + w.h) return true;
        }
        return false;
    }}

    function initMap() {{
        wls=[]; let count = 5;
        for(let i=0; i<count; i++){{
            let w=Math.random()*60+40, h=Math.random()*60+40, x=Math.random()*450+50, y=Math.random()*250+50;
            // Pastikan tidak spawn di tengah player
            if(Math.abs(x-300) > 80 && Math.abs(y-200) > 80) wls.push({{x,y,w,h}});
        }}
    }}

    function useSkill() {{
        if(!ply.sRdy || go) return;
        ply.sRdy = false; ply.sT = 0;
        if(ply.type==='assault') {{
            for(let i=0; i<8; i++) setTimeout(()=>{{
                let a=Math.atan2(mY-ply.y, mX-ply.x);
                fire(ply.x, ply.y, a+(Math.random()-0.5)*0.1, 15, "#ff4500", true);
            }}, i*100);
        }} else if(ply.type==='tank') {{
            ply.sh=true; setTimeout(()=>ply.sh=false, 5000);
        }} else if(ply.type==='scout') {{
            let a=Math.atan2(mY-ply.y, mX-ply.x);
            let jX = Math.cos(a)*150, jY = Math.sin(a)*150;
            if(!checkWall(ply.x+jX, ply.y+jY, ply.s)) {{ ply.x+=jX; ply.y+=jY; }}
        }}
    }}

    function update() {{
        if(go || store.style.display==='block') return;

        if(ply.sT < ply.mST) ply.sT++; else ply.sRdy=true;
        if(ply.buffs.speed > 0) ply.buffs.speed--;
        if(ply.buffs.triple > 0) ply.buffs.triple--;

        let bMsg = [];
        if(ply.buffs.speed > 0) bMsg.push("⚡ SPEED ("+Math.ceil(ply.buffs.speed/60)+"s)");
        if(ply.buffs.triple > 0) bMsg.push("🔫 TRIPLE ("+Math.ceil(ply.buffs.triple/60)+"s)");
        uiB.innerText = bMsg.join(" | ");

        uiF.style.width = (ply.sT/ply.mST*100) + "%";
        uiK.innerText = ply.sRdy ? "READY (SPACE)" : "CHARGING...";
        uiS.innerText = "Skor: " + sc;
        uiH.innerText = "❤️".repeat(li);

        let curS = (ply.buffs.speed > 0) ? ply.spd * 1.7 : ply.spd;
        let nX=ply.x, nY=ply.y;
        if(ks["KeyW"]) nY-=curS; if(ks["KeyS"]) nY+=curS; if(ks["KeyA"]) nX-=curS; if(ks["KeyD"]) nX+=curS;
        
        if(!checkWall(nX, ply.y, ply.s)) ply.x = Math.max(ply.s, Math.min(600-ply.s, nX));
        if(!checkWall(ply.x, nY, ply.s)) ply.y = Math.max(ply.s, Math.min(400-ply.s, nY));
        
        if(ply.inv>0) ply.inv--;

        // ENEMY LOGIC (Fixed Sticking & Ghosting)
        let entities = [...enms]; if(boss) entities.push(boss);
        entities.forEach(e => {{
            let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy);
            let vx=(dx/d)*e.sp, vy=(dy/d)*e.sp;
            
            if(!checkWall(e.x+vx, e.y+vy, e.s/2)) {{
                e.x += vx; e.y += vy;
            }} else {{
                // Slide Logic yang lebih mulus agar tidak tembus
                if(!checkWall(e.x+vy, e.y-vx, e.s/2)) {{ e.x+=vy*0.8; e.y-=vx*0.8; }} 
                else if(!checkWall(e.x-vy, e.y+vx, e.s/2)) {{ e.x-=vy*0.8; e.y+=vx*0.8; }}
            }}
            
            if(ply.inv<=0 && !ply.sh && Math.sqrt((e.x-ply.x)**2+(e.y-ply.y)**2)<(e.s/2+ply.s)){{
                li--; ply.inv=60; if(li<=0) go=true;
            }}
        }});

        // PROJECTILE LOGIC (Fix Ghost Collision)
        buls.forEach((b,i)=>{{
            b.x+=b.vx; b.y+=b.vy;
            if(checkWall(b.x, b.y, 2) || b.x<0 || b.x>600 || b.y<0 || b.y>400) {{ 
                buls.splice(i,1); return; 
            }}
            
            if(boss && b.x>boss.x-boss.s/2 && b.x<boss.x+boss.s/2 && b.y>boss.y-boss.s/2 && b.y<boss.y+boss.s/2){{
                boss.h -= b.r ? ply.dmg*4 : ply.dmg; buls.splice(i,1);
                if(boss.h<=0){{ sc+=500; boss=null; store.style.display='block'; }}
                return;
            }}
            enms.forEach((e,ei)=>{{
                if(Math.sqrt((b.x-e.x)**2+(b.y-e.y)**2)<e.s/2){{
                    e.h-=ply.dmg; buls.splice(i,1);
                    if(e.h<=0){{ sc+=e.sc; enms.splice(ei,1); }}
                }}
            }});
        }});

        itms.forEach((it,i)=>{{
            if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){{
                if(it.t==='speed') ply.buffs.speed = ply.bDur;
                if(it.t==='triple') ply.buffs.triple = ply.bDur;
                itms.splice(i,1);
            }}
        }});
        
        if(enms.length < 3 + lvl) {{
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            let rnd=Math.random();
            let type = rnd < 0.6 ? {{c:'#e74c3c', s:20, sp:1.2, h:5, sc:10}} : 
                       rnd < 0.85 ? {{c:'#2ecc71', s:26, sp:0.7, h:15, sc:20}} : 
                                    {{c:'#9b59b6', s:16, sp:2.2, h:3, sc:25}};
            if(!checkWall(rx,ry,20)) enms.push({{x:rx, y:ry, ...type}});
        }}
        if(sc >= lvl*300 && !boss) boss={{x:300,y:50,s:70,h:500+(lvl*200),mH:500+(lvl*200),sp:0.7,fT:0}};
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        ctx.fillStyle="#444"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{{
            ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db";
            ctx.beginPath(); ctx.arc(it.x,it.y,10,0,7); ctx.fill();
        }});
        enms.forEach(e=>{{
            ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s);
        }});
        if(boss){{
            ctx.fillStyle="#e74c3c"; ctx.fillRect(boss.x-boss.s/2, boss.y-boss.s/2, boss.s, boss.s);
            ctx.fillStyle="#f00"; ctx.fillRect(boss.x-boss.s/2, boss.y-boss.s/2-10, (boss.h/boss.mH)*boss.s, 5);
        }}
        buls.forEach(b=>{{
            ctx.fillStyle=b.col; ctx.beginPath(); ctx.arc(b.x,b.y,b.r?7:3,0,7); ctx.fill();
        }});
        
        ctx.globalAlpha = ply.inv % 10 < 5 ? 1 : 0.5;
        ctx.fillStyle=ply.col; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill();
        ctx.globalAlpha = 1;

        if(ply.sh) {{
            ctx.strokeStyle="#00e5ff"; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s+8,0,7); ctx.stroke();
        }}
        update(); 
        if(!go && store.style.display!=='block') requestAnimationFrame(draw);
        if(go) {{ ctx.fillStyle="white"; ctx.font="30px Arial"; ctx.fillText("GAME OVER",220,200); }}
    }}
    initMap(); 
    setInterval(()=>{{ if(itms.length<2) itms.push({{x:Math.random()*500+50, y:Math.random()*300+50, t:Math.random()<0.5?'speed':'triple'}}); }}, 5000);
    draw();
</script>
"""

cp.html(game_html, height=600)
