import streamlit as st
import random

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND ULTIMATE", page_icon="⚔️", layout="wide")

# =========================
# SOUND EFFECTS SYSTEM
# =========================
def play_sound(action_type):
    """Memutar efek suara retro berbasis 8-bit WAV data URI"""
    sounds = {
        # Suara tebasan / serang
        "attack": "UklGRlQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVB9AEX/Rf9F/0X/Rf9F/0V/RX9Ff0V/RYBFgEWARUBFQEVCRUJFQkVDRENEQ0RDRENFQUVBRUFFQUZCRkJGQkZCRkNHQ0dDR0NHQ0hDSERIREREREVFRUVFRUVFRUZGRkZGRkZGRkc=",
        # Suara meminum ramuan / heal
        "heal": "UklGRpAAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVAAAABAAEAAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB",
        # Suara sukses / beli senjata / level up
        "success": "UklGRlQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVB9AHV1dXV1dXV2dnZ2dnZ2dnd3d3d3d3d3enh4eHR0dHR0dHR1dXV1dXV1dXZ2dnZ2dnZ2d3d3d3d3d3d6eHh4eHh4eHh5eXl5eXl5eXl6enp6enp6enp7e3t7e3t7e3t8fHx4eHg=",
        # Suara kalah / game over
        "gameover": "UklGRlQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YVB9AEX/Rf9F/0X/Rf9F/0X/Rf9F/0X/Zf9l/2X/Zf9l/2V/ZX9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/2X/Zf9l/0X/"
    }
    
    sound_data = sounds.get(action_type, sounds["attack"])
    st.markdown(f"""
    <audio autoplay style="display:none;">
        <source src="data:audio/wav;base64,{sound_data}" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

# =========================
# STYLE UI (Modern Dark RPG Theme)
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;900&family=Poppins:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0e15 !important;
    font-family: 'Poppins', sans-serif;
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

div[data-testid="column"]:nth-of-type(1) .stButton>button {
    border-left: 4px solid #ff4b4b !important;
}
div[data-testid="column"]:nth-of-type(3) .stButton>button {
    border-left: 4px solid #6e7687 !important;
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
</style>
""", unsafe_allow_html=True)

# =========================
# INIT PLAYER
# =========================
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Hero",
        "hp": 120,          # Dipermudah: HP awal lebih tinggi
        "max_hp": 120,
        "level": 1,
        "exp": 0,
        "gold": 30,         # Dipermudah: Modal awal 30 gold
        "weapon": "Tangan Kosong",
        "inventory": ["Potion", "Potion"] # Dipermudah: Potion awal ada 2
    }

if "screen" not in st.session_state:
    st.session_state.screen = "menu"

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# DATA CONFIG (BUFFED / EASIER)
# =========================
weapons = {
    "Tangan Kosong": (5, 12),       # Dipermudah: Sebelumnya (3, 7)
    "Pedang Kayu": (15, 25),        # Dipermudah: Sebelumnya (8, 14)
    "Pedang Besi": (30, 45),        # Dipermudah: Sebelumnya (15, 22)
    "Pedang Legendaris": (55, 85)   # Dipermudah: Sebelumnya (25, 40)
}

monsters = [
    ("Slime 💧", 15, 2, 5),          # Dipermudah: HP & DMG Musuh diturunkan
    ("Goblin 👺", 25, 4, 8),
    ("Zombie 🧟", 40, 6, 11),
    ("Orc 🧌", 60, 8, 14),
    ("Skeleton 💀", 80, 10, 16),
    ("Dark Knight ♞", 110, 12, 20),
]

bosses = [
    ("Demon King 👑", 180, 18, 30),
    ("Ancient Dragon 🐉", 230, 22, 38)
]

# =========================
# GAME FUNCTIONS
# =========================
def level_up():
    need = player["level"] * 100
    if player["exp"] >= need:
        player["exp"] -= need
        player["level"] += 1
        player["max_hp"] += 40       # Dipermudah: Naik HP lebih besar (sebelumnya 25)
        player["hp"] = player["max_hp"]
        play_sound("success")
        st.toast(f"⚡ LEVEL UP! Sekarang kamu Level {player['level']}!", icon="🎉")

def reset_game():
    player.update({
        "hp": 120,
        "max_hp": 120,
        "level": 1,
        "exp": 0,
        "gold": 30,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion", "Potion"]
    })
    st.session_state.enemy = None
    st.session_state.screen = "menu"

def spawn_enemy(zone):
    scale = player["level"]
    # Pengali skala dipelankan agar musuh tidak langsung menjadi terlalu kuat
    if zone == "castle" and random.random() < 0.3:
        name, hp, mn, mx = random.choice(bosses)
        play_sound("attack")
        st.toast("⚠️ BOSS RAMPAGING!", icon="🚨")
    else:
        name, hp, mn, mx = random.choice(monsters)
        play_sound("attack")
        st.toast(f"Seekor {name} menghadang jalanmu!", icon="⚔️")

    st.session_state.enemy = {
        "name": name,
        "hp": hp + scale * 10,       # Dipermudah: Skala HP musuh dikurangi setengah
        "max_hp": hp + scale * 10,
        "min": mn + max(1, int(scale * 0.5)),
        "max": mx + scale
    }

def attack():
    play_sound("attack")
    enemy = st.session_state.enemy

    # Serangan Hero
    dmg = random.randint(*weapons[player["weapon"]])
    enemy["hp"] -= dmg
    st.chat_message("user", avatar="⚔️").write(f"Kamu menyerang **{enemy['name']}** sebesar **{dmg} DMG**!")

    # Jika musuh mati
    if enemy["hp"] <= 0:
        gold = random.randint(50, 100) # Dipermudah: Dapat emas lebih banyak
        exp = random.randint(60, 120)  # Dipermudah: Dapat EXP lebih banyak

        player["gold"] += gold
        player["exp"] += exp

        play_sound("success")
        st.balloons()
        st.success(f"🎉 **{enemy['name']}** Telah Dikalahkan! Kamu mendapatkan **+{gold} 💰 Gold** & **+{exp} ⭐ EXP**.")
        st.session_state.enemy = None
        level_up()
        return

    # Serangan Musuh Balik
    enemy_dmg = random.randint(enemy["min"], enemy["max"])
    player["hp"] -= enemy_dmg
    st.chat_message("assistant", avatar="👹").write(f"**{enemy['name']}** menyerang kamu sebesar **{enemy_dmg} DMG**!")

    # Jika Hero mati
    if player["hp"] <= 0:
        play_sound("gameover")
        st.error("💀 Kamu telah gugur di medan perang... GAME OVER!")
        reset_game()

def heal():
    if "Potion" in player["inventory"]:
        play_sound("heal")
        player["inventory"].remove("Potion")
        heal_amt = 60 # Dipermudah: Pemuilhan HP naik dari 40 ke 60
        player["hp"] = min(player["max_hp"], player["hp"] + heal_amt)
        st.toast(f"🧪 Meminum Potion! Pulih +{heal_amt} HP", icon="❤️")
    else:
        st.warning("Kamu tidak punya Potion tersisa!")

def buy_weapon(name, price):
    if player["gold"] >= price:
        play_sound("success")
        player["gold"] -= price
        player["weapon"] = name
        st.success(f"⚔️ Berhasil membeli **{name}**!")
    else:
        st.error("Uang emasmu tidak mencukupi untuk membeli senjata ini.")

# =========================
# UI HEADER
# =========================
st.markdown("<div class='title'>⚔️ RPG LEGEND ULTIMATE ⚔️</div>", unsafe_allow_html=True)

# =========================
# SCREEN: MENU UTAMA
# =========================
if st.session_state.screen == "menu":
    st.markdown("<p style='text-align:center; color:#8a8fab;'>Selamat datang di dunia antah-berantah. Persiapkan namamu sebelum memulai petualangan mendebarkan ini.</p>", unsafe_allow_html=True)
    
    col_center, _ = st.columns([2, 2])
    with col_center:
        name = st.text_input("🛡️ Berikan Nama Heromu:", player["name"])
        if st.button("▶ MEMULAI PETUALANGAN"):
            play_sound("success")
            player["name"] = name if name.strip() != "" else "Hero"
            st.session_state.screen = "game"
            st.rerun()

# =========================
# SCREEN: GAMEPLAY
# =========================
elif st.session_state.screen == "game":

    # --- SIDEBAR STATUS PLAYER ---
    st.sidebar.markdown(f"### 🛡️ STATUS PLAYER")
    st.sidebar.markdown(f"**Nama:** `{player['name']}`")
    
    # HP Bar Indicator
    hp_pct = max(0.0, min(1.0, player["hp"] / player["max_hp"]))
    st.sidebar.write(f"❤️ **HP:** {player['hp']} / {player['max_hp']}")
    st.sidebar.progress(hp_pct)
    
    # EXP Bar Indicator
    need_exp = player["level"] * 100
    exp_pct = max(0.0, min(1.0, player["exp"] / need_exp))
    st.sidebar.write(f"⭐ **Level:** {player['level']} | **EXP:** {player['exp']}/{need_exp}")
    st.sidebar.progress(exp_pct)
    
    st.sidebar.markdown("---")
    
    # Metric Info
    col_side1, col_side2 = st.sidebar.columns(2)
    col_side1.metric("💰 Kantong Gold", f"{player['gold']} g")
    col_side2.metric("⚔️ Senjata", player["weapon"])
    
    # Inventory list
    st.sidebar.markdown(f"🎒 **Isi Tas (Inventory):**\n" + "\n".join([f"- 🧪 {i}" for i in player["inventory"]]) if player["inventory"] else "🎒 *Kosong*")

    # --- MAIN CONTENT AREA ---
    main_col, side_col = st.columns([5, 3])

    with main_col:
        # ZONE EXPLORATION
        st.markdown("### 🌍 JELAJAHI DUNIA")
        col_w1, col_w2, col_w3 = st.columns(3)
        with col_w1:
            if st.button("🌲 Masuki Hutan Forest"): spawn_enemy("forest"); st.rerun()
        with col_w2:
            if st.button("🕳️ Telusuri Goa Cave"): spawn_enemy("cave"); st.rerun()
        with col_w3:
            if st.button("🏰 Serbu Istana Castle"): spawn_enemy("castle"); st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # PLAYER ACTIONS
        st.markdown("### 🎮 AKSI PERTEMPURAN")
        col_a1, col_a2, col_a3 = st.columns(3)
        with col_a1:
            disable_attack = False if st.session_state.enemy else True
            if st.button("⚔️ Serang Musuh", disabled=disable_attack):
                attack()
        with col_a2:
            if st.button("🧪 Minum Ramuan Potion"):
                heal()
        with col_a3:
            if st.button("💾 Mulai Ulang (Reset)"):
                play_sound("gameover")
                reset_game()
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ARSENAL / SHOP
        with st.container(border=True):
            st.markdown("### 🛒 PEDAGANG SENJATA (SHOP)")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("Pedang Kayu\n(💰 50 Gold)"): buy_weapon("Pedang Kayu", 50)
            with col_s2:
                if st.button("Pedang Besi\n(💰 120 Gold)"): buy_weapon("Pedang Besi", 120)
            with col_s3:
                if st.button("Pedang Legendaris\n
