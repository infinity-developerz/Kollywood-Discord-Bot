import discord
from discord.ext import commands

intents=discord.Intents.all()
intents.members=True
bot=commands.AutoShardedBot(command_prefix="!",description="WORKING WITH SMF",intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online")
    
@bot.command(aliases=[])
async def rulesupdate(ctx:commands.Context):
    await ctx.message.delete()

    message=await ctx.fetch_message(1081975124758122497)
    # embeds=message.embeds
    # for embed in embeds:
    #     dict1=embed.to_dict()

    embed=discord.Embed(title="RolePlay Rules and Guidelines",color=discord.Colour.gold())
    
    embed.add_field(
        name="Role playing",
        value=f" <a:ArrowRightGlow:876672231789457449> Role-playing is the changing of one's behaviour to assume a role inside the city (game server), either unconsciously to fill a social role or consciously to act out an adopted role.",
        inline=False
        )

    embed.add_field(
        name="VDM - Vehicle Death Match",
        value=f''' <a:ArrowRightGlow:876672231789457449> Vehicle Death Match: A "vehicle death match" is when you hit someone with the help of a vehicle (car, bike, helicopter, or boat), which is supposed to be the cause of the person's death.
        Randomly running over others is not acceptable and will result in a kick or ban. You have the ability to run someone over if they pose a threat or if you have a compelling character reason to do so. Police may be pitted against reason.''',
        inline=False
        )

    embed.add_field(
        name="RDM Random Death Match",
        value=f''' <a:ArrowRightGlow:876672231789457449> Random Death Match: A "random death match" is when you kill someone without any roleplay reason or for fun.
        An interaction with a player must be established before you can kill someone and be valid in a character exchange.''',
        inline=False
        )

    embed.add_field(
        name="Combat Logging",
        value=f''' <a:ArrowRightGlow:876672231789457449> Combat logging is prohibited and is defined as when a player exits their game to avoid an RP, for example, to avoid being arrested, charged with a crime, or being booked in jail.
        Disconnecting & Re-Connecting to Avoid a Jail Sentence or Waiting for the Death Timer to End also avoiding any present RP.''',
        inline=False
        )

    embed.add_field(
        name="Meta Gaming",
        value=f''' <a:ArrowRightGlow:876672231789457449> Meta gaming is defined as using OOC knowledge in IC to break character. 
        It is strictly forbidden to use OOC inside the city as if you saw or heard something. It is not permitted to stream-snipe an opponent in order to gain information and change the RP.''',
        inline=False
        )

    embed.add_field(
        name="Fear RP",
        value=f''' <a:ArrowRightGlow:876672231789457449> Describes the IC character's aversion to anything on the server. No matter how tough or self-composed the character normally behaves, you must remain fearful of the danger; otherwise, it counts as failed RP.
        At all times, you must value your life as if it were your last. If you’re at a clear disadvantage, for example, if a gun is pointed at the back of your head while you’re looking in the other direction, you must comply with their demands. If you are outnumbered 3 to 1, you must comply.''',
        inline=False
        )
    
    embed.add_field(
        name="Power Gaming",
        value=f''' <a:ArrowRightGlow:876672231789457449> Taking Advantage of In-Game Power
        This involves using either game or roleplay mechanics to alter a situation so it best suits your desires. You must be willing to roleplay a situation to its fullest and not ruin the experience of others.''',
        inline=False
        )
    
    embed.add_field(
        name="FCR",
        value=f''' <a:ArrowRightGlow:876672231789457449> Female Character Rule 
        This rule should be followed by all male characters by showing respect to the female character. Failing (FCR): Toxic Relationships with or Sexual Harassment of Female Characters, etc.''',
        inline=False
        )
    
    embed.add_field(
        name="Suppress Fire",
        value=f''' <a:ArrowRightGlow:876672231789457449> If you want to initiate a shooting scenario and the opposing party is unaware that you intend to shoot, 
        you must give them a chance by suppressing fire and allowing them to react to the gunfight. 
        Suppressing fire doesn't mean firing one bullet in the sky and shooting the second bullet in the head. 
        Suppressing fire is not needed in a place where the opposite party's guns are brandished and seen through your eyes. 
        For example, if you are robbing a store with a gun pointed at a hostage, you cannot expect the police to suppress fire because they have already seen your weapon.''',
        inline=False
        )

    embed.add_field(
        name="Toxicity and Bullying",
        value=f''' <a:ArrowRightGlow:876672231789457449> Respect every player of KDRP inside and outside of the game. Do not bully a player by their physical appearance or by their voice. Do not speak vulgarly or by using abusive words; if found, strict actions will be taken by the management immediately.''',
        inline=False
        )

    embed.add_field(
        name="Cop Baiting",
        value=f''' <a:ArrowRightGlow:876672231789457449> Cop baiting is prohibited; this is when your sole goal is to attract the attention of LEO with no benefit to your character development, such as returning to find the cops after losing them in pursuit only to have them chase you again.''',
        inline=False
        )

    embed.add_field(
        name="NO EXPLOITING OR HACKING",
        value=f''' <a:ArrowRightGlow:876672231789457449> External apps, system-supporting apps, hacking, or cheating are not allowed. This includes abusing in-game bugs, etc. This will result in immediate server action or a permanent ban. If you find any bugs, kindly report them to helping hands or admins through Discord. If exploited, that will lead to a temporary or permanent ban.''',
        inline=False
        )

    embed.add_field(
        name="NLR",
        value=f''' <a:ArrowRightGlow:876672231789457449> Means that the player's character forgets knowledge of various information learned before dying(e.g. Burnt, drowned in ocean for a long time etc.)
        Players must follow NLR if they Die & Re-Spawn at a Hospital.''',
        inline=False
        )

    embed.add_field(
        name="In-Game",
        value=f''' <a:ArrowRightGlow:876672231789457449> In-game, you must always remain in character. If you must go out of character, find a way that does not interrupt the quality of roleplay for others.''',
        inline=False
        )

    embed.add_field(
        name="NLR",
        value=f''' <a:ArrowRightGlow:876672231789457449> Means that the player's character forgets knowledge of various information learned before dying(e.g. Burnt, drowned in ocean for a long time etc.)
        Players must follow NLR if they Die & Re-Spawn at a Hospital.''',
        inline=False
        )

    embed.set_footer(text="Welcome to Kollywood City")

    msg:discord.Message=await message.edit(embed=embed)
    # msg:discord.Message=await ctx.send(embed=embed)
    # await msg.add_reaction("<a:Alphabet_K:878036802269761537>")
    # await msg.add_reaction("<a:Alphabet_D:878035992395800677>")
    # await msg.add_reaction("<a:Alphabet_R:878037454345621574>")
    # await msg.add_reaction("<a:Alphabet_P:878037293699575818>")
    # await ctx.send("<@&1058816348580483122>")

bot.run("",reconnect=True)