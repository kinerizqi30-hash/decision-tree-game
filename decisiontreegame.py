import streamlit as st
import random
import time
import json
import os
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND AAA", layout="wide")

# =========================
# SCREEN STATE
# =========================
if "screen" not in st.session_state:
    st.session_state.screen = "menu"

# =========================
# SOUND CLICK
# =========================
def sfx():
    components.html("""
    <audio autoplay>
        <source src="https://www.fesliyanstudios.com/play-mp3/387" type="audio/mpeg">
    </audio>
    """, height=0)

# =========================
# STYLE
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0b1020, #020617);
    color: white;
}

h1 {
    text-align:center;
    color:#38bdf8;
    text-shadow:0 0 20px #38bdf8;
}

.stButton > button {
    background: linear-gradient(45deg,#22d3ee,#3b82f6);
    color:white;
    border-radius:12px;
    padding:10px;
    font-weight:bold;
    border:none;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚔️ RPG LEGEND AAA ULTIMATE</h1>", unsafe_allow_html=True)

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

if "mp" not in st.session_state:
    st.session_state.mp = 50
    st.session_state.max_mp = 50

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# DATA
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
    {"name":"Orc","hp":80,"min":10,"max":18},
]

bosses = [
    {"name":"Dark Demon Lord","hp":300,"min":15,"max":25},
]

# =========================
# UTIL
# =========================
def log(msg):
    st.markdown(f"### {msg}")
    time.sleep(0.4)

def level_up():
    need = player["level"] * 60
    if player["exp"] >= need:
        player["level"] += 1
        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        player["gold"] += 50
        st.success("✨ LEVEL UP!")

def spawn_enemy():
    base = random.choice(monsters)

    st.session_state.enemy = {
        "name": base["name"],
        "hp": base["hp"] + player["level"] * 5,
        "max_hp": base["hp"] + player["level"] * 5,
        "min": base["min"],
        "max": base["max"],
        "rage": False
    }

def spawn_boss():
    base = random.choice(bosses)

    st.session_state.enemy = {
        "name": base["name"],
        "hp": base["hp"] + player["level"] * 25,
        "max_hp": base["hp"] + player["level"] * 25,
        "min": base["min"],
        "max": base["max"],
        "rage": False
    }

# =========================
# BATTLE SYSTEM AAA
# =========================
def enemy_turn():
    e = st.session_state.enemy

    log("👹 ENEMY TURN")

    if e["hp"] < e["max_hp"] * 0.4 and not e["rage"]:
        e["rage"] = True
        e["min"] += 10
        e["max"] += 15
        log("🔥 BOSS RAGE MODE!")

    dmg = random.randint(e["min"], e["max"])

    if random.randint(1,100) < 15:
        dmg *= 2
        log("💀 CRITICAL HIT!")

    player["hp"] -= dmg
    log(f"💀 Enemy deals {dmg}")

    if player["hp"] <= 0:
        game_over()

def player_attack():
    e = st.session_state.enemy

    log("🎮 PLAYER TURN")

    dmg = random.randint(*weapons[player["weapon"]])

    if random.randint(1,100) < 20:
        dmg *= 2
        log("💥 CRITICAL!")

    e["hp"] -= dmg
    log(f"⚔️ Damage {dmg}")

    check_enemy()

def use_skill(skill):
    e = st.session_state.enemy

    if skill == "Fireball" and st.session_state.mp >= 15:
        st.session_state.mp -= 15
        dmg = random.randint(25,45)
        log("🔥 FIREBALL!")
        e["hp"] -= dmg

    elif skill == "Heal" and st.session_state.mp >= 10:
        st.session_state.mp -= 10
        heal = random.randint(20,40)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        log(f"✨ Heal +{heal}")

    elif skill == "Double":
        if st.session_state.mp >= 20:
            st.session_state.mp -= 20
            dmg = random.randint(15,25) * 2
            log("⚔️ DOUBLE STRIKE!")
            e["hp"] -= dmg

    check_enemy()

def check_enemy():
    time.sleep(0.3)
    e = st.session_state.enemy

    if e["hp"] <= 0:
        log(f"👹 {e['name']} DEFEATED!")
        player["gold"] += 100
        player["exp"] += 80
        player["score"] += 200
        level_up()
        st.session_state.enemy = None
        return

    enemy_turn()

def game_over():
    log("💀 GAME OVER")
    player.update({
        "hp":100,"max_hp":100,"level":1,
        "exp":0,"gold":0,"score":0,
        "weapon":"Tangan Kosong"
    })
    st.session_state.enemy = None

# =========================
# MENU
# =========================
def menu():
    st.subheader("🎮 MENU")

    if st.button("🚀 START GAME"):
        sfx()
        st.session_state.screen = "game"

    if st.button("👹 BOSS FIGHT"):
        sfx()
        st.session_state.screen = "boss"

# =========================
# GAME SCREEN
# =========================
def game():
    st.subheader("⚔️ ADVENTURE")

    st.write(f"HP: {player['hp']}/{player['max_hp']}")
    st.write(f"MP: {st.session_state.mp}")
    st.write(f"Level: {player['level']}")

    if st.button("🗺️ EXPLORE"):
        spawn_enemy()

    enemy = st.session_state.enemy

    if enemy:
        st.subheader(f"👹 {enemy['name']}")
        st.write(f"HP: {enemy['hp']}")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⚔️ ATTACK"):
                player_attack()

        with col2:
            if st.button("🔥 FIREBALL"):
                use_skill("Fireball")

        with col3:
            if st.button("✨ HEAL"):
                use_skill("Heal")

        if st.button("⚔️ DOUBLE STRIKE"):
            use_skill("Double")

    if st.button("🏠 MENU"):
        st.session_state.screen = "menu"

# =========================
# BOSS SCREEN
# =========================
def boss():
    st.subheader("👹 BOSS MODE")

    if st.button("SUMMON BOSS"):
        spawn_boss()

    enemy = st.session_state.enemy

    if enemy:
        st.error(f"🔥 {enemy['name']}")
        st.write(f"HP: {enemy['hp']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⚔️ ATTACK BOSS"):
                player_attack()

        with col2:
            if st.button("🔥 FIREBALL"):
                use_skill("Fireball")

    if st.button("🏠 MENU"):
        st.session_state.screen = "menu"

# =========================
# ROUTER
# =========================
if st.session_state.screen == "menu":
    menu()
elif st.session_state.screen == "game":
    game()
elif st.session_state.screen == "boss":
    boss()
