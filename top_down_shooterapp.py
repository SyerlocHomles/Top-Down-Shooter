import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Power-Up", layout="centered")
st.title("🌟 Island.io: Power-Up Chaos")
st.write("Item: ⚡ Kuning (Cepat), 🔫 Biru (Triple Shot)")

game_html = """
<div style="text-align:center; position:relative;">
    <h2 id="st">Skor: 0 | Nyawa: ❤️❤️❤️</h2>
    <canvas id="gC" width="600" height="400" style="border:5px solid #2c3e50; background:#ecf0f1; border-radius:10px; cursor:crosshair;"></canvas>
    <div id="gO" style="display:none; position:absolute; top:100px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.9); color:white; padding:30px; border-radius:15px; border:3px solid red; z-index:100;">
        <h1>GAME OVER! 💀</h1>
        <button onclick="location.reload()" style="padding:10px 20px; font-size:18px; cursor:pointer; background:#27ae60; color:white; border:none; border-radius:5px;">MAIN LAGI 🔄</button>
    </div>
</div>
<script>
    const cvs=document.getElementById("gC"), ctx=cvs.getContext("2d"), stB=document.getElementById("st"), gOS=document.getElementById("gO");
    let sc=0, li=3, isGO=false, ks={}, mX=0, mY=0, ply={x:300, y:200, s:12, inv:0, pwr:null, pT:0}, buls=[], enms=[], wls=[], itms=[];

    window.onkeydown=(e)=>ks[e.code]=true; window.onkeyup=(e)=>ks[e.code]=false;
    cvs.onmousemove=(e)=>{ const r=cvs.getBoundingClientRect(); mX=e.clientX-r.left; mY=e.clientY-r.top; };
    cvs.onmousedown=()=>{
        if(isGO) return; let a=Math.atan2(mY-ply.y, mX-ply.x);
        const sh=(ang)=>buls.push({x:ply.x, y:ply.y, vx:Math.cos(ang)*10, vy:Math.sin(ang)*10});
        sh(a); if(ply.pwr==='triple'){ sh(a+0.2); sh(a-0.2); }
    };

    function col(x,y,s,ws){ for(let w of ws){ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; } return false; }
    function spE(){
        let ok=false; while(!ok){
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!col(rx,ry,15,wls) && Math.sqrt((rx-ply.x)**2+(ry-ply.y)**2)>150){ enms.push({x:rx, y:ry, s:22, m:'sk', tT:0, d:{x:0,y:0}}); ok=true; }
        }
    }
    function spI(){ let t=Math.random()<0.5?'speed':'triple', rx=Math.random()*500+50, ry=Math.random()*300+50; if(!col(rx,ry,10,wls)) itms.push({x:rx, y:ry, t:t}); }

    function init(){
        wls=[]; for(let i=0; i<6; i++){
            let w=Math.random()*80+40, h=Math.random()*80+40, x=Math.random()*500+50, y=Math.random()*300+50;
            if(!(x<350 && x+w>250 && y<250 && y+h>150)) wls.push({x,y,w,h});
        }
        for(let i=0; i<4; i++) spE(); setInterval(spI, 7000);
    }

    function upd(){
        if(isGO) return; let curS=ply.pwr==='speed'?7:4, nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=curS; if(ks["KeyS"]) ny+=curS; if(ks["KeyA"]) nx-=curS; if(ks["KeyD"]) nx+=curS;
        if(!col(nx,ny,ply.s,wls)){ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }
        if(ply.inv>0) ply.inv--; if(ply.pT>0){ ply.pT--; if(ply.pT<=0) ply.pwr=null; }
        
        itms.forEach((it,i)=>{ if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){ ply.pwr=it.t; ply.pT=300; itms.splice(i,1); }});
        buls.forEach((b,i)=>{
            b.x+=b.vx; b.y+=b.vy; if(col(b.x,b.y,2,wls)||b.x<0||b.x>600||b.y<0||b.y>400) buls.splice(i,1);
            enms.forEach((e,ei)=>{ if(b.x>e.x && b.x<e.x+e.s && b.y>e.y && b.y<e.y+e.s){ buls.splice(i,1); enms.splice(ei,1); sc+=10; spE(); }});
        });

        enms.forEach(e=>{
            let s=1.3; if(e.m==='sk'){
                let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy), vx=(dx/d)*s, vy=(dy/d)*s;
                if(!col(e.x+vx+11,e.y+vy+11,11,wls)){ e.x+=vx; e.y+=vy; } 
                else { e.m='av'; e.tT=50; e.d=Math.abs(dx)>Math.abs(dy)?{x:0,y:dy>0?s:-s}:{x:dx>0?s:-s,y:0}; }
            } else {
                if(!col(e.x+e.d.x+11,e.y+e.d.y+11,11,wls)){ e.x+=e.d.x; e.y+=e.d.y; } else { e.d.x*=-1; e.d.y*=-1; }
                if(--e.tT<=0) e.m='sk';
            }
            if(ply.inv<=0 && Math.sqrt((e.x+11-ply.x)**2+(e.y+11-ply.y)**2)<(11+ply.s)){
                li--; ply.inv=60; if(li<=0){ isGO=true; gOS.style.display="block"; }
            }
        });
        stB.innerText=`Skor: ${sc} | Nyawa: ${"❤️".repeat(li)} ${ply.pwr?'| POWER: '+ply.pwr.toUpperCase():''}`;
    }

    function drw(){
        ctx.clearRect(0,0,600,400); ctx.fillStyle="#34495e"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,8,0,7); ctx.fill(); });
        ctx.fillStyle="#e74c3c"; enms.forEach(e=>ctx.fillRect(e.x,e.y,e.s,e.s));
        ctx.fillStyle="#f39c12"; buls.forEach(b=>{ ctx.beginPath(); ctx.arc(b.x,b.y,4,0,7); ctx.fill(); });
        if(ply.inv%10<5){ ctx.fillStyle="#00a2e8"; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill(); }
        upd(); requestAnimationFrame(drw);
    }
    init(); drw();
</script>
"""
components.html(game_html, height=580)
