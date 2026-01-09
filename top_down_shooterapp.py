import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Island Shooter 2D", layout="centered")

st.title("🛡️ Island Defender 2D")
st.write("Gunakan **W, A, S, D** untuk bergerak dan **SPASI** untuk menembak!")

# Koding Game dalam HTML & JavaScript (Biar Smooth tanpa Loading)
game_html = """
<canvas id="gameCanvas" width="600" height="400" style="border:5px solid #000; background: #fff;"></canvas>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    // Properti Game
    let player = { x: 100, y: 300, size: 25, color: "#00a2e8" };
    let bullets = [];
    let enemies = [{ x: 500, y: 50, size: 30, color: "#ed1c24" }];
    let walls = [
        { x: 0, y: 0, w: 200, h: 100 }, // Bangunan kiri atas
        { x: 250, y: 150, w: 100, h: 100 } // Bangunan tengah
    ];
    let keys = {};

    // Kontrol Keyboard
    window.addEventListener("keydown", (e) => keys[e.code] = true);
    window.addEventListener("keyup", (e) => keys[e.code] = false);

    function update() {
        let nextX = player.x;
        let nextY = player.y;

        if (keys["KeyW"]) nextY -= 4;
        if (keys["KeyS"]) nextY += 4;
        if (keys["KeyA"]) nextX -= 4;
        if (keys["KeyD"]) nextX += 4;
        if (keys["Space"]) {
            if (bullets.length < 5) { // Batasi jumlah peluru
                bullets.push({ x: player.x + 10, y: player.y, speed: 7 });
                keys["Space"] = false; // Mencegah spam
            }
        }

        // Cek Tabrakan Bangunan
        let hitWall = false;
        walls.forEach(w => {
            if (nextX < w.x + w.w && nextX + player.size > w.x &&
                nextY < w.y + w.h && nextY + player.size > w.y) {
                hitWall = true;
            }
        });

        if (!hitWall) {
            player.x = nextX;
            player.y = nextY;
        }

        // Update Peluru
        bullets.forEach((b, index) => {
            b.x += b.speed;
            if (b.x > canvas.width) bullets.splice(index, 1);
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Gambar Bangunan
        ctx.fillStyle = "#000";
        walls.forEach(w => ctx.fillRect(w.x, w.y, w.w, w.h));

        // Gambar Musuh
        ctx.fillStyle = "#ed1c24";
        enemies.forEach(e => ctx.fillRect(e.x, e.y, e.size, e.size));

        // Gambar Peluru
        ctx.fillStyle = "orange";
        bullets.forEach(b => ctx.beginPath() || ctx.arc(b.x, b.y, 5, 0, Math.PI*2) || ctx.fill());

        // Gambar Player (Biru)
        ctx.fillStyle = player.color;
        ctx.beginPath();
        ctx.arc(player.x + 12, player.y + 12, 12, 0, Math.PI*2);
        ctx.fill();

        update();
        requestAnimationFrame(draw);
    }

    draw();
</script>
"""

# Masukkan kode HTML tadi ke Streamlit
components.html(game_html, height=450)

st.success("TIPS: Klik pada area kotak putih sebelum mulai menggerakkan karakter!")
