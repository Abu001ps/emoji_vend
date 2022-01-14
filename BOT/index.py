import discord
from discord.ext import commands
import random
import randomstring
import json
import datetime
from datetime import timedelta
from datetime import timedelta
import sqlite3
from discord_components import *
import os
import asyncio
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
from discord.ext.commands import CommandNotFound

_TOKEN_ = "봇 토큰"


intents = discord.Intents.all()
client = commands.Bot(
    intents=intents,
    command_prefix = "-"
)

database = 'ids/emoji.json' ## 메시지 이모지 저장

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True

def get_expiretime(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        how_long = (ExpireTime - ServerTime)
        days = how_long.days
        hours = how_long.seconds // 3600
        minutes = how_long.seconds // 60 - hours * 60
        return str(round(days)) + "일 " + str(round(hours)) + "시간 " + str(round(minutes)) + "분" 
    else:
        return False

def prime_number(number):
    if number != 1:                 
        for f in range(2, number):  
            if number % f == 0:     
                return False
    else:
        return False
    return True

def make_expiretime(days):
    ServerTime = datetime.datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = (ServerTime + timedelta(days=days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def add_time(now_days, add_days):
    ExpireTime = datetime.datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def nowstr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM sever;")
    data = cur.fetchone()[0]
    con.close()
    return data

def get_buylogwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT buylogwebhk FROM sever;")
    data = cur.fetchone()[0]
    con.close()
    return data

def get_roleid(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT roleid FROM sever;")
    data = cur.fetchone()[0]
    con.close()
    if (str(data).isdigit()):
        return int(data)
    else:
        return data

@client.event
async def on_ready():
    print("βετα Online")
    DiscordComponents(client)
    while True:
        await client.change_presence(activity=discord.Game(name=f"{len(client.guilds)}개의 서버에서"))

master_ids=[899093949891903489, 189355862983180298,900025157022806147]
@client.command()
async def 명령어(ctx):
    embed12 = discord.Embed(title ="Dev Emoji", description= "-명령어 : 이 명령어를 보여줍니다.\n -등록 <라이센스> : 구매하신 라이센스를 등록 합니다.\n -세팅 : 구매하는 이모지를 생성합니다.\n -연장 : 라이센스를 연장합니다.\n -이전 <서버아이디> : 서버를 이전합니다.\n -백업 : DB를 백업합니다.\n -라이센스 : 라이센스가 남은 시간을 보여줍니다.",color=discord.Color.green())
    await ctx.channel.send(embed=embed12)
@client.command()
async def 생성(ctx):
    if ctx.author.id in master_ids:
        try:
            create_day = ctx.message.content.split(" ")[1]
        except:
            await ctx.send("라이센스키 생성도중 오류가 발견되었습니다.\n생성할 날짜수를 작성해주세요")
            return
        try:
            create_amount = int(ctx.message.content.split(" ")[2])
            if (create_amount <= 0 or create_amount > 20):
                raise TypeError
        except:
            await ctx.channel.send("라이센스키 생성도중 오류가 발견되었습니다.\n1개 ~ 20개 사이로 생성해주세요.")
            return

        con = sqlite3.connect("../DB/" + "license.db")
        cur = con.cursor()
        created_licenses = []

        for n in range(create_amount):
            code = randomstring.pick(4).upper()
            code1 = randomstring.pick(4).upper()
            code2 = randomstring.pick(4).upper()
            code3 = randomstring.pick(6).upper()

            tcode = code + '-' + code1 + '-' + code2 + '-' + code3
            cur.execute("INSERT INTO license Values(?, ?, ?, ?, ?);", (tcode, int(create_day), 0, "None", 0))
            created_licenses.append(tcode)

        con.commit()
        con.close()

        await ctx.send("**생성된 라이센스** 날짜 : **`" + create_day + "`** 일\n" + "\n".join(created_licenses) + "\n생성갯수 : **`" + str(create_amount) + "`** 개")
    else:
        await ctx.send(":tools: 당신은 패널 관리자가 아닙니다.\n패널 관리자 권한을 구매하세요.")

@client.command()
async def 이전(ctx):
    if ctx.author.id == ctx.guild.owner.id:
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            j = ctx.message.content.split(" ")
            try:
                j[1]
            except:
                e=discord.Embed(description="서버아이디를 작성해주세요.", color=discord.Color.red())
                e.set_author(name="이전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                await ctx.send(embed=e)
                return
            if not (os.path.isfile("../DB/" + j[1] + ".db")):
                e = discord.Embed(description="잠시만 기다려주세요.", color=discord.Color.green())
                e.set_author(name="DB 이전중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                gg = await ctx.send(embed=e)
                file_oldname = os.path.join("../db/", str(ctx.guild.id) + ".db")
                file_newname_newfile = os.path.join("../db/", j[1] + ".db")
                os.rename(file_oldname, file_newname_newfile) ## 파일이름 수정
                await asyncio.sleep(1)
                await gg.delete()
                e = discord.Embed(description="", color=discord.Color.green())
                e.set_author(name="이전완료", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
                e.add_field(
                    name="DB이전이 완료되었습니다.",
                    value=f"{ctx.guild.id}.db => " + j[1] + ".db"
                )
                await ctx.send(embed=e)
            else:
                e=discord.Embed(description="이미 존재하는 DB입니다.", color=discord.Color.red())
                e.set_author(name="이전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                await ctx.send(embed=e)
                return
        else:
            e=discord.Embed(description="해당서버는 등록되지 않은 서버입니다.", color=discord.Color.red())
            e.set_author(name="이전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
    else:
        e=discord.Embed(description="당신은 서버의 소유자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="이전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.send(embed=e)
        return

@client.command()
async def 역할(ctx):
    con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
    cur = con.cursor()
    cur.execute(f"select roleid from sever;")
    data = cur.fetchone()
    data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
    roles = discord.utils.get(ctx.guild.roles, id=int(data1))
    await ctx.author.add_roles(roles)

@client.command()
async def 삭제(ctx):
    if ctx.author.id in master_ids:
        j = ctx.message.content.split(" ")
        try:
            j[1]
        except:
            e=discord.Embed(description="서버아이디를 제대로 작성해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
        if (os.path.isfile("../DB/" + str(j[1]) + ".db")):
            e = discord.Embed(description="잠시만 기다려주세요.", color=discord.Color.green())
            e.set_author(name="DB삭제중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
            gg = await ctx.send(embed=e)
            await asyncio.sleep(1)
            e=discord.Embed(
                title="DB삭제가 완료되었습니다.",
                description=f"삭제된 DB : {j[1]}.db",
                color=discord.Color.blue()
            )
            file=discord.File('../db/' + j[1] + ".db")
            e.set_author(name="삭제완료", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
            await gg.edit(embed=e)
            await ctx.send(file=file)
            os.remove("../db/" + j[1] + ".db")
        else:
            e=discord.Embed(description="해당 DB는 없는 DB입니다.", color=discord.Color.red())
            e.set_author(name="삭제실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
    else:
        return

@client.command()
async def 등록(ctx):
    if ctx.author.guild_permissions.administrator:
        j = ctx.message.content.split(" ")
        try:
            j[1]
        except:
            e=discord.Embed(description="라이센스 코드를 제대로 작성해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
        con = sqlite3.connect("../DB/license.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM license WHERE code == ?;", (j[1],))
        data = cur.fetchone()
        con.close()                
        if data == None:
            e=discord.Embed(description="해당 라이센스키는 없는 라이센스키 입니다.\n관리자에게 문의해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
        if data[2] == 1:
            e=discord.Embed(description="해당 라이센스키는 이미 사용된 라이센스키 입니다.\n관리자에게 문의해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            e=discord.Embed(description="서버는 이미 등록된 서버입니다.\n`-연장` 으로 연장해주세요.", color=discord.Color.red())
            e.set_author(name="등록실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
        else:
            e = discord.Embed(description="", color=discord.Color.green())
            e.set_author(name="서버등록중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
            gg = await ctx.send(embed=e)
            date = data[1]
            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), ctx.guild.id, j[1]))
            con.commit()
            con.close()
            con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("CREATE TABLE sever (id INTEGER, expiredate TEXT, pw TEXT, roleid INTEGER, logwebhk TEXT, buylogwebhk TEXT, vip INTENGER, vvip INTENGER, cal INTENGER);")
            con.commit()
            pw = randomstring.pick(6)
            cur.execute("INSERT INTO sever VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (ctx.guild.id, make_expiretime(date), pw, 0, "", "", 0, 0, 0))
            con.commit()
            cur.execute("CREATE TABLE owner (cid TEXT, cpw TEXT, own TEXT, bank TEXT, num INTENGER);")
            con.commit()
            cur.execute("INSERT INTO owner VALUES(?, ?, ?, ?, ?);", ("", "", "", "", 0))
            con.commit()
            cur.execute("CREATE TABLE user (id INTEGER, money INTEGER, warn INTENGER, black INTENGER, buy INTENGER, vip INTENGER, vvip INTENGER);")
            con.commit()
            cur.execute("CREATE TABLE product (name INTEGER, money INTEGER, stock TEXT);")
            con.commit()
            con.close()
            await asyncio.sleep(1)
            e = discord.Embed(
                description="서버가 정상적으로 등록되었습니다.",
                color=discord.Color.blue()
            )
            e.set_author(name="등록완료", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
            e.add_field(
                name="서버 정보",
                value="서버이름 : **`" + str(ctx.guild.name) + "`**\n라이센스 기간: `"+ str(date) + "`일\n만료일: `" + make_expiretime(date) + "`\n아이디: `" +str(ctx.guild.id) + "`\n비밀번호: `" + pw + "`"
            )
            e1=discord.Embed(
                description="DM을 확인해주세요",
                color=discord.Color.blue()
            )
            e1.set_author(name="등록완료", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
            await gg.edit(embed=e1)
            await ctx.author.send(
                embed=e,
                components = [
                    [
                        Button(label = "웹패널", style=ButtonStyle.URL, url="http://iker.mcgo.kr/", emoji="🌐")
                    ]
                ]
            )
            return
    else:
        e=discord.Embed(description="당신은 서버의 관리자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="조회실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.send(embed=e)
        return

@client.command()
async def 세팅(ctx):
    if ctx.author.guild_permissions.administrator:
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
            cur = con.cursor()
            cur.execute("SELECT * FROM sever;")
            cmdchs = cur.fetchone()
            con.close()
            try:
                await ctx.message.delete()
            except:
                pass

            msg = await ctx.channel.send("이용하시려면 아래의 이모지를 클릭해주세요")
            await msg.add_reaction('<:102658E53E3941588D1B03C26018BDD8:908342891561242644>')

            with open(database, 'r') as f:
                data = json.loads(f.read())

            new_value = {'msg' : f'{msg.id}'}
            data[f'{ctx.channel.guild.id}'] = new_value

            with open(database, 'w') as f:
                f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            e=discord.Embed(description="등록되지 않은 서버입니다.\n라이센스키를 구입하여 등록 해주세요.", color=discord.Color.red())
            e.set_author(name="세팅실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
    else:
        e=discord.Embed(description="당신은 서버의 관리자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="세팅실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.send(embed=e)
        return

@client.command()
async def 연장(ctx):
    if ctx.author.guild_permissions.administrator:
        try:
            license_add = ctx.message.content.split(" ")[1]
        except:
            await ctx.send("서버 연장실패\n연장할 라이센스키를 작성해주세요.")
            return
        con = sqlite3.connect("../DB/" + "license.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM license WHERE code == ?;", (license_add,))
        search_result = cur.fetchone()
        con.close()
        if (search_result != None):
            if (search_result[2] == 0):
                if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
                    e=discord.Embed(
                        description="잠시만 기다려주세요.",
                        color=discord.Color.green()
                    )
                    e.set_author(name="연장하는중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                    gg = await ctx.send(embed=e)
                    con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM sever;")
                    server_info = cur.fetchone()
                    if (is_expired(server_info[1])):
                        new_expiretime = make_expiretime(search_result[1])
                    else:
                        new_expiretime = add_time(server_info[1], search_result[1])
                    cur.execute("UPDATE sever SET expiredate = ?;", (new_expiretime,))
                    con.commit()
                    con.close()
                    con = sqlite3.connect("../DB/" + "license.db")
                    cur = con.cursor()
                    cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), ctx.guild.id, license_add))
                    con.commit()
                    con.close()
                    await asyncio.sleep(1)
                    e=discord.Embed(
                        title="사용해주셔서 감사합니다",
                        description="연장된 기간 : **`" + str(search_result[1]) + "`** 일",
                        color=discord.Color.green()
                    )
                    e.set_author(name="연장성공", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
                    await gg.edit(embed=e)
                else:
                    e=discord.Embed(description="이 명령어는 등록된 서버만 사용 가능합니다\n`-등록` 으로 등록을 먼저 해주세요.", color=discord.Color.red())
                    e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                    await ctx.send(embed=e)
                    return
            else:
                e=discord.Embed(description="이 코드는 사용된 코드입니다.\n문제가 있다면 판매자에게 문의해주세요.", color=discord.Color.red())
                e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                await ctx.send(embed=e)
                return
        else:
            e=discord.Embed(description="존재하지 않는 라이센스입니다.\n문제가 있다면 판매자에게 문의해주세요.", color=discord.Color.red())
            e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
            await ctx.send(embed=e)
            return
    else:
        e=discord.Embed(description="당신은 서버의 관리자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="연장실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.send(embed=e)
        return

@client.command()
async def 라이센스(ctx):
    if ctx.author.guild_permissions.administrator:
        con = sqlite3.connect("../DB/" + str(ctx.guild.id) + ".db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM sever;")
        except:
            return
        cmdchs = cur.fetchone()
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M')
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            if nowDatetime >= cmdchs[1]:
                e=discord.Embed(description="기간이 만료된 서버입니다.\n연장을 원할시 `-연장` 으로 연장해주세요.", color=discord.Color.red())
                e.set_author(name="조회실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                await ctx.send(embed=e)
                return
            else:
                await ctx.send("만료일: " + cmdchs[1] + "\n( " + get_expiretime(cmdchs[1]) + " )")
        else:
            await ctx.send("현재 이 서버는 등록되지 않은 서버입니다.\n라이센스 코드를 구입하여 등록해주세요.")
            return
    else:
        e=discord.Embed(description="당신은 서버의 관리자 권한이 없습니다.", color=discord.Color.red())
        e.set_author(name="조회실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
        await ctx.send(embed=e)
        return

@client.command()
async def 백업(ctx):
    if ctx.guild.owner.id == ctx.author.id:
        if (os.path.isfile("../DB/" + str(ctx.guild.id) + ".db")):
            file = discord.File('../DB/' + str(ctx.guild.id) + ".db")
            await ctx.send("> DM을 확인해주세요")
            ServerTime = datetime.datetime.now()
            ExpireTime_STR = ServerTime.strftime('%Y-%m-%d %H:%M')
            await ctx.author.send("DB가 백업되었습니다\n백업날짜 : " + ExpireTime_STR, file=file)
        else:
            await ctx.send("등록되지 않은 서버이므로 백업할 DB가 없습니다")
            return
    else:
        await ctx.send("> 당신은 서버 소유 권한이 없습니다")
        return

@client.event
async def on_raw_reaction_add(payload):
    if not (os.path.isfile("../DB/" + str(payload.guild_id) + ".db")):
        return
    emoji, user, member, channel = payload.emoji, await client.fetch_user(user_id=payload.user_id), payload.member, client.get_channel(payload.channel_id)
    try:
        msg = await channel.fetch_message(payload.message_id)
    except:
        return
    data = json.loads(open(database).read())
    author = payload.user_id 
    payload.guild_id = payload.guild_id
    try:
        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
    except:
        return
    if user.bot:
        return
    try:
        json_guild = data[f'{payload.guild_id}']
    except: 
        return

    cur = con.cursor()
    cur.execute("SELECT * FROM sever;")
    cmdchs = cur.fetchone()

    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M')

    if not nowDatetime >= cmdchs[1]:
        if str(payload.message_id) == json_guild['msg']:
            if str(payload.emoji) == '<:102658E53E3941588D1B03C26018BDD8:908342891561242644>':
                con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                cur = con.cursor()
                cur.execute("SELECT * FROM user WHERE id == ?;", (author,))
                user_info = cur.fetchone()
                if (user_info == None):
                    cur.execute("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?);", (author, 0, 0, 0, 0, 0, 0))
                    con.commit()
                await msg.clear_reactions()
                await msg.add_reaction('<:102658E53E3941588D1B03C26018BDD8:908342891561242644>')
                m = discord.Embed(
                    title="2021 VEND",
                    description="무엇을 하시겠습니까?",
                    color=discord.Color.green()
                )
                m.add_field(
                    name="카테고리",
                    value="0️⃣ 구매\n1️⃣ 재고확인\n2️⃣ 충전\n3️⃣ 정보확인"
                )
                m.set_footer(
                    text = f"현재 자판기 서버 : {str(msg.guild.name)}"
                )
                try:
                    gh = await user.send(embed=m)
                    await gh.add_reaction("0️⃣")
                    await gh.add_reaction("1️⃣")
                    await gh.add_reaction("2️⃣")
                    await gh.add_reaction("3️⃣")
                except:
                    return
                while True:
                    def check(reaction, user):
                        return user == payload.member
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        return

                    if (str(reaction.emoji) == '0️⃣'):
                        try:
                            await gh.delete()
                        except:
                            pass
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        try:
                            cur.execute("SELECT * FROM product;")
                        except:
                            await user.send("아무런 제품이 없습니다")
                            return
                        products = cur.fetchall()

                        product_list = []
                        for product in products:
                            if (product[2] != ""):
                                product_list.append(SelectOption(label=f"{product[0]}",description=str(product[1]) + "원/" + str(len(product[2].split("\n"))) + "개", value=f"{product[0]}"))
                            else:
                                product_list.append(SelectOption(label=f"{product[0]}",description=str(product[1]) + "원/재고소진", value=f"{product[0]}"))

                        try:
                            gg = await user.send(
                                "구매하실 목록을 선택해주세요",
                                components=[Select(placeholder="구매하기", options=product_list)]
                            )
                        except:
                            e=discord.Embed(description="해당서버엔 아무런 제품이 없습니다.", color=discord.Color.red())
                            e.set_author(name="구매실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                            await user.send(embed=e)
                            return
                        try:
                            ctx = await client.wait_for("select_option", timeout=60.0)
                        except asyncio.TimeoutError:
                            try:
                                await gg.delete()
                            except:
                                pass
                            await try_msg.delete()
                            e=discord.Embed(description="시간이 초과되었습니다.", color=discord.Color.red())
                            e.set_author(name="구매실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                            await user.send(embed=e)
                            return
                        product_name = ctx.values[0]
                        cur.execute("SELECT * FROM product WHERE name = ?;", (str(product_name),))
                        product_info = cur.fetchone()
                        if (product_info != None):
                            if (str(product_info[2]) != ""):
                                await gg.delete()
                                e=discord.Embed(
                                    title="수량선택",
                                    description=f"아래 이모지 `📩` 를 눌러 {product_name} 제품 `1`개를 구매합니다.\n갯수를 수정하고 싶다면 `✏️` 이모지를 클릭해주세요.",
                                    color=discord.Color.green()
                                )
                                info_msg = await user.send(embed=e)
                                try:
                                    await info_msg.add_reaction("📩")
                                    await info_msg.add_reaction("✏️")
                                except:
                                    pass
                                def check(reaction, user):
                                    return user == payload.member
                                try:
                                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                                except asyncio.TimeoutError:
                                    return
                                if str(reaction.emoji) == "📩":
                                    if (len(product_info[2].split("\n")) >= 1):
                                        if (int(user_info[1]) >= int(product_info[1])):
                                            e=discord.Embed(
                                                description="",
                                                color=discord.Color.green()
                                            )
                                            e.set_author(name="구매진행중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                                            await info_msg.delete()
                                            try_msg = await user.send(embed=e)
                                            stocks = product_info[2].split("\n")
                                            bought_stock = []
                                            for n in range(1):
                                                picked = random.choice(stocks)
                                                bought_stock.append(picked)
                                                stocks.remove(picked)
                                            now_stock = "\n".join(stocks)
                                            now_money = int(user_info[1]) - (int(product_info[1]))
                                            now_bought = int(user_info[2]) + (int(product_info[1]))
                                            con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                            cur = con.cursor()
                                            cur.execute("UPDATE user SET money = ?, warn = ? WHERE id == ?;", (now_money, now_bought, author))
                                            con.commit()
                                            cur.execute("UPDATE product SET stock = ? WHERE name == ?;", (now_stock, product_name))
                                            con.commit()
                                            con.close()
                                            bought_stock = "\n".join(bought_stock)
                                            if (len(bought_stock) > 1000):
                                                con = sqlite3.connect("../DB/docs.db")
                                                cur = con.cursor()
                                                docs_name = randomstring.pick(30)
                                                cur.execute("INSERT INTO docs VALUES(?, ?);", (docs_name, bought_stock))
                                                con.commit()
                                                con.close()
                                                docs_url = "http://iker.mcgo.kr/rawviewer/" + docs_name
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기](http://iker.mcgo.kr/)', color=0x00ff00)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user.name), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `" + str(buy_amount) + "`개 구매 감사합니다! :thumbsup:"))
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)

                                                    except:
                                                        pass

                                                    e = discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="이용해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False).add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1])) + "`원", inline=False)
                                                    await try_msg.edit(embed=e)
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        e=discord.Embed(
                                                            title="구매 실패",
                                                            description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요."
                                                        )
                                                        await try_msg.edit(embed=e)

                                            else:
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기](http://iker.mcgo.kr/)', color=0x00ff00)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value=bought_stock, inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `1`개 구매 감사합니다! :thumbsup:"))
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)
                                                    except:
                                                        pass

                                                    e=discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="구매해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False)
                                                    e.add_field(name="구매하신 코드", value="`" + str(bought_stock) + "`", inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1])) + "`원", inline=False)
                                                    await asyncio.sleep(1)
                                                    await try_msg.delete()
                                                    await user.send(embed=e)
                                                    await user.send(f"{str(bought_stock)}")
                                                    return
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        pass
                                                    e=discord.Embed(
                                                        title="제품 구매 실패",
                                                        description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요.",
                                                        color=discord.Color.red()
                                                    )
                                                    await user.send(embed=e)
                                                    return
                                        else:
                                            e=discord.Embed(
                                                title="구매 실패",
                                                description="구매할 돈을 소지하지않고 있습니다",
                                                color=discord.Color.red()
                                            )
                                            await info_msg.delete()
                                            await user.send(embed=e)
                                            return
                                elif str(reaction.emoji) == "✏️":
                                    await info_msg.delete()
                                    e=discord.Embed(
                                        title="수량 설정하기",
                                        description="구매하실 수량을 작성해주세요.",
                                        color=discord.Color.green()
                                    )
                                    gg = await user.send(embed=e)
                                    def check(m):
                                        return user == m.author
                                    try:
                                        msg = await client.wait_for("message", timeout=60.0, check=check)
                                    except asyncio.TimeoutError:
                                        try:
                                            await gg.delete()
                                        except:
                                            pass
                                        e=discord.Embed(
                                            title="시간초과",
                                            description="처음부터 다시 시도해주세요",
                                            color=discord.Color.red()
                                        )
                                        await client.get_user(author).send(embed=e)
                                        return None
                                    if not ((msg.content.isdigit()) and (msg.content != "0")):
                                        e=discord.Embed(
                                            title="구매실패",
                                            description="수량은 숫자로만 입력해주세요",
                                            color=discord.Color.red()
                                        )
                                        await client.get_user(author).send(embed=e)
                                        return None
                                    buy_amount = int(msg.content)
                                    if (len(product_info[2].split("\n")) >= buy_amount):
                                        if (int(user_info[1]) >= int(product_info[1] * buy_amount)):
                                            await gg.delete()
                                            e=discord.Embed(
                                                description="",
                                                color=discord.Color.green()
                                            )
                                            e.set_author(name="구매진행중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                                            try_msg = await client.get_user(author).send(embed=e)
                                            stocks = product_info[2].split("\n")
                                            bought_stock = []
                                            for n in range(buy_amount):
                                                picked = random.choice(stocks)
                                                bought_stock.append(picked)
                                                stocks.remove(picked)
                                            now_stock = "\n".join(stocks)
                                            now_money = int(user_info[1]) - (int(product_info[1]) * buy_amount)
                                            now_bought = int(user_info[2]) + (int(product_info[1]) * buy_amount)
                                            con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                            cur = con.cursor()
                                            cur.execute("UPDATE user SET money = ?, warn = ? WHERE id == ?;", (now_money, now_bought, author))
                                            con.commit()
                                            cur.execute("UPDATE product SET stock = ? WHERE name == ?;", (now_stock, product_name))
                                            con.commit()
                                            con.close()
                                            bought_stock = "\n".join(bought_stock)
                                            if (len(bought_stock) > 1000):
                                                con = sqlite3.connect("../DB/docs.db")
                                                cur = con.cursor()
                                                docs_name = randomstring.pick(30)
                                                cur.execute("INSERT INTO docs VALUES(?, ?);", (docs_name, bought_stock))
                                                con.commit()
                                                con.close()
                                                docs_url = "http://iker.mcgo.kr/rawviewer/" + docs_name
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기](http://iker.mcgo.kr/)', color=0x00ff00)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user.name), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `" + str(buy_amount) + "`개 구매 감사합니다! :thumbsup:"))
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        await user.add_roles(data1)
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)
                                                    except:
                                                        pass

                                                    e = discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="이용해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False).add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="구매하신 코드", value='[구매한 코드 보기](' + docs_url + ')', inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1]) * buy_amount) + "`원", inline=False)
                                                    await try_msg.edit(embed=e)
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        e=discord.Embed(
                                                            title="구매 실패",
                                                            description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요."
                                                        )
                                                        await try_msg.edit(embed=e)
                                                        return

                                            else:
                                                try:
                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                        eb = DiscordEmbed(title='제품 구매 로그', description='[웹 패널로 이동하기](http://iker.mcgo.kr/)', color=0x00ff00)
                                                        eb.add_embed_field(name='디스코드 닉네임', value=str(user), inline=False)
                                                        eb.add_embed_field(name='구매 제품', value=str(product_name), inline=False)
                                                        eb.add_embed_field(name='구매 코드', value=bought_stock, inline=False)
                                                        webhook.add_embed(eb)
                                                        webhook.execute()
                                                    except:
                                                        pass

                                                    try:
                                                        webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_buylogwebhk(payload.guild_id))
                                                        webhook.add_embed(DiscordEmbed(description="<@" + str(author) + ">" + "님, `" + product_name + "` 제품 `" + str(buy_amount) + "`개 구매 감사합니다! :thumbsup:"))
                                                        webhook.execute()
                                                    except:
                                                        pass
                                                    try:
                                                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                                                        cur = con.cursor()
                                                        cur.execute(f"select roleid from sever;")
                                                        data = cur.fetchone()
                                                        data1 = str(data).replace("(", "").replace(")", "").replace(",", "")
                                                        await user.add_roles(data1)
                                                        roles = discord.utils.get(payload.member.guild.roles, id=int(data1))
                                                        await user.add_roles(roles)
                                                    except:
                                                        pass

                                                    e=discord.Embed(
                                                        title="구매가 완료되었습니다",
                                                        description="구매해주셔서 감사합니다",
                                                        color=discord.Color.green()
                                                    )

                                                    e.add_field(name="구매하신 제품", value="`" + product_name + "`", inline=False)
                                                    e.add_field(name="구매하신 코드", value="`" + str(bought_stock) + "`", inline=False)
                                                    e.add_field(name="차감 금액", value="`" + str(int(product_info[1]) * buy_amount) + "`원", inline=False)
                                                    await asyncio.sleep(1)
                                                    await try_msg.delete()
                                                    await user.send(embed=e)
                                                    await user.send(f"{str(bought_stock)}")
                                                    return
                                                except:
                                                    try:
                                                        await try_msg.delete()
                                                    except:
                                                        pass
                                                    e=discord.Embed(
                                                        title="제품 구매 실패",
                                                        description="제품 구매 중 알 수 없는 오류가 발생했습니다.\n샵 관리자에게 문의해주세요.",
                                                        color=discord.Color.red()
                                                    )
                                                    await gh.edit(embed=e)
                                                    return
                                        else:
                                            e=discord.Embed(
                                                title="구매 실패",
                                                description="구매할 돈을 소지하지않고 있습니다",
                                                color=discord.Color.red()
                                            )
                                            try:
                                                await info_msg.delete()
                                            except:
                                                pass
                                            await user.send(embed=e)
                                            return
                    elif (str(reaction.emoji) == '1️⃣'):
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM product;")
                        products = cur.fetchall()
                        products1 = cur.fetchone()
                        con.close()
                        e=discord.Embed(
                            title=f"제품목록입니다.",
                            description="",
                            color=discord.Color.green()
                        )
                        for product in products:
                            if (product[2] != ""):
                                e.add_field(name="제품명 : " + product[0], value="가격: `" + str(product[1]) + "`원\n재고: `" + str(len(product[2].split("\n"))) + "`개")
                            else:
                                e.add_field(name="제품명 : " + product[0], value="가격: " + str(product[1]) + "원\n재고: `부족`")
                        try:
                            await gh.delete()
                        except:
                            pass
                        await user.send(embed=e)
                        break
                    elif str(reaction.emoji) == "2️⃣":
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM user WHERE id == ?;", (user.id,))
                        user_info = cur.fetchone()
                        cur.execute("SELECT * FROM owner;")
                        server_info = cur.fetchone()
                        con.close()
                        if (server_info[0] != "" and server_info[1] != ""):
                            if (user_info != None):
                                def check(m):
                                    return user == m.author
                                try:
                                    e = discord.Embed(
                                        title="문화상품권 충전방법",
                                        description="문화상품권 코드를 `-`을 포함해서 입력해주세요.",
                                        color=discord.Color.green()
                                    )
                                    await gh.delete()
                                    jk21 = await user.send(embed=e)
                                except:
                                    return

                                try:
                                    msg = await client.wait_for("message", timeout=60.0, check=check)
                                except asyncio.TimeoutError:
                                    try:
                                        e = discord.Embed(
                                            title="문화상품권 충전 실패",
                                            description="시간 초과되었습니다.",
                                            color=discord.Color.red()
                                        )
                                        await jk21.edit(embed=e)
                                    except:
                                        pass
                                    return None

                                if msg.content: 
                                    try:
                                        jsondata = {"id" : str(server_info[0]), "pw" : str(server_info[1]), "pin" : msg.content, "token" : "VWlybhv0AgLc8eZgHC2DRqEGa863"}
                                        res = requests.post("http://culture.shard.kr/api/charge", json=jsondata)
                                        if (res.status_code != 200):
                                            raise TypeError
                                        else:
                                            print(str(res))
                                            res = res.json()
                                    except:
                                        try:
                                            e = discord.Embed(
                                                title="문화상품권 충전 실패",
                                                description="일시적인 서버 오류입니다.\n잠시 후 다시 시도해주세요.",
                                                color=discord.Color.red()
                                            )
                                            await jk21.delete()
                                            await client.get_user(author).send(embed=e)
                                        except:
                                            pass
                                        return None

                                    if (res["result"] == True):
                                        culture_amount = int(res["amount"])
                                        cur = con.cursor()
                                        cur.execute("SELECT * FROM user WHERE id == ?;", (msg.author.id,))
                                        user_info = cur.fetchone()
                                        current_money = int(user_info[1])
                                        now_money = current_money + culture_amount
                                        cur.execute("UPDATE user SET money = ? WHERE id == ?;", (now_money, msg.author.id))
                                        con.commit()
                                        con.close()
                                        try:
                                            e=discord.Embed(
                                                title="문화상품권 충전 성공",
                                                description="핀코드: `" + msg.content + "`\n금액: `" + str(culture_amount) + "`원\n충전 후 금액: `" + str(now_money) + "`원",
                                                color=discord.Color.green()
                                            )
                                            await jk21.edit(embed=e)
                                            try:
                                                webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                eb = DiscordEmbed(title='문화상품권 충전 성공', description='[웹 패널로 이동하기](http://iker.mcgo.kr/)', color=0x00ff00)
                                                eb.add_embed_field(name='디스코드 닉네임', value=str(msg.author), inline=False)
                                                eb.add_embed_field(name='핀 코드', value=str(msg.content), inline=False)
                                                eb.add_embed_field(name='충전 금액', value=str(res["amount"]), inline=False)
                                                webhook.add_embed(eb)
                                                webhook.execute()
                                            except:
                                                pass
                                        except:
                                            pass
                                    else:
                                        try:
                                            e.set_author(name="충전실패", icon_url="https://media.discordapp.net/attachments/899122675736272976/899194197305851924/3595-failed.png?width=180&height=180")
                                            e=discord.Embed(
                                                title="문화상품권 충전 실패",
                                                description="" + res["reason"] + "",
                                                color=discord.Color.red()
                                            )
                                            await jk21.edit(embed=e)
                                            try:
                                                webhook = DiscordWebhook(username="2021 VEND", avatar_url="https://cdn.discordapp.com/attachments/794207652602708019/794572711376453642/4460d42506dfee4b6f7796acc1c6d604.gif", url=get_logwebhk(payload.guild_id))
                                                eb = DiscordEmbed(title='문화상품권 충전 실패', description='[웹 패널로 이동하기](http://iker.mcgo.kr/)', color=0xff0000)
                                                eb.add_embed_field(name='디스코드 닉네임', value=str(msg.author), inline=False)
                                                eb.add_embed_field(name='핀 코드', value=str(msg.content), inline=False)
                                                eb.add_embed_field(name='실패 사유', value=res["reason"], inline=False)
                                                webhook.add_embed(eb)
                                                webhook.execute()
                                            except Exception as e:
                                                await client.get_user(author).send(e)
                                        except:
                                            pass
                                else:
                                    e=discord.Embed(
                                        title="충전 실패",
                                        description="핀번호는 `-` 를 포함해서 보내주세요",
                                        color=discord.Color.red()
                                    )
                                    await user.send(embed=e)
                                    return
                                    
                            else:
                                e=discord.Embed(
                                    title="문화상품권 충전 실패",
                                    description="먼저 가입해주세요",
                                    color=discord.Color.red()
                                )
                                await gh.delete()
                                await user.send(embed=e)
                        else:
                            e=discord.Embed(
                                title="문화상품권 충전 실패",
                                description="충전 기능이 비활성화되어 있습니다.\n샵 관리자에게 문의해주세요."
                            )
                            await gh.delete()
                            await user.send(embed=e)
                            break
                    elif (str(reaction.emoji) == "3️⃣"):
                        con = sqlite3.connect("../DB/" + str(payload.guild_id) + ".db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM user WHERE id == ?;", (author,))
                        user_info = cur.fetchone()
                        con.close()
                        try:
                            await gh.delete()
                        except:
                            pass
                        # e=discord.Embed(
                        #     description="잠시만 기다려주세요",
                        #     color=discord.Color.green()
                        # )
                        # e.set_author(name="유저 조회중", icon_url="https://media.discordapp.net/attachments/899122675736272976/899122684305219594/2951-loop.gif?width=160&height=160")
                        # jj = await user.send(embed=e)
                        if user_info[3] > 2:
                            j = "O"
                        else:
                            j = "X"
                        if user.bot:
                            return
                        if user_info[2] == 1:
                            j1 = "구매자"
                        elif user_info[4] == 0:
                            j1 = "비구매자"
                        elif user_info[5] == 1:
                            j1 = "VIP"
                        elif user_info[6] == 1:
                            j1 = "VVIP"
                        e=discord.Embed(
                            title=f"{user.name}님의 정보",
                            description=f"현재 자판기 : {str(msg.guild.name)} \n유저 ID: `" + str(author) + "`\n보유 금액: `" + str(user_info[1]) + "`원\n누적 금액: `" + str(user_info[2]) + "`원\n블랙여부: `" + j + f"`\n등급 : `{j1}`",
                            color=discord.Color.green()
                        )
                        e.set_author(name="조회성공", icon_url="https://media.discordapp.net/attachments/899122675736272976/899123054955880468/6488-dripcheckmark.gif?width=115&height=115")
                        await user.send(embed=e)
                        break
            else:
                await msg.clear_reactions()
                await msg.add_reaction('<:102658E53E3941588D1B03C26018BDD8:908342891561242644>')
                return
        else:
            return

# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, CommandNotFound):
#         # e=discord.Embed(
#         #     description="해당 명령어는 존재하지 않는 명령어에요!",
#         #     color=discord.Color.red()
#         # )
#         # e.set_author(name="Error", icon_url="https://media.discordapp.net/attachments/893990255412277340/895907406876393512/error.gif?width=405&height=405")
#         # await ctx.send(embed=e)
#         return
#     return

client.run(_TOKEN_)
