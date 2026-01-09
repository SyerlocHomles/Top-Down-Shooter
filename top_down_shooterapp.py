import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Final Stable", layout="centered")
st.title("⚔️ Island.io: Character Select")

# 1. Pilih Karakter
if "char" not in st.session_state:
    st.session_state.char = None

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Assault"):
        st.session_state.char = {"hp": 3, "spd": 4.6, "col": "#00a2e8", "name": "Assault"}
with col2:
    if st.button("🟢 Tank"):
        st.session_state.char = {"hp": 6, "spd": 3.2, "col": "#2ecc71", "name": "Tank"}
with col3:
    if st.button("🟡 Scout"):
        st.session_state.char = {"hp": 2, "spd": 6.5, "col": "#f1c40f", "name": "Scout"}

if not st.session_state.char:
    st.info("Pilih kelas karaktermu untuk memulai!")
    st.stop()

c = st.session_state.char
st.success(f"Mode: {c['name']} | Darah: {c['hp']} | Klik Layar untuk Tembak!")

# 2. HTML & CSS
game_html = """
<div style="text-align:center; background:#111; padding:15px; border-radius:15px;">
    <h2 id="s" style="color:white; margin:0; font-family:sans-serif;">Skor: 0 | Nyawa: </h2>
    <div style="width:200px; height:12px; background:#333; margin:10px auto; border-radius:6px; overflow:hidden; border:1px solid #555;">
        <div id="uF" style="width:0%; height:100%; background:#9b59b6;"></div>
    </div>
    <canvas id="c" width="600" height="400" style="border:4px solid #444; background:#0a0a0a; cursor:crosshair; border-radius:5px;"></canvas>
</div>

<script>
    // Ambil data dari Python via string replacement sederhana agar tidak error
    const P_HP = """ + str(c['hp']) + """;
    const P_SPD = """ + str(c['spd']) + """;
    const P_COL = '""" + str(c['col']) + """';

    const cv=document.getElementById("c"), ctx=cv.getContext("2d"), stB=document.getElementById("s"), uF=document.getElementById("uF");
    let sc=0, li=P_HP, go=false, ks={}, ply={x:300,y:200,s:12,inv:0,pw:null,pT:0,ult:0,ultA:false,ultT:0}, buls=[], ebuls=[], enms=[], wls=[], itms=[], boss=null, sk=0;

    window.onkeydown=(e)=>ks[e.code]=true; window.onkeyup=(e)=>ks[e.code]=false;
    cv.onmousedown=(e)=>{
        if(go) return; 
        let r=cv.getBoundingClientRect(), a=Math.atan2((e.clientY-r.top)-ply.y, (e.clientX-r.left)-ply.x);
        const sh=(ng)=>buls.push({x:ply.x,y:ply.y,vx:Math.cos(ng)*10,vy:Math.sin(ng)*10});
        sh(a); if(ply.pw==='triple'){ sh(a+0.25); sh(a-0.25); }
    };

    function col(x,y,s,ws){
        for(let i=0; i<ws.length; i++){
            let w=ws[i];
            if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true;
        }
        return false;
    }
    
    function fixS(e){
        let t=0; while(col(e.x,e.y,e.s/2,wls) && t<30){ e.x+=(Math.random()-0.5)*20; e.y+=(Math.random()-0.5)*20; t++; }
    }

    function shufMap(){
        wls=[]; 
        for(let i=0; i<5; i++){
            let w=Math.random()*60+40, h=Math.random()*60+40, x=Math.random()*500+50, y=Math.random()*300+50;
            if(Math.sqrt(Math.pow(x-ply.x,2)+Math.pow(y-ply.y,2))>100) wls.push({x:x,y:y,w:w,h:h});
        }
        enms.forEach(fixS); if(boss) fixS(boss);
    }

    function spE(){
        let ok=false; 
        while(!ok){
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!col(rx,ry,15,wls) && Math.sqrt(Math.pow(rx-ply.x,2)+Math.pow(ry-ply.y,2))>150){
                let r=Math.random();
                let t=r<0.5?{c:'#e74c3c',s:20,sp:1.6,h:5,sc:5}:(r<0.8?{c:'#2ecc71',s:14,sp:2.1,h:3,sc:10}:{c:'#9b59b6',s:35,sp:0.9,h:15,sc:20});
                enms.push({x:rx,y:ry,c:t.c,s:t.s,sp:t.sp,h:t.h,sc:t.sc});
                ok=true;
            }
        }
    }

    function spB(){
        boss={x:300,y:50,s:60,h:350,mH:350,sp:0.8,fT:0,sT:0,sh:false};
        shufMap();
    }

    function move(e){
        let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy);
        let vx=(dx/d)*e.sp, vy=(dy/d)*e.sp;
        if(!col(e.x+vx, e.y+vy, e.s/2, wls)){ e.x+=vx; e.y+=vy; }
        else if(!col(e.x+vx, e.y, e.s/2, wls)) e.x+=vx;
        else if(!col(e.x, e.y+vy, e.s/2, wls)) e.y+=vy;
    }

    function upd(){
        if(go) return;
        if(sk>0) sk--;
        if(enms.length < 5) spE();

        let cs = (ply.pw==='speed') ? P_SPD*1.7 : P_SPD;
        let nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=cs; if(ks["KeyS"]) ny+=cs; if(ks["KeyA"]) nx-=cs; if(ks["KeyD"]) nx+=cs;
        if(!col(nx,ny,ply.s,wls)){
            ply.x=Math.max(ply.s, Math.min(588, nx));
            ply.y=Math.max(ply.s, Math.min(388, ny));
        }

        if(ply.inv>0) ply.inv--;
        if(ply.pT>0) { ply.pT--; if(ply.pT<=0) ply.pw=null; }

        if(!ply.ultA && ply.ult < 100) ply.ult += 0.35;
        if(ks["Space"] && ply.ult >= 100) { ply.ultA = true; ply.ultT = 150; ply.ult = 0; }
        
        buls.forEach((b,i)=>{
            b.x+=b.vx; b.y+=b.vy;
            if(col(b.x,b.y,4,wls) || b.x<0 || b.x>600 || b.y<0 || b.y>400){ buls.splice(i,1); return; }
            if(boss && b.x>boss.x && b.x<boss.x+boss.s && b.y>boss.y && b.y<boss.y+boss.s){
                if(!boss.sh){ boss.h-=5; if(boss.h<=0){ sc+=1000; boss=null; } }
                buls.splice(i,1);
            }
            enms.forEach((e,ei)=>{
                if(b.x>e.x && b.x<e.x+e.s && b.y>e.y && b.y<e.y+e.s){
                    e.h-=5; buls.splice(i,1);
                    if(e.h<=0){ sc+=e.sc; enms.splice(ei,1); if(sc%100===0 && !boss) spB(); }
                }
            });
        });

        ebuls.forEach((eb,i)=>{
            eb.x+=eb.vx; eb.y+=eb.vy;
            if(col(eb.x,eb.y,5,wls) || eb.x<0 || eb.x>600 || eb.y<0 || eb.y>400){ ebuls.splice(i,1); return; }
            if(ply.inv<=0 && Math.sqrt(Math.pow(eb.x-ply.x,2)+Math.pow(eb.y-ply.y,2))<ply.s){
                li--; ply.inv=60; sk=12; ebuls.splice(i,1); if(li<=0) go=true;
            }
        });

        if(boss){
            move(boss); boss.fT++; boss.sT++;
            if(boss.fT > 80) { sk=20; for(let a=0; a<6.2; a+=0.6) ebuls.push({x:boss.x+boss.s/2,y:boss.y+boss.s/2,vx:Math.cos(a)*5,vy:Math.sin(a)*5}); boss.fT = 0; }
            if(boss.sT > 200) { boss.sh = true; if(boss.h < boss.mH) boss.h += 0.4; if(boss.sT > 300) { boss.sh = false; boss.sT = 0; } }
            if(boss.fT % 20 === 0) { let a=Math.atan2(ply.y-boss.y, ply.x-boss.x); ebuls.push({x:boss.x+boss.s/2,y:boss.y+boss.s/2,vx:Math.cos(a)*8,vy:Math.sin(a)*8}); }
        }

        enms.forEach(e=>{
            move(e);
            if(ply.inv<=0 && Math.sqrt(Math.pow(e.x+e.s/2-ply.x,2)+Math.pow(e.y+e.s/2-ply.y,2))<(e.s/2+ply.s)){
                li--; ply.inv=60; sk=10; if(li<=0) go=true;
            }
        });

        let hearts = ""; for(let i=0; i<li; i++) hearts += "❤️";
        stB.innerHTML = "Skor: " + sc + " | Nyawa: " + hearts;
        uF.style.width = ply.ult + "%";
        if(go) { ctx.fillStyle="white"; ctx.font="40px Arial"; ctx.fillText("GAME OVER", 180, 200); }
    }

    function drw(){
        ctx.save();
        if(sk > 0) ctx.translate(Math.random()*sk-sk/2, Math.random()*sk-sk/2);
        ctx.clearRect(0,0,600,400);
        ctx.fillStyle="#444"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,12,0,7); ctx.fill(); });
        enms.forEach(e=>{ ctx.fillStyle=e.c; ctx.fillRect(e.x,e.y,e.s,e.s); });
        
        if(boss){
            if(boss.sh) { ctx.strokeStyle="#2ecc71"; ctx.lineWidth=6; ctx.beginPath(); ctx.arc(boss.x+boss.s/2, boss.y+boss.s/2, boss.s/1.1, 0, 7); ctx.stroke(); }
            ctx.fillStyle="#e74c3c"; ctx.fillRect(boss.x,boss.y,boss.s,boss.s);
            ctx.fillStyle="#2ecc71"; ctx.fillRect(boss.x,boss.y-15,(boss.h/boss.mH)*boss.s,10);
        }

        if(ply.ultA){
            let target = boss || enms[0];
            if(target){
                ctx.strokeStyle = "#9b59b6"; ctx.lineWidth = 8; ctx.beginPath();
                ctx.moveTo(ply.x, ply.y); ctx.lineTo(target.x+target.s/2, target.y+target.s/2); ctx.stroke();
                target.h -= 1.5; ply.ultT--; if(ply.ultT<=0) ply.ultA=false;
            }
        }

        ctx.fillStyle="#f1c40f"; buls.forEach(b=>{ ctx.beginPath(); ctx.arc(b.x,b.y,4,0,7); ctx.fill(); });
        ctx.fillStyle="#ff4757"; ebuls.forEach(eb=>{ ctx.beginPath(); ctx.arc(eb.x,eb.y,6,0,7); ctx.fill(); });
        if(ply.inv%10<5){ ctx.fillStyle=P_COL; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill(); }
        ctx.restore(); upd(); requestAnimationFrame(drw);
    }

    shufMap(); 
    for(let i=0; i<5; i++) spE();
    setInterval(() => { if(itms.length<2) itms.push({x:Math.random()*540+30, y:Math.random()*340+30, t:Math.random()<0.5?'speed':'triple'}); }, 7000);
    drw();
</script>
"""

cp.html(game_html, height=550)
