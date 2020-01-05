# CafeChat SE
# Work with Python 3.7.3 Linux

import os
import psycopg2
import platform
from sys import version
from datetime import datetime
from random import random, gauss, randint
from scipy.stats import norm
from discord import Embed, Emoji
from discord.ext import commands

DB_URL = os.environ['DATABASE_URL']

def percent_box():
    per1 = round(random() * 100) % 10
    box = "["
    i = 0

    while i < per1:
        i += 1
        box += "■"

    while i < 10:
        i += 1
        box += "□"

    box += "] "

    per2 = 0 if per1 == 10 else round(random() * 10) % 10
    result = box + (str(per1) if per1 > 0 else "") + str(per2) + "." + (str(round(random() * 100) % 100) if per1 != 10 else "00") + "%"

    return result

class CafeChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ran Ran Ru!
    @commands.command(pass_context=True, aliases=['rrr', 'fff', 'ㄹㄹㄹ', '란란루'], description='Say Ran Ran Ru')
    async def ranranru(self, ctx):
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
                    await ctx.send(embed=embed)
        except psycopg2.Error as e:
            print(e)
        finally:
            conn.close()

    # Cheese!
    @commands.command(aliases=['사진기'], description='Cheese!')
    async def camera(self, ctx):
        await ctx.send(":camera_with_flash: 찰칵! :camera_with_flash:")

    # Show Rank
    @commands.command(pass_context=True, aliases=['랭크'], description='Show your rank')
    async def rank(self, ctx):
        try:
            conn = psycopg2.connect(DB_URL, sslmode='require')
            cur = conn.cursor()

            try:
                cur.execute(
                    "INSERT INTO users (id, name, rank, count) "
                    "SELECT * FROM (SELECT {0}, '{1}', 1, 0) AS tmp "
                    "WHERE NOT EXISTS ("
                        "SELECT id FROM users WHERE id = {0}"
                    ") LIMIT 1;".format(
                        ctx.message.author.id,
                        ctx.message.author.name
                    )
                )
                conn.commit()
            except psycopg2.Error as e:
                print(e)
            finally:
                data = cur.execute("SELECT rank FROM users WHERE id={}".format(ctx.message.author.id))
                result = cur.fetchall()

                for row in result:
                    await ctx.send("현재 랭크: {}".format(row[0]))
        except psycopg2.Error as e:
            print(e)
        finally:
            conn.close()

    # Generate Random Percent
    @commands.command(pass_context=True, aliases=['평균', '확률'], description='Generate random percentage')
    async def percent(self, ctx, *, subject : str=None):
        if subject is None:
            await ctx.send("{}의 확률\n{}".format(ctx.message.author.mention, percent_box()))
        else:
            await ctx.send("{}의 {} 확률\n{}".format(ctx.message.author.mention, subject, percent_box()))

    # Generate Random IQ
    @commands.command(pass_context=True, aliases=['아이큐', '지능'], description='Generate random IQ')
    async def iq(self, ctx):
        iq = int(gauss(100.0, 15.0))
        percent = int(norm.cdf((iq - 100.0) / 15.0) * 100)

        idx_iq = int(iq / 10)
        if iq is 88:
            result_list = "<:mamja:282829569420165121>"
        if iq is 95:
            result_list = "<:dntks:281632203362926594>"
        if iq is 96:
            result_list = "<:dntks:281632203362926594>"
        if iq is 97:
            result_list = "<:dntks:281632203362926594>"
        if iq is 98:
            result_list = "<:dntks:281632203362926594>"
        if iq is 99:
            result_list = "<:dntks:281632203362926594>"
        elif iq is 116:
            result_list = "<:haba:535884612149444610>"
        elif iq is 130:
            result_list = "<:mensa:543726315564433408>"
        else:
            iq_list = {
                4: "<:muncher:312635223445864448>",
                5: "<:muncher:312635223445864448>",
                6: "<:muncher:312635223445864448>",
                7: "<:qjtjt:662978800497459220>",
                8: "<:alth:281630097780244485>",
                9: "<:dytnfwlvkddl:281633702188941312>",
                10: "<:dntdma:281634197745958922>",
                11: "<:roa:281632770764177409>",
                12: "<:tjsanf:290502846099750912>",
                13: "<:vjwmf:281634733824147457>",
                14: "<:bono:308806567946616832>",
                15: "<:bono:308806567946616832>",
            }

            result_list = iq_list[idx_iq]

        ret = "%s의 IQ는 %d 입니다. %s " % (ctx.message.author.mention, iq, result_list)

        if percent >= 50:
            ret += '(상위 %d%%)' % (100 - percent)
        else:
            ret += '(하위 %d%%)' % (percent)

        await ctx.send(ret)

    # Time
    @commands.command(aliases=['시간'], description='Show current time')
    async def time(self, ctx):
        now = datetime.now()
        await ctx.send("{0.year}년 {0.month}월 {0.day}일 {0.hour}시 {0.minute}분 {0.second}초".format(now))

    # Version
    @commands.command(pass_context=True, aliases=['버전'], description='This bot\'s info')
    async def version(self, ctx):
        await ctx.send(
            "CafeChat Extension by DevHackers from SMWComm."
            "```css\n"
            "Python Version: {}\n"
            "System: {}\nNode: {}\n"
            "Release: {}\n"
            "Version: {}\n"
            "Machine: {}"
            "```"
            .format(
                version.split('\n'),
                platform.system(),
                platform.node(),
                platform.release(),
                platform.version(),
                platform.machine()
            )
        )

def setup(bot):
    bot.add_cog(CafeChat(bot))
