import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Ultimate", layout="centered")
st.title("🔥 Island.io: Ultimate Skill")
st.write("Tekan **SPASI** untuk aktifkan Skill Ultimate (Laser Lock-on)!")

gh = """
<div style="text-align:center; background:#111; padding:10px; border-radius:10px;">
    <h2 id="s" style="color:white; margin:0;">Skor: 0 | Nyawa: ❤️❤️❤️</h2>
    <div id="uBar" style="width:200px; height:10px; background:#444; margin:5px auto; border-radius:5px; overflow:hidden;">
        <div id="uFill" style="width:0%; height:100%; background:#9b59b6; transition: width 0.1s;"></div>
    </div>
    <canvas id="c" width="600" height="400" style="border:3px solid #444; background:#0a0a0a; cursor:crosshair;"></canvas>
</div>
<script>
    const cv=document.getElementById("c"), ctx=cv.getContext("2d"), stB=document.getElementById("s"), uFill=document.getElementById("uFill");
    let sc=0, li=3, go=false, ks={}, mX=0, mY=0, ply={x:300,y:200,s:12,inv:0,pw:null,pT:0, ult:0, ultA:false, ultT:0}, buls=[], ebuls=[], enms=[], wls=[], itms=[], boss=null;

    window.onkeydown=(e)=>ks[e.code]=true; window.onkeyup=(e)=>ks[e.code]=false;
    cv.onmousemove=(e)=>{let r=cv.getBoundingClientRect(); mX=e.clientX-r.left; mY=e.clientY-r.top};
    cv.onmousedown=()=>{
        if(go) return; let a=Math.atan2(mY-ply.y, mX-ply.x);
        const sh=(ng)=>buls.push({x:ply.x, y:ply.y, vx:Math.cos(ng)*10, vy:Math.sin(ng)*10});
        sh(a); if(ply.pw==='triple'){ sh(a+0.2); sh(a-0.2); }
    };

    function col(x,y,s,ws){ for(let w of ws){ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; } return false; }
    function spE(){
        if(boss) return; let ok=false; while(!ok){
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!col(rx,ry,15,wls) && Math.sqrt((rx-ply.x)**2+(ry-ply.y)**2)>150){
                let r=Math.random(), t=r<0.6?{c:'#e74c3c',s:20,sp:1.5,h:5,sc:5}:(r<0.85?{c:'#2ecc71',s:15,sp:2.6,h:5,sc:10}:{c:'#9b59b6',s:30,sp:0.9,h:15,sc:20});
                enms.push({x:rx,y:ry,...t,m:'sk',tT:0,d:{x:0,y:0}}); ok=true;
            }
        }
    }
    function spB(){ boss={x:300,y:50,s:60,h:50,mH:50,sp:0.8,m:'sk',tT:0,d:{x:0,y:0},fT:0,sT:0,sh:false}; enms=[]; }
    function spI(){ let t=Math.random()<0.5?'speed':'triple', rx=Math.random()*500+50, ry=Math.random()*300+50; if(!col(rx,ry,10,wls)) itms.push({x:rx,y:ry,t:t}); }

    function init(){
        wls=[]; for(let i=0; i<4; i++){
            let w=Math.random()*100+50, h=Math.random()*100+50, x=Math.random()*450+50, y=Math.random()*250+50;
            if(!(x<380&&x+w>220&&y<280&&y+h>120)) wls.push({x,y,w,h});
        }
        for(let i=0; i<4; i++) spE(); setInterval(spI, 9000);
    }

    function move(e){
        if(e.m==='sk'){
            let dx=ply.x-e.x, dy=ply.y-e.y, d=Math.sqrt(dx*dx+dy*dy), vx=(dx/d)*e.sp, vy=(dy/d)*e.sp;
            if(!col(e.x+vx+e.s/2, e.y+vy+e.s/2, e.s/2, wls)){ e.x+=vx; e.y+=vy; }
            else { e.m='av'; e.tT=40; e.d=Math.abs(dx)>Math.abs(dy)?{x:0,y:dy>0?e.sp:-e.sp}:{x:dx>0?e.sp:-e.sp,y:0}; }
        } else {
            if(!col(e.x+e.d.x+e.s/2, e.y+e.d.y+e.s/2, e.s/2, wls)){ e.x+=e.d.x; e.y+=e.d.y; } else { e.d.x*=-1; e.d.y*=-1; }
            if(--e.tT<=0) e.m='sk';
        }
    }

    function upd(){
        if(go) return; 
        let cs=ply.pw==='speed'?7.8:4.3, nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=cs; if(ks["KeyS"]) ny+=cs; if(ks["KeyA"]) nx-=cs; if(ks["KeyD"]) nx+=cs;
        if(!col(nx,ny,ply.s,wls)){ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }
        if(ply.inv>0) ply.inv--; if(ply.pT>0 && --ply.pT<=0) ply.pw=null;

        // Ultimate Logic
        if(!ply.ultA && ply.ult < 100) ply.ult += 0.2;
        if(ks["Space"] && ply.ult >= 100) { ply.ultA = true; ply.ultT = 180; ply.ult = 0; }
        if(ply.ultA) { 
            ply.ultT--; if(ply.ultT <= 0) ply.ultA = false; 
            let target = boss || enms[0];
            if(target) {
                if(!boss || !boss.sh) target.h -= 0.2; // Laser damage 1 unit per 5 frames (approx)
                ctx.strokeStyle = "#9b59b6"; ctx.lineWidth = 4; ctx.beginPath();
                ctx.moveTo(ply.x, ply.y); ctx.lineTo(target.x+target.s/2, target.y+target.s/2); ctx.stroke();
                ctx.shadowBlur = 10; ctx.shadowColor = "#9b59b6";
            }
        } else { ctx.shadowBlur = 0; }
        uFill.style.width = ply.ult + "%";

        itms.forEach((it,i)=>{ if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){ ply.pw=it.t; ply.pT=350; itms.splice(i,1); }});
        
        buls.forEach((b,i)=>{
            b.x+=b.vx; b.y+=b.vy; if(col(b.x,b.y,2,wls)||b.x<0||b.x>600||b.y<0||b.y>400){ buls.splice(i,1); return; }
            if(boss && b.x>boss.x && b.x<boss.x+boss.s && b.y>boss.y && b.y<boss.y+boss.s){ 
                if(!boss.sh){ boss.h -= 5; if(boss.h<=0){ sc+=200; boss=null; for(let j=0; j<4; j++) spE(); } }
                buls.splice(i,1);
            }
            enms.forEach((e,ei)=>{ if(b.x>e.x && b.x<e.x+e.s && b.y>e.y && b.y<e.y+e.s){ e.h -= 5; buls.splice(i,1); if(e.h<=0){ sc+=e.sc; enms.splice(ei,1); if(sc>0 && sc%100===0) spB(); else spE(); }}});
        });

        ebuls.forEach((eb,i)=>{ eb.x+=eb.vx; eb.y+=eb.vy; if(eb.x<0||eb.x>600||eb.y<0||eb.y>400) ebuls.splice(i,1); if(ply.inv<=0 && Math.sqrt((eb.x-ply.x)**2+(eb.y-ply.y)**2)<ply.s){ li--; ply.inv=60; ebuls.splice(i,1); if(li<=0) go=true; }});

        if(boss){
            move(boss); boss.fT++; boss.sT++;
            if(boss.fT > 120) { for(let a=0; a<6.2; a+=0.5) ebuls.push({x:boss.x+boss.s/2,y:boss.y+boss.s/2,vx:Math.cos(a)*5,vy:Math.sin(a)*5}); boss.fT = 0; }
            if(boss.sT > 300) { boss.sh = true; if(boss.h < boss.mH) boss.h += 0.05; if(boss.sT > 450) { boss.sh = false; boss.sT = 0; } }
            if(boss.fT % 30 === 0) { let a=Math.atan2(ply.y-boss.y, ply.x-boss.x); ebuls.push({x:boss.x+boss.s/2,y:boss.y+boss.s/2,vx:Math.cos(a)*6,vy:Math.sin(a)*6}); }
            if(ply.inv<=0 && ply.x>boss.x && ply.x<boss.x+boss.s && ply.y>boss.y && ply.y<boss.y+boss.s){ li--; ply.inv=60; if(li<=0) go=true; }
        }
        enms.forEach(e=>{ move(e); if(ply.inv<=0 && Math.sqrt((e.x+e.s/2-ply.x)**2+(e.y+e.s/2-ply.y)**2)<(e.s/2+ply.s)){ li--; ply.inv=60; if(li<=0) go=true; }});
        stB.innerText=`Skor: ${sc} | Nyawa: ${"❤️".repeat(li)} ${ply.pw?'| '+ply.pw.toUpperCase():''}`;
        if(go) { ctx.fillStyle="white"; ctx.font="40px Arial"; ctx.fillText("GAME OVER", 180, 200); }
    }

    function drw(){
        ctx.clearRect(0,0,600,400); ctx.fillStyle="#333"; wls.forEach(w=>ctx.fillRect(w.x,w.y,w.w,w.h));
        itms.forEach(it=>{ ctx.fillStyle=it.t==='speed'?"#f1c40f":"#3498db"; ctx.beginPath(); ctx.arc(it.x,it.y,9,0,7); ctx.fill(); });
        enms.forEach(e=>{ ctx.fillStyle=e.c; ctx.fillRect(e.x,e.y,e.s,e.s); });
        if(boss){ 
            if(boss.sh) { ctx.strokeStyle="#2ecc71"; ctx.lineWidth=4; ctx.beginPath(); ctx.arc(boss.x+boss.s/2, boss.y+boss.s/2, boss.s/1.2, 0, 7); ctx.stroke(); }
            ctx.fillStyle="#e74c3c"; ctx.fillRect(boss.x,boss.y,boss.s,boss.s); 
            ctx.fillStyle="#2ecc71"; ctx.fillRect(boss.x,boss.y-12,(boss.h/boss.mH)*boss.s,6); 
        }
        ctx.fillStyle="#f39c12"; buls.forEach(b=>{ ctx.beginPath(); ctx.arc(b.x,b.y,4,0,7); ctx.fill(); });
        ctx.fillStyle="red"; ebuls.forEach(eb=>{ ctx.beginPath(); ctx.arc(eb.x,eb.y,5,0,7); ctx.fill(); });
        if(ply.inv%10<5){ ctx.fillStyle="#00a2e8"; ctx.beginPath(); ctx.arc(ply.x,ply.y,ply.s,0,7); ctx.fill(); }
        upd(); requestAnimationFrame(drw);
    }
    init(); drw();
</script>
"""
cp.html(gh, height=580)
