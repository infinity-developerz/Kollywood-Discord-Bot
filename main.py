import re
import datetime
import asyncio
import json
import gspread
import discord
from discord.ext import commands,tasks
from io import BytesIO
import aiohttp
from PIL import Image,ImageDraw,ImageFont
from typing import Union
import random

intents=discord.Intents.all()
intents.members=True
bot=commands.AutoShardedBot(command_prefix="!",description="WORKING WITH SMF",intents=intents)

def now():
    now=datetime.datetime.today().__format__("%Y-%m-%d %H:%M:%S")
    return now

sa=gspread.service_account(filename='flowing-digit-368412-438cc4bcc41a.json')
sh=sa.open("KDRP")
sh1=sa.open("KDRP BANS")
wks=sh.worksheet("application")
banwks=sh1.worksheet("ban logs")

def configuration():
    global config
    with open("config.json","r") as f1:
        config=json.load(f1)
    print(f"{now()} INFO     configuration affirmative")

configuration()

@bot.event
async def on_ready():
    global formcategory
    global form_log_channel
    global log_channel

    formchannel=bot.get_channel(config["channels"]["form_channel_id"])
    form_log_channel=bot.get_channel(config["channels"]["application_form_log_channel_id"])
    formcategory=formchannel.category

    for cnl in formcategory.text_channels:
        if cnl.id==formchannel.id:
            pass
        else:
            await cnl.delete()

    log_channel=bot.get_channel(config["channels"]["bot_logging_channel_id"])
    await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching,name="KOLLYWOOD CITY ACTIVITIES"))
    checkforunban.start()
    print(f"{now()} INFO     the bot is ready to perform as {bot.user} on {now()} ! ! !")

bot.remove_command('help')

@tasks.loop(minutes=5)
async def checkforunban():
    activebanlistcnl=bot.get_channel(1100483238209794048)
    messages = activebanlistcnl.history(limit=None)
    async for msg in messages:
        embeds=msg.embeds
        for embed in embeds:
            dict=embed.to_dict()
        ctx=await bot.get_context(msg)
        if msg.embeds and dict['title']=="BAN PROCESS":
            member=activebanlistcnl.guild.get_member(int(dict['fields'][1]['value']))
            l=datetime.datetime.timestamp(datetime.datetime.now())
            try:
                if int(float(dict['fields'][7]['value'])) <= int(l):
                    await unban(ctx,member=member)
            except:
                pass
@bot.event
async def on_member_join(member:discord.Member):
    print(f"{now()} LOG      {member} joined our server")
    cell=wks.findall(str(member.id))
    if cell==[]:
        return
    await member.send("We had rececived your application already, It means you leave the server. We issue a Warrent against you. Please content Ticket support Team")

@bot.event
async def on_member_remove(member):
    print(f"{now()} LOG      {member} leaves the server")

def checkem(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):
        return False
    else:
        return True

webhookurls={
    1077306950628417536:["webhook-url","<@&role-id>"],
}

@bot.event
async def on_message(message:discord.Message):
    if message.channel.id in config["reaction_message_channel_id"]:
        for reac in config["reaction_emoji"]:
            await message.add_reaction(reac)

    async def web_hook_send(content="",file="web.png",url=True,username=""):
        url=webhookurls[message.channel.id][0]
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=url, session=session)
            if not file:
                await webhook.send(username=username,content=f"{message.content} {webhookurls[message.channel.id][1]}")
            else:
                await webhook.send(username=username,file=discord.File(file),content=f"{content} {webhookurls[message.channel.id][1]}")

    if message.channel.id in webhookurls:
        username=""
        delstate=False
        if message.channel.id==1078733357107662899:
            dark_chat_log_channel=bot.get_channel(1081643303352672256)
            username=f"{datetime.datetime.now().timestamp()}"+f"{random.randint(10000,99999)}"
            await dark_chat_log_channel.send(f"message id : {username} , author : {message.author.mention}")
            delstate=True

        if message.attachments and message.content:
            for attachment in message.attachments:
                await attachment.save("web.png")
            await web_hook_send(username=username,content=f"{message.content}")

        elif message.content:
            await web_hook_send(username=username,content=f"{message.content}",file=False)

        elif message.attachments:
            for attachment in message.attachments:
                await attachment.save("web.png")
            await web_hook_send(username=username)

        if delstate:
            await message.delete()

    await bot.process_commands(message)

@bot.command(aliases=['cf'])
@commands.has_guild_permissions(administrator=True)
async def setformchannel(ctx:commands.Context):
    channel:discord.TextChannel=ctx.channel
    cat=channel.category
    await cat.edit(name="VISA APPLICATION")
    await cat.edit(position=cat.position)
    await channel.edit(name="🪪┆ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ ꜰᴏʀᴍ")
    await channel.purge(limit=None)
    embed=discord.Embed(title = 'KOLLYWOOD CITY PASSPORT OFFICE',description="Before Apply for Visa Please read the following City Rules and Regulations", color = discord.Color.dark_blue())
    embed.add_field(name="rules channels",value=f"<#{config['channels']['rules_channel1_id']}>",inline=False)
    embed.add_field(name="rules channels",value=f"<#{config['channels']['rules_channel2_id']}>",inline=False)
    embed.add_field(name="rules channels",value=f"<#{config['channels']['rules_channel3_id']}>",inline=False)
    embed.add_field(name="rules channels",value=f"<#{config['channels']['rules_channel4_id']}>",inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1040853669291229294/1052554238229762079/trial-banner-1.png")
    embed.set_footer(text="Click the bellow reaction 📄 to start application",icon_url="https://cdn.discordapp.com/attachments/1040853669291229294/1052554238229762079/trial-banner-1.png")
    embmsg=await channel.send(embed=embed)
    await embmsg.add_reaction('📄')
    print(f"{now()} LOG      form channel : {channel}")

@bot.command(aliases=[])
async def newform(ctx:commands.Context,author:discord.Member=None):
    if author==None:
        author:discord.Member=ctx.author
    appcnl=await formcategory.create_text_channel(name=f"🪪┆{author} form")
    starttime=now()
    print(f"{starttime} LOG      new form created {appcnl} by {author}")
    channel:discord.TextChannel=ctx.channel
    guild:discord.Guild = channel.guild
    everyonerole=guild.default_role
    audition_team_role=guild.get_role(config["roles"]["audition_team_role_id"])
    directors_role=guild.get_role(1051904348961120296)
    await appcnl.edit(overwrites={
        author:discord.PermissionOverwrite(view_channel=True),
        everyonerole:discord.PermissionOverwrite(view_channel=False,read_messages=False),
        audition_team_role:discord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=False),
        directors_role:discord.PermissionOverwrite(view_channel=True,read_messages=True,send_messages=False)
        })
    discord_details={
        "Member":str(author),
        "Name":author.name,
        "ID":str(author.id),
        "NickName":author.nick,
        "Account Created":author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'),
        "Join Date":author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')
    }

    async def alpha():
        await appcnl.send(f"{author.mention}Welcome to Kollywood Roleplay")
        embed=discord.Embed(title="VISA APPLICATION",description=f"{author.mention}",color=discord.colour.Color.gold())
        for con in discord_details:
            embed.add_field(name=con,value=discord_details[con],inline=True)
        embed.set_thumbnail(url=author.display_avatar)

        await appcnl.send(embed=embed)

        def check(m: discord.Message):
            return m.author.id == author.id and m.channel.id == appcnl.id 
        
        async def sendembed(value,name=None):
            if name==None:
                name="Please provide the following information ✅"

            embed=discord.Embed(color = discord.colour.Color.random())
            embed.add_field(name=name,value=f"{value}")
            await appcnl.send(embed=embed)
        form_answers={
            "member_id":str(author.id),
            "member_name":str(author)
            }
        async def email():
            val="Enter your Valid Email Address :"
            await sendembed(value=val)
            em:discord.Message=await bot.wait_for("message",check=check,timeout=300)
            if checkem(str(em.content)):
                nam="Invalid Email address ❌❌❌"
                await sendembed(value="You Email address Doesn't exist",name=nam)
                await email()
            else:
                form_answers[val]=em.content
                embed.add_field(name=val,value=f"--- {em.content}")
        await email()
        await sendembed(name="INSTRUCTIONS ⚠️⚠️⚠️",value="I wait 7 minutes for each question to be answered; if you do not respond within 7 minutes, I am supposed to consider your application as malpractice.")
        await asyncio.sleep(7)
        questions=[
            "What is Your Date Of Birth ? Format : (DD/MM/YYYY)",
            "What Is Your Gender ? (Real Life) ",
            "What do u know about RP ? ( Explain Shortly )",
            "What is RDM And VDM ? ( Expand And Explain Shortly)",
            "What is Combat Logging ? ( Explain Shortly)",
            "What is Cop Baiting ? ( Explain Shortly)",
            "What is NLR Rule ? ( Expand And Explain Shortly)",
            "What is Fail RP ? ( Explain Shortly)",
            "What is Meta Gaming? ( Explain Shortly)",
            "What is Fear RP ? ( Explain Shortly)",
            "What is Power Gaming ? (Explain Shortly)",
            "What is Suppress Fire ? (Explain Shortly)",
            "Explain your Backgroud Story (Explain Shortly)"
        ]
        for ques in questions:

            async def beta():
                await sendembed(value=ques)
                answer:discord.Message=await bot.wait_for("message",check=check,timeout=600)
                try:
                    form_answers[ques]=answer.content
                    embed.add_field(name=ques,value=f"-- {answer.content}")
                
                except:
                    await answer.reply("The message you have send exceed the discord limit. Your response must be 1024 or fewer in length")
                    await beta()
            await beta()

        endtime=now()
        embed.add_field(name="Start Time",value=f"{starttime}")
        embed.add_field(name="Endtime",value=f"{endtime}")
        form_answers["starttime"]=starttime
        form_answers["endtime"]=endtime
        
        temlogcnl=ctx.guild.get_channel(1102503060011491339)
        application=await form_log_channel.send(embed=embed)
        await temlogcnl.send(embed=embed)
        
        def gsupdate():
            content=[]
            for ans in form_answers:
                content.append(form_answers[ans])
            wks.append_row(content)
        
        gsupdate()

        on_hold_announcment_channel=bot.get_channel(config["channels"]["on_hold_announcment_channel_id"])
        on_hold_role = guild.get_role(config["roles"]["voice_process_role_id"])
        community_role=guild.get_role(config["roles"]["community_role"])

        await author.add_roles(on_hold_role)
        await author.remove_roles(community_role)

        await on_hold_announcment_channel.send(f'''{author.mention} , We have received your application. You will be notified about your voice process at <#{config["channels"]["voice_process_announcement_channel_id"]}>, along with the appropriate date and time. ! ! !''') 

        await application.add_reaction('✅')
        await application.add_reaction('❌')
        await appcnl.delete()
        print(f"{now()} LOG      {author} has been submitted visa application")
        try:
            await author.send("```ʏᴏᴜʀ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ ʜᴀꜱ ʙᴇᴇɴ ꜱᴜʙᴍɪᴛᴛᴇᴅ,ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ꜰᴏʀ ʏᴏᴜʀ ᴀᴘᴘʟɪᴄᴀᴛɪᴏɴ ᴛᴏ ʙᴇ ᴘʀᴏᴄᴇꜱꜱᴇᴅ ʙʏ ɪᴍᴍᴇɢʀᴀᴛɪᴏɴ ꜱᴛᴀꜰꜰꜱ```")
        except:
            pass
    
    try:
        await alpha()
    except Exception as e:
        await appcnl.delete()
        if isinstance(e,asyncio.exceptions.TimeoutError):
            try:
                await author.send(f'''ʏᴏᴜʀ ꜰᴏʀᴍ ɪꜱ ʙᴇɪɴɢ ɪᴅʟᴇ ꜰᴏʀ 10 ᴍɪɴᴜᴛᴇꜱ , ꜱᴏ ʏᴏᴜʀ ꜰᴏʀᴍ ɪꜱ ᴅᴇʟᴇᴛᴇᴅ,ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ʙʏ ʀᴇᴀᴄᴛɪɴɢ ᴀɢᴀɪɴ 📄 ɪɴ <#1051904492829954092>''')
            except:
                pass
            print(f"{now()} LOG      {appcnl} has been deleted , form closed")
        elif isinstance(e,discord.errors.Forbidden):
            pass
        elif isinstance(e,discord.errors.HTTPException):
            pass
        else:
            raise e

@bot.command(aliases=[])
@commands.has_any_role(1055869948360142868,1055851463110307881,1098962476453859368,1098962476453859368)
async def publish(ctx:commands.Context,channel:discord.TextChannel,*,message):
    await channel.send(f"{message} .")

@bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def dmuser(ctx:commands.Context,member:discord.Member,*,content="DM check"):
    dm_failure_log_channel=ctx.guild.get_channel(1105556987061751908)
    try:
        await member.send(content=content)
    except:
        await dm_failure_log_channel.send(f"{member.mention}\n{content}")

@bot.command(aliases=[])
@commands.has_any_role(config["roles"]["bot_permission_role_name"],1051904358662553622)
async def findform(ctx:commands.Context,member:discord.Member):
    channel:discord.TextChannel=ctx.channel
    if channel.id!=config['channels']['find_member_channel_id']:
        await ctx.message.delete()
        msg=await channel.send(f"search users application in <#{config['channels']['find_member_channel_id']}>")
        await asyncio.sleep(10)
        await msg.delete()
    else:

        messages = form_log_channel.history(limit=None)
        async for msg in messages:
            embeds=msg.embeds
            for embed in embeds:
                dict1=embed.to_dict()
            if msg.embeds and dict1['title']=="VISA APPLICATION":
                if int(dict1["fields"][2]["value"])==member.id:
                    embed=discord.Embed(title="Finding User Form",description=f"{member.mention}")
                    embed.add_field(name="Jump Url",value=f"{msg.jump_url}")
                    embed.set_footer(text=f"requested by {ctx.author}")
                    await channel.send(embed=embed)

@bot.command(aliases=[])
@commands.has_any_role(config["roles"]["bot_permission_role_name"],1051904358662553622)
async def vpprocess(ctx:commands.Context):
    voice_process_role=ctx.guild.get_role(1051904368837931050)
    if ctx.author.voice:
        for member in ctx.author.voice.channel.members:
            if voice_process_role in member.roles:
                await findform(ctx,member)
        await ctx.message.delete()
    else:
        msg=await ctx.reply("You are Not in Voice Channel")
        await asyncio.sleep(7)
        await msg.delete()
        await ctx.message.delete()

@bot.command(aliases=[])
@commands.has_role(config["roles"]["bot_permission_role_name"])
async def formdetails(ctx:commands.Context,member:discord.Member):
    cell=wks.findall(str(member.id))
    if cell==[]:
        await ctx.send("Cannot find in the form")
        return
    find_member_channel=bot.get_channel(config['channels']['find_member_channel_id'])
    vl=cell[-1].row
    m=wks.row_values(vl)
    discord_details={
        "Member":str(member),
        "Name":member.name,
        "ID":str(member.id),
        "NickName":member.nick,
        "Account Created":member.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'),
        "Join Date":member.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')
    }
    embed=discord.Embed(title="VISA APPLICATION",description=f"{member.mention}",color=discord.colour.Color.random())
    for con in discord_details:
        embed.add_field(name=con,value=discord_details[con],inline=True)
    embed.set_thumbnail(url=member.display_avatar)

    questions=[
        "Enter your Valid Email Address :",
        "What is Your Date Of Birth ? Format : (DD/MM/YYYY)",
        "What Is Your Gender ? (Real Life) ",
        "What do u know about RP ? ( Explain Shortly )",
        "What is RDM And VDM ( Expand And Explain Shortly)",
        "What is Combat Logging ( Explain Shortly)",
        "What is Cop Baiting ? ( Explain Shortly)",
        "What is NLR Rule ? ( Expand And Explain Shortly)",
        "What is Fail RP ? ( Explain Shortly)",
        "What is Meta Gaming? ( Explain Shortly)",
        "What is Fear RP ? ( Explain Shortly)",
        "What is Power Gaming ? (Explain Shortly)",
        "What is Suppress Fire ? (Explain Shortly)",
        "Explain your Backgroud Story (Explain Shortly)",
        "Starttime",
        "Endtime",
        "Status",
        "Processed By"
    ]

    for i,question in enumerate(questions):
        try:
            embed.add_field(name=f"{question}",value=f"--- {m[i+2]}")
        except:
            pass
    embed.set_footer(text=f"requested by{ctx.author}")
    form=await find_member_channel.send(embed=embed)

    # if len(m)<=16:
    #     pass 
    # else:
    #     if m[16] == "Approved":
    #         await form.add_reaction('❌')
    #     elif m[16] == "Declained":
    #         await form.add_reaction('✅')
    
    await form.add_reaction('🧹')
    tag_msg = await find_member_channel.send(ctx.author.mention)
    await asyncio.sleep(7)
    await tag_msg.delete()

@bot.command(aliases=[])
@commands.has_any_role()
async def setgangembed(ctx:commands.Context,role:discord.Role,image_url):
    embed=discord.Embed(title=f"{role.name}",color=role.color)
    for member in role.members:
        embed.add_field(name=f"{member.nick}",value=f"{member.mention}")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@bot.command(aliases=[])
@commands.has_any_role()
async def addmember(ctx:commands.Context,member:discord.Member):
    pass

@bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def immegrationteamcheck(ctx:commands.Context):
    immegrationrole:discord.Role=ctx.guild.get_role(1051904358662553622)
    embed2=discord.Embed(title="Audition Team Process Rechecking . . . .")
    for j,staff2 in enumerate(immegrationrole.members):
        cell=wks.findall(f"-- {str(staff2)}")
        embed2.add_field(name=f"{j+1}",value=f"{staff2.mention} -- {len(cell)}")
    await ctx.send(embed=embed2)

@bot.command(aliases=[]) 
@commands.has_any_role(1051904351637090406)
async def unban(ctx:commands.Context,member:discord.Member=None):

    civilion_role=ctx.guild.get_role(1058816348580483122)
    banlog_channel=bot.get_channel(1079813109558026310)
    goa_role=ctx.guild.get_role(1056512659194916914)
    if member==None:
        if ctx.message.reference!=None:
            msg=await ctx.fetch_message(ctx.message.reference.message_id)

            if msg.embeds:
                for embed in msg.embeds:
                    dict=embed.to_dict()
                try:
                    if dict['title'] == "BAN PROCESS":
                        member_id=int(dict['fields'][1]["value"])
                        member=ctx.guild.get_member(member_id)                    
                except:
                    await ctx.reply("Unban Process cannot be complete. Please contact the discord admin")
        else:
            await ctx.reply("please reply for ban log or mention the banned member")
            return
    else:
        active_ban_log_channel=ctx.guild.get_channel(1100483238209794048)
        messages=active_ban_log_channel.history(limit=None)
        async for msg in messages:
            if msg.embeds:
                for embed in msg.embeds:
                    dict=embed.to_dict()
                try:
                    if dict['title'] == "BAN PROCESS":
                        member_id=dict['fields'][1]["value"]
                        if member.id==int(member_id):
                            break
                except:
                    pass

    if civilion_role in member.roles:
        await ctx.send(f"{member.mention} has already have civilion role which mean the ban process not done in proper way. I can't process the command. Please contact discord admins")
        return

    if goa_role in member.roles:
        await member.remove_roles(goa_role)
        await member.add_roles(civilion_role)
        await msg.delete()
        await banlog_channel.send(f"{member.mention} has been unbanned by {ctx.author.mention}")
    
        try:
            await member.send(f"Your ban has been revoked. Please go through the city rules before entering Kollywood City. Please avoid doing FAIL RP.")
        except:
            pass
        try:
            await ctx.message.delete()
        except:
            pass
    else:
        await ctx.message.reply("Missing Goa role. Can't process the command. Please contact discord admins")

@bot.command(aliases=[])
@commands.has_any_role(1051904351637090406)
async def ban(ctx:commands.Context,member:discord.Member=None):

    def check(m: discord.Message):
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
    
    def recheck(r: discord.Reaction, u: Union[discord.Member, discord.User]):  
        return u.id == ctx.author.id and r.message.id == conmsg.id

    bandetails={
        "member":member.mention,
        "id":member.id,
        "number of days":None,
        "reason":None
    }

    for i in bandetails:
        if bandetails[i]==None:
            msg=await ctx.reply(f'''Please mention {i} below :''')
            async def tryit():
                try:
                    reply:discord.Message=await bot.wait_for("message",check=check,timeout=100)
                    bandetails[i]=reply.content
                    await reply.delete()
                except Exception as e:
                    await msg.delete()
                    await ctx.message.delete()
                    return
            await tryit()

            try:
                numdays=int(bandetails["number of days"])
            except:
                await tryit()
            await msg.delete()

    starting_date = datetime.datetime.today()
    ending_date =starting_date + datetime.timedelta(days = numdays)
    
    embed=discord.Embed(title="BAN PROCESS",description=f"Ban Process Confirmation",color=discord.colour.Colour.brand_red())

    for j in bandetails:
        embed.add_field(name=j,value=f"{bandetails[j]}")

    embed.add_field(name="Start at",value=f"{starting_date}")
    embed.add_field(name="End at",value=f"{ending_date}")
    embed.add_field(name="Processed By",value=f"{ctx.author.mention}")
    
    embed.add_field(name="End Timestamp",value=f"{datetime.datetime.timestamp(ending_date)}")
    embed.set_footer(text="Please react ✅ to confirm \nTo cancel the ban process click ❌")
    conmsg=await ctx.reply(embed=embed)
    await conmsg.add_reaction("✅")
    await conmsg.add_reaction("❌")

    reaction, user = await bot.wait_for('reaction_add', check = recheck, timeout = 100)
    if str(reaction)=="✅":
        civilion_role=ctx.guild.get_role(1058816348580483122)
        banlog_channel=bot.get_channel(1079813109558026310)
        goa_role=ctx.guild.get_role(1056512659194916914)
        active_ban_log_channel=ctx.guild.get_channel(1100483238209794048)
        if civilion_role in member.roles:
    
            await member.add_roles(goa_role)
            await member.remove_roles(civilion_role)
            await banlog_channel.send(embed=embed)
            await active_ban_log_channel.send(embed=embed)
            await member.send(f"You have been banned for {bandetails['reason']} for {bandetails['number of days']} days")

        await ctx.reply("Ban Process Completed ✅")
        await conmsg.delete()
    
        banwks.append_rows([f"{bandetails['id']}",f"{member}",f"{bandetails['number of days']}",f"{bandetails['reason']}"],f"{starting_date}",f"{ending_date}",f"{ctx.author}")

    elif str(reaction)=="❌":
        await ctx.message.delete()
        await conmsg.delete()
    else:
        pass

@bot.command(aliases=[])
@commands.has_any_role(1051904351637090406)
async def ooccall(ctx:commands.Context,member:discord.Member=None):
    def check(m: discord.Message):
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
    
    active_warrent_channel=ctx.guild.get_channel(1108440520658792509)
    
    details={
        "member":member.mention,
        "member_id":member.id,
        "reason":None,
        "explanation":None
    }
    
    for i in details:
        if details[i]==None:
            msg=await ctx.reply(f'''Please mention {i} below :''')
            async def tryit():
                try:
                    reply:discord.Message=await bot.wait_for("message",check=check,timeout=100)
                    details[i]=reply.content
                    await reply.delete()
                except Exception as e:
                    await msg.delete()
                    await ctx.message.delete()
                    return
            await tryit()

            await msg.delete()

    await member.add_roles(ctx.guild.get_role(1095762605794148392))
    await member.remove_roles(ctx.guild.get_role(1058816348580483122))
    embed=discord.Embed(title="Warrent Details",color=discord.Color.yellow())
    for j in details:
        embed.add_field(name=f"{j}",value=f"{details[j]}")

    rolelist=""

    for role in member.roles:
        if role==ctx.guild.default_role:
            pass
        else:
            rolelist+=f"{role.mention}"

    embed.add_field(name="Role List",value=f"{rolelist}")
    await active_warrent_channel.send(embed=embed)
    await ctx.reply("Warrent issued")
    await member.send('''```
    We are currently working on the case against you. 
    The Supreme Court of Kollywood had called for your presence. 
    We have temporarily restricted your visa from Kollywood City due to your absence in court. 
    Please meet the ticket team in OOC chat to get your visa.
    We have temporarily removed all of your roles, and the roles will surely return to you once you come to OOC Drag.```
    ''')

@bot.command(aliases=[])
@commands.has_any_role(1051904351637090406)
async def giveciv(ctx:commands.Context,member:discord.Member):
    civilion_role=ctx.guild.get_role(1058816348580483122)
    ooccallrole=ctx.guild.get_role(1095762605794148392)
    if civilion_role in member.roles:
        await ctx.send(f"{member.mention} has already have civilion. I can't process the command. Please contact discord admins")
        return

    if ooccallrole in member.roles:
        await member.remove_roles(ooccallrole)
        await member.add_roles(civilion_role)

        try:
            await member.send(f"Your OOC call has been done and verified by the Supreme Court of Kollywood.")
        except:
            pass

    else:
        await ctx.message.reply("Missing OOC call role. Can't process the command. Please contact discord admins")

@bot.command(aliases=[])
@commands.has_any_role(1058816348580483122)
async def kdpdofficer(ctx:commands.Context):
    if ctx.channel.id!=1076542129712672870:
        return
    responce_channel=ctx.guild.get_channel(1076542374152507573)
    resreqmsg=await responce_channel.send(f"PD role requested by :{ctx.author.mention}")
    await resreqmsg.add_reaction("🔼")
    await resreqmsg.add_reaction("⏫")

@bot.command(aliases=[])
@commands.has_any_role(config["roles"]["bot_permission_role_name"],1051904358662553622)
async def vp(ctx:commands.Context,antype=None):
    guild:discord.Guild=ctx.channel.guild
    voice_process_role=guild.get_role(config["roles"]["voice_process_role_id"])
    voice_process_announcement_channel = bot.get_channel(config["channels"]["voice_process_announcement_channel_id"])
    
    if antype=="start":

        msg=f''' <a:kdvisa:1052958083749531658> {voice_process_role.mention} <@&1051904368250716320> Voice Process is Open Now Apply <#1051904492829954092> And Join <#{config["channels"]["voice_process_waiting_voice_channel_id"]}> To get Your Visa <a:joinvc:876729846577893376> <a:kdvisa:1052958083749531658> '''
        await voice_process_announcement_channel.send(msg)
        await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.listening,name="VOICE PROCESS HAS BEEN GOING ON"))

    elif antype=="close":

        msg=f''' <a:megaphone:876673298388385883> {voice_process_role.mention} <@&1051904368250716320> Today's Voice-process has been ended. <a:giphypray:876672231357431859> 
        <a:ArrowRightGlow:876672231789457449>  Next Voice-process will be held Tomorrow Guys !! Stay Tuned !! <a:rose:876672232544403506> '''
        await voice_process_announcement_channel.send(msg)
        await bot.change_presence(status=discord.Status.idle,activity=discord.Activity(type=discord.ActivityType.watching,name="KOLLYWOOD CITY ACTIVITIES"))

    else:
        await ctx.send('''mention announcement type : [start,close]
        command format : !vp <type>''')
        return

    for member in voice_process_role.members:
        try:
            await member.send(msg)
        except:
            pass

@bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def ping(ctx:commands.Context):
    await ctx.send(f'Pong! In {round(bot.latency * 1000)}ms')

business_roles={
    1080188877677007008:1080189082476486777,
    1080480806444744726:1080480817387688016,
    1056987146189287444:1051904365369233428,
    1080547431894237234:1080547429839016106,
    1056987990393626644:1080536485461233664,
    1080177888415981629:1080180562637115422,
    1080680520272322570:1080680522264625213
}

wtjobs={
    1055860016084680784:[1051904362877812846,[1051904362877812846,1076224165037744160]],
    1055860033742712932:[1051904363678945280,[1051904363678945280,1076086416846639104,1077257987053326447,1077257694630662235,1076081722057306132]]
}

@bot.command(aliases=[])
@commands.has_any_role(1055860016084680784,1055860033742712932)
async def dismiss(ctx:commands.Context,member:discord.Member):
    nofound=True
    for role in ctx.author.roles:
        if role.id in wtjobs:
            highcommand=role
            nofound=False
            break
    if nofound:
        return
    msg=await ctx.reply(f"{member.mention} has been Dismissed")
    for i in wtjobs[highcommand.id][1]:
        removerole=ctx.guild.get_role(i)
        await member.remove_roles(removerole)
        await msg.edit(content=f"{msg.content}"+f"\n {removerole.mention} has been revoked")
        await asyncio.sleep(1)
    await asyncio.sleep(7)
    await msg.delete()
    await ctx.message.delete()
    
@bot.command(aliases=[])
@commands.has_any_role(1080188877677007008,1080480806444744726,1056987146189287444,1080547431894237234,1056987990393626644,1080177888415981629,1080680520272322570)
async def appoint(ctx:commands.Context,member:discord.Member):
    nofound=True
    for role in ctx.author.roles:
        if role.id in business_roles:
            boss_role=role
            nofound=False
            break
    if nofound:
        return
    team_role=ctx.guild.get_role(business_roles[boss_role.id])
    buss_log_channel=ctx.guild.get_channel(1080852757596082317)
    await member.add_roles(team_role)
    confirm_msg=await ctx.message.reply(f"{member.mention} has been appointed as {team_role.mention}")
    await buss_log_channel.send(f"{team_role.mention} has been provided to {member.mention} by {ctx.author.mention}")
    await asyncio.sleep(10)
    await confirm_msg.delete()
    await ctx.message.delete()

@bot.command(aliases=[])
@commands.has_any_role(1080188877677007008,1080480806444744726,1056987146189287444,1080547431894237234,1056987990393626644,1080177888415981629,1080680520272322570)
async def layoff(ctx:commands.Context,member:discord.Member):    
    nofound=True
    for role in ctx.author.roles:
        if role.id in business_roles:
            boss_role=role
            nofound=False
            break
    if nofound:
        return
    team_role=ctx.guild.get_role(business_roles[boss_role.id])
    buss_log_channel=ctx.guild.get_channel(1080852757596082317)
    await member.remove_roles(team_role)
    confirm_msg=await ctx.message.reply(f"{member.mention} has been fired from {team_role.mention}")
    await buss_log_channel.send(f"{team_role.mention} has been revoked to {member.mention} by {ctx.author.mention}")
    await asyncio.sleep(10)
    await confirm_msg.delete()
    await ctx.message.delete()

@bot.event
async def on_raw_reaction_add(payload : discord.RawReactionActionEvent):

    reaction=payload.emoji
    if str(reaction) not in ["📄","✅","❌","🧹","⏳","👨‍💻","🔼","⏫","🩹"]:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    embeds=message.embeds
    guild=bot.get_guild(payload.guild_id)
    user:discord.Member = guild.get_member(payload.user_id)
    ctx=await bot.get_context(message)

    pdhighcommandrole=guild.get_role(1055860016084680784)
    pddefaulerole=guild.get_role(1051904362877812846)
    pdseniorrole=guild.get_role(1076224165037744160)
    kmshighcommandrole=guild.get_role(1055860033742712932) 
    kmsrole=guild.get_role(1051904363678945280)
    kmsinterviewrole=guild.get_role(1076081722057306132)
    pdlogchannel=guild.get_channel(1076488306788937768)
    emslogchannel=guild.get_channel(1076409624481235004)

    if user.id == bot.user.id:
        return

    if message.embeds:
        pass
    else:
        if kmshighcommandrole in user.roles and message.channel.id==1051904557304778832:
            if str(reaction)=="✅":
                await message.author.add_roles(kmsrole)
                await message.author.remove_roles(kmsinterviewrole)
                await message.author.send('''Congradulation You have been selected for Kollywood Medical Service.\nOur duty is to serve people.\nIt is our responsibility to create a healthy Kollywood city.\nWe work for it; we would, we will, and we are.''')
                await emslogchannel.send(f"{message.author.mention} has been selected to KMS and {kmsrole} has been given")
            elif str(reaction)=="⏳":
                await message.author.add_roles(kmsinterviewrole)
                await message.author.send("We are currently reviewing your profile; an interview will be scheduled shortly. Please go through the KMS rules.")
                await emslogchannel.send(f"{message.author.mention}'s applicaton has been process and {kmsinterviewrole} has been given")
            elif str(reaction)=="👨‍💻":
                await message.author.send("We are delighted to announce that your application has been shortlisted. Please visit the Kollywood Medical Center.")
                await emslogchannel.send(f"{message.author.mention} is called for Hospital Visit")
            elif str(reaction)=="❌":
                await message.author.remove_roles(kmsinterviewrole)
                await message.author.send("Sorry, based on our discussion, your application didn't meet the required criteria. Please re-apply after three days.")
                await emslogchannel.send(f"{message.author.mention} has been rejected to KMS and {kmsinterviewrole} has been removed")

        if pdhighcommandrole in user.roles and message.channel.id==1076542374152507573:
            member:discord.Member=message.mentions[0]
            if str(reaction)=="🔼":
                await member.add_roles(pddefaulerole)
                await member.send("Congradulation You have been selected for Kollywood Police Department.\nCongradulation ! You have been given access to confidential PD files and radio. \nIt is our responsibility to create a crime free Kollywood city.")
                await message.delete()
                await pdlogchannel.send(f"{pddefaulerole} has been given to {member.mention}")
            elif str(reaction)=="⏫":
                await member.add_roles(pdseniorrole)
                await member.send('''Congradulation ! ! ! You are defined as senior officer of our KDPD''')
                await message.delete()
                await pdlogchannel.send(f"{member.mention} has been promoted to {pdseniorrole}")
        return
    
    for embed in embeds:
        dict1=embed.to_dict()

    if str(reaction) == "📄":
        await newform(ctx,author=user)
        return

    if dict1['title'] == "VISA APPLICATION":

        userid=dict1['fields'][2]['value']

        member=guild.get_member(int(userid))

        if str(reaction) == "✅":

            if user.voice==None or member.voice==None:
                ivpmsg=await ctx.send(f"{user.mention} Invalid voice process : either Member or Staff is not Voice Channel")
                await asyncio.sleep(7)
                await ivpmsg.delete()
                return
            elif user.voice.channel != member.voice.channel:
                vpsv=await ctx.send(f"{user.mention} Voice Process done only if both Member and Staff in same Voice Channel")
                await asyncio.sleep(7)
                await vpsv.delete()
                return
            membervc=user.voice.channel
            
            visa_role = guild.get_role(config["roles"]["visa_give_role_id"])
            on_hold_role = guild.get_role(config["roles"]["voice_process_role_id"])
            community_role=guild.get_role(config["roles"]["community_role"])
            visa_approved_announcement_channel = bot.get_channel(config["channels"]["visa_approved_announcement_channel_id"])
            visa_process_log_channel = bot.get_channel(config["channels"]["visa_process_log_channel_id"])

            #opening image for visa dm
            img = Image.open("visa.png")

            asset = member.display_avatar
            data =BytesIO(await asset.read())
            pfp = Image.open(data).convert("RGBA")
            set1=pfp.resize((175,175))
            img.paste(set1,(133,217),set1)

            font = ImageFont.truetype("nasalization-rg.otf",30)
            signaturefont=ImageFont.truetype("font.ttf",40)
            draw =ImageDraw.Draw(img)
            name = str(member)
            dob=str(member.created_at.__format__('%d/%m/%Y @ %H:%M:%S'))
            passno=str(member.id)
            doc=str(datetime.datetime.now().__format__('%d/%m/%Y @ %H:%M:%S'))
            cd=(0,255,253)
            draw.text((645,242),name,cd,font=font)
            draw.text((645,293),dob,cd,font=font)
            draw.text((645,342),passno,cd,font=font)
            draw.text((460,434),doc,cd,font=font)
            draw.text((880,435),str(user.name),(127,255,0),font=signaturefont)

            img.save("visa1.png")
            
            await member.add_roles(visa_role)

            await member.remove_roles(on_hold_role)

            await member.remove_roles(community_role)

            await visa_approved_announcement_channel.send(member.mention + '''
            ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ ʏᴏᴜʀ ᴠɪꜱᴀ ʜᴀᴠᴇ ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ.
            ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ <a:Alphabet_K:878036802269761537> <a:Alphabet_D:878035992395800677> <a:Alphabet_R:878037454345621574> <a:Alphabet_P:878037293699575818>. 
            ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛᴏ ʀᴇᴀᴅ ᴀʟʟ ᴏᴜʀ ʀᴜʟᴇꜱ ʙᴇꜰᴏʀᴇ ᴇɴᴛᴇʀɪɴɢ ᴛʜᴇ ᴄɪᴛʏ.
            ᴇɴᴊᴏʏ ʏᴏᴜʀ <a:Alphabet_R:878037454345621574> <a:Alphabet_P:878037293699575818> ''')
            
            await visa_approved_announcement_channel.send(file = discord.File("visa1.png"))
            await visa_process_log_channel.send(member.mention + f"visa has been approved by {user.mention}, Processed in Voice channel : {membervc.mention}")
            await message.delete()

            try:
                cell=wks.findall(str(member.id))
                vl=cell[-1].row
                wks.update_cell(vl,19,"Approved")
                wks.update_cell(vl,20,f"-- {user}")
                print(f"{now()} LOG      {member}'s visa has been approved by {user}")

            except:
                pass

            try:
                await member.send(f'''
                ✔✔✔🎫ʏᴏᴜʀ ᴠɪꜱᴀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴄᴄᴇᴘᴛᴇᴅ ᴇɴᴊᴏʏ ʏᴏᴜʀ ʀᴏʟᴇᴘʟᴀʏ
                ʙᴇꜰᴏʀᴇ ᴇɴᴛᴇʀɪɴɢ ᴛʜᴇ ꜱᴇʀᴠᴇʀ ʀᴇᴀᴅ ᴏᴜʀ ᴄɪᴛʏ ʀᴜʟᴇꜱ
                \t ❗<#{config["channels"]["rules_channel1_id"]}>
                \t ❗❗<#{config["channels"]["rules_channel2_id"]}>
                \t ❗❗❗<#{config["channels"]["rules_channel3_id"]}>
                \t ❗❗❗❗<#{config["channels"]["rules_channel4_id"]}>''')
                
                await member.send(file = discord.File("visa1.png"))
            except:
                pass

        elif str(reaction) == "❌":

            visa_decliend_announcement_channel=bot.get_channel(config["channels"]["visa_decliend_announcement_channel_id"])
            visa_process_log_channel=bot.get_channel(config["channels"]["visa_process_log_channel_id"])
            on_hold_role = guild.get_role(config["roles"]["voice_process_role_id"])
            community_role=guild.get_role(config["roles"]["community_role"])

            await member.remove_roles(on_hold_role)
            await member.add_roles(community_role)

            await visa_decliend_announcement_channel.send( member.mention + "ʏᴏᴜʀ ᴠɪꜱᴀ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛᴏ ꜰɪʟʟ ᴛʜᴇ ꜰᴏʀᴍ ᴄᴏʀʀᴇᴄᴛʟʏ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ʀᴇ-ᴀᴘᴘʟʏ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ ᴠɪꜱᴀ")
            await member.send( member.mention + "ʏᴏᴜʀ ᴠɪꜱᴀ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛᴏ ꜰɪʟʟ ᴛʜᴇ ꜰᴏʀᴍ ᴄᴏʀʀᴇᴄᴛʟʏ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ʀᴇ-ᴀᴘᴘʟʏ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ ᴠɪꜱᴀ")
            await visa_process_log_channel.send(member.mention + f"visa has been declined by {user.mention}")
            await message.delete()
            try:
                cell=wks.findall(str(member.id))
                vl=cell[-1].row
                wks.update_cell(vl,19,"Declained")
                wks.update_cell(vl,20,f"-- {user}")
            except:
                pass
            print(f"{now()} LOG      {member}'s visa has been declined by {user}")
        elif str(reaction) == "🧹":
            await message.delete()
        else:
            pass

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError) -> None:
	return

@bot.event
async def on_command_error(ctx:commands.Context,error):
    if isinstance(error,commands.MissingPermissions):
        ermsg1=await ctx.send("YOU DON'T HAVE PERMISSION TO DO THAT ---MP--- ")
        await asyncio.sleep(5)
        await ctx.message.delete()
        await ermsg1.delete()
    elif isinstance(error,commands.errors.MissingRole):
        ermsg2=await ctx.send("YOU DON'T HAVE PERMISSION TO DO THAT ---MR---")
        await asyncio.sleep(5)
        await ctx.message.delete()
        await ermsg2.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        ermsg3=await ctx.send("USE THE COMMAND IN CORRECT FORMATE")
        await asyncio.sleep(5)
        await ctx.message.delete()
        await ermsg3.delete()
    elif isinstance(error,commands.errors.MemberNotFound):
        ermsg4=await ctx.send("Member Not Found")
        await asyncio.sleep(5)
        await ermsg4.delete()
    elif isinstance(error,commands.errors.MissingAnyRole):
        ermsg5=await ctx.send("YOU DON'T HAVE REQUIRED ROLES")
        await asyncio.sleep(5)
        await ermsg5.delete()
    elif isinstance(error,commands.errors.ChannelNotFound):
        ermsg6=await ctx.send("Channel Not Found")
        await asyncio.sleep(5)
        await ermsg6.delete()
    elif isinstance(error,commands.errors.CommandNotFound):
        pass
    elif isinstance(error,commands.errors.CommandInvokeError):
        pass
    elif isinstance(error,discord.errors.Forbidden):
        pass
    else:
        await log_channel.send(f'''<@784426572445646858> error found ! ! ! \n {error}''')
        raise error

bot.run("",reconnect=True)
