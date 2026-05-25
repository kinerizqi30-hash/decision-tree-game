import streamlit as st
import random

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND ULTIMATE", page_icon="⚔️", layout="wide")

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
# STYLE UI
# =========================
st.markdown("""
<style>
body {background:#0e0f1a; color:white;}
.title {
    font-size:40px;
    text-align:center;
    color:#ffd700;
    font-weight:bold;
}
.card {
    background:rgba(255,255,255,0.05);
    padding:15px;
    border-radius:15px;
    margin:10px 0;
}
button {
    border-radius:12px !important;
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
        "inventory": ["Potion"]
    }

if "screen" not in st.session_state:
    st.session_state.screen = "menu"

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# WEAPONS
# =========================
weapons = {
    "Tangan Kosong": (3, 7),
    "Pedang Kayu": (8, 14),
    "Pedang Besi": (15, 22),
    "Pedang Legendaris": (25, 40)
}

# =========================
# MONSTERS (scaling world)
# =========================
monsters = [
    ("Slime", 20, 5, 8),
    ("Goblin", 35, 8, 12),
    ("Zombie", 55, 10, 15),
    ("Orc", 80, 12, 18),
    ("Skeleton", 100, 15, 22),
    ("Dark Knight", 140, 18, 28),
]

bosses = [
    ("Demon King", 250, 25, 40),
    ("Ancient Dragon", 300, 30, 50)
]

# =========================
# LEVEL SYSTEM
# =========================
def level_up():
    need = player["level"] * 100
    if player["exp"] >= need:
        player["exp"] -= need
        player["level"] += 1
        player["max_hp"] += 25
        player["hp"] = player["max_hp"]
        st.success("⚡ LEVEL UP!")

# =========================
# RESET GAME
# =========================
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

# =========================
# SPAWN ENEMY (difficulty scaling)
# =========================
def spawn_enemy(zone):
    scale = player["level"]

    if zone == "castle" and random.random() < 0.3:
        name, hp, mn, mx = random.choice(bosses)
    else:
        name, hp, mn, mx = random.choice(monsters)

    st.session_state.enemy = {
        "name": name,
        "hp": hp + scale * 20,
        "min": mn + scale,
        "max": mx + scale * 2
    }

# =========================
# ATTACK SYSTEM
# =========================
def attack():
    play_sound()
    enemy = st.session_state.enemy

    dmg = random.randint(*weapons[player["weapon"]])
    enemy["hp"] -= dmg

    st.success(f"You deal {dmg} damage!")

    if enemy["hp"] <= 0:
        gold = random.randint(30, 80)
        exp = random.randint(40, 90)

        player["gold"] += gold
        player["exp"] += exp

        st.success(f"Enemy defeated! +{gold} gold +{exp} exp")

        st.session_state.enemy = None
        level_up()
        return

    enemy_dmg = random.randint(enemy["min"], enemy["max"])
    player["hp"] -= enemy_dmg

    st.error(f"Enemy hits {enemy_dmg}")

    if player["hp"] <= 0:
        st.error("💀 GAME OVER")
        reset_game()

# =========================
# HEAL
# =========================
def heal():
    play_sound()
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        player["hp"] = min(player["max_hp"], player["hp"] + 40)
        st.success("Healed +40 HP")
    else:
        st.warning("No potion!")

# =========================
# SHOP
# =========================
def buy_weapon(name, price):
    play_sound()
    if player["gold"] >= price:
        player["gold"] -= price
        player["weapon"] = name
        st.success(f"Bought {name}")
    else:
        st.error("Not enough gold")

# =========================
# UI HEADER
# =========================
st.markdown("<div class='title'>⚔️ RPG LEGEND ULTIMATE</div>", unsafe_allow_html=True)

# =========================
# MENU
# =========================
if st.session_state.screen == "menu":

    name = st.text_input("Enter Character Name", player["name"])

    if st.button("▶ START GAME"):
        play_sound()
        player["name"] = name
        st.session_state.screen = "game"

# =========================
# GAME SCREEN
# =========================
elif st.session_state.screen == "game":

    # HUD
    st.sidebar.title("🎮 STATUS")
    st.sidebar.write("👤", player["name"])
    st.sidebar.write("❤️ HP:", player["hp"], "/", player["max_hp"])
    st.sidebar.write("⭐ Level:", player["level"])
    st.sidebar.write("📊 EXP:", player["exp"])
    st.sidebar.write("💰 Gold:", player["gold"])
    st.sidebar.write("⚔️ Weapon:", player["weapon"])

    # WORLD
    st.subheader("🌍 WORLD")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🌲 Forest"):
            spawn_enemy("forest")

    with col2:
        if st.button("🕳️ Cave"):
            spawn_enemy("cave")

    with col3:
        if st.button("🏰 Castle"):
            spawn_enemy("castle")

    # ACTIONS
    st.subheader("🎮 ACTIONS")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⚔️ Attack"):
            if st.session_state.enemy:
                attack()

    with col2:
        if st.button("🧪 Heal"):
            heal()

    with col3:
        if st.button("💾 Restart Game"):
            reset_game()

    # SHOP
    st.subheader("🛒 SHOP")

    if st.button("Pedang Kayu (50)"):
        buy_weapon("Pedang Kayu", 50)

    if st.button("Pedang Besi (120)"):
        buy_weapon("Pedang Besi", 120)

    if st.button("Pedang Legendaris (300)"):
        buy_weapon("Pedang Legendaris", 300)

    # ENEMY
    enemy = st.session_state.enemy

    if enemy:
        st.subheader("👹 ENEMY")
        st.write("Name:", enemy["name"])
        st.write("HP:", enemy["hp"])

    else:
        st.info("No enemy - explore world!")

    # INVENTORY
    st.subheader("🎒 INVENTORY")
    st.write(player["inventory"])
