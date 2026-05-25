import streamlit as st
import random
import base64
import json
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="OPEN WORLD RPG AAA", layout="wide")

SAVE_FILE = "open_world_save.json"

# =========================
# SOUND
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
# NEW GAME
# =========================
def new_game():
    return {
        "x": 2,
        "y": 2,
        "hp": 120,
        "max_hp": 120,
        "level": 1,
        "exp": 0,
        "gold": 0,
        "weapon": "Tangan Kosong",
        "inventory": ["Potion"],
        "quest": None,
        "quest_progress": 0
    }

if "player" not in st.session_state:
    st.session_state.player = new_game()

if "enemy" not in st.session_state:
    st.session_state.enemy = None

player = st.session_state.player

# =========================
# WORLD MAP (5x5)
# =========================
WORLD = [
    ["🌲","🌲","🏡","🌲","👹"],
    ["🌲","🕳️","🌲","🏰","🌲"],
    ["🌲","🌲","⚔️","🌲","🌲"],
    ["👹","🌲","🏡","🌲","🌲"],
    ["🌲","🏰","🌲","🕳️","👹"],
]

# =========================
# DATA
# =========================
weapons = {
    "Tangan Kosong": (3,7),
    "Pedang Kayu": (8,14),
    "Pedang Besi": (15,25),
}

monsters = ["Slime","Goblin","Zombie","Orc","Skeleton"]
bosses = ["Dragon", "Dark Demon"]

quests = [
    {"name":"Bunuh 3 monster", "target":3, "reward":50},
    {"name":"Kalahkan 1 boss", "target":1, "reward":100},
]

# =========================
# UTIL
# =========================
def r(a,b): return random.randint(a,b)

def save_game():
    with open(SAVE_FILE,"w") as f:
        json.dump(player,f)
    st.success("💾 Saved!")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE,"r") as f:
            data = json.load(f)
        st.session_state.player = data
        st.success("📂 Loaded!")

def level_up():
    if player["exp"] >= player["level"]*60:
        player["level"] += 1
        player["max_hp"] += 25
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        play_sound("levelup.mp3")
        st.success("🔥 LEVEL UP!")

# =========================
# MOVEMENT
# =========================
def move(dx,dy):
    player["x"] = max(0,min(4,player["x"]+dx))
    player["y"] = max(0,min(4,player["y"]+dy))
    play_sound("click.mp3")
    check_tile_event()

# =========================
# TILE EVENTS
# =========================
def check_tile_event():
    tile = WORLD[player["y"]][player["x"]]

    if tile == "🌲":
        if random.random() < 0.5:
            spawn_enemy()
    elif tile == "👹":
        spawn_enemy(boss=True)
    elif tile == "🏡":
        player["hp"] = player["max_hp"]
        st.success("🏡 Rest + Heal full!")
    elif tile == "⚔️":
        player["gold"] += 20
        st.success("⚔️ Found loot!")

# =========================
# ENEMY
# =========================
def spawn_enemy(boss=False):
    if boss:
        name = random.choice(bosses)
        hp = 200 + player["level"]*20
        mn, mx = 15, 30
    else:
        name = random.choice(monsters)
        hp = 60 + player["level"]*10
        mn, mx = 5, 15

    st.session_state.enemy = {
        "name": name,
        "hp": hp,
        "min": mn,
        "max": mx,
        "boss": boss
    }

# =========================
# QUEST
# =========================
def give_quest():
    player["quest"] = random.choice(quests)
    player["quest_progress"] = 0
    st.success(f"📜 Quest: {player['quest']['name']}")

# =========================
# BATTLE
# =========================
def attack():
    enemy = st.session_state.enemy
    w = weapons[player["weapon"]]

    dmg = r(w[0],w[1])

    if r(1,100) < 20:
        dmg *= 2

    enemy["hp"] -= dmg
    st.success(f"⚔️ Hit {dmg}")

    if enemy["hp"] <= 0:
        if enemy["boss"]:
            player["quest_progress"] += 1

        player["gold"] += r(20,80)
        player["exp"] += 40
        st.session_state.enemy = None
        level_up()
        return

    # enemy attack
    ed = r(enemy["min"],enemy["max"])
    player["hp"] -= ed

    if player["hp"] <= 0:
        game_over()

def game_over():
    st.error("💀 GAME OVER")
    st.session_state.player = new_game()
    st.session_state.enemy = None
    st.rerun()

# =========================
# UI
# =========================
st.title("🌍⚔️ OPEN WORLD RPG AAA")

# STATUS
col1,col2,col3 = st.columns(3)
with col1:
    st.write("❤️ HP:", player["hp"], "/", player["max_hp"])
with col2:
    st.write("⭐ Level:", player["level"])
with col3:
    st.write("💰 Gold:", player["gold"])

st.progress(player["hp"]/player["max_hp"])

st.markdown("---")

# =========================
# MAP
# =========================
st.subheader("🗺️ WORLD MAP")

for y in range(5):
    cols = st.columns(5)
    for x in range(5):
        cell = WORLD[y][x]

        if player["x"] == x and player["y"] == y:
            cols[x].markdown("🧍")
        else:
            cols[x].markdown(cell)

st.markdown("---")

# =========================
# CONTROLS
# =========================
st.subheader("🎮 MOVE")

c1,c2,c3,c4 = st.columns(4)

with c1:
    if st.button("⬆️"):
        move(0,-1)
with c2:
    if st.button("⬇️"):
        move(0,1)
with c3:
    if st.button("⬅️"):
        move(-1,0)
with c4:
    if st.button("➡️"):
        move(1,0)

# =========================
# ACTIONS
# =========================
st.subheader("⚔️ ACTION")

if st.button("📜 Quest"):
    give_quest()

if st.button("💾 Save"):
    save_game()

if st.button("📂 Load"):
    load_game()

# =========================
# BATTLE UI
# =========================
enemy = st.session_state.enemy

if enemy:
    st.error(f"👹 {enemy['name']} HP: {enemy['hp']}")

    if st.button("⚔️ Attack"):
        attack()

    if st.button("🧪 Heal Potion"):
        if "Potion" in player["inventory"]:
            player["hp"] = min(player["max_hp"], player["hp"]+40)
            player["inventory"].remove("Potion")
