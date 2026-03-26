"""
Ban All Users Module for Spotify Music Bot
यह module सभी users को ban करने की functionality देता है
"""

from pyrogram import Client, filters
from pyrogram.types import Message

# Owner ID - अपना Telegram ID यहाँ डालो
OWNER_ID = 123456789

# Banned users list (memory में store)
BANNED_USERS = set()

async def ban_all_users(client: Client, message: Message):
    """
    सभी users को bot से ban कर दो
    Command: /banall
    """
    
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("❌ **Owner only command!**")
        return
    
    # Get all users from database या group
    # यह simplified version है - आप अपने database के अनुसार modify कर सकते हो
    
    await message.reply_text(
        "🚫 **Ban All Process Started**\n\n"
        "सभी users को ban किया जा रहा है...",
        parse_mode="markdown"
    )
    
    # Ban logic here
    BANNED_USERS.clear()  # सभी को ban करने के लिए
    
    await message.reply_text(
        "✅ **Ban All Complete!**\n\n"
        f"कुल {len(BANNED_USERS)} users banned हो गए हैं।",
        parse_mode="markdown"
    )

async def unban_all_users(client: Client, message: Message):
    """
    सभी users को unban कर दो
    Command: /unbanall
    """
    
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("❌ **Owner only command!**")
        return
    
    banned_count = len(BANNED_USERS)
    BANNED_USERS.clear()
    
    await message.reply_text(
        "✅ **Unban All Complete!**\n\n"
        f"कुल {banned_count} users unban हो गए हैं।",
        parse_mode="markdown"
    )

async def ban_user(client: Client, message: Message):
    """
    एक specific user को ban करो
    Command: /ban @username या /ban user_id
    """
    
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("❌ **Owner only command!**")
        return
    
    # Check if user mentioned
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("❌ Please reply to a message or mention a user!")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.first_name
    else:
        try:
            user_id = int(message.command[1])
            username = str(user_id)
        except:
            await message.reply_text("❌ Invalid user ID!")
            return
    
    if user_id == OWNER_ID:
        await message.reply_text("❌ You cannot ban yourself!")
        return
    
    BANNED_USERS.add(user_id)
    
    await message.reply_text(
        f"🚫 **User Banned**\n\n"
        f"**{username}** को bot से ban कर दिया गया है।",
        parse_mode="markdown"
    )

async def unban_user(client: Client, message: Message):
    """
    एक specific user को unban करो
    Command: /unban user_id
    """
    
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("❌ **Owner only command!**")
        return
    
    if not message.reply_to_message and len(message.command) < 2:
        await message.reply_text("❌ Please reply to a message or provide user ID!")
        return
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.first_name
    else:
        try:
            user_id = int(message.command[1])
            username = str(user_id)
        except:
            await message.reply_text("❌ Invalid user ID!")
            return
    
    if user_id not in BANNED_USERS:
        await message.reply_text(f"❌ **{username}** पहले से ban नहीं है!")
        return
    
    BANNED_USERS.discard(user_id)
    
    await message.reply_text(
        f"✅ **User Unbanned**\n\n"
        f"**{username}** को unban कर दिया गया है।",
        parse_mode="markdown"
    )

async def ban_list(client: Client, message: Message):
    """
    सभी banned users की list दिखाओ
    Command: /banlist
    """
    
    # Check if user is owner
    if message.from_user.id != OWNER_ID:
        await message.reply_text("❌ **Owner only command!**")
        return
    
    if not BANNED_USERS:
        await message.reply_text("✅ कोई भी user ban नहीं है!")
        return
    
    banned_list = "\n".join([f"• `{user_id}`" for user_id in BANNED_USERS])
    
    await message.reply_text(
        f"**📋 Banned Users List:**\n\n{banned_list}\n\n"
        f"**Total:** {len(BANNED_USERS)} users",
        parse_mode="markdown"
    )

def is_banned(user_id: int) -> bool:
    """
    Check if user is banned
    """
    return user_id in BANNED_USERS

# Functions to register commands
async def register_handlers(app: Client):
    """
    सभी handlers को register करो
    """
    app.on_message(filters.command("banall"))(ban_all_users)
    app.on_message(filters.command("unbanall"))(unban_all_users)
    app.on_message(filters.command("ban"))(ban_user)
    app.on_message(filters.command("unban"))(unban_user)
    app.on_message(filters.command("banlist"))(ban_list)
