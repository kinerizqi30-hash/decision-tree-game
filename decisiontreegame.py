import streamlit as st
import random

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="RPG LEGEND AAA", page_icon="⚔️", layout="wide")

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
# MONSTER BASE (difficulty scaling)
# =========================
monsters = [
    ("Slime", 20, 5, 8),
    ("Goblin", 35, 8, 12),
    ("Zombie", 50, 10, 15),
    ("Orc", 70, 12, 18),
    ("Skeleton", 90, 15, 22),
    ("Dark Knight", 130, 18, 28),
    ("Demon King", 180, 22, 35)
]

# =========================
# LEVEL SYSTEM
# =========================
def level_up():
    while player["exp"] >= player["level"] * 100:
        player["exp"] -= player["level"] * 100
        player["level"] += 1
        player["max_hp"] += 20
        player["hp"] = player["max_hp"]
        st.success(f"LEVEL UP! Now Level {player['level']} ⚡")

# =========================
# MONSTER GENERATOR (scaled)
# =========================
def spawn_enemy():
    name, hp, mn, mx = random.choice(monsters)

    scale = player["level"]

    st.session_state.enemy = {
        "name": name,
        "hp": hp + scale * 15,
        "min": mn + scale,
        "max": mx + scale * 2
    }

# =========================
# RESET GAME (GAME OVER AUTO)
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

# =========================
# ATTACK SYSTEM
# =========================
def attack():
    play_sound()
    enemy = st.session_state.enemy

    dmg = random.randint(*weapons[player["weapon"]])
    enemy["hp"] -= dmg

    st.success(f"You deal {dmg} damage!")

    # enemy dead
    if enemy["hp"] <= 0:
        reward_gold = random.randint(20, 60)
        reward_exp = random.randint(30, 60)

        player["gold"] += reward_gold
        player["exp"] += reward_exp

        st.success(f"Enemy defeated! +{reward_gold} gold +{reward_exp} exp")

        st.session_state.enemy = None
        level_up()
        return

    # enemy attack
    enemy_dmg = random.randint(enemy["min"], enemy["max"])
    player["hp"] -= enemy_dmg

    st.error(f"Enemy hit you for {enemy_dmg}")

    # GAME OVER AUTO RESET
    if player["hp"] <= 0:
        st.error("💀 GAME OVER - Respawning...")
        reset_game()

# =========================
# HEAL
# =========================
def heal():
    play_sound()
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")
        heal_amount = random.randint(25, 50)
        player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
        st.success(f"Healed +{heal_amount} HP")
    else:
        st.warning("No Potion!")

# =========================
# UI HEADER
# =========================
st.title("⚔️ RPG LEGEND - AAA UPGRADE")

# =========================
# CHARACTER SETUP
# =========================
if "setup" not in st.session_state:
    st.session_state.setup = True

if st.session_state.setup:
    name = st.text_input("Enter Character Name", player["name"])
    if st.button("START ADVENTURE"):
        player["name"] = name
        st.session_state.setup = False
        play_sound()

# =========================
# GAME UI
# =========================
if not st.session_state.setup:

    # HUD
    st.sidebar.title("🎮 STATUS")
    st.sidebar.write("👤", player["name"])
    st.sidebar.write("❤️ HP:", player["hp"], "/", player["max_hp"])
    st.sidebar.write("⭐ Level:", player["level"])
    st.sidebar.write("📊 EXP:", player["exp"])
    st.sidebar.write("💰 Gold:", player["gold"])
    st.sidebar.write("⚔️ Weapon:", player["weapon"])

    # ACTIONS
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🌲 Hunt Monster"):
            spawn_enemy()

    with col2:
        if st.button("⚔️ Attack"):
            if st.session_state.enemy:
                attack()

    with col3:
        if st.button("🧪 Heal"):
            heal()

    # ENEMY DISPLAY
    enemy = st.session_state.enemy

    if enemy:
        st.subheader("👹 ENEMY")
        st.write("Name:", enemy["name"])
        st.write("HP:", enemy["hp"])

    else:
        st.info("No enemy. Go hunt!")
