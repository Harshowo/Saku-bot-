
import discord
from discord.ext import commands
import random
import json
from discord import Embed
from dotenv import load_dotenv
import os

# Load bot token from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot setup
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Data structures
floors = {i: {"name": f"Floor {i}", "monsters": [], "boss": None} for i in range(1, 101)}
player_data = {"items": [], "level": 1, "xp": 0, "health": 100, "monster_eyes": 0}
leaderboard = {}

all_monsters = [
    {"name": "Goblin 🌟🌀✨", "health": 20, "damage": 5, "drops": ["Monster Eyes", "basic gear"]},
    {"name": "Orc 🪓🥩💀", "health": 50, "damage": 15, "drops": ["Monster Eyes", "advanced gear"]},
    {"name": "Dragon 🐉🔥✨💎", "health": 200, "damage": 50, "drops": ["Monster Eyes", "legendary gear"]},
    {"name": "Zombie 🧟‍♂️🌿🍄", "health": 30, "damage": 10, "drops": ["Monster Eyes", "food"]},
    {"name": "Skeleton ☠️🎻🕯️", "health": 40, "damage": 12, "drops": ["Monster Eyes", "bones"]},
    {"name": "Troll 🌋🪨🌀", "health": 60, "damage": 20, "drops": ["Monster Eyes", "rock"]},
]

all_bosses = [
    {"name": "Minotaur 🐃🔥⚔️🌪️", "health": 300, "damage": 75, "drops": ["Monster Eyes", "epic gear"]},
    {"name": "Lich King 👑🕸️❄️💀", "health": 500, "damage": 100, "drops": ["Monster Eyes", "artifact"]},
    {"name": "Demon Lord 🌌🖤🔥✨", "health": 700, "damage": 120, "drops": ["Monster Eyes", "demonic relic"]},
]

# Populate floors
for i in range(1, 101):
    if i % 10 == 0:  # Boss floors
        floors[i]["boss"] = random.choice(all_bosses)
    else:
        floors[i]["monsters"] = [random.choice(all_monsters) for _ in range(random.randint(1, 5))]

# Commands
@bot.event
async def on_ready():
    print(f"{bot.user} is now online and ready for adventure!")

@bot.command()
async def enter_floor(ctx, floor: int):
    if floor < 1 or floor > 100:
        await ctx.send("Invalid floor! Choose between 1 and 100.")
        return

    floor_data = floors[floor]
    if floor_data["boss"]:
        await ctx.send(f"Welcome to Floor {floor}: {floor_data['boss']['name']} awaits!")
    else:
        await ctx.send(f"Welcome to Floor {floor}: Prepare to fight monsters!")
    await fight(ctx, floor)

async def fight(ctx, floor):
    floor_data = floors[floor]
    if floor_data["boss"]:
        enemy = floor_data["boss"]
    else:
        enemy = random.choice(floor_data["monsters"])

    player_hp = player_data["health"]
    enemy_hp = enemy["health"]

    await ctx.send(f"Battle begins! You are fighting {enemy['name']} (HP: {enemy_hp}, Damage: {enemy['damage']})")

    while player_hp > 0 and enemy_hp > 0:
        # Player's turn
        damage = random.randint(10, 20)
        enemy_hp -= damage
        await ctx.send(f"You dealt {damage} damage to {enemy['name']}. Enemy HP: {max(enemy_hp, 0)}")

        if enemy_hp <= 0:
            loot = random.choice(enemy["drops"])
            await ctx.send(f"You defeated {enemy['name']}! You loot: {loot}")
            player_data["items"].append(loot)
            player_data["monster_eyes"] += 10
            player_data["xp"] += 20
            break

        # Enemy's turn
        damage = enemy["damage"]
        player_hp -= damage
        await ctx.send(f"{enemy['name']} dealt {damage} damage to you. Your HP: {max(player_hp, 0)}")

        if player_hp <= 0:
            await ctx.send("You were defeated! Better luck next time.")
            player_data["health"] = 100  # Reset health
            break

    player_data["health"] = player_hp

@bot.command()
async def shop(ctx):
    shop_items = {
        "potion": 20,
        "sword": 50,
        "shield": 50,
    }
    embed = Embed(title="Shop", description="Spend your Monster Eyes here!", color=0xffd700)
    for item, price in shop_items.items():
        embed.add_field(name=item.capitalize(), value=f"{price} Monster Eyes", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def leaderboard(ctx):
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    msg = "
".join([f"{player}: {xp} XP" for player, xp in sorted_leaderboard])
    await ctx.send(f"Leaderboard:
{msg}")

@bot.command()
async def monster_info(ctx):
    monster = random.choice(all_monsters)
    await ctx.send(f"Random Monster:
{monster['name']} - HP: {monster['health']}, Damage: {monster['damage']}")

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
