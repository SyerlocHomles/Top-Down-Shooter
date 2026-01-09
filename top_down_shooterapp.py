import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island.io: Nightmare Boss", layout="centered")
st.title("👹 Island.io: Boss Unleashed")
st.write("Skor putih di atas! Boss mengejarmu ke mana saja!")

game_html = """
<div style="text-align:center; position:relative;">
    <h2 id="st" style="color:white; background:rgba(0,0,0,0.6); padding:5px 15px; border-radius:10px; display:inline-block; font-family:sans-serif;">Skor: 0 | Nyawa: ❤️❤️❤️</h2>
    <canvas id="gC" width="600" height="400" style="border:5px solid #2c3e50; background:#111; border-radius:10px; cursor:crosshair;"></canvas>
    <div id="gO" style="display:none; position:absolute; top:100px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.9); color:white; padding:30px; border-radius:15px; border:3px solid red; z-index:100;">
        <h1>DIHABISI BOSS! 💀</h1>
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
        if(boss) return; let ok=false; while(!ok){
            let rx=Math.random()*560+20, ry=Math.random()*360+20;
            if(!col(rx,ry,15,wls) && Math.sqrt((rx-ply.x)**2+(ry-ply.y)**2)>150){
                let r=Math.random(), t
