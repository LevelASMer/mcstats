# Discord Bot
# Work with Python 3.7.3 Linux

import os
import ctypes
import psycopg2
from discord import Game, Status, Embed
from discord.ext import commands

BOT_PREFIX = ("?", "!")
game = Game("Public Beta")
TOKEN = os.environ['TOKEN']
DB_URL = os.environ['DATABASE_URL']

# This specifies what extensions to load when the bot starts up
startup_extensions = ["overstats", "cafechat"]

bot = commands.Bot(command_prefix=BOT_PREFIX, description='A Discord Bot by DevHackers\nBuild 2019.07.11 UTC+09:00\nUpdate: ranranru command update')

def create_connection():
    # Create a database connection to a PostgreSQL database
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS users ("
                "id bigint PRIMARY KEY,"
                "name text NOT NULL,"
                "rank int,"
                "count int"
            ");"
        )
        conn.commit()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS ranranru ("
                "id int PRIMARY KEY,"
                "count int NOT NULL"
            ");"
        )
        conn.commit()

        cur.execute(
            "INSERT INTO ranranru (id, count) "
            "SELECT * FROM (SELECT 1, 0) AS tmp "
            "WHERE NOT EXISTS ("
                "SELECT id FROM ranranru WHERE id = 1"
            ") LIMIT 1;"
        )
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        conn.close()

@bot.event
async def on_ready():
    await bot.change_presence(status=Status.online, activity=game)
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def load(ctx, extension_name : str=None, description='Load extension'):
    # Loads an extension.
    if extension_name is None:
        await ctx.send("Please input extension name.")
    else:
        try:
            bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))

@bot.command()
async def unload(ctx, extension_name : str=None, description='Unload extension'):
    # Unloads an extension.
    if extension_name is None:
        await ctx.send("Please input extension name.")
    else:
        bot.unload_extension(extension_name)
        await ctx.send("{} unloaded.".format(extension_name))

@bot.command()
async def list(ctx, description='Show available extensions'):
    await ctx.send("List of extensions: {}".format(startup_extensions))

@bot.event
async def on_message(message):
    channel = message.channel
    if message.content.startswith("ㄹㄹㄹ"):
        try:
            conn = psycopg2.connect(DB_URL, sslmode='require')
            cur = conn.cursor()

            try:
                cur.execute("UPDATE ranranru SET count = count + 1 WHERE id = 1")
                conn.commit()
            except psycopg2.Error as e:
                print(e)
            finally:
                cur.execute("SELECT count FROM ranranru WHERE id = 1")
                result = cur.fetchall()

                for row in result:
                    embed = Embed(title="란란루를 외치셨습니다", description="총 란란루 횟수: {}".format(row[0]), color=0x7289da)
                    await channel.send(embed=embed)
        except psycopg2.Error as e:
            print(e)
        finally:
            conn.close()

    await bot.process_commands(message)
    
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    create_connection()

    bot.run(TOKEN)
