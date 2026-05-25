import streamlit as st
import random
import base64

# =========================
# CONFIG UI MODERN
# =========================
st.set_page_config(page_title="RPG LEGEND", page_icon="⚔️", layout="wide")

# =========================
# SOUND FUNCTION
# =========================
def play_sound(sound_file):
    audio_bytes = open(sound_file, "rb").read()
    b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


# =========================
# CSS THEME (RPG STYLE)
# =========================
st.markdown("""
<style>
body {
    background-color: #0b0f19;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

h1 {
    text-align: center;
    color: #ffcc00;
    text-shadow: 0px 0px 20px #ffcc00;
}

div.stButton > button {
    background: linear-gradient(45deg, #ff3c3c, #ff9900);
    color: white;
    border-radius: 10px;
    height: 50px;
    font-weight: bold;
    transition: 0.2s;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 15px #ffcc00;
}

.sidebar .sidebar-content {
    background-color: #111827;
}

.enemy-box {
    padding: 15px;
    border: 2px solid red;
    border-radius: 10px;
    background-color: #1f2937;
    animation: shake 0.5s;
}

@keyframes shake {
  0% { transform: translate(1px, 1px); }
  25% { transform: translate(-2px, 2px); }
  50% { transform: translate(2px, -2px); }
  100% { transform: translate(0, 0); }
}
</style>
""", unsafe_allow_html=True)

# =========================
# INIT STATE
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
# WEAPON
# =========================
weapons = {
    "Tangan Kosong": (3, 7),
    "Pedang Kayu": (8, 14),
    "Pedang Besi": (15, 22),
    "Pedang Legendaris": (25, 40)
}

# =========================
# MONSTER
# =========================
monsters = [
    {"name": "Slime", "hp": 25, "min": 2, "max": 5, "level": 1},
    {"name": "Goblin", "hp": 40, "min": 5, "max": 10, "level": 2},
    {"name": "Zombie", "hp": 55, "min": 8, "max": 14, "level": 3},
    {"name": "Orc", "hp": 80, "min": 10, "max": 18, "level": 4},
    {"name": "Skeleton", "hp": 100, "min": 14, "max": 22, "level": 5},
    {"name": "Dark Knight", "hp": 140, "min": 18, "max": 28, "level": 6},
]

# =========================
# FUNCTION CORE
# =========================
def rand(a, b):
    return random.randint(a, b)


def start_battle():
    base = random.choice(monsters)

    st.session_state.enemy = {
        "name": base["name"],
        "hp": base["hp"] + player["level"] * 5,
        "min": base["min"],
        "max": base["max"]
    }


def level_up():
    need = player["level"] * 60
    if player["exp"] >= need:
        player["level"] += 1
        player["max_hp"] += 25
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        player["gold"] += 50
        player["inventory"].append("Potion")

        st.success("🔥 LEVEL UP!")
        play_sound("levelup.mp3")


def attack():
    enemy = st.session_state.enemy

    w = weapons[player["weapon"]]
    dmg = rand(w[0], w[1])

    crit = False
    if rand(1, 100) <= 20:
        dmg *= 2
        crit = True

    enemy["hp"] -= dmg
    play_sound("hit.mp3")

    st.success(f"⚔️ Kamu menyerang {dmg} damage!")

    if crit:
        st.warning("💥 CRITICAL HIT!")

    if enemy["hp"] <= 0:
        st.success(f"☠️ {enemy['name']} kalah!")
        player["gold"] += rand(20, 50)
        player["exp"] += rand(20, 40)
        play_sound("win.mp3")
        level_up()
        st.session_state.enemy = None
        return

    # enemy attack
    edmg = rand(enemy["min"], enemy["max"])
    player["hp"] -= edmg
    play_sound("hurt.mp3")

    st.error(f"👹 Musuh menyerang {edmg}")

    if player["hp"] <= 0:
        play_sound("gameover.mp3")
        game_over()


def use_potion():
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal = rand(20, 40)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        play_sound("heal.mp3")
        st.success(f"💚 Heal +{heal}")
    else:
        st.error("Tidak ada potion!")


def game_over():
    st.error("💀 GAME OVER")
    player.update({
        "hp": 100,
        "max_hp": 100,
        "level": 1,
        "exp": 0,
        "gold": 0,
        "score": 0,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion"]
    })
    st.session_state.enemy = None


def click():
    play_sound("click.mp3")


# =========================
# UI
# =========================
st.title("⚔️ RPG LEGEND - ULTIMATE EDITION")

# SIDEBAR STATUS
st.sidebar.header("📊 STATUS")
st.sidebar.write(f"❤️ HP {player['hp']}/{player['max_hp']}")
st.sidebar.write(f"⭐ Level {player['level']}")
st.sidebar.write(f"💰 Gold {player['gold']}")
st.sidebar.write(f"⚔️ Weapon {player['weapon']}")
st.sidebar.write("🎒 Inventory:", player["inventory"])

# LOCATION
st.subheader("🌍 Petualangan")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌲 Hutan"):
        click()
        start_battle()

with col2:
    if st.button("🏰 Kastil"):
        click()
        player["exp"] += 10
        start_battle()

with col3:
    if st.button("🕳️ Gua"):
        click()
        start_battle()

# SHOP
st.subheader("🛒 Toko")
if st.button("Beli Pedang Kayu (50 Gold)"):
    click()
    if player["gold"] >= 50:
        player["gold"] -= 50
        player["weapon"] = "Pedang Kayu"
        st.success("Purchased!")

# BATTLE
enemy = st.session_state.enemy

if enemy:
    st.markdown(f"""
    <div class="enemy-box">
        👹 <b>{enemy['name']}</b><br>
        ❤️ HP: {enemy['hp']}
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("⚔️ Attack"):
            attack()

    with c2:
        if st.button("🧪 Potion"):
            use_potion()

else:
    st.info("Belum ada musuh")
