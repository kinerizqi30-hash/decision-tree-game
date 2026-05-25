import streamlit as st
import random

# =========================
# RPG LEGEND - STREAMLIT VERSION
# =========================

# Session state
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

# Weapon data
weapons = {
    "Tangan Kosong": (3, 7),
    "Pedang Kayu": (8, 14),
    "Pedang Besi": (15, 22),
    "Pedang Legendaris": (25, 40)
}

# Monster data
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

def rand(min_val, max_val):
    return random.randint(min_val, max_val)


def level_up():
    need = player["level"] * 60

    if player["exp"] >= need:
        player["level"] += 1
        player["max_hp"] += 25
        player["hp"] = player["max_hp"]
        player["exp"] = 0
        player["gold"] += 50
        player["inventory"].append("Potion")

        st.success(f"LEVEL UP! Sekarang level {player['level']}")


def start_battle():
    available = [
        m for m in monsters
        if m["level"] <= player["level"] + 1
    ]

    base = random.choice(available)

    st.session_state.enemy = {
        "name": base["name"],
        "hp": base["hp"] + player["level"] * 5,
        "min": base["min"] + player["level"] // 2,
        "max": base["max"] + player["level"] // 2
    }


def attack_enemy():
    enemy = st.session_state.enemy

    weapon_damage = weapons[player["weapon"]]

    damage = rand(
        weapon_damage[0],
        weapon_damage[1]
    )

    critical = False

    if rand(1, 100) <= 20:
        damage *= 2
        critical = True

    enemy["hp"] -= damage

    if critical:
        st.warning("CRITICAL HIT!")

    st.success(f"Kamu menyerang {damage} damage!")

    if enemy["hp"] <= 0:
        st.success(f"{enemy['name']} dikalahkan!")

        gold_reward = rand(20, 50)
        exp_reward = rand(20, 40)

        player["gold"] += gold_reward
        player["exp"] += exp_reward
        player["score"] += 50

        st.info(f"Gold +{gold_reward}")
        st.info(f"EXP +{exp_reward}")

        if rand(1, 100) <= 35:
            player["inventory"].append("Potion")
            st.info("Mendapat Potion!")

        level_up()

        st.session_state.enemy = None
        return

    # Enemy attack
    enemy_attack = rand(enemy["min"], enemy["max"])

    player["hp"] -= enemy_attack

    if player["hp"] < 0:
        player["hp"] = 0

    st.error(f"Musuh menyerang {enemy_attack} damage!")

    if player["hp"] <= 0:
        game_over()


def use_potion():
    if "Potion" in player["inventory"]:
        player["inventory"].remove("Potion")

        heal = rand(20, 40)

        player["hp"] += heal

        if player["hp"] > player["max_hp"]:
            player["hp"] = player["max_hp"]

        st.success(f"HP bertambah {heal}")

    else:
        st.error("Tidak punya Potion!")


def game_over():
    st.error("GAME OVER")

    player["hp"] = 100
    player["max_hp"] = 100
    player["level"] = 1
    player["exp"] = 0
    player["gold"] = 0
    player["score"] = 0
    player["weapon"] = "Tangan Kosong"
    player["inventory"] = ["Potion"]

    st.session_state.enemy = None

    st.info("Game dimulai ulang!")


def buy_weapon(name, price):
    if player["gold"] >= price:
        player["gold"] -= price
        player["weapon"] = name

        if name not in player["inventory"]:
            player["inventory"].append(name)

        st.success(f"Berhasil membeli {name}")

    else:
        st.error("Gold tidak cukup!")


# =========================
# UI
# =========================

st.set_page_config(
    page_title="RPG Legend",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ RPG LEGEND")

# Sidebar
st.sidebar.header("PLAYER STATUS")

st.sidebar.write(f"❤️ HP : {player['hp']} / {player['max_hp']}")
st.sidebar.write(f"⭐ Level : {player['level']}")
st.sidebar.write(f"✨ EXP : {player['exp']}")
st.sidebar.write(f"💰 Gold : {player['gold']}")
st.sidebar.write(f"🏆 Score : {player['score']}")
st.sidebar.write(f"⚔️ Weapon : {player['weapon']}")
st.sidebar.write("🎒 Inventory:")
st.sidebar.write(", ".join(player["inventory"]))

# Adventure
st.subheader("🏰 Lokasi Petualangan")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌊 Sungai Gelap"):
        start_battle()

    if st.button("⛰️ Gunung Es"):
        start_battle()

with col2:
    if st.button("🏘️ Desa Misterius"):
        gold_found = rand(10, 30)
        player["gold"] += gold_found

        st.success(f"Menemukan {gold_found} gold!")
        start_battle()

    if st.button("🕳️ Gua Gelap"):
        start_battle()

with col3:
    if st.button("🏰 Kastil Tua"):
        player["exp"] += 20
        start_battle()

    if st.button("🌲 Hutan Terlarang"):
        start_battle()

# Shop
st.subheader("🛒 Toko Senjata")

shop1, shop2, shop3 = st.columns(3)

with shop1:
    if st.button("Beli Pedang Kayu (50 Gold)"):
        buy_weapon("Pedang Kayu", 50)

with shop2:
    if st.button("Beli Pedang Besi (120 Gold)"):
        buy_weapon("Pedang Besi", 120)

with shop3:
    if st.button("Beli Pedang Legendaris (250 Gold)"):
        buy_weapon("Pedang Legendaris", 250)

# Battle Area
enemy = st.session_state.enemy

if enemy:
    st.subheader("👹 BATTLE")

    st.write(f"Musuh: {enemy['name']}")
    st.write(f"HP Musuh: {enemy['hp']}")

    b1, b2 = st.columns(2)

    with b1:
        if st.button("⚔️ Serang"):
            attack_enemy()

    with b2:
        if st.button("🧪 Gunakan Potion"):
            use_potion()

else:
    st.info("Belum ada musuh.")
