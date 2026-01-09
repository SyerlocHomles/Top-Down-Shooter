import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Pro Edition", layout="centered")
st.title("🛡️ Island.io: Final Polish")

if "char" not in st.session_state:
    st.session_state.char = None

# Inisialisasi State Karakter
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

c = st.session_state.char

game_html = f"""
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 4px solid #444;">
    <div style="display:flex; justify-content: space-between; color:white; font-family:Arial; font-weight:bold; padding:0 10px;">
        <div id="ui-lvl">LEVEL: 1</div>
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">❤️❤️❤️</div>
    </div>
    
    <div style="margin: 10px auto; width: 250px;">
        <div id="ui-skill" style="color:#00e5ff; font-size: 12px; font-weight:bold; margin-bottom:4px;">SKILL CHARGING...</div>
        <div style="width:100%; height:8px; background:#333; border-radius:4px; overflow:hidden; border: 1px solid #555;">
            <div id="skill-fill" style="width:0%; height:100%; background:#00e5ff; transition: width 0.1s;"></div>
        </div>
    </div>
    
    <div id="store" style="display:none; position:absolute; width:580px; height:380px; background:rgba(0,0,0,0.85); z-index:10; color:white; padding-top:100px; border-radius:10px;">
        <h2>⬆️ LEVEL UP! Pilih Upgrade:</h2>
        <button onclick="applyUpgrade('hp')" style="padding:10px 20px; margin:10px; cursor:pointer;">Tambah 1 Darah</button>
        <button onclick="applyUpgrade('atk')" style="padding:10px 20px; margin:10px; cursor:pointer;">Damage + (Rocket/Bullet)</button>
        <button onclick="applyUpgrade('buff')" style="padding:10px 20px; margin:10px; cursor:pointer;">Durasi Buff +2s</button>
    </div>

    <canvas id="c" width="600" height="400" style="background:#0a0a0a; border-radius:5px; cursor:crosshair;"></canvas>
</div>

<script>
    const cv=document.getElementById("c"), ctx=cv.getContext("2d");
    const uiS=document.getElementById("ui-score"), uiH=document.getElementById("ui-hp"), uiL=document.getElementById("ui-lvl"), 
          uiK=document.getElementById("ui-skill"), uiF=document.getElementById("skill-fill"), store=document.getElementById("store");
    
    let sc=0, li={c['hp']}, lvl=1, go=false, ks={{}}, buls=[], ebuls=[], enms=[], wls=[], itms=[], pX=[], boss=null, mX=0, mY=0;
    let ply={{x:300, y:200, s:12, inv:0, pw:null, pT:0, spd:{c['spd']}, col:'{c['col']}', type:'{c['type']}', sRdy:false, sT:0, mST:600, sh:false, bDur:400, dmg:5}};
    let wCount = 7;

    function applyUpgrade(type) {{
        if(type==='hp') li++;
        if(type==='atk') ply.dmg += 3;
        if(type==='buff') ply.bDur += 120;
        store.style.display = 'none';
        lvl++;
        initMap();
        requestAnimationFrame(draw);
    }}

    window.onkeydown=(e)=>{{ ks[e.code]=true; if(e.code==="Space") useSkill(); }};
    window.onkeyup=(e)=>ks[e.code]=false;
    cv.onmousemove=(e)=>{{ let r=cv.getBoundingClientRect(); mX=e.clientX-r.left; mY=e.clientY-r.top; }};

    cv.onmousedown=(e)=>{{
        if(go || store.style.display==='block') return; 
        let a=Math.atan2(mY-ply.y, mX-ply.x);
        fire(ply.x, ply.y, a, 12, "#f1c40f", false);
        if(ply.pw === 'triple') {{ fire(ply.x, ply.y, a+0.22, 12, "#f1c40f", false); fire(ply.x, ply.y, a-0.22, 12, "#f1c40f", false); }}
    }};

    function fire(x, y, a, spd, col, isR) {{
        buls.push({{x, y, vx:Math.cos(a)*spd, vy:Math.sin(a)*spd, col, r:isR}});
    }}

    function useSkill() {{
        if(!ply.sRdy || go) return;
        ply.sRdy = false; ply.sT = 0; 

        if(ply.type === 'assault') {{
            for(let i=0; i<8; i++) setTimeout(()=>{{
                let a = Math.atan2(mY - ply.y, mX - ply.x); // Ikuti kursor
                fire(ply.x, ply.y, a + (Math.random()-0.5)*0.1, 15, "#ff4500", true);
                spawnExplosion(ply.x, ply.y, "#ff4500", 2);
            }}, i*100);
        }} else if(ply.type === 'tank') {{
            ply.sh = true; spawnExplosion(ply.x, ply.y, "#00e5ff", 20);
            setTimeout(()=> ply.sh = false, 5000);
        }} else if(ply.type === 'scout') {{
            let a = Math.atan2(mY - ply.y, mX - ply.x);
            let dx = Math.cos(a)*150, dy = Math.sin(a)*150;
            if(!isCol(ply.x+dx, ply.y+dy, ply.s, wls)) {{ ply.x+=dx; ply.y+=dy; }}
            spawnExplosion(ply.x, ply.y, "#fff", 20);
        }}
    }}

    function spawnExplosion(x, y, color, count=12) {{
        for(let i=0; i<count; i++) pX.push({{ x, y, vx:(Math.random()-0.5)*12, vy:(Math.random()-0.5)*12, life:25, col:color, s:Math.random()*4+2 }});
    }}

    function isCol(x,y,s,ws){{
        for(let w of ws){{ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; }}
        return false;
    }}

    function initMap() {{
        wls=[]; 
        let count = Math.max(2, wCount - (lvl-1));
        for(let i=0; i<count; i++){{
            let w=Math.random()*60+40, h=Math.random()*60+40, x=Math.random()*450+50, y=Math.random()*250+50;
            if(Math.sqrt((x-ply.x)**2+(y-ply.y)**2)>120) wls.push({{x,y,w,h}});
        }}
    }}

    function update() {{
        if(go || store.style.display==='block') return;
        
        // Skill Charging Logic
        if(ply.sT < ply.mST) ply.sT++;
        else ply.sRdy = true;
        
        let sPct = (ply.sT / ply.mST) * 100;
        uiF.style.width = sPct + "%";
        uiF.style.background = ply.sRdy ? "#00ff88" : "#00e5ff";
        uiK.innerText = ply.sRdy ? "SKILL READY (SPACE)" : "CHARGING ULTIMATE...";
        uiK.style.color = ply.sRdy ? "#00ff88" : "#00e5ff";

        uiS.innerText = "Skor: " + sc;
        uiL.innerText = "LEVEL: " + lvl;
        let hText = ""; for(let i=0; i<li; i++) hText += "❤️";
        uiH.innerText = hText;

        // Spawn Kroco
        if(enms.length < 3 + lvl) {{
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!isCol(rx,ry,20,wls) && Math.sqrt((rx-ply.x)**2+(ry-ply.y)**2)>200)
                enms.push({{x:rx,y:ry,c:'#e74c3c',s:20,sp:1.1+(lvl*0.1),h:5,sc:10}});
        }}

        // Player Move
        let curS = (ply.pw==='speed')?ply.spd*1.6:ply.spd, nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=curS; if(ks["KeyS"]) ny+=curS; if(ks["KeyA"]) nx-=curS; if(ks["KeyD"]) nx+=curS;
        if(!isCol(nx,ny,ply.s,wls)){{ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }}
        
        if(ply.inv>0) ply.inv--;
        if(ply.pT>0) {{ ply.pT--; if(ply.pT<=0) ply.pw=null; }}

        // Boss
        if(sc >= lvl * 300 && !boss) boss={{x:300,y:50,s:65,h:500+(lvl*200),mH:500+(lvl*200),sp:0.6+(lvl*0.05),fT:0}};

        if(boss){{
            let dx=ply.x-boss.x, dy=ply.y-boss.y, d=Math.sqrt(dx*dx+dy*dy);
            if(!isCol(boss.x+(dx/d)*boss.sp, boss.y+(dy/d)*boss.sp, boss.s/2, wls)){{ boss.x+=(dx/d)*boss.sp; boss.y+=(dy/d)*boss.sp; }}
            boss.fT++;
            if(boss.fT > (110 - (lvl*5))){{
                for(let a=0; a<Math.PI*2; a+=0.75) ebuls.push({{x:boss.x+boss.s/2, y:boss.y+boss.s/2, vx:Math.cos(a)*5, vy:Math.sin(a)*5}});
                boss.fT=0;
            }}
        }}

        // AI Kroco Avoidance Logic (Anti-Stuck)
        enms.forEach(e=>{{
            let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy);
            let vx=(dx/d)*e.sp, vy=(dy/d)*e.sp;
            
            if(!isCol(e.x+vx, e.y+vy, e.s/2, wls)) {{
                e.x += vx; e.y += vy;
            }} else {{
                // Jika terhalang, coba geser ke samping (90 derajat)
                if(!isCol(e.x+vy, e.y-vx, e.s/2, wls)) {{ e.x += vy; e.y -= vx; }}
                else if(!isCol(e.x-vy, e.y+vx, e.s/2, wls)) {{ e.x -= vy; e.y += vx; }}
            }}
            
            if(ply.inv<=0 && !ply.sh && Math.sqrt((e.x-ply.x)**2+(e.y-ply.y)**2)<(e.s/2+ply.s)){{ li--; ply.inv=60; if(li<=0) go=true; }}
        }});

        // Projectiles
        buls.forEach((b,i)=>{{
            b.x+=b.vx; b.y+=b.vy;
            if(isCol(b.x,b.y,4,wls) || b.x<0 || b.x>600 || b.y<0 || b.y>400) {{ buls.splice(i,1); return; }}
            if(boss && b.x>boss.x && b.x<boss.x+boss.s && b.y>boss.y && b.y<boss.y+boss.s){{
                boss.h -= b.r ? ply.dmg*4 : ply.dmg; buls.splice(i,1);
                if(boss.h<=0){{ sc+=500; boss=null; store.style.display='block'; }}
                return;
            }}
            enms.forEach((e,ei)=>{{
                if(Math.sqrt((b.x-e.x)**2+(b.y-e.y)**2)<e.s){{
                    e.h-=ply.dmg; buls.splice(i,1);
                    if(e.h<=0){{ sc+=e.sc; enms.splice(ei,1); spawnExplosion(e.x,e.y,e.c,15); }}
                }}
            }});
        }});

        ebuls.forEach((eb,i)=>{{
            eb.x+=eb.vx; eb.y+=eb.vy;
            if(isCol(eb.x, eb.y, 4, wls) || eb.x<0 || eb.x>600) {{ ebuls.splice(i, 1); return; }}
            if(Math.sqrt((eb.x-ply.x)**2+(eb.y-ply.y)**2)<ply.s && ply.inv<=0){{
                ebuls.splice(i,1);
                if(!ply.sh) {{ li--; ply.inv=60; if(li<=0) go=true; }}
            }}
        }});

        itms.forEach((it,i)=>{{ if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){{ ply.pw=it.t; ply.pT=ply.bDur; itms.splice(i,1); }} }});
        pX.forEach((p,i)=>{{ p.x+=p.vx; p.y+=p.vy; p.life--; if(p.life<=0) pX.splice(i,1); }});
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        ctx.fillStyle="#444"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,10,0,7); ctx.fill(); }});
        enms.forEach(e=>{{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2,e.y-e.s/2,e.s,e.s); }});
        if(boss){{
            ctx.fillStyle="#e74c3c"; ctx.fillRect(boss.x,boss.y,boss.s,boss.s);
            ctx.fillStyle="#f00"; ctx.fillRect(boss.x, boss.y-15, (boss.h/boss.mH)*boss.s, 8);
        }}
        buls.forEach(b=>{{ ctx.fillStyle=b.col; ctx.beginPath(); ctx.arc(b.x,b.y,b.r?7:4,0,7); ctx.fill(); }});
        ctx.fillStyle="#ff4757"; ebuls.forEach(eb=>{{ ctx.beginPath(); ctx.arc(eb.x,eb.y,6,0,7); ctx.fill(); }});
        pX.forEach(p=>{{ ctx.fillStyle=p.col; ctx.globalAlpha=p.life/25; ctx.fillRect(p.x,p.y,p.s,p.s); }});
        ctx.globalAlpha=1;
        if(ply.inv%10<5){{ 
            ctx.fillStyle=ply.col; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill(); 
            if(ply.sh) {{ ctx.strokeStyle="#00e5ff"; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s+8,0,7); ctx.stroke(); }}
        }}
        update(); 
        if(!go) {{ if(store.style.display !== 'block') requestAnimationFrame(draw); }}
        else {{ ctx.fillStyle="#fff"; ctx.font="40px Arial"; ctx.fillText("GAME OVER",180,200); }}
    }}
    initMap(); setInterval(()=>{{ if(itms.length<2) {{ let rx=Math.random()*540+30, ry=Math.random()*340+30; if(!isCol(rx,ry,15,wls)) itms.push({{x:rx,y:ry,t:Math.random()<0.5?'speed':'triple'}}); }} }}, 7000);
    draw();
</script>
"""

cp.html(game_html, height=600)
