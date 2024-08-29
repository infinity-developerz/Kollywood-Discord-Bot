import datetime
import gspread
import discord
import asyncio
from discord.ext import commands,tasks
from typing import Union

intents=discord.Intents.all()
intents.members=True
bot=commands.AutoShardedBot(command_prefix="$",description="WORKING WITH SMF",intents=intents)

def now():
    now=datetime.datetime.today().__format__("%Y-%m-%d %H:%M:%S")
    return now


sa=gspread.service_account(filename='flowing-digit-368412-438cc4bcc41a.json')
sh=sa.open("KDRP")

wks=sh.worksheet("application")
banlog=sh.worksheet("ban logs")

@bot.event
async def on_ready():
    # checkforunban.start()
    print(f"--- --- the bot is ready to perform as {bot.user} on {now()} ! ! !")


# @bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def auditionteamcheck(ctx:commands.Context):
    auditionrole:discord.Role=ctx.guild.get_role(1051904350852751400)
    embed1=discord.Embed(title="Audition Team Process Rechecking . . . .")
    for i,staff1 in enumerate(auditionrole.members):
        cell=wks.findall(f"-- {str(staff1)}")
        embed1.add_field(name=f"{i+1}",value=f"{staff1.mention} -- {len(cell)}")
    await ctx.send(embed=embed1)

    immegrationrole:discord.Role=ctx.guild.get_role(1051904358662553622)
    embed2=discord.Embed(title="Immegration Team Process Rechecking . . . .")
    for j,staff2 in enumerate(immegrationrole.members):
        cell=wks.findall(f"-- {str(staff2)}")
        embed2.add_field(name=f"{j+1}",value=f"{staff2.mention} -- {len(cell)}")
    await ctx.send(embed=embed2)

# @bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def rolemembers(ctx:commands.Context,role:discord.Role):
    embed=discord.Embed(title=f"{role.name}",description=f"Roled Member List {role.mention}")
    for member in role.members:
        embed.add_field(name="--- ---",value=f"{member.mention}")
    count=len(role.members)
    embed.set_footer(text=f"roled member count : {count}")
    await ctx.send(embed=embed)

@bot.command(aliases=[])
@commands.has_any_role(1051904351637090406)
async def ooccall(ctx:commands.Context,member:discord.Member=None):
    premium_role=ctx.guild.get_role()
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
        if role==ctx.guild.default_role or premium_role:
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

# Under Testing
@bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def setgangembed(ctx:commands.Context,role:discord.Role,image_url=None):
    embed=discord.Embed(title=f"{role.name}",color=role.color)
    for member in role.members:
        embed.add_field(name="-- -- -- -- -- -- ",value=f"{member.mention}",inline=False)
    # embed.set_image(url=image_url)
    await ctx.send(embed=embed)


# @bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def civcheck(ctx:commands.Context):
    guild=ctx.guild
    msg=await ctx.send("Checking civilion logs ...")
    role:discord.Role=guild.get_role(1058816348580483122)
    verified=0
    anonymous=0
    for member in role.members:
        print(member)
        cell=wks.findall(str(member.id))
        if cell==[]:
            state="Anonymous People ⚠️"
            await ctx.send(f"{member.mention} has no form")
            anonymous+=1
        else:
            state="Application Found Civilian ✅"
            vl=cell[-1].row
            m=wks.row_values(vl)
            async def aprcheck():
                if m[18]=="Approved":
                    pass
                else:
                    await ctx.send(f"{member.mention} visa has no approval status")
            try:
                m[18]
                await aprcheck()
            except:
                pass
            verified +=1
        if len(cell)>1:
            await ctx.send(f"{member.mention} has more than one form ")
        await asyncio.sleep(10)
        try:
            await msg.edit(content=f"Checking civilion logs ...\nchecking member : {member} \nstatus : {state}")
        except:
            await msg.delete()
            msg=await ctx.send(f"Checking civilion logs ...\n checking member : {member}")
    await msg.delete()
    await ctx.send(f"total verified members count : {verified} \n non - verified members count : {anonymous}")
    exit()

@bot.command(aliases=[])
@commands.has_permissions(administrator=True)
async def catcopy(ctx:commands.Context):
    cat=ctx.channel.category
    newcats=await ctx.guild.create_category(name=f"{cat.name}",position=cat.position)
    for txcnl in cat.text_channels:
        await newcats.create_text_channel(name=txcnl.name)
    for vccnl in cat.voice_channels:
        await newcats.create_voice_channel(name=vccnl.name)  

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error,discord.errors.NotFound):
        pass
    else:
        raise error
    
bot.run("",reconnect=True)