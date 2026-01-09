import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Explosive", layout="centered")
st.title("💥 Island.io: Explosive Edition")

# Inisialisasi Karakter
if "char" not in st.session_state:
    st.session_state.char = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Assault (Balanced)"):
        st.session_state.char = {"type": "Assault", "hp": 3, "speed": 4.6, "color": "#00a2e8"}
with col2:
    if st.button("🟢 Tank (Heavy HP)"):
        st.session_state.char = {"type": "Tank", "hp": 6, "speed": 3.2, "color": "#2ecc71"}
with col3:
    if st.button("🟡 Scout (Super Fast)"):
        st.session_state.char = {"type": "Scout", "hp": 2, "speed": 6.5, "color": "#f1c40f"}

if not st.session_state.char:
    st.info("Pilih karakter untuk memulai aksi!")
    st.stop()

c = st.session_state.char

game_html = f"""
<div style="text-align:center; background:#111; padding:15px; border-radius:15px; border: 2px solid #333;">
    <h2 id="s" style="color:white; margin:0; font-family:Arial;">Skor: 0 | Nyawa: </h2>
    <p id="p-info" style="color:#f1c40f; font-weight:bold; margin:5px 0; height:20px; font-family:Courier;"></p>
    <canvas id="c" width="600" height="400" style="background:#0a0a0a; cursor:crosshair; border-radius:5px;"></canvas>
</div>

<script>
    const cv=document.getElementById("c"), ctx=cv.getContext("2d"), stB=document.getElementById("s"), pInf=document.getElementById("p-info");
    let sc=0, li={c['hp']}, go=false, ks={{}}, buls=[], ebuls=[], enms=[], wls=[], itms=[], pX=[], boss=null, sk=0;
    let ply={{x:300,y:200,s:12,inv:0,pw:null,pT:0,spd:{c['speed']},col:'{c['color']}'}};

    window.onkeydown=(e)=>ks[e.code]=true; window.onkeyup=(e)=>ks[e.code]=false;
    
    cv.onmousedown=(e)=>{{
        if(go) return; 
        let r=cv.getBoundingClientRect(), a=Math.atan2((e.clientY-r.top)-ply.y, (e.clientX-r.left)-ply.x);
        const fire = (ang) => buls.push({{x:ply.x, y:ply.y, vx:Math.cos(ang)*11, vy:Math.sin(ang)*11}});
        fire(a);
        if(ply.pw === 'triple') {{ fire(a + 0.2); fire(a - 0.2); }}
    }};

    function spawnExplosion(x, y, color, count=10) {{
        for(let i=0; i<count; i++) {{
            pX.push({{
                x: x, y: y,
                vx: (Math.random()-0.5)*6,
                vy: (Math.random()-0.5)*6,
                life: 30 + Math.random()*20,
                col: color,
                s: Math.random()*4+1
            }});
        }}
    }}

    function col(x,y,s,ws){{ for(let w of ws){{ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; }} return false; }}

    function initLevel(){{
        wls=[]; for(let i=0; i<5; i++){{
            let w=Math.random()*60+40, h=Math.random()*60+40, x=Math.random()*500+50, y=Math.random()*300+50;
            if(Math.sqrt((x-ply.x)**2+(y-ply.y)**2)>100) wls.push({{x,y,w,h}});
        }}
    }}

    function spawnEnemy(){{
        let rx=Math.random()*560+20, ry=Math.random()*360+20;
        if(!col(rx,ry,15,wls) && Math.sqrt((rx-ply.x)**2+(ry-ply.y)**2)>150){{
            let r=Math.random(), t=r<0.5?{{c:'#e74c3c',s:20,sp:1.6,h:5,sc:5}}:(r<0.8?{{c:'#2ecc71',s:14,sp:2.2,h:3,sc:10}}:{{c:'#9b59b6',s:35,sp:0.9,h:15,sc:20}});
            enms.push({{x:rx,y:ry,...t}});
        }}
    }}

    function update(){{{
        if(go) return; if(sk>0) sk--;
        if(enms.length < 5) spawnEnemy();
        
        let curSpd = (ply.pw === 'speed') ? ply.spd * 1.7 : ply.spd;
        let nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=curSpd; if(ks["KeyS"]) ny+=curSpd; if(ks["KeyA"]) nx-=curSpd; if(ks["KeyD"]) nx+=curSpd;
        if(!col(nx,ny,ply.s,wls)){{ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }}
        if(ply.inv>0) ply.inv--;
        if(ply.pT > 0) {{ ply.pT--; pInf.innerText = "BUFF: " + ply.pw.toUpperCase() + " (" + Math.ceil(ply.pT/60) + "s)"; if(ply.pT<=0) {{ ply.pw=null; pInf.innerText=""; }} }}

        itms.forEach((it, i) => {{
            if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2) < 25) {{ ply.pw=it.t; ply.pT=450; itms.splice(i, 1); spawnExplosion(it.x, it.y, "#fff", 15); sk=5; }}
        }});

        buls.forEach((b,i)=>{{
            b.x+=b.vx; b.y+=b.vy;
            if(col(b.x,b.y,4,wls) || b.x<0 || b.x>600 || b.y<0 || b.y>400) buls.splice(i,1);
            enms.forEach((e,ei)=>{{
                if(b.x>e.x && b.x<e.x+e.s && b.y>e.y && b.y<e.y+e.s){{
                    e.h-=5; buls.splice(i,1);
                    spawnExplosion(b.x, b.y, "#ffa500", 5);
                    if(e.h<=0){{ 
                        sc+=e.sc; spawnExplosion(e.x+e.s/2, e.y+e.s/2, e.c, 20); 
                        enms.splice(ei,1); sk=10;
                        if(sc%100===0 && !boss) {{ boss={{x:300,y:50,s:60,h:400,mH:400,sp:0.8,fT:0}}; initLevel(); }}
                    }}
                }}
            }});
        }});

        pX.forEach((p, i) => {{
            p.x += p.vx; p.y += p.vy; p.life--;
            if(p.life <= 0) pX.splice(i, 1);
        }});

        enms.forEach(e=>{{
            let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy);
            e.x+=(dx/d)*e.sp; e.y+=(dy/d)*e.sp;
            if(ply.inv<=0 && Math.sqrt((e.x+e.s/2-ply.x)**2+(e.y+e.s/2-ply.y)**2)<(e.s/2+ply.s)){{ li--; ply.inv=60; sk=20; spawnExplosion(ply.x, ply.y, "#ff0000", 25); if(li<=0) go=true; }}
        }});

        if(boss){{
            let dx=ply.x-boss.x, dy=ply.y-boss.y, d=Math.sqrt(dx*dx+dy*dy);
            boss.x+=(dx/d)*boss.sp; boss.y+=(dy/d)*boss.sp;
            boss.fT++; if(boss.fT > 100) {{ spawnExplosion(boss.x+30, boss.y+30, "#ff4500", 40); sk=15; boss.fT=0; }}
        }}

        let hearts = ""; for(let i=0; i<li; i++) hearts += "❤️";
        stB.innerHTML = "Skor: " + sc + " | Nyawa: " + hearts;
    }}}

    function draw(){{{
        ctx.save();
        if(sk > 0) ctx.translate((Math.random()-0.5)*sk, (Math.random()-0.5)*sk);
        ctx.clearRect(0,0,600,400); 
        ctx.fillStyle="#444"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,10,0,7); ctx.fill(); }});
        enms.forEach(e=>{{ ctx.fillStyle=e.c; ctx.fillRect(e.x,e.y,e.s,e.s); }});
        if(boss){{ ctx.fillStyle="#e74c3c"; ctx.fillRect(boss.x,boss.y,boss.s,boss.s); }}
        pX.forEach(p=>{{ ctx.fillStyle=p.col; ctx.globalAlpha=p.life/50; ctx.fillRect(p.x,p.y,p.s,p.s); }});
        ctx.globalAlpha=1;
        ctx.fillStyle="#f1c40f"; buls.forEach(b=>{{ ctx.beginPath(); ctx.arc(b.x,b.y,4,0,7); ctx.fill(); }});
        if(ply.inv%10<5){{ ctx.fillStyle=ply.col; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill(); }}
        ctx.restore();
        update(); requestAnimationFrame(draw);
    }}}

    initLevel(); setInterval(()=>{{ if(itms.length<2) itms.push({{x:Math.random()*540+30, y:Math.random()*340+30, t:Math.random()<0.5?'speed':'triple'}}); }}, 6000); draw();
</script>
"""

cp.html(game_html, height=600)
