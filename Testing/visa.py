from PIL import Image,ImageFont,ImageDraw,ImageOps
from io import BytesIO
import datetime

now=datetime.datetime.now().__format__("%d/%m/%Y @ %H:%M:%S")


loc="discordfiles/discord full bot/KOLLYWOOD RP/visasample.png"

img = Image.open(loc)

# asset = "https://media.discordapp.net/attachments/1009118371100504065/1049274734535254097/JPG_c2845d2b498d273fbb57ea5cea04d623.png?width=662&height=662"
# data =BytesIO(asset)
data="profile.png"#"discordfiles/discord full bot/KOLLYWOOD RP/logo.png"
pfp = Image.open(data).convert("RGBA")
pfp=pfp.resize((175,175))
img.paste(pfp,(133,217),pfp)

font = ImageFont.truetype("discordfiles/discord full bot/KOLLYWOOD RP/nasalization-rg.otf",30)
draw =ImageDraw.Draw(img)
name = "i_am_smf_#2747"
dob="28/12/2022 @ 14:51:24"
passno="0980980870807800"
doc=str(now)
cd=(0,255,253)
draw.text((645,242),name,cd,font=font)
draw.text((645,293),dob,cd,font=font)
draw.text((645,342),passno,cd,font=font)
draw.text((460,434),doc,cd,font=font)

# img.save("discordfiles/discord full bot/KOLLYWOOD RP/visa1.png")
img.show()