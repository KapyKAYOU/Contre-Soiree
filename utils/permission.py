from utils.config import (
    CHANNEL_WHITELIST,
    CHANNEL_HOST,
    MANAGE_ROLE_IDS,
    VIEW_ROLE_IDS,
    CLEAR_ALLOWED_USER_ID,
    CHANNEL_THREAD_ID
)


async def check_whitelist_channel(ctx):
    if ctx.channel.id == CHANNEL_WHITELIST:
        return True

    try:
        msg = await ctx.send("❌ Cette commande doit être utilisée dans #whitelist.")
        await msg.delete(delay=5)
        await ctx.message.delete(delay=5)
    except:
        pass
    return False

async def check_host_channel(ctx):
    if ctx.channel.id == CHANNEL_HOST:
        return True

    try:
        msg = await ctx.send("❌ Cette commande doit être utilisée dans #chat-host.")
        await msg.delete(delay=5)
        await ctx.message.delete(delay=5)
    except:
        pass
    return False

async def check_thread_channel(ctx):
    if ctx.channel.id == CHANNEL_THREAD_ID:
        return True

    try:
        msg = await ctx.send("❌ Cette commande doit être utilisée dans **#annonce-game**.")
        await msg.delete(delay=5)
        await ctx.message.delete(delay=5)
    except:
        pass

    return False

async def can_manage(ctx):
    if any(role.id in MANAGE_ROLE_IDS for role in ctx.author.roles):
        return True

    try:
        msg = await ctx.send("🚫 Tu n'as pas la permission.")
        await msg.delete(delay=5)
        await ctx.message.delete(delay=5)
    except:
        pass
    return False

async def can_view(ctx):
    if any(role.id in VIEW_ROLE_IDS for role in ctx.author.roles):
        return True

    try:
        msg = await ctx.send("🚫 Réservé aux hosts.")
        await msg.delete(delay=5)
        await ctx.message.delete(delay=5)
    except:
        pass
    return False

async def can_clear(ctx):
    if ctx.author.id == CLEAR_ALLOWED_USER_ID:
        return True

    try:
        msg = await ctx.send("🚫 Commande réservée à l’admin.")
        await msg.delete(delay=5)
        await ctx.message.delete(delay=5)
    except:
        pass
    return False
