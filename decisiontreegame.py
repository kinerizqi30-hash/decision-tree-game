import streamlit as st
import random
import json
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND ULTIMATE", layout="wide")

# =========================
# 🎨 CSS + ANIMATION
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
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #38bdf8; }
    to { text-shadow: 0 0 25px #22d3ee; }
}

/* Button */
.stButton > button {
    background: linear-gradient(45deg,#22d3ee,#3b82f6);
    color:white;
    border-radius:12px;
    padding:10px;
    font-weight:bold;
    transition:0.2s;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #22d3ee;
}

/* Card */
.block-container {
    padding-top: 20px;
}

/* Battle shake effect */
.shake {
    animation: shake 0.3s;
}

@keyframes shake {
    0% {transform: translate(1px,1px);}
    25% {transform: translate(-2px,2px);}
    50% {transform: translate(2px,-2px);}
    100% {transform: translate(0,0);}
}

</style>
""", unsafe_allow_html=True)

st.markdown("<h1>⚔️ RPG LEGEND ULTIMATE</h1>", unsafe_allow_html=True)

# =========================
# SOUND (Streamlit workaround)
# =========================
def play_sound(name):
    st.audio(f"sounds/{name}.mp3", autoplay=True)

# =========================
# LEADERBOARD
# =========================
LB_FILE = "leaderboard.json"

def load_lb():
    if os.path.exists(LB_FILE):
        return json.load(open(LB_FILE))
    return []

def save_lb(data):
    json.dump(data, open(LB_FILE,"w"))

# =========================
# SESSION STATE
# =========================
if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Hero",
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

if "map" not in st.session_state:
    st.session_state.map = "🌲 Hutan"

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
    {"name":"Slime","hp":25,"min":2,"max":5,"level":1},
    {"name":"Goblin","hp":40,"min":5,"max":10,"level":2},
    {"name":"Zombie","hp":55,"min":8,"max":14,"level":3},
    {"name":"Orc","hp":80,"min":10,"max":18,"level":4},
    {"name":"Skeleton","hp":100,"min":14,"max":22,"level":5},
    {"name":"Dark Knight","hp":140,"min":18,"max":28,"level":6},
]

# =========================
# UTIL
# =========================
def rand(a,b):
    return random.randint(a,b)

def level_up():
    need = player["level"] * 60
    if player["exp"] >= need:
        player["level"] += 1
        player["max_hp"] += 25
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        player["gold"] += 50
        player["inventory"].append("Potion")
        st.success("✨ LEVEL UP!")

# =========================
# AI ENEMY (lebih kuat sesuai level)
# =========================
def spawn_enemy():
    base = random.choice(monsters)

    difficulty = player["level"] * 5

    st.session_state.enemy = {
        "name": base["name"],
        "hp": base["hp"] + difficulty,
        "min": base["min"] + player["level"]//2,
        "max": base["max"] + player["level"]//2
    }

# =========================
# BATTLE SYSTEM
# =========================
def attack():
    e = st.session_state.enemy
    dmg = rand(*weapons[player["weapon"]])

    if rand(1,100) < 20:
        dmg *= 2
        st.warning("💥 CRITICAL!")

    e["hp"] -= dmg
    st.success(f"Damage {dmg}")

    if e["hp"] <= 0:
        st.success("Monster kalah!")
        player["gold"] += rand(20,50)
        player["exp"] += rand(20,40)
        player["score"] += 50

        if rand(1,100) < 30:
            player["inventory"].append("Potion")

        level_up()

        st.session_state.enemy = None
        play_sound("win")
        return

    # enemy AI attack
    edmg = rand(e["min"], e["max"]) + player["level"]

    player["hp"] -= edmg
    st.error(f"Enemy hit {edmg}")

    play_sound("hit")

    if player["hp"] <= 0:
        game_over()

def use_potion():
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal = rand(20,40)
        player["hp"] = min(player["max_hp"], player["hp"]+heal)
        st.success(f"Heal +{heal}")

# =========================
# GAME OVER + LEADERBOARD
# =========================
def game_over():
    st.error("💀 GAME OVER")

    lb = load_lb()
    lb.append({"score": player["score"]})
    save_lb(lb)

    player.update({
        "hp":100,"max_hp":100,"level":1,"exp":0,
        "gold":0,"score":0,"weapon":"Tangan Kosong",
        "inventory":["Potion"]
    })

    st.session_state.enemy = None

# =========================
# MAP SYSTEM
# =========================
maps = ["🌲 Hutan","🕳️ Gua","🏰 Kastil","⛰️ Gunung"]

st.sidebar.title("📍 MAP")
choice_map = st.sidebar.radio("Pilih lokasi", maps)
st.session_state.map = choice_map

if st.sidebar.button("🚀 Explore"):
    spawn_enemy()

# =========================
# PLAYER STATUS
# =========================
st.sidebar.title("👤 STATUS")
st.sidebar.write(player)

# =========================
# UI ACTION
# =========================
enemy = st.session_state.enemy

if enemy:
    st.subheader(f"👹 {enemy['name']}")

    st.write(f"HP Enemy: {enemy['hp']}")

    c1,c2 = st.columns(2)

    with c1:
        if st.button("⚔️ Attack"):
            attack()

    with c2:
        if st.button("🧪 Potion"):
            use_potion()

else:
    st.info("Belum ada musuh. Explore map!")

# =========================
# SHOP
# =========================
st.subheader("🛒 SHOP")

if st.button("Pedang Kayu (50)"):
    if player["gold"]>=50:
        player["weapon"]="Pedang Kayu"
        player["gold"]-=50

if st.button("Pedang Besi (120)"):
    if player["gold"]>=120:
        player["weapon"]="Pedang Besi"
        player["gold"]-=120

if st.button("Pedang Legendaris (250)"):
    if player["gold"]>=250:
        player["weapon"]="Pedang Legendaris"
        player["gold"]-=250

# =========================
# LEADERBOARD
# =========================
st.subheader("🏆 LEADERBOARD")

lb = sorted(load_lb(), key=lambda x:x["score"], reverse=True)

for i,l in enumerate(lb[:5]):
    st.write(f"{i+1}. Score: {l['score']}")
