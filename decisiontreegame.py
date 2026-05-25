import streamlit as st
import random
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND", page_icon="⚔️", layout="wide")

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
# CSS MODERN RPG
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

html, body {
    background: radial-gradient(circle at top, #0b1220, #05070f);
    color: white;
    font-family: 'Orbitron', sans-serif;
}

h1 {
    text-align: center;
    color: #ffd700;
    text-shadow: 0 0 25px #ffcc00;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #ffcc00; }
    to { text-shadow: 0 0 30px #ffcc00; }
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    transition: 0.3s;
}

.card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px #00ffcc;
}

.enemy-card {
    background: rgba(255,0,0,0.1);
    border: 1px solid red;
    padding: 15px;
    border-radius: 15px;
}

button {
    border-radius: 12px !important;
    font-weight: bold;
}

.stButton > button {
    background: linear-gradient(45deg, #ff3c3c, #ff9900);
    color: white;
    height: 50px;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 15px #ffcc00;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INIT GAME STATE
# =========================
if "player" not in st.session_state:
    st.session_state.player = {
        "hp": 100,
        "max_hp": 100,
        "level": 1,
        "exp": 0,
        "gold": 0,
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
    {"name": "Slime", "hp": 25, "min": 2, "max": 5},
    {"name": "Goblin", "hp": 40, "min": 5, "max": 10},
    {"name": "Zombie", "hp": 60, "min": 8, "max": 14},
    {"name": "Orc", "hp": 90, "min": 10, "max": 18},
    {"name": "Skeleton", "hp": 110, "min": 14, "max": 22},
    {"name": "Dark Knight", "hp": 150, "min": 18, "max": 28},
]

# =========================
# UTIL
# =========================
def r(a, b):
    return random.randint(a, b)

def click():
    play_sound("click.mp3")

def level_up():
    need = player["level"] * 60
    if player["exp"] >= need:
        player["level"] += 1
        player["max_hp"] += 25
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        player["gold"] += 50
        player["inventory"].append("Potion")
        play_sound("levelup.mp3")
        st.success("🔥 LEVEL UP!")

def spawn_enemy():
    m = random.choice(monsters)
    st.session_state.enemy = {
        "name": m["name"],
        "hp": m["hp"] + player["level"] * 6,
        "min": m["min"],
        "max": m["max"]
    }

# =========================
# BATTLE SYSTEM
# =========================
def attack():
    enemy = st.session_state.enemy
    w = weapons[player["weapon"]]

    dmg = r(w[0], w[1])
    crit = r(1, 100) <= 20

    if crit:
        dmg *= 2

    enemy["hp"] -= dmg
    play_sound("hit.mp3")

    st.success(f"⚔️ Damage: {dmg}")

    if crit:
        st.warning("💥 CRITICAL HIT!")

    if enemy["hp"] <= 0:
        st.success(f"☠️ {enemy['name']} defeated!")
        player["gold"] += r(20, 60)
        player["exp"] += r(20, 50)
        play_sound("win.mp3")
        level_up()
        st.session_state.enemy = None
        return

    # enemy attack
    edmg = r(enemy["min"], enemy["max"])
    player["hp"] -= edmg
    play_sound("hurt.mp3")

    if player["hp"] <= 0:
        play_sound("gameover.mp3")
        game_over()

def use_potion():
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal = r(25, 50)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        play_sound("heal.mp3")
        st.success(f"💚 Heal +{heal}")
    else:
        st.error("Potion habis!")

def game_over():
    st.error("💀 GAME OVER - RESET")
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

# =========================
# UI TITLE
# =========================
st.title("⚔️ RPG LEGEND ULTIMATE")

# =========================
# STATUS PANEL
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ❤️ HP")
    st.progress(player["hp"] / player["max_hp"])

with col2:
    st.markdown(f"### ⭐ Level {player['level']}")
    st.write(f"EXP: {player['exp']}")

with col3:
    st.markdown(f"### 💰 Gold: {player['gold']}")

st.markdown("---")

# =========================
# WORLD ACTION
# =========================
st.subheader("🌍 Dunia")

a, b, c = st.columns(3)

with a:
    if st.button("🌲 Hutan"):
        click()
        spawn_enemy()

with b:
    if st.button("🏰 Kastil"):
        click()
        player["exp"] += 10
        spawn_enemy()

with c:
    if st.button("🕳️ Gua"):
        click()
        spawn_enemy()

# =========================
# SHOP
# =========================
st.subheader("🛒 Shop")

if st.button("⚔️ Pedang Kayu (50 Gold)"):
    click()
    if player["gold"] >= 50:
        player["gold"] -= 50
        player["weapon"] = "Pedang Kayu"
        st.success("Weapon upgraded!")

# =========================
# ENEMY UI
# =========================
enemy = st.session_state.enemy

if enemy:
    st.markdown(f"""
    <div class="enemy-card">
        👹 <b>{enemy['name']}</b><br>
        ❤️ HP: {enemy['hp']}
    </div>
    """, unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        if st.button("⚔️ Attack"):
            attack()

    with b2:
        if st.button("🧪 Potion"):
            use_potion()
else:
    st.info("Tidak ada musuh. Jelajahi dunia!")
