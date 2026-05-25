import streamlit as st
import random

# =========================
# CONFIG (FORCE FULL WIDE)
# =========================
st.set_page_config(page_title="RPG LEGEND ULTIMATE", page_icon="⚔️", layout="wide")

# =========================
# SOUND EFFECTS SYSTEM
# =========================
def play_sound(action_type):
    """Memutar efek suara retro berbasis 8-bit WAV data URI"""
    sounds = {
        "attack": "UklGRlQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVB9AEX/Rf9F/0X/Rf9F/0V/RX9Ff0V/RYBFgEWARUBFQEVCRUJFQkVDRENEQ0RDRENFQUVBRUFFQUZCRkJGQkZCRkNHQ0dDR0NHQ0hDSERIREREREVFRUVFRUVFRUZGRkZGRkZGRkc=",
        "heal": "UklGRpAAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVAAAABAAEAAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB",
        "success": "UklGRlQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVB9AHV1dXV1dXV2dnZ2dnZ2dnd3d3d3d3d3enh4eHR0dHR0dHR1dXV1dXV1dXZ2dnZ2dnZ2d3d3d3d3d3d6eHh4eHh4eHh5eXl5eXl5eXl6enp6enp6enp7e3t7e3t7e3t8fHx4eHg=",
        "gameover": "UklGRlQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVB9AEX/Rf9F/0X/Rf9F/0X/Rf9F/0X/Zf9l/2X/Zf9l/2V/ZX9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/0X/"
    }
    
    sound_data = sounds.get(action_type, sounds["attack"])
    st.markdown(f"""
    <audio autoplay style="display:none;">
        <source src="data:audio/wav;base64,{sound_data}" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

# =========================
# STYLE UI (Modern Full-Width RPG Theme)
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght=600;900&family=Poppins:wght=400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0e15 !important;
    font-family: 'Poppins', sans-serif;
}

/* Memaksimalkan space block utama streamlit */
[data-testid="stMainBlockContainer"] {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

.title {
    font-family: 'Cinzel', serif;
    font-size: 45px;
    text-align: center;
    color: #ffcc00;
    font-weight: 900;
    text-shadow: 0px 0px 15px rgba(255, 204, 0, 0.6);
    margin-bottom: 25px;
    letter-spacing: 2px;
}

.stButton>button {
    width: 100% !important;
    background: linear-gradient(135deg, #1f2336 0%, #161926 100%) !important;
    color: #e0e2ed !important;
    border: 1px solid #3a3f58 !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.2) !important;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #ffcc00 0%, #ff9900 100%) !important;
    color: #0d0e15 !important;
    border-color: #ffcc00 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0px 6px 15px rgba(255, 153, 0, 0.4) !important;
}

.enemy-card {
    background: linear-gradient(135deg, #2b1414 0%, #1c0b0b 100%);
    border: 2px solid #ff4b4b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.3);
    margin-bottom: 20px;
}

.status-card {
    background: linear-gradient(135deg, #14192b 0%, #0d101d 100%);
    border: 2px solid #00ccff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 0px 15px rgba(0, 204, 255, 0.2);
}
</style>
""", unsafe_allow_html=True)

# =========================
# INIT PLAYER
# =========================
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Hero",
        "hp": 150,          # Dipermudah: HP awal lebih besar
        "max_hp": 150,
        "level": 1,
        "exp": 0,
        "gold": 50,         # Dipermudah: Emas awal lebih banyak
        "weapon": "Tangan Kosong",
        "inventory": ["Potion", "Potion", "Potion"] # Dipermudah: Potion awal 3
    }

if "screen" not in st.session_state:
    st.session_state.screen = "menu"

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# DATA CONFIG (EXPANDED TOKENS)
# =========================
weapons = {
    "Tangan Kosong": (5, 12),
    "Pedang Kayu": (15, 25),
    "Pedang Besi": (35, 55),
    "Pedang Legendaris": (65, 95),
    "Tombak Langit 🔱": (110, 160),     # Senjata Baru lategame
    "Pedang Kosmik 🌌": (210, 310)     # Senjata Baru endgame
}

# Pembagian Monster berdasarkan Zona kesulitan (Lebih Banyak Wilayah)
zone_monsters = {
    "forest": [
        ("Slime 💧", 20, 2, 5),
        ("Goblin 👺", 35, 4, 8)
    ],
    "cave": [
        ("Zombie 🧟", 55, 6, 12),
        ("Skeleton 💀", 80, 10, 18)
    ],
    "desert": [
        ("Sand Worm 🪱", 110, 14, 22),
        ("Mummy 🧻", 140, 18, 28)
    ],
    "castle": [
        ("Orc Berserker 🧌", 180, 22, 35),
        ("Dark Knight ♞", 230, 26, 42)
    ],
    "hell": [
        ("Fire Demon 👹", 300, 35, 55),
        ("Necromancer 🧙‍♂️", 380, 40, 65)
    ]
}

bosses = [
    ("Demon King 👑", 450, 45, 70),
    ("Ancient Dragon 🐉", 650, 55, 90),
    ("Cthulhu 🐙", 1000, 75, 120),
    ("The Void Creator 🌌", 1500, 95, 150) # Ultimate Overlord Boss
]

# =========================
# GAME FUNCTIONS
# =========================
def level_up():
    need = player["level"] * 120 # Kurva level progresif panjang
    if player["exp"] >= need:
        player["exp"] -= need
        player["level"] += 1
        player["max_hp"] += 50   # Dipermudah: Pertumbuhan stat hero sangat besar
        player["hp"] = player["max_hp"]
        play_sound("success")
        st.toast(f"⚡ LEVEL UP! Sekarang kamu Level {player['level']}!", icon="🎉")

def reset_game():
    player.update({
        "hp": 150,
        "max_hp": 150,
        "level": 1,
        "exp": 0,
        "gold": 50,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion", "Potion", "Potion"]
    })
    st.session_state.enemy = None
    st.session_state.screen = "menu"

def spawn_enemy(zone):
    scale = player["level"]
    
    # Peluang memicu pertarungan Boss di zona berbahaya (Castle & Hell)
    if zone in ["castle", "hell"] and random.random() < 0.35:
        name, hp, mn, mx = random.choice(bosses)
        play_sound("attack")
        st.toast("🚨 PERINGATAN: DEWA KUNO / BOSS TELAH BANGKIT!", icon="⚠️")
    else:
        name, hp, mn, mx = random.choice(zone_monsters[zone])
        play_sound("attack")
        st.toast(f"Kamu dihadang oleh {name}!", icon="⚔️")

    # Kalkulasi stat musuh + scaling yang diperlambat agar game tetap MUDAH
    st.session_state.enemy = {
        "name": name,
        "hp": hp + (scale * 12),       
        "max_hp": hp + (scale * 12),
        "min": mn + max(1, int(scale * 0.5)),
        "max": mx + scale
    }

def attack():
    play_sound("attack")
    enemy = st.session_state.enemy

    # Serangan Hero
    dmg = random.randint(*weapons[player["weapon"]])
    enemy["hp"] -= dmg
    st.chat_message("user", avatar="⚔️").write(f"Kamu menebas **{enemy['name']}** sebesar **{dmg} DMG**!")

    # Musuh Mati
    if enemy["hp"] <= 0:
        gold = random.randint(40, 90) + (player["level"] * 12) # Dapat bonus mas berlimpah
        exp = random.randint(50, 110) + (player["level"] * 15) # Cepat naik level

        player["gold"] += gold
        player["exp"] += exp

        play_sound("success")
        st.balloons()
        st.success(f"🎉 **{enemy['name']}** Hancur Lebur! Memperoleh **+{gold} 💰 Gold** & **+{exp} ⭐ EXP**.")
        st.session_state.enemy = None
        level_up()
        return

    # Serangan Balasan Musuh
    enemy_dmg = random.randint(enemy["min"], enemy["max"])
    player["hp"] -= enemy_dmg
    st.chat_message("assistant", avatar="👹").write(f"**{enemy['name']}** menyerang balik! Kamu terkena **{enemy_dmg} DMG**!")

    # Player Mati
    if player["hp"] <= 0:
        play_sound("gameover")
        st.error("💀 Pandanganmu menggelap... Kamu tewas dalam pertempuran. GAME OVER!")
        reset_game()

def heal():
    if "Potion" in player["inventory"]:
        play_sound("heal")
        player["inventory"].remove("Potion")
        heal_amt = 80 # Buff Potion agar seimbang di level tinggi
        player["hp"] = min(player["max_hp"], player["hp"] + heal_amt)
        st.toast(f"🧪 Meneguk Potion! HP pulih +{heal_amt}", icon="❤️")
    else:
        st.warning("Kamu kehabisan Potion! Segera beli di toko.")

def buy_item(name, price, is_potion=False):
    if player["gold"] >= price:
        play_sound("success")
        player["gold"] -= price
        if is_potion:
            player["inventory"].append("Potion")
            st.success("🧪 Berhasil membeli **1x Potion**!")
        else:
            player["weapon"] = name
            st.success(f"⚔️ Senjata legendaris **{name}** kini telah dipakai!")
    else:
        st.error("Emas yang kamu miliki tidak mencukupi!")

# =========================
# UI HEADER
# =========================
st.markdown("<div class='title'>⚔️ RPG LEGEND ULTIMATE ⚔️</div>", unsafe_allow_html=True)

# =========================
# SCREEN: MENU UTAMA
# =========================
if st.session_state.screen == "menu":
    st.markdown("<p style='text-align:center; color:#8a8fab; font-size: 18px;'>Masuki dunia tanpa akhir, kalahkan monster kosmik, dan capai Level Tertinggi!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("🛡️ Masukkan Nama Karaktermu:", player["name"])
        if st.button("▶ MULAI PETUALANGAN BARU"):
            play_sound("success")
            player["name"] = name if name.strip() != "" else "Hero"
            st.session_state.screen = "game"
            st.rerun()

# =========================
# SCREEN: GAMEPLAY (3 KOLOM FULL LAYAR KESAMPING)
# =========================
elif st.session_state.screen == "game":

    # Struktur Grid Tiga Kolom Menyamping Penuh
    col_status, col_action, col_enemy = st.columns([3, 5, 4])

    # ----------------------------------------
    # KOLOM 1: STATUS PLAYER (KIRI)
    # ----------------------------------------
    with col_status:
        st.markdown("### 🛡️ KARTU STATUS HERO")
        
        st.markdown(f"""
        <div class='status-card'>
            <h3 style='color:#00ccff; margin:0;'>👤 {player['name']}</h3>
            <p style='margin:5px 0 0 0; color:#8a8fab;'>Senjata aktif: <b>{player['weapon']}</b></p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # HP Bar
        hp_pct = max(0.0, min(1.0, player["hp"] / player["max_hp"]))
        st.write(f"❤️ **HP Kamu:** {player['hp']} / {player['max_hp']}")
        st.progress(hp_pct)
        
        # EXP Bar
        need_exp = player["level"] * 120
        exp_pct = max(0.0, min(1.0, player["exp"] / need_exp))
        st.write(f"⭐ **Level {player['level']}** | **EXP:** {player['exp']} / {need_exp}")
        st.progress(exp_pct)
        
        st.markdown("---")
        st.metric("💰 Kantong Emas (Gold)", f"{player['gold']} g")
        
        # Inventory Display
        st.markdown("### 🎒 KANTONG BARANG")
        potions_count = player["inventory"].count("Potion")
        st.write(f"- 🧪 **Ramuan Potion:** {potions_count} buah")
        if len(player["inventory"]) > potions_count:
            other_items = [i for i in player["inventory"] if i != "Potion"]
            st.write(f"- 📦 **Barang Lain:** {', '.join(other_items)}")

    # ----------------------------------------
    # KOLOM 2: JELAJAH & AKSI TOKO (TENGAH)
    # ----------------------------------------
    with col_action:
        st.markdown("### 🌍 JELAJAHI DUNIA (PILIH LOKASI)")
        col_z1, col_z2, col_z3, col_z4, col_z5 = st.columns(5)
        with col_z1:
            if st.button("🌲 Hutan"): spawn_enemy("forest"); st.rerun()
        with col_z2:
            if st.button("🕳️ Goa"): spawn_enemy("cave"); st.rerun()
        with col_z3:
            if st.button("⏳ Gurun"): spawn_enemy("desert"); st.rerun()
        with col_z4:
            if st.button("🏰 Istana"): spawn_enemy("castle"); st.rerun()
        with col_z5:
            if st.button("🔥 Hell"): spawn_enemy("hell"); st.rerun()

        st.markdown("### 🎮 PERINTAH AKSI")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            disable_attack = False if st.session_state.enemy else True
            if st.button("⚔️ SERANG MUSUH", disabled=disable_attack):
                attack()
        with col_btn2:
            if st.button("🧪 MINUM POTION"):
                heal()
                st.rerun()
        with col_btn3:
            if st.button("💾 RESET TOTAL"):
                play_sound("gameover")
                reset_game()
                st.rerun()

        # TOKO SENJATA & BARANG (LEBIH BANYAK VARIASI)
        with st.container(border=True):
            st.markdown("### 🛒 TOKO PERLENGKAPAN KERAJAAN")
            
            col_shop1, col_shop2 = st.columns(2)
            with col_shop1:
                if st.button("🧪 Beli Potion (💰 20 Gold)"): buy_item("Potion", 20, is_potion=True)
                if st.button("🪵 Pedang Kayu (💰 50 Gold)"): buy_item("Pedang Kayu", 50)
                if st.button("⚔️ Pedang Besi (💰 120 Gold)"): buy_item("Pedang Besi", 120)
            with col_shop2:
                if st.button("✨ Pedang Legendaris (💰 300 Gold)"): buy_item("Pedang Legendaris", 300)
                if st.button("🔱 Tombak Langit (💰 650 Gold)"): buy_item("Tombak Langit 🔱", 650)
                if st.button("🌌 Pedang Kosmik (💰 1200 Gold)"): buy_item("Pedang Kosmik 🌌", 1200)

    # ----------------------------------------
    # KOLOM 3: AREA MONSTER (KANAN)
    # ----------------------------------------
    with col_enemy:
        st.markdown("### 👁️ AREA PERTEMPURAN")
        enemy = st.session_state.enemy

        if enemy:
            enemy_hp_pct = max(0.0, min(1.0, enemy["hp"] / enemy["max_hp"]))
            
            st.markdown(f"""
            <div class='enemy-card'>
                <h2 style='color:#ff4b4b; margin:0;'>{enemy['name']}</h2>
                <p style='color:#ccc; font-size:14px; margin:5px 0 15px 0;'>Batas Serangan: {enemy['min']} - {enemy['max']} DMG</p>
                <h3 style='color:white; margin:0;'>Darah: {enemy['hp']} / {enemy['max_hp']} HP</h3>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.progress(enemy_hp_pct)
        else:
            st.info("Suasana aman terkendali. Silakan tentukan lokasi eksplorasi di kolom tengah untuk memburu musuh!")
