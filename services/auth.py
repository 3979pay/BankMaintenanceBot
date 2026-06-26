from telegram import Update


async def is_admin(update: Update, context):

    user = update.effective_user
    chat = update.effective_chat

    member = await context.bot.get_chat_member(
        chat.id,
        user.id
    )

    return member.status in (
        "administrator",
        "creator"
    )