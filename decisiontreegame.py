import streamlit as st
import random
import base64
import json
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND AAA", page_icon="⚔️", layout="wide")

SAVE_FILE = "savegame.json"

# =========================
# SOUND SYSTEM
# =========================
def play_sound(file):
    try:
        audio = open(file, "rb").read()
        b64 = base64.b64encode(audio).decode()

        st.markdown(f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)
    except:
        pass

# =========================
# INIT GAME STATE
# =========================
def new_game():
    return {
        "hp": 120,
        "max_hp": 120,
        "level": 1,
        "exp": 0,
        "gold": 0,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion"],
        "skill_point": 0
    }

if "started" not in st.session_state:
    st.session_state.started = False

if "player" not in st.session_state:
    st.session_state.player = new_game()

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# DATA
# =========================
weapons = {
    "Tangan Kosong": (3, 7),
    "Pedang Kayu": (8, 14),
    "Pedang Besi": (15, 25),
    "Pedang Legendaris": (25, 40)
}

skills = {
    "Slash": (10, 20),
    "Fireball": (15, 30),
    "Heal": (20, 35)  # heal value
}

monsters = [
    ("Slime", 30, 2, 6),
    ("Goblin", 50, 5, 10),
    ("Zombie", 70, 7, 12),
    ("Orc", 100, 10, 18),
    ("Skeleton", 120, 12, 20)
]

bosses = [
    ("Dark Demon", 250, 20, 30),
    ("Dragon", 400, 25, 40)
]

# =========================
# UTIL
# =========================
def r(a,b): return random.randint(a,b)

def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f)
    st.success("💾 Game Saved!")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        st.session_state.player = data
        st.success("📂 Game Loaded!")

def level_up():
    need = player["level"] * 70
    if player["exp"] >= need:
        player["level"] += 1
        player["max_hp"] += 30
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        player["skill_point"] += 1
        play_sound("levelup.mp3")
        st.success("🔥 LEVEL UP!")

def spawn_enemy(is_boss=False):
    if is_boss:
        name, hp, mn, mx = random.choice(bosses)
    else:
        name, hp, mn, mx = random.choice(monsters)

    st.session_state.enemy = {
        "name": name,
        "hp": hp + player["level"] * 10,
        "min": mn,
        "max": mx,
        "boss": is_boss
    }

# =========================
# START SCREEN
# =========================
if not st.session_state.started:
    st.title("⚔️ RPG LEGEND AAA ULTIMATE")

    st.markdown("## 🎮 Start Game")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ START GAME"):
            st.session_state.started = True
            play_sound("click.mp3")
            st.rerun()

    with col2:
        if st.button("📂 LOAD GAME"):
            load_game()
            st.session_state.started = True
            st.rerun()

    st.stop()

# =========================
# CSS
# =========================
st.markdown("""
<style>
body {
    background: radial-gradient(circle, #0b1220, #05070f);
    color: white;
}

h1 {
    text-align: center;
    color: gold;
    text-shadow: 0 0 20px gold;
}

.card {
    padding: 15px;
    border-radius: 15px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}

.enemy {
    background: rgba(255,0,0,0.1);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid red;
}

button {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("⚔️ RPG LEGEND AAA")

# =========================
# STATUS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ❤️ HP")
    st.progress(player["hp"] / player["max_hp"])

with col2:
    st.markdown("### ⭐ EXP")
    st.progress(player["exp"] / (player["level"] * 70))

with col3:
    st.markdown(f"💰 Gold: {player['gold']}")

st.markdown("---")

# =========================
# WORLD
# =========================
st.subheader("🌍 EXPLORE")

a,b,c,d = st.columns(4)

with a:
    if st.button("🌲 Hutan"):
        play_sound("click.mp3")
        spawn_enemy(False)

with b:
    if st.button("🕳️ Gua"):
        play_sound("click.mp3")
        spawn_enemy(False)

with c:
    if st.button("🏰 Kastil"):
        play_sound("click.mp3")
        spawn_enemy(True)

with d:
    if st.button("💾 Save"):
        save_game()

# =========================
# SHOP
# =========================
st.subheader("🛒 SHOP")

if st.button("⚔️ Upgrade Weapon (50 Gold)"):
    if player["gold"] >= 50:
        player["gold"] -= 50
        player["weapon"] = "Pedang Besi"
        st.success("Weapon upgraded!")

# =========================
# ENEMY
# =========================
enemy = st.session_state.enemy

def attack():
    enemy = st.session_state.enemy
    w = weapons[player["weapon"]]

    dmg = r(w[0], w[1])

    crit = r(1,100) < 20
    dodge = r(1,100) < 10

    if crit:
        dmg *= 2

    enemy["hp"] -= dmg
    play_sound("hit.mp3")

    st.success(f"⚔️ Damage: {dmg}")

    if enemy["hp"] <= 0:
        reward = r(30,80)
        player["gold"] += reward
        player["exp"] += 40
        play_sound("win.mp3")
        level_up()
        st.session_state.enemy = None
        return

    if dodge:
        st.info("🌀 Kamu menghindari serangan!")
        return

    edmg = r(enemy["min"], enemy["max"])
    player["hp"] -= edmg
    play_sound("hurt.mp3")

    if player["hp"] <= 0:
        play_sound("gameover.mp3")
        game_over()

def game_over():
    st.error("💀 GAME OVER")
    st.session_state.player = new_game()
    st.session_state.enemy = None
    st.session_state.started = False
    st.rerun()

if enemy:
    st.markdown(f"""
    <div class="enemy">
        👹 {enemy['name']} <br>
        ❤️ HP: {enemy['hp']}
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⚔️ Attack"):
            attack()

    with col2:
        if st.button("🧪 Heal"):
            if "Potion" in player["inventory"]:
                player["hp"] = min(player["max_hp"], player["hp"] + 40)
                player["inventory"].remove("Potion")
                play_sound("heal.mp3")
                st.success("Healed!")

    with col3:
        if st.button("👹 Boss Fight"):
            spawn_enemy(True)

else:
    st.info("Tidak ada musuh. Jelajahi dunia!")

# =========================
# DEBUG INFO
# =========================
st.sidebar.title("📊 STATUS")
st.sidebar.write(player)
