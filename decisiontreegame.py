import streamlit as st
import random
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND", page_icon="⚔️", layout="wide")

# =========================
# SOUND CLICK (BEEP)
# =========================
def play_sound():
    sound_base64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA="
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{sound_base64}" type="audio/wav">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "screen" not in st.session_state:
    st.session_state.screen = "menu"

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

if "save_data" not in st.session_state:
    st.session_state.save_data = None

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
    {"name": "Slime", "hp": 25, "min": 2, "max": 5, "level": 1},
    {"name": "Goblin", "hp": 40, "min": 5, "max": 10, "level": 2},
    {"name": "Zombie", "hp": 55, "min": 8, "max": 14, "level": 3},
    {"name": "Orc", "hp": 80, "min": 10, "max": 18, "level": 4},
    {"name": "Skeleton", "hp": 100, "min": 14, "max": 22, "level": 5},
    {"name": "Dark Knight", "hp": 140, "min": 18, "max": 28, "level": 6},
    {"name": "Demon King", "hp": 200, "min": 25, "max": 35, "level": 8}
]

# =========================
# FUNCTIONS
# =========================
def rand(a, b):
    return random.randint(a, b)

def start_game():
    play_sound()
    st.session_state.screen = "game"

def show_menu():
    st.session_state.screen = "menu"

def save_game():
    play_sound()
    st.session_state.save_data = st.session_state.player.copy()
    st.success("Game Saved!")

def load_game():
    play_sound()
    if st.session_state.save_data:
        st.session_state.player = st.session_state.save_data.copy()
        st.success("Save Loaded!")
    else:
        st.error("Belum ada save data!")

def how_to_play():
    st.session_state.screen = "how"

def start_battle():
    available = [m for m in monsters if m["level"] <= player["level"] + 1]
    base = random.choice(available)

    st.session_state.enemy = {
        "name": base["name"],
        "hp": base["hp"] + player["level"] * 5,
        "min": base["min"] + player["level"] // 2,
        "max": base["max"] + player["level"] // 2
    }

def attack_enemy():
    play_sound()
    enemy = st.session_state.enemy
    w = weapons[player["weapon"]]

    dmg = rand(w[0], w[1])

    if rand(1, 100) <= 20:
        dmg *= 2
        st.warning("CRITICAL!")

    enemy["hp"] -= dmg
    st.success(f"Damage: {dmg}")

    if enemy["hp"] <= 0:
        st.success("Musuh kalah!")
        player["gold"] += rand(20, 50)
        player["exp"] += rand(20, 40)
        st.session_state.enemy = None

    else:
        enemy_dmg = rand(enemy["min"], enemy["max"])
        player["hp"] -= enemy_dmg
        st.error(f"Musuh menyerang {enemy_dmg}")

        if player["hp"] <= 0:
            st.error("GAME OVER")
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

def use_potion():
    play_sound()
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal = rand(20, 40)
        player["hp"] = min(player["max_hp"], player["hp"] + heal)
        st.success(f"Heal +{heal}")
    else:
        st.error("Tidak ada Potion!")

def buy_weapon(name, price):
    play_sound()
    if player["gold"] >= price:
        player["gold"] -= price
        player["weapon"] = name
        st.success(f"Buy {name}")
    else:
        st.error("Gold kurang!")

# =========================
# UI - MENU
# =========================
st.title("⚔️ RPG LEGEND")

if st.session_state.screen == "menu":
    st.subheader("🎮 MAIN MENU")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶ START GAME"):
            start_game()

    with col2:
        if st.button("💾 LOAD SAVE"):
            load_game()

    with col3:
        if st.button("📖 CARA BERMAIN"):
            how_to_play()

elif st.session_state.screen == "how":
    st.subheader("📖 CARA BERMAIN")
    st.write("""
    - Pilih lokasi untuk bertarung
    - Kalahkan monster untuk EXP & Gold
    - Upgrade senjata di shop
    - Gunakan potion untuk heal
    - Jangan sampai HP habis!
    """)

    if st.button("⬅ Kembali"):
        show_menu()

# =========================
# GAME SCREEN
# =========================
elif st.session_state.screen == "game":

    st.sidebar.write("❤️ HP:", player["hp"])
    st.sidebar.write("⭐ Level:", player["level"])
    st.sidebar.write("💰 Gold:", player["gold"])
    st.sidebar.write("⚔️ Weapon:", player["weapon"])

    if st.button("🏠 Kembali ke Menu"):
        show_menu()

    if st.button("💾 SAVE GAME"):
        save_game()

    st.subheader("🏰 Adventure")

    if st.button("🌲 Hutan"):
        start_battle()

    if st.button("🕳️ Gua"):
        start_battle()

    st.subheader("🛒 Shop")

    if st.button("Pedang Kayu (50)"):
        buy_weapon("Pedang Kayu", 50)

    if st.button("Pedang Besi (120)"):
        buy_weapon("Pedang Besi", 120)

    enemy = st.session_state.enemy

    if enemy:
        st.subheader("👹 BATTLE")
        st.write(enemy["name"], "HP:", enemy["hp"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⚔️ Attack"):
                attack_enemy()

        with col2:
            if st.button("🧪 Potion"):
                use_potion()
