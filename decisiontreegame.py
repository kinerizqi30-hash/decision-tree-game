import streamlit as st
import random
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND", page_icon="⚔️", layout="wide")

# =========================
# THEME CSS (RPG STYLE)
# =========================
st.markdown("""
<style>
body {
    background-color: #0f0f1a;
    color: white;
}

.big-title {
    font-size: 40px;
    text-align: center;
    font-weight: bold;
    color: #f5c542;
    text-shadow: 2px 2px 10px black;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.6);
}

button {
    border-radius: 10px !important;
    transition: 0.2s;
}
button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# =========================
# SOUND CLICK
# =========================
def play_sound():
    sound = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="
    st.markdown(f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{sound}" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "screen" not in st.session_state:
    st.session_state.screen = "menu"

if "player" not in st.session_state:
    st.session_state.player = {
        "name": "Hero",
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
# MONSTER DATA + REAL IMAGE
# =========================
monsters = [
    {
        "name": "Slime",
        "hp": 25,
        "min": 2,
        "max": 5,
        "img": "https://images.unsplash.com/photo-1618331833071-1d1c7b2f5c9b"
    },
    {
        "name": "Goblin",
        "hp": 40,
        "min": 5,
        "max": 10,
        "img": "https://images.unsplash.com/photo-1608889175123-1c6f7d2b3f3c"
    },
    {
        "name": "Zombie",
        "hp": 55,
        "min": 8,
        "max": 14,
        "img": "https://images.unsplash.com/photo-1608889175678-9b1a7d2c1a11"
    },
    {
        "name": "Demon Knight",
        "hp": 140,
        "min": 18,
        "max": 28,
        "img": "https://images.unsplash.com/photo-1620121684840-edffcfc4d2d5"
    }
]

weapons = {
    "Tangan Kosong": (3, 7),
    "Pedang Kayu": (8, 14),
    "Pedang Besi": (15, 22),
    "Pedang Legendaris": (25, 40)
}

# =========================
# FUNCTIONS
# =========================
def rand(a, b):
    return random.randint(a, b)

def start_battle():
    m = random.choice(monsters)
    st.session_state.enemy = {
        "name": m["name"],
        "hp": m["hp"] + player["level"] * 5,
        "min": m["min"],
        "max": m["max"],
        "img": m["img"]
    }

def attack():
    play_sound()
    enemy = st.session_state.enemy
    dmg = rand(*weapons[player["weapon"]])

    enemy["hp"] -= dmg

    if enemy["hp"] <= 0:
        player["gold"] += rand(20, 50)
        player["exp"] += 30
        st.session_state.enemy = None
        st.success("Monster defeated!")
    else:
        player["hp"] -= rand(enemy["min"], enemy["max"])

        if player["hp"] <= 0:
            player["hp"] = 100
            player["gold"] = 0
            player["exp"] = 0
            st.session_state.enemy = None
            st.error("GAME OVER - Respawn!")

# =========================
# UI
# =========================
st.markdown("<div class='big-title'>⚔️ RPG LEGEND ULTIMATE</div>", unsafe_allow_html=True)

# =========================
# MENU
# =========================
if st.session_state.screen == "menu":
    name = st.text_input("Masukkan nama karakter:", "Hero")
    player["name"] = name

    if st.button("▶ START GAME"):
        play_sound()
        st.session_state.screen = "game"

# =========================
# GAME
# =========================
elif st.session_state.screen == "game":

    # SIDEBAR HUD
    st.sidebar.markdown("## 🎮 STATUS")
    st.sidebar.write("👤", player["name"])
    st.sidebar.write("❤️ HP:", player["hp"])
    st.sidebar.write("⭐ Level:", player["level"])
    st.sidebar.write("💰 Gold:", player["gold"])
    st.sidebar.write("⚔️ Weapon:", player["weapon"])

    if st.button("🌲 HUNT MONSTER"):
        start_battle()

    enemy = st.session_state.enemy

    # =========================
    # BATTLE UI
    # =========================
    if enemy:
        st.markdown("## 👹 BATTLE")

        col1, col2 = st.columns(2)

        with col1:
            st.image(enemy["img"], width=300)

        with col2:
            st.markdown(f"### {enemy['name']}")
            st.write("HP:", enemy["hp"])

            if st.button("⚔️ ATTACK"):
                attack()

            if st.button("🧪 HEAL"):
                play_sound()
                player["hp"] += 20
                st.success("Healed +20 HP")
