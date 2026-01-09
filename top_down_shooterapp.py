import streamlit as st
import streamlit.components.v1 as cp

st.set_page_config(page_title="Island.io: Chaos Mode", layout="centered")
st.title("💀 Island.io: Chaos Boss Battle")
st.write("Waspada! Boss sekarang sangat tebal dan Kroco tetap muncul!")

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
    let sc=0, li=3, go=false, ks={}, mX=0, mY=0, ply={x:300,y:200,s:12,inv:0,pw:null,pT:0, ult:0, ultA:false, ultT:0}, buls=[], ebuls=[], enms=[], wls=[], itms=[], boss=null, sk=0;

    window.onkeydown=(e)=>ks[e.code]=true; window.onkeyup=(e)=>ks[e.code]=false;
    cv.onmousemove=(e)=>{let r=cv.getBoundingClientRect(); mX=e.clientX-r.left; mY=e.clientY-r.top};
    cv.onmousedown=()=>{
        if(go) return; let a=Math.atan2(mY-ply.y, mX-ply.x);
        const sh=(ng)=>buls.push({x:ply.x, y:ply.y, vx:Math.cos(ng)*10, vy:Math.sin(ng)*10});
        sh(a); if(ply.pw==='triple'){ sh(a+0.2); sh(a-0.2); }
    };

    function col(x,y,s,ws){ for(let w of ws){ if(x>w.x-s && x<w.x+w.w+s && y>w.y-s && y<w.y+w.h+s) return true; } return false; }
    function spE(){
        let ok=false; while(!ok){
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!col(rx,ry,15,wls) && Math.sqrt((rx-ply.x)**2+(ry-
