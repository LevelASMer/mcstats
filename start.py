# Discord Bot + GUI
# Work with Python 3.7.3 Linux

import os
import ctypes
import psycopg2
import threading, time
import tkinter as tk
from discord import Game, Status, Embed
from discord.ext import commands

BOT_PREFIX = ("?", "!")
game = Game("Public Beta")
TOKEN = os.environ['TOKEN']
DB_URL = os.environ['DATABASE_URL']

# This specifies what extensions to load when the bot starts up
startup_extensions = ["overstats", "cafechat", "random_donald"]

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

        cur.execute(
            "CREATE TABLE IF NOT EXISTS random_donald ("
                "name text PRIMARY KEY NOT NULL,"
                "description text NOT NULL"
            ");"
        )
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        conn.close()

def ranranru_count():
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
        cur = conn.cursor()

        try:
            cur.execute("UPDATE ranranru SET count = count + 1 WHERE id = 1")
            conn.commit()
        except psycopg2.Error as e:
            print(e)
    except psycopg2.Error as e:
        print(e)
    finally:
        conn.close()

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
    if message.content.startswith("fff"):
        ranranru_count()
    if message.content.startswith("rrr"):
        ranranru_count()
    if message.content.startswith("ㄹㄹㄹ"):
        ranranru_count()
    if message.content.startswith("란란루"):
        ranranru_count()
    await bot.process_commands(message)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Run Bot"
        self.hi_there["command"] = self.runbotButton
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def runbotButton(self):
        t = threading.Thread(target=letrunbot)
        t.daemon = True
        t.start()

def letrunbot():
    bot.run(TOKEN)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(status=Status.online, activity=game)

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    create_connection()

    root = tk.Tk()
    root.title("McStats")
    root.geometry("640x480")
    app = Application(master=root)
    app.mainloop()
