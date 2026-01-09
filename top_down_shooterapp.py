import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Ultimate", layout="centered")
st.title("🔥 Island.io: Ultimate Skill Edition")
st.write("Gunakan **WASD** untuk gerak, **Klik** tembak, dan **SPASI** untuk Skill!")

if "char" not in st.session_state:
    st.session_state.char = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Assault (Rockets)"):
        st.session_state.char = {"hp": 3, "speed": 4.5, "color": "#00a2e8", "type": "assault"}
with col2:
    if st.button("🟢 Tank (Shield)"):
        st.session_state.char = {"hp": 6, "speed": 3.0, "color": "#2ecc71", "type": "tank"}
with col3:
    if st.button("🟡 Scout (Dash)"):
        st.session_state.char = {"hp": 2, "speed": 6.5, "color": "#f1c40f", "type": "scout"}

if not st.session_state.char:
    st.info("Pilih karakter untuk memulai!")
    st.stop()

c = st.session_state.char

game_html = f"""
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 2px solid #333;">
    <div style="display:flex; justify-content: space-around; color:white; font-family:Arial; font-weight:bold; margin-bottom:10px;">
        <div id="ui-score">Skor: 0</div>
        <div id="ui-skill">SKILL: READY (SPACE)</div>
        <div id="ui-hp">Nyawa: </div>
    </div>
    <p id="p-info" style="color:#f1c40f; font-weight:bold; margin:5px 0; height:20px; font-family:Courier;"></p>
    <canvas id="c" width="600" height="400" style="background:#0a0a0a; cursor:crosshair; border-radius:5px;"></canvas>
</div>

<script>
    const cv=document.getElementById("c"), ctx=cv.getContext("2d");
    const uiS=document.getElementById("ui-score"), uiH=document.getElementById("ui-hp"), uiK=document.getElementById("ui-skill"), pInf=document.getElementById("p-info");
    
    let sc=0, li={c['hp']}, go=false, ks={{}}, buls=[], ebuls=[], enms=[], wls=[], itms=[], pX=[], boss=null, sk=0;
    let ply={{x:300, y:200, s:12, inv:0, pw:null, pT:0, spd:{c['speed']}, col:'{c['color']}', type:'{c['type']}', sRdy:true, sT:0, sh:false}};
    let wallCount = 8;

    window.onkeydown=(e)=>{{ 
        ks[e.code]=true; 
        if(e.code==="Space") useSkill(); 
    }};
    window.onkeyup=(e)=>ks[e.code]=false;
    
    cv.onmousedown=(e)=>{{
        if(go) return; 
        let r=cv.getBoundingClientRect(), a=Math.atan2((e.clientY-r.top)-ply.y, (e.clientX-r.left)-ply.x);
        fire(ply.x, ply.y, a, 11, "#f1c40f", false);
        if(ply.pw === 'triple') {{ fire(ply.x, ply.y, a+0.2, 11, "#f1c40f", false); fire(ply.x, ply.y, a-0.2, 11, "#f1c40f", false); }}
    }};

    function fire(x, y, a, spd, col, isR) {{
        buls.push({{x, y, vx:Math.cos(a)*spd, vy:Math.sin(a)*spd, col, r:isR}});
    }}

    function useSkill() {{
        if(!ply.sRdy || go) return;
        ply.sRdy = false; ply.sT = 600; // Cooldown 10 detik (60fps * 10)

        if(ply.type === 'assault') {{
            for(let i=0; i<5; i++) setTimeout(()=>{{
                let target = enms[0] || boss || {{x: Math.random()*600, y:0}};
                let a = Math.atan2(target.y - ply.y, target.x - ply.x);
                fire(ply.x, ply.y, a + (Math.random()-0.5), 8, "#ff4500", true);
            }}, i*150);
        }} else if(ply.type === 'tank') {{
            ply.sh = true;
            setTimeout(()=> ply.sh = false, 4000);
        }} else if(ply.type === 'scout') {{
            let dx=0, dy=0;
            if(ks["KeyW"]) dy-=80; if(ks["KeyS"]) dy+=80; if(ks["KeyA"]) dx-=80; if(ks["KeyD"]) dx+=80;
            if(!isCol(ply.x+dx, ply.y+dy, ply.s, wls)) {{ ply.x+=dx; ply.y+=dy; }}
            spawnExplosion(ply.x, ply.y, ply.col, 15);
        }}
    }}

    function spawnExplosion(x, y, color, count=12) {{
        for(let i=0; i<count; i++) pX.push({{ x, y, vx:(Math.random()-0.5)*10, vy:(Math.random()-0.5)*10, life:20, col:color, s:Math.random()*4+2 }});
    }}

    function isCol(x,y,s,ws){{
        for(let w of ws){{ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; }}
        return false;
    }}

    function initMap() {{
        wls=[]; 
        for(let i=0; i<wallCount; i++){{
            let w=Math.random()*50+30, h=Math.random()*50+30, x=Math.random()*500+50, y=Math.random()*300+50;
            if(Math.sqrt((x-ply.x)**2+(y-ply.y)**2)>100) wls.push({{x,y,w,h}});
        }}
    }}

    function update() {{
        if(go) return;
        if(sk>0) sk--;
        if(ply.sT > 0) ply.sT--; else ply.sRdy = true;

        // UI Update
        uiS.innerText = "Skor: " + sc;
        uiK.innerText = ply.sRdy ? "SKILL: READY (SPACE)" : "COOLDOWN: " + Math.ceil(ply.sT/60) + "s";
        let hText = ""; for(let i=0; i<li; i++) hText += "❤️";
        uiH.innerText = "Nyawa: " + hText;

        // Enemy Spawn (Skor per kroco dikurangi)
        if(enms.length < 5) {{
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!isCol(rx,ry,20,wls)) enms.push({{x:rx,y:ry,c:'#e74c3c',s:20,sp:1.2,h:5,sc:5}}); // Hanya 5 skor
        }}

        // Move Player
        let curS = (ply.pw==='speed')?ply.spd*1.6:ply.spd, nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=curS; if(ks["KeyS"]) ny+=curS; if(ks["KeyA"]) nx-=curS; if(ks["KeyD"]) nx+=curS;
        if(!isCol(nx,ny,ply.s,wls)){{ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }}
        
        if(ply.inv>0) ply.inv--;
        if(ply.pT>0) {{ ply.pT--; if(ply.pT<=0) ply.pw=null; }}

        // Boss
        if(sc >= 200 && !boss) boss={{x:300,y:50,s:60,h:600,mH:600,sp:0.6,fT:0}};

        if(boss){{
            let dx=ply.x-boss.x, dy=ply.y-boss.y, d=Math.sqrt(dx*dx+dy*dy);
            if(!isCol(boss.x+(dx/d)*boss.sp, boss.y+(dy/d)*boss.sp, boss.s/2, wls)){{ boss.x+=(dx/d)*boss.sp; boss.y+=(dy/d)*boss.sp; }}
            boss.fT++;
            if(boss.fT > 120){{
                for(let a=0; a<Math.PI*2; a+=0.8) ebuls.push({{x:boss.x+boss.s/2, y:boss.y+boss.s/2, vx:Math.cos(a)*4, vy:Math.sin(a)*4}});
                boss.fT=0;
            }}
        }}

        // Bullets logic
        buls.forEach((b,i)=>{{
            b.x+=b.vx; b.y+=b.vy;
            if(isCol(b.x,b.y,4,wls) || b.x<0 || b.x>600 || b.y<0 || b.y>400) {{ buls.splice(i,1); return; }}
            if(boss && b.x>boss.x && b.x<boss.x+boss.s && b.y>boss.y && b.y<boss.y+boss.s){{
                boss.h -= b.r ? 20 : 5; spawnExplosion(b.x,b.y,"#ffa500",5); buls.splice(i,1);
                if(boss.h<=0){{ 
                    sc+=500; boss=null; wallCount=Math.max(2, wallCount-2); initMap(); // Map Evolution
                    spawnExplosion(300,200,"#fff",50);
                }}
                return;
            }}
            enms.forEach((e,ei)=>{{
                if(Math.sqrt((b.x-e.x)**2+(b.y-e.y)**2)<e.s){{
                    e.h-=5; buls.splice(i,1);
                    if(e.h<=0){{ sc+=e.sc; enms.splice(ei,1); spawnExplosion(e.x,e.y,e.c,15); }}
                }}
            }});
        }});

        // Enemy Bullets logic (Can be blocked by walls)
        ebuls.forEach((eb,i)=>{{
            eb.x+=eb.vx; eb.y+=eb.vy;
            if(isCol(eb.x, eb.y, 4, wls)) {{ ebuls.splice(i, 1); return; }} // Peluru bos hancur kena tembok
            if(Math.sqrt((eb.x-ply.x)**2+(eb.y-ply.y)**2)<ply.s && ply.inv<=0){{
                ebuls.splice(i,1);
                if(!ply.sh) {{ li--; ply.inv=60; spawnExplosion(ply.x,ply.y,"#f00",20); if(li<=0) go=true; }}
            }}
            if(eb.x<0||eb.x>600||eb.y<0||eb.y>400) ebuls.splice(i,1);
        }});

        enms.forEach(e=>{{
            let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy);
            if(!isCol(e.x+(dx/d)*e.sp, e.y+(dy/d)*e.sp, e.s/2, wls)){{ e.x+=(dx/d)*e.sp; e.y+=(dy/d)*e.sp; }}
            if(ply.inv<=0 && !ply.sh && Math.sqrt((e.x-ply.x)**2+(e.y-ply.y)**2)<(e.s/2+ply.s)){{ li--; ply.inv=60; if(li<=0) go=true; }}
        }});

        itms.forEach((it,i)=>{{ if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){{ ply.pw=it.t; ply.pT=400; itms.splice(i,1); }} }});
        pX.forEach((p,i)=>{{ p.x+=p.vx; p.y+=p.vy; p.life--; if(p.life<=0) pX.splice(i,1); }});
    }}

    function draw() {{
        ctx.clearRect(0,0,600,400);
        ctx.fillStyle="#333"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,10,0,7); ctx.fill(); }});
        enms.forEach(e=>{{ ctx.fillStyle=e.c; ctx.fillRect(e.x-e.s/2,e.y-e.s/2,e.s,e.s); }});
        if(boss){{
            ctx.fillStyle="#e74c3c"; ctx.fillRect(boss.x,boss.y,boss.s,boss.s);
            ctx.fillStyle="#f00"; ctx.fillRect(boss.x, boss.y-15, (boss.h/boss.mH)*boss.s, 8);
        }}
        buls.forEach(b=>{{ ctx.fillStyle=b.col; ctx.beginPath(); ctx.arc(b.x,b.y,b.r?6:4,0,7); ctx.fill(); }});
        ctx.fillStyle="#ff4757"; ebuls.forEach(eb=>{{ ctx.beginPath(); ctx.arc(eb.x,eb.y,6,0,7); ctx.fill(); }});
        pX.forEach(p=>{{ ctx.fillStyle=p.col; ctx.globalAlpha=p.life/20; ctx.fillRect(p.x,p.y,p.s,p.s); }});
        ctx.globalAlpha=1;
        if(ply.inv%10<5){{ 
            ctx.fillStyle=ply.col; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill(); 
            if(ply.sh) {{ ctx.strokeStyle="#3498db"; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s+5,0,7); ctx.stroke(); }}
        }}
        update(); if(!go) requestAnimationFrame(draw); else {{ ctx.fillStyle="#fff"; ctx.font="40px Arial"; ctx.fillText("GAME OVER",180,200); }}
    }}
    initMap(); setInterval(()=>{{ if(itms.length<2) {{ let rx=Math.random()*540+30, ry=Math.random()*340+30; if(!isCol(rx,ry,15,wls)) itms.push({{x:rx,y:ry,t:Math.random()<0.5?'speed':'triple'}}); }} }}, 8000);
    draw();
</script>
"""

cp.html(game_html, height=600)
