import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Boss Hunt", layout="centered")
st.title("👹 Island.io: Nightmare Boss")
st.write("Skor 100 = BOSS MUNCUL! (Gunakan Triple Shot Biru)")

gh = """
<div style="text-align:center; background:#111; padding:10px; border-radius:10px;">
    <h2 id="s" style="color:white; margin:0;">Skor: 0 | Nyawa: ❤️❤️❤️</h2>
    <canvas id="c" width="600" height="400" style="border:3px solid #444; background:#1a1a1a; cursor:crosshair;"></canvas>
</div>
<script>
    const cv=document.getElementById("c"), ctx=cv.getContext("2d"), stB=document.getElementById("s");
    let sc=0, li=3, go=false, ks={}, mX=0, mY=0, ply={x:300,y:200,s:12,inv:0,pw:null,pT:0}, buls=[], ebuls=[], enms=[], wls=[], itms=[], boss=null;

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
                let r=Math.random(), t=r<0.6?{c:'#e74c3c',s:20,sp:1.4,h:1,sc:5}:(r<0.85?{c:'#2ecc71',s:15,sp:2.6,h:1,sc:10}:{c:'#9b59b6',s:30,sp:0.9,h:3,sc:20});
                enms.push({x:rx,y:ry,...t,m:'sk',tT:0,d:{x:0,y:0}}); ok=true;
            }
        }
    }
    function spB(){ boss={x:50,y:50,s:55,h:25,mH:25,sp:0.8,m:'sk',tT:0,d:{x:0,y:0},fT:0}; enms=[]; }
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
        if(go) return; let cs=ply.pw==='speed'?7.5:4.2, nx=ply.x, ny=ply.y;
        if(ks["KeyW"]) ny-=cs; if(ks["KeyS"]) ny+=cs; if(ks["KeyA"]) nx-=cs; if(ks["KeyD"]) nx+=cs;
        if(!col(nx,ny,ply.s,wls)){ ply.x=Math.max(ply.s,Math.min(588,nx)); ply.y=Math.max(ply.s,Math.min(388,ny)); }
        if(ply.inv>0) ply.inv--; if(ply.pT>0 && --ply.pT<=0) ply.pw=null;

        itms.forEach((it,i)=>{ if(Math.sqrt((it.x-ply.x)**2+(it.y-ply.y)**2)<25){ ply.pw=it.t; ply.pT=350; itms.splice(i,1); }});
        buls.forEach((b,i)=>{
            b.x+=b.vx; b.y+=b.vy; if(col(b.x,b.y,2,wls)||b.x<0||b.x>600||b.y<0||b.y>400) buls.splice(i,1);
            if(boss && b.x>boss.x && b.x<boss.x+boss.s && b.y>boss.y && b.y<boss.y+boss.s){ boss.h--; buls.splice(i,1); if(boss.h<=0){ sc+=150; boss=null; for(let j=0; j<4; j++) spE(); }}
            enms.forEach((e,ei)=>{ if(b.x>e.x && b.x<e.x+e.s && b.y>e.y && b.y<e.y+e.s){ e.h--; buls.splice(i,1); if(e.h<=0){ sc+=e.sc; enms.splice(ei,1); if(sc%100===0) spB(); else spE(); }}});
        });

        ebuls.forEach((eb,i)=>{ eb.x+=eb.vx; eb.y+=eb.vy; if(eb.x<0||eb.x>600||eb.y<0||eb.y>400) ebuls.splice(i,1); if(ply.inv<=0 && Math.sqrt((eb.x-ply.x)**2+(eb.y-ply.y)**2)<ply.s){ li--; ply.
