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

        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass  # kalau file tidak ada tetap jalan

# =========================
# CSS RPG UI
# =========================
st.markdown("""
<style>
body {
    background: #0b0f19;
    color: white;
}

h1 {
    text-align: center;
    color: #ffcc00;
    text-shadow: 0 0 20px #ffcc00;
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
    box-shadow: 0 0 15px #ffcc00;
}

.enemy-box {
    padding: 15px;
    border: 2px solid red;
    border-radius: 10px;
    background: #1f2937;
}
</style>
""", unsafe_allow_html=True)

# =========================
# INIT PLAYER
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
# FUNCTIONS
# =========================
def r(a, b):
    return random.randint(a, b)


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
        "hp": m["hp"] + player["level"] * 5,
        "min": m["min"],
        "max": m["max"]
    }


def attack():
    enemy = st.session_state.enemy

    w = weapons[player["weapon"]]
    dmg = r(w[0], w[1])

    crit = r(1, 100) <= 20
    if crit:
        dmg *= 2

    enemy["hp"] -= dmg
    play_sound("hit.mp3")

    st.success(f"⚔️ Kamu serang {dmg}")

    if crit:
        st.warning("💥 CRITICAL!")

    if enemy["hp"] <= 0:
        st.success(f"☠️ {enemy['name']} kalah!")
        player["gold"] += r(20, 50)
        player["exp"] += r(20, 40)
        play_sound("win.mp3")
        level_up()
        st.session_state.enemy = None
        return

    # enemy attack
    edmg = r(enemy["min"], enemy["max"])
    player["hp"] -= edmg
    play_sound("hurt.mp3")

    st.error(f"👹 Musuh serang {edmg}")

    if player["hp"] <= 0:
        play_sound("gameover.mp3")
        game_over()


def use_potion():
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal = r(20, 40)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        play_sound("heal.mp3")
        st.success(f"💚 Heal +{heal}")
    else:
        st.error("Tidak ada potion")


def game_over():
    st.error("💀 GAME OVER RESET")

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


def click():
    play_sound("click.mp3")

# =========================
# UI HEADER
# =========================
st.title("⚔️ RPG LEGEND ULTIMATE")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("STATUS")
st.sidebar.write(f"❤️ HP {player['hp']}/{player['max_hp']}")
st.sidebar.write(f"⭐ Level {player['level']}")
st.sidebar.write(f"💰 Gold {player['gold']}")
st.sidebar.write(f"⚔️ Weapon {player['weapon']}")
st.sidebar.write("🎒", player["inventory"])

# =========================
# WORLD
# =========================
st.subheader("🌍 Dunia")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🌲 Hutan"):
        click()
        spawn_enemy()

with c2:
    if st.button("🏰 Kastil"):
        click()
        player["exp"] += 10
        spawn_enemy()

with c3:
    if st.button("🕳️ Gua"):
        click()
        spawn_enemy()

# =========================
# SHOP
# =========================
st.subheader("🛒 Shop")

if st.button("Beli Pedang Kayu (50 Gold)"):
    click()
    if player["gold"] >= 50:
        player["gold"] -= 50
        player["weapon"] = "Pedang Kayu"
        st.success("Terbeli!")

# =========================
# BATTLE
# =========================
enemy = st.session_state.enemy

if enemy:
    st.markdown(f"""
    <div class="enemy-box">
        👹 {enemy['name']}<br>
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
    st.info("Belum ada musuh")
