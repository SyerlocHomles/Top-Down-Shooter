import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Anti-Bug", layout="centered")
st.title("🛡️ Island.io: Pro Edition (Bug Fix)")

if "char" not in st.session_state:
    st.session_state.char = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Assault"):
        st.session_state.char = {"hp": 3, "speed": 4.6, "color": "#00a2e8", "name": "Assault"}
with col2:
    if st.button("🟢 Tank"):
        st.session_state.char = {"hp": 6, "speed": 3.0, "color": "#2ecc71", "name": "Tank"}
with col3:
    if st.button("🟡 Scout"):
        st.session_state.char = {"hp": 2, "speed": 6.8, "color": "#f1c40f", "name": "Scout"}

if not st.session_state.char:
    st.info("Pilih karakter untuk memulai!")
    st.stop()

c = st.session_state.char

game_html = f"""
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 2px solid #333;">
    <div style="display:flex; justify-content: space-around; color:white; font-family:Arial; font-weight:bold; margin-bottom:10px;">
        <div id="ui-score">Skor: 0</div>
        <div id="ui-hp">Nyawa: </div>
    </div>
    <p id="p-info" style="color:#f1c40f; font-weight:bold; margin:5px 0; height:20px; font-family:Courier;"></p>
    <canvas id="c" width="600" height="400" style="background:#0a0a0a; cursor:crosshair; border-radius:5px;"></canvas>
</div>

<script>
    const cv=document.getElementById("c"), ctx=cv.getContext("2d"), uiS=document.getElementById("ui-score"), uiH=document.getElementById("ui-hp"), pInf=document.getElementById("p-info");
    let sc=0, li={c['hp']}, go=false, ks={{}}, buls=[], ebuls=[], enms=[], wls=[], itms=[], pX=[], boss=null, sk=0;
    let ply={{x:300, y:200, s:12, inv:0, pw:null, pT:0, spd:{c['speed']}, col:'{c['color']}'}};

    window.onkeydown=(e)=>ks[e.code]=true; window.onkeyup=(e)=>ks[e.code]=false;
    
    cv.onmousedown=(e)=>{{
        if(go) return; 
        let r=cv.getBoundingClientRect(), a=Math.atan2((e.clientY-r.top)-ply.y, (e.clientX-r.left)-ply.x);
        const fire = (ang) => buls.push({{x:ply.x, y:ply.y, vx:Math.cos(ang)*11, vy:Math.sin(ang)*11}});
        fire(a);
        if(ply.pw === 'triple') {{ fire(a + 0.25); fire(a - 0.25); }}
    }};

    function spawnExplosion(x, y, color, count=12) {{
        for(let i=0; i<count; i++) {{
            pX.push({{ x: x, y: y, vx: (Math.random()-0.5)*10, vy: (Math.random()-0.5)*10, life: 20, col: color, s: Math.random()*4+2 }});
        }}
    }}

    function isCol(x,y,s,ws){{
        for(let w of ws){{ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; }}
        return false;
    }}

    function initMap() {{
        wls=[]; for(let i=0; i<6; i++){{
            let w=Math.random()*60+40, h=Math.random()*60+40, x=Math.random()*480+40, y=Math.random()*280+40;
            if(Math.sqrt((x-ply.x)**2+(y-ply.y)**2)>120) wls.push({{x,y,w,h}});
        }}
    }}

    function spawnItem() {{
        let rx, ry;
        for(let i=0; i<20; i++) {{ // Mencoba mencari tempat kosong 20x
            rx = Math.random()*540+30; ry = Math.random()*340+30;
            if(!isCol(rx, ry, 20, wls)) {{
                itms.push({{x:rx, y:ry, t:Math.random()<0.5?'speed':'triple'}});
                return;
            }}
        }}
    }}

    function update() {{
        if(go) return; 
        if(sk>0) sk--;
        
        // Spawn Kroco
        if(enms.length < 5) {{
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!isCol(rx,ry,20,wls) && Math.sqrt((rx-ply.x)**2+(ry-ply.y)**2)>180){{
                let r=Math.random(), t=r<0.5?{{c:'#e74c3c',s:20,sp:1.5,h:5,sc:10}}:(r<0.8?{{c:'#2ecc71',s:15,sp:2.2,h:3,sc:15}}:{{c:'#9b59b6',s:30,sp:0.8,h:15,sc:25}});
                enms.push({{x:rx,y:ry,...t}});
            }}
        }}

        // Player Move
        let curS = (ply.pw==='speed')?ply.spd*1.7:ply.spd, nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=curS; if(ks["KeyS"]) ny+=curS; if(ks["KeyA"]) nx-=curS; if(ks["KeyD"]) nx+=curS;
        if(!isCol(nx,ny,ply.s,wls)){{ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }}
        
        if(ply.inv>0) ply.inv--;
        if(ply.pT>0) {{ 
            ply.pT--; 
            pInf.innerText = "BUFF: " + ply.pw.toUpperCase() + " (" + Math.ceil(ply.pT/60) + "s)";
            if(ply.pT<=0) {{ ply.pw=null; pInf.innerText = ""; }}
        }}

        // AI Musuh (Kroco) Anti-Stuck
        enms.forEach(e=>{{
            let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy);
            let vx=(dx/d)*e.sp, vy=(dy/d)*e.sp;
            
            // Mencoba gerak X dan Y secara terpisah agar tidak mudah nyangkut
            if(!isCol(e.x+vx, e.y, e.s/2, wls)) e.x += vx;
            else {{ // Jika nyangkut di X, mencoba geser sedikit
                e.y += (Math.random()-0.5)*2; 
            }}
            
            if(!isCol(e.x, e.y+vy, e.s/2, wls)) e.y += vy;
            else {{ // Jika nyangkut di Y, mencoba geser sedikit
                e.x += (Math.random()-0.5)*2;
            }}

            if(ply.inv<=0 && Math.sqrt((e.x-ply.x)**2+(e.y-ply.y)**2)<(e.s/2+ply.s)){{ 
                li--; ply.inv=60; spawnExplosion(ply.x,ply.y,"#f00",20); if(li<=0) go=true; 
            }}
        }});

        // Boss logic
        if(boss){{
            let dx=ply.x-boss.x, dy=ply.y-boss.y, d=Math.sqrt(dx*dx+dy*dy);
            let vx=(dx/d)*boss.sp, vy=(dy/d)*boss.sp;
            if(!isCol(boss.x+vx, boss.y, boss.s/2, wls)) boss.x+=vx;
            if(!isCol(boss.x, boss.y+vy, boss.s/2, wls)) boss.y+=vy;
            
            boss.fT++; boss.sT++;
            if(boss.fT > 100){{
                for(let a=0; a<Math.PI*2; a+=0.6) ebuls.push({{x:boss.x+boss.s/2, y:boss.y+boss.s/2, vx:Math.cos(a)*5, vy:Math.sin(a)*5}});
                boss.fT=0;
            }}
            if(boss.sT > 300){{
                boss.sh=true; if(boss.h < boss.mH) boss.h += 0.2;
                if(boss.sT > 450) {{ boss.sh=false; boss.sT=0; }}
            }}
        }}

        // Projectiles & Collision
        buls.forEach((b,i)=>{{
            b.x+=b.vx; b.y+=b.vy;
            if(isCol(b.x,b.y,4,wls) || b.x<0 || b.x>600 || b.y<0 || b.y>400) {{ buls.splice(i,1); return; }}
            
            if(boss && b.x>boss.x && b.x<boss.x+boss.s && b.y>boss.y && b.y<boss.y+boss.s){{
                if(!boss.sh){{ boss.h-=5; spawnExplosion(b.x,b.y,"#ffa500",5); if(boss.h<=0){{sc+=1000; boss=null;}} }}
                buls.splice(i,1); return;
            }}

            enms.forEach((e,ei)=>{{
                if(b.x>e.x-e.s/2 && b.x<e.x+e.s/2 && b.y>e.y-e.s/2 && b.y<e.y+e.s/2){{
                    e.h-=5; buls.splice(i,1);
                    if(e.h<=0){{ 
                        sc+=e.sc; spawnExplosion(e.x, e.y, e.c, 20); enms.splice(ei,1); 
                        if(sc >= 500 && !boss) boss={{x:300,y:50,s:60,h:500,mH:500,sp:0.7,fT:0,sT:0,sh:false}};
                    }}
                }}
            }});
        }});

        ebuls.forEach((eb,i)=>{{
            eb.x+=eb.vx; eb.y+=eb.vy;
            if(Math.sqrt((eb.x-ply.x)**2+(eb.y-ply.y)**2)<ply.s && ply.inv<=0){{ li--; ply.inv=60; ebuls.splice(i,1); if(li<=0) go=true; }}
            if(eb.x<0||eb.x>600||eb.y<0||eb.y>400) ebuls.splice(i,1);
        }});

        itms.forEach((it,i)=>{{ if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){{ ply.pw=it.t; ply.pT=450; itms.splice(i,1); spawnExplosion(it.x,it.y,"#fff",10); }} }});
        pX.forEach((p,i)=>{{ p.x+=p.vx; p.y+=p.vy; p.life--; if(p.life<=0) pX.splice(i,1); }});

        uiS.innerText = "Skor: " + sc;
        let hText = ""; for(let i=0; i<li; i++) hText += "❤️";
        uiH.innerText = "Nyawa: " + hText;
    }}

    function draw() {{
        ctx.save(); if(sk>0) ctx.translate((Math.random()-0.5)*sk, (Math.random()-0.5)*sk);
        ctx.clearRect(0,0,600,400);
        ctx.fillStyle="#444"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,10,0,7); ctx.fill(); }});
        
        enms.forEach(e=>{{ 
            ctx.fillStyle=e.c; 
            ctx.fillRect(e.x-e.s/2, e.y-e.s/2, e.s, e.s); 
        }});

        if(boss){{
            if(boss.sh){{ ctx.strokeStyle="#0f0"; ctx.lineWidth=4; ctx.beginPath(); ctx.arc(boss.x+boss.s/2,boss.y+boss.s/2,50,0,7); ctx.stroke(); }}
            ctx.fillStyle="#e74c3c"; ctx.fillRect(boss.x,boss.y,boss.s,boss.s);
            ctx.fillStyle="#333"; ctx.fillRect(boss.x, boss.y-15, boss.s, 8);
            ctx.fillStyle="#f00"; ctx.fillRect(boss.x, boss.y-15, (boss.h/boss.mH)*boss.s, 8);
        }}
        
        ctx.fillStyle="#f1c40f"; buls.forEach(b=>{{ ctx.beginPath(); ctx.arc(b.x,b.y,4,0,7); ctx.fill(); }});
        ctx.fillStyle="#ff4757"; ebuls.forEach(eb=>{{ ctx.beginPath(); ctx.arc(eb.x,eb.y,6,0,7); ctx.fill(); }});
        pX.forEach(p=>{{ ctx.fillStyle=p.col; ctx.globalAlpha=p.life/20; ctx.fillRect(p.x,p.y,p.s,p.s); }});
        ctx.globalAlpha=1;
        if(ply.inv%10<5){{ ctx.fillStyle=ply.col; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill(); }}
        ctx.restore(); update();
        if(go){{ ctx.fillStyle="#fff"; ctx.font="40px Arial"; ctx.fillText("GAME OVER",180,200); return; }}
        requestAnimationFrame(draw);
    }}

    initMap();
    setInterval(spawnItem, 6000);
    draw();
</script>
"""

cp.html(game_html, height=600)
