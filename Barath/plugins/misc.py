import asyncio 

from Barath import barath 
from config import OWNER_ID, HANDLER
from pyrogram import filters
from gpytranslate import Translator

import requests


@barath.on_message(filters.command(["ud","define"],prefixes=HANDLER) & filters.user(OWNER_ID))
async def ud(_, message):
        if len(message.command) < 2:
             return await message.edit("where you input the text?")         
        text = message.text.split(None, 1)[1]
        try:
          results = requests.get(
            f'https://api.urbandictionary.com/v0/define?term={text}').json()
          reply_text = f'**results: {text}**\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
        except Exception as e: 
              return await message.edit_text(f"Somthing wrong Happens:\n`{e}`")
        ud = await message.edit_text("Exploring....")
        await ud.edit_text(reply_text)
        
        
trans = Translator()
@barath.on_message(filters.command("tr",prefixes=HANDLER) & filters.user(OWNER_ID))
async def translate(_, message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("[Reply To The Message Using The Translation Code Provided!](https://telegra.ph/Lang-Codes-03-19-3)")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"**Translated from {source} to {dest}**:\n"
        f"`{translation.text}`"
    )
    await message.delete()
    await reply_msg.reply_text(reply)
    return 

@barath.on_message(filters.command("cc",HANDLER) & filters.user(OWNER_ID))
async def cc(_, m):
     try:
        code = m.command[1]
     except:
         return await m.edit("=> Input the bin code")
     api = requests.get(f"https://spamx.id/gen/?bin={code}&limit=50").json()
     cc = ""
     credits = api["Gen"]
     for x in credits:
         cc += f"{x}\n"
     bank = api.get("Bin Info")
     bank_name = bank.get("bank")
     bin_code = bank.get("bin")
     country = bank.get("country")
     flag = bank.get("flag")
     ios = bank.get("ios")
     level = bank.get("level")
     prepaid = bank.get("prepaid")
     type = bank.get("type")
     vendor = bank.get("vendor")
     string = f"""\u0020
=> Bin details:
🏦 **Bank**: {bank_name}
💳 **Bin**: {bin_code}
🌍 **Country**: {country}
⁉️ **Flag**: {flag}
📛 **Ios**: {ios}
⬆️ **Level**: {level}
🧐 **Prepaid**: {prepaid}
🧮 **Type**: {type}
❤️ **Vendor**: {vendor}\n

=> **Here credit cards**:
{cc}
"""
     return await m.edit(string)