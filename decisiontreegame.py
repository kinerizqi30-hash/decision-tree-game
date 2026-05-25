import streamlit as st
import random

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND ULTIMATE", page_icon="⚔️", layout="wide")

# =========================
# SOUND CLICK (Fix & Cleaned)
# =========================
def play_sound():
    sound = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="
    st.markdown(f"""
    <audio autoplay style="display:none;">
        <source src="data:audio/wav;base64,{sound}" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

# =========================
# STYLE UI (Modern Dark RPG Theme)
# =========================
st.markdown("""
<style>
/* Mengubah font global dan background game */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;900&family=Poppins:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d0e15 !important;
    font-family: 'Poppins', sans-serif;
}

/* Judul Utama ala Game RPG */
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

/* Modifikasi Tombol Streamlit agar lebih interaktif */
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

/* Tombol Khusus Aksi Vital (Attack & Restart) */
div[data-testid="column"]:nth-of-type(1) .stButton>button {
    /* Tombol Attack */
    border-left: 4px solid #ff4b4b !important;
}
div[data-testid="column"]:nth-of-type(3) .stButton>button {
    /* Tombol Restart */
    border-left: 4px solid #6e7687 !important;
}

/* Desain Card Status Musuh */
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
        "hp": 100,
        "max_hp": 100,
        "level": 1,
        "exp": 0,
        "gold": 0,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion", "Potion"]
    }

if "screen" not in st.session_state:
    st.session_state.screen = "menu"

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# DATA CONFIG (Weapons & Monsters)
# =========================
weapons = {
    "Tangan Kosong": (3, 7),
    "Pedang Kayu": (8, 14),
    "Pedang Besi": (15, 22),
    "Pedang Legendaris": (25, 40)
}

monsters = [
    ("Slime 💧", 20, 5, 8),
    ("Goblin 👺", 35, 8, 12),
    ("Zombie 🧟", 55, 10, 15),
    ("Orc 🧌", 80, 12, 18),
    ("Skeleton 💀", 100, 15, 22),
    ("Dark Knight ♞", 140, 18, 28),
]

bosses = [
    ("Demon King 👑", 250, 25, 40),
    ("Ancient Dragon 🐉", 300, 30, 50)
]

# =========================
# GAME FUNCTIONS
# =========================
def level_up():
    need = player["level"] * 100
    if player["exp"] >= need:
        player["exp"] -= need
        player["level"] += 1
        player["max_hp"] += 25
        player["hp"] = player["max_hp"]
        st.toast(f"⚡ LEVEL UP! Sekarang kamu Level {player['level']}!", icon="🎉")

def reset_game():
    player.update({
        "hp": 100,
        "max_hp": 100,
        "level": 1,
        "exp": 0,
        "gold": 0,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion"]
    })
    st.session_state.enemy = None
    st.session_state.screen = "menu"

def spawn_enemy(zone):
    scale = player["level"]
    if zone == "castle" and random.random() < 0.3:
        name, hp, mn, mx = random.choice(bosses)
        st.toast("⚠️ BOSS RAMPAGING!", icon="🚨")
    else:
        name, hp, mn, mx = random.choice(monsters)
        st.toast(f"Seekor {name} menghadang jalanmu!", icon="⚔️")

    st.session_state.enemy = {
        "name": name,
        "hp": hp + scale * 20,
        "max_hp": hp + scale * 20,
        "min": mn + scale,
        "max": mx + scale * 2
    }

def attack():
    play_sound()
    enemy = st.session_state.enemy

    dmg = random.randint(*weapons[player["weapon"]])
    enemy["hp"] -= dmg
    st.chat_message("user", avatar="⚔️").write(f"Kamu menyerang **{enemy['name']}** sebesar **{dmg} DMG**!")

    if enemy["hp"] <= 0:
        gold = random.randint(30, 80)
        exp = random.randint(40, 90)

        player["gold"] += gold
        player["exp"] += exp

        st.balloons()
        st.success(f"🎉 **{enemy['name']}** Telah Dikalahkan! Kamu mendapatkan **+{gold} 💰 Gold** & **+{exp} ⭐ EXP**.")
        st.session_state.enemy = None
        level_up()
        return

    enemy_dmg = random.randint(enemy["min"], enemy["max"])
    player["hp"] -= enemy_dmg
    st.chat_message("assistant", avatar="👹").write(f"**{enemy['name']}** mencakar kamu sebesar **{enemy_dmg} DMG**!")

    if player["hp"] <= 0:
        st.error("💀 Kamu telah gugur di medan perang... GAME OVER!")
        reset_game()

def heal():
    play_sound()
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal_amt = 40
        player["hp"] = min(player["max_hp"], player["hp"] + heal_amt)
        st.toast(f"🧪 Meminum Potion! Pulih +{heal_amt} HP", icon="❤️")
    else:
        st.warning("Kamu tidak punya Potion tersisa!")

def buy_weapon(name, price):
    play_sound()
    if player["gold"] >= price:
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
            play_sound()
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
            # Di-disable jika musuh tidak ada
            disable_attack = False if st.session_state.enemy else True
            if st.button("⚔️ Serang Musuh", disabled=disable_attack):
                attack()
        with col_a2:
            if st.button("🧪 Minum Ramuan Potion"):
                heal()
        with col_a3:
            if st.button("💾 Mulai Ulang (Reset)"):
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
                if st.button("Pedang Legendaris\n(💰 300 Gold)"): buy_weapon("Pedang Legendaris", 300)

    # --- MUSUH / ENEMY DISPLAY SIDE ---
    with side_col:
        st.markdown("### 👁️ AREA MUSUH")
        enemy = st.session_state.enemy

        if enemy:
            # HTML Card Custom untuk status musuh yang mencolok
            enemy_hp_pct = max(0.0, min(1.0, enemy["hp"] / enemy["max_hp"]))
            
            st.markdown(f"""
            <div class='enemy-card'>
                <h2 style='color:#ff4b4b; margin:0;'>👹 {enemy['name']}</h2>
                <p style='color:#ccc; font-size:14px; margin:5px 0 15px 0;'>DMG: {enemy['min']} - {enemy['max']}</p>
                <h3 style='color:white; margin:0;'>HP: {enemy['hp']} / {enemy['max_hp']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(enemy_hp_pct)
        else:
            st.info("Keadaan aman terendali. Silakan pilih lokasi eksplorasi di sebelah kiri untuk mencari musuh!")
