import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Boss Edition", layout="centered")
st.title("👾 Island.io: Boss & Elite Waves")
st.write("Kalahkan musuh untuk memicu BOSS setiap skor 100!")

game_html = """
<div style="text-align:center; position:relative;">
    <h2 id="st" style="color: white; background: rgba(0,0,0,0.5); padding: 5px; border-radius: 5px; display: inline-block;">Skor: 0 | Nyawa: ❤️❤️❤️</h2>
    <canvas id="gC" width="600" height="400" style="border:5px solid #2c3e50; background:#222; border-radius:10px; cursor:crosshair;"></canvas>
    <div id="gO" style="display:none; position:absolute; top:100px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.9); color:white; padding:30px; border-radius:15px; border:3px solid red; z-index:100;">
        <h1 id="goMsg">GAME OVER! 💀</h1>
        <button onclick="location.reload()" style="padding:10px 20px; font-size:18px; cursor:pointer; background:#27ae60; color:white; border:none; border-radius:5px;">MAIN LAGI 🔄</button>
    </div>
</div>
<script>
    const cvs=document.getElementById("gC"), ctx=cvs.getContext("2d"), stB=document.getElementById("st"), gOS=document.getElementById("gO");
    let sc=0, li=3, isGO=false, ks={}, mX=0, mY=0, ply={x:300, y:200, s:12, inv:0, pwr:null, pT:0}, buls=[], ebuls=[], enms=[], wls=[], itms=[], boss=null;

    window.onkeydown=(e)=>ks[e.code]=true; window.onkeyup=(e)=>ks[e.code]=false;
    cvs.onmousemove=(e)=>{ const r=cvs.getBoundingClientRect(); mX=e.clientX-r.left; mY=e.clientY-r.top; };
    cvs.onmousedown=()=>{
        if(isGO) return; let a=Math.atan2(mY-ply.y, mX-ply.x);
        const sh=(ang)=>buls.push({x:ply.x, y:ply.y, vx:Math.cos(ang)*10, vy:Math.sin(ang)*10});
        sh(a); if(ply.pwr==='triple'){ sh(a+0.2); sh(a-0.2); }
    };

    function col(x,y,s,ws){ for(let w of ws){ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; } return false; }

    function spE() {
        if(boss) return;
        let ok=false; while(!ok){
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!col(rx,ry,15,wls) && Math.sqrt((rx-ply.x)**2+(ry-ply.y)**2)>150){
                let r = Math.random();
                let type = r < 0.6 ? {c:'#e74c3c', s:20, sp:1.2, h:1, sc:5} : (r < 0.85 ? {c:'#2ecc71', s:15, sp:2.2, h:1, sc:10} : {c:'#9b59b6', s:30, sp:0.8, h:3, sc:20});
                enms.push({x:rx, y:ry, ...type, m:'sk', tT:0, d:{x:0,y:0}}); ok=true;
            }
        }
    }

    function spB() {
        boss = {x:300, y:50, s:60, h:20, maxH:20, d:{x:2, y:0}, fT:0};
        enms = []; // Bersihkan kroco saat boss muncul
    }

    function spI(){ let t=Math.random()<0.5?'speed':'triple', rx=Math.random()*500+50, ry=Math.random()*300+50; if(!col(rx,ry,10,wls)) itms.push({x:rx, y:ry, t:t}); }

    function init(){
        wls=[]; for(let i=0; i<5; i++){
            let w=Math.random()*80+40, h=Math.random()*80+40, x=Math.random()*500+50, y=Math.random()*300+50;
            if(!(x<350 && x+w>250 && y<250 && y+h>150)) wls.push({x,y,w,h});
        }
        for(let i=0; i<4; i++) spE(); setInterval(spI, 8000);
    }

    function upd(){
        if(isGO) return; 
        let curS=ply.pwr==='speed'?7:4, nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=curS; if(ks["KeyS"]) ny+=curS; if(ks["KeyA"]) nx-=curS; if(ks["KeyD"]) nx+=curS;
        if(!col(nx,ny,ply.s,wls)){ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }
        if(ply.inv>0) ply.inv--; if(ply.pT>0){ ply.pT--; if(ply.pT<=0) ply.pwr=null; }
        
        itms.forEach((it,i)=>{ if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){ ply.pwr=it.t; ply.pT=300; itms.splice(i,1); }});

        buls.forEach((b,i)=>{
            b.x+=b.vx; b.y+=b.vy; if(col(b.x,b.y,2,wls)||b.x<0||b.x>600||b.y<0||b.y>400){ buls.splice(i,1); return; }
            if(boss && b.x>boss.x && b.x<boss.x+boss.s && b.y>boss.y && b.y<boss.y+boss.s) {
                boss.h--; buls.splice(i,1);
                if(boss.h<=0){ sc+=100; boss=null; for(let j=0; j<4; j++) spE(); }
            }
            enms.forEach((e,ei)=>{ if(b.x>e.x && b.x<e.x+e.s && b.y>e.y && b.y<e.y+e.s){
                e.h--; buls.splice(i,1); if(e.h<=0){ sc+=e.sc; enms.splice(ei,1); if(sc%100===0 && sc>0) spB(); else spE(); }
            }});
        });

        ebuls.forEach((eb,i)=>{
            eb.x+=eb.vx; eb.y+=eb.vy; if(eb.x<0||eb.x>600||eb.y<0||eb.y>400) ebuls.splice(i,1);
            if(ply.inv<=0 && Math.sqrt((eb.x-ply.x)**2+(eb.y-ply.y)**2)<ply.s){ li--; ply.inv=60; ebuls.splice(i,1); if(li<=0) isGO=true; }
        });

        if(boss) {
            boss.x += boss.d.x; if(boss.x<0 || boss.x>600-boss.s) boss.d.x *= -1;
            boss.fT++; if(boss.fT > 60) {
                let a = Math.atan2(ply.y-(boss.y+30), ply.x-(boss.x+30));
                ebuls.push({x:boss.x+30, y:boss.y+30, vx:Math.cos(a)*5, vy:Math.sin(a)*5});
                boss.fT = 0;
            }
            if(ply.inv<=0 && ply.x>boss.x && ply.x<boss.x+boss.s && ply.y>boss.y && ply.y<boss.y+boss.s){ li--; ply.inv=60; if(li<=0) isGO=true; }
        }

        enms.forEach(e=>{
            if(e.m==='sk'){
                let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy), vx=(dx/d)*e.sp, vy=(dy/d)*e.sp;
                if(!col(e.x+vx+10,e.y+vy+10,10,wls)){ e.x+=vx; e.y+=vy; } 
                else { e.m='av'; e.tT=40; e.d=Math.abs(dx)>Math.abs(dy)?{x:0,y:dy>0?e.sp:-e.sp}:{x:dx>0?e.sp:-e.sp,y:0}; }
            } else {
                if(!col(e.x+e.d.x+10,e.y+e.d.y+10,10,wls)){ e.x+=e.d.x; e.y+=e.d.y; } else { e.d.x*=-1; e.d.y*=-1; }
                if(--e.tT<=0) e.m='sk';
            }
            if(ply.inv<=0 && Math.sqrt((e.x+e.s/2-ply.x)**2+(e.y+e.s/2-ply.y)**2)<(e.s/2+ply.s)){
                li--; ply.inv=60; if(li<=0) isGO=true;
            }
        });
        if(isGO) gOS.style.display="block";
        stB.innerText=`Skor: ${sc} | Nyawa: ${"❤️".repeat(li)} ${ply.pwr?'| POWER: '+ply.pwr.toUpperCase():''}`;
    }

    function drw(){
        ctx.clearRect(0,0,600,400); ctx.fillStyle="#333"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,8,0,7); ctx.fill(); });
        enms.forEach(e=> { ctx.fillStyle=e.c; ctx.fillRect(e.x,e.y,e.s,e.s); });
        if
