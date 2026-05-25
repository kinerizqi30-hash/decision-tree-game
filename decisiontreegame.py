import streamlit as st
import random
import json
import os
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND ULTIMATE", layout="wide")

# =========================
# SCREEN STATE
# =========================
if "screen" not in st.session_state:
    st.session_state.screen = "menu"  # menu / game / how

# =========================
# 🔊 SOUND CLICK
# =========================
def click_sound():
    components.html("""
    <audio autoplay>
        <source src="https://www.fesliyanstudios.com/play-mp3/387" type="audio/mpeg">
    </audio>
    """, height=0)

def sfx():
    click_sound()

# =========================
# 🎨 CSS RPG
# =========================
st.markdown("""
<style>

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0b1020, #020617);
    color: white;
}

/* Title */
h1 {
    text-align:center;
    color:#38bdf8;
    text-shadow:0 0 20px #38bdf8;
}

/* Button */
.stButton > button {
    background: linear-gradient(45deg,#22d3ee,#3b82f6);
    color:white;
    border-radius:12px;
    padding:10px;
    font-weight:bold;
    border:none;
    transition:0.2s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #22d3ee;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚔️ RPG LEGEND ULTIMATE</h1>", unsafe_allow_html=True)

# =========================
# PLAYER INIT
# =========================
if "player" not in st.session_state:
    st.session_state.player = {
        "hp": 100,
        "max_hp": 100,
        "level": 1,
        "exp": 0,
        "gold": 0,
        "score": 0,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion"]
    }

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# DATA GAME
# =========================
weapons = {
    "Tangan Kosong": (3, 7),
    "Pedang Kayu": (8, 14),
    "Pedang Besi": (15, 22),
    "Pedang Legendaris": (25, 40)
}

monsters = [
    {"name":"Slime","hp":25,"min":2,"max":5},
    {"name":"Goblin","hp":40,"min":5,"max":10},
    {"name":"Zombie","hp":55,"min":8,"max":14},
    {"name":"Orc","hp":80,"min":10,"max":18},
]

# =========================
# LEVEL UP
# =========================
def level_up():
    need = player["level"] * 60
    if player["exp"] >= need:
        player["level"] += 1
        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        player["gold"] += 50
        player["inventory"].append("Potion")
        st.success("✨ LEVEL UP!")

# =========================
# SPAWN ENEMY
# =========================
def spawn_enemy():
    base = random.choice(monsters)
    st.session_state.enemy = {
        "name": base["name"],
        "hp": base["hp"] + player["level"] * 5,
        "min": base["min"] + player["level"],
        "max": base["max"] + player["level"]
    }

# =========================
# ATTACK SYSTEM
# =========================
def attack():
    e = st.session_state.enemy

    dmg = random.randint(*weapons[player["weapon"]])

    if random.randint(1,100) < 20:
        dmg *= 2
        st.warning("💥 CRITICAL HIT!")

    e["hp"] -= dmg
    st.success(f"Damage: {dmg}")

    if e["hp"] <= 0:
        st.success(f"{e['name']} defeated!")
        player["gold"] += random.randint(20,50)
        player["exp"] += random.randint(20,40)
        player["score"] += 50

        if random.randint(1,100) < 30:
            player["inventory"].append("Potion")

        level_up()
        st.session_state.enemy = None
        return

    edmg = random.randint(e["min"], e["max"])
    player["hp"] -= edmg

    st.error(f"Enemy hit: {edmg}")

    if player["hp"] <= 0:
        game_over()

# =========================
# HEAL
# =========================
def use_potion():
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal = random.randint(20,40)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        st.success(f"Heal +{heal}")

# =========================
# GAME OVER
# =========================
def game_over():
    st.error("💀 GAME OVER")

    player.update({
        "hp":100,"max_hp":100,"level":1,"exp":0,
        "gold":0,"score":0,"weapon":"Tangan Kosong",
        "inventory":["Potion"]
    })

    st.session_state.enemy = None

# =========================
# MENU
# =========================
def menu():
    st.subheader("🎮 MENU UTAMA")

    if st.button("🚀 START GAME"):
        sfx()
        st.session_state.screen = "game"

    if st.button("📖 CARA BERMAIN"):
        sfx()
        st.session_state.screen = "how"

# =========================
# HOW TO PLAY
# =========================
def how():
    st.subheader("📖 CARA BERMAIN")

    st.write("""
    - Klik EXPLORE untuk lawan monster  
    - Klik ATTACK untuk menyerang  
    - Gunakan Potion untuk heal  
    - Upgrade senjata di shop  
    - Naik level untuk lebih kuat  
    """)

    if st.button("⬅ KEMBALI"):
        sfx()
        st.session_state.screen = "menu"

# =========================
# GAME SCREEN
# =========================
def game():
    st.subheader("⚔️ ADVENTURE MODE")

    st.write(f"HP: {player['hp']}/{player['max_hp']}")
    st.write(f"Level: {player['level']}")
    st.write(f"Gold: {player['gold']}")
    st.write(f"Weapon: {player['weapon']}")

    if st.button("🗺️ EXPLORE"):
        sfx()
        spawn_enemy()

    enemy = st.session_state.enemy

    if enemy:
        st.subheader(f"👹 {enemy['name']}")
        st.write(f"HP Enemy: {enemy['hp']}")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("⚔️ ATTACK"):
                sfx()
                attack()

        with c2:
            if st.button("🧪 POTION"):
                sfx()
                use_potion()

    else:
        st.info("Belum ada monster, klik EXPLORE")

    st.subheader("🛒 SHOP")

    if st.button("Pedang Kayu (50)"):
        if player["gold"] >= 50:
            sfx()
            player["weapon"] = "Pedang Kayu"
            player["gold"] -= 50

    if st.button("Pedang Besi (120)"):
        if player["gold"] >= 120:
            sfx()
            player["weapon"] = "Pedang Besi"
            player["gold"] -= 120

    if st.button("Pedang Legendaris (250)"):
        if player["gold"] >= 250:
            sfx()
            player["weapon"] = "Pedang Legendaris"
            player["gold"] -= 250

    if st.button("🏠 KEMBALI MENU"):
        sfx()
        st.session_state.screen = "menu"

# =========================
# ROUTER
# =========================
if st.session_state.screen == "menu":
    menu()
elif st.session_state.screen == "how":
    how()
elif st.session_state.screen == "game":
    game()
