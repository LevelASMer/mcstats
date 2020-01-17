# Random Donald
# Work with Python 3.7.3 Linux

import os
import psycopg2
from discord import Embed
from discord.ext import commands

DB_URL = os.environ['DATABASE_URL']

class RandomDonald(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ran Ran Ru!
    @commands.command(pass_context=True, aliases=['추가'], description='Add Donald Dictionary')
    async def ranadd(self, ctx, name : str=None, *description):
        if name is None or description is None:
            await ctx.send("!추가 (이름) (내용)")
        else:
            try:
                conn = psycopg2.connect(DB_URL, sslmode='require')
                cur = conn.cursor()

                try:
                    data = str(description)
                    data = data.replace(" ","")
                    data = data.replace(","," ")
                    data = data.replace("(","")
                    data = data.replace(")","")
                    data = data.replace("'","")
                    cur.execute(
                        "INSERT INTO random_donald (name, description) "
                        "SELECT * FROM (SELECT '{0}', '{1}') AS tmp "
                        "WHERE NOT EXISTS ("
                            "SELECT name FROM random_donald WHERE name='{0}'"
                        ") LIMIT 1;".format(
                            name,
                            data
                        )
                    )
                    conn.commit()
                except psycopg2.Error as e:
                    print(e)
                finally:
                    cur.execute("SELECT name, description FROM random_donald WHERE name = '" + name +"'")
                    result = cur.fetchall()

                    for row in result:
                        embed = Embed(title="추가 되었습니다", description="{}: {}".format(row[0],row[1]), color=0x7289da)
                        await ctx.send(embed=embed)
            except psycopg2.Error as e:
                print(e)
            finally:
                conn.close()

    # Ran Ran Ru!
    @commands.command(pass_context=True, aliases=['삭제'], description='Delete Donald Dictionary')
    async def randel(self, ctx, name : str=None):
        if name is None:
            await ctx.send("!삭제 (이름)")
        else:
            try:
                conn = psycopg2.connect(DB_URL, sslmode='require')
                cur = conn.cursor()

                try:
                    cur.execute("DELETE FROM random_donald WHERE name = '" + name + "'")
                    conn.commit()
                except psycopg2.Error as e:
                    print(e)
                finally:
                    embed = Embed(title="삭제 되었습니다", description="", color=0x7289da)
                    await ctx.send(embed=embed)
            except psycopg2.Error as e:
                print(e)
            finally:
                conn.close()

    # Ran Ran Ru!
    @commands.command(pass_context=True, aliases=['검색'], description='Search Donald Dictionary')
    async def ransearch(self, ctx, name : str=None):
        if name is None:
            await ctx.send("!검색 (이름)")
        else:
            try:
                conn = psycopg2.connect(DB_URL, sslmode='require')
                cur = conn.cursor()

                try:
                    cur.execute("SELECT name, description FROM random_donald WHERE name = '" + name + "'")
                    result = cur.fetchall()

                    for row in result:
                        embed = Embed(title=row[0], description=row[1], color=0x7289da)
                        await ctx.send(embed=embed)
                except psycopg2.Error as e:
                    embed = Embed(title="검색 결과가 없습니다.", description="", color=0x7289da)
                    await ctx.send(embed=embed)
                    print(e)
            except psycopg2.Error as e:
                print(e)
            finally:
                conn.close()

    # Ran Ran Ru!
    @commands.command(pass_context=True, aliases=['랜덤'], description='Generate randomly Donald Dictionary')
    async def ranrandom(self, ctx):
        try:
            conn = psycopg2.connect(DB_URL, sslmode='require')
            cur = conn.cursor()

            try:
                cur.execute("SELECT name, description FROM random_donald ORDER BY RANDOM() LIMIT 1")
                result = cur.fetchall()

                for row in result:
                    embed = Embed(title=row[0], description=row[1], color=0x7289da)
                    await ctx.send(embed=embed)
            except psycopg2.Error as e:
                embed = Embed(title="검색 결과가 없습니다.", description="", color=0x7289da)
                await ctx.send(embed=embed)
                print(e)
        except psycopg2.Error as e:
            print(e)
        finally:
            conn.close()

def setup(bot):
    bot.add_cog(RandomDonald(bot))
