import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

CHANNELS = {
    'JAPAN 2025': 'https://t.me/your_japan_channel',
    'INDIA 2023-2024': 'https://t.me/your_india_channel',
    'VIETNAM': 'https://t.me/your_vietnam_channel',
    'KENYA': 'https://t.me/your_kenya_channel'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = f"Welcome {user.first_name}!\n\nDADA OTP SMS BOT\n\nAvailable Channels:\n"
    for country, link in CHANNELS.items():
        text += f"• {country}: [Join Now]({link})\n"

    text += "\n/menu - Main Menu"

    await update.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📱 Buy Account", callback_data='buy')],
        [InlineKeyboardButton("💰 Balance", callback_data='balance'),
         InlineKeyboardButton("💳 Recharge", callback_data='recharge')],
        [InlineKeyboardButton("👥 Refer Friends", callback_data='refer'),
         InlineKeyboardButton("🎁 Redeem", callback_data='redeem')],
        [InlineKeyboardButton("🆘 Support", callback_data='support')]
    ]

    await update.message.reply_text(
        "Welcome To Otp Bot\n\nUse menu below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy':
        text = "Available Accounts:\n1. Gmail - ₹50\n2. Instagram - ₹30"
    
    elif query.data == 'balance':
        text = "Your Balance: ₹100"

    elif query.data == 'recharge':
        text = "Recharge ₹100 / ₹500 / ₹1000\nContact admin"

    elif query.data == 'refer':
        user_id = update.effective_user.id
        text = f"Referral link:\nhttps://t.me/your_bot?start={user_id}"

    elif query.data == 'redeem':
        text = "Send /redeem CODE"

    elif query.data == 'support':
        text = "Contact @admin_username"

    elif query.data == 'back_to_menu':
        return await menu(update, context)

    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(f"Buying account {context.args[0]}")
    else:
        await update.message.reply_text("Usage: /buy 1")

async def redeem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(f"Redeemed: {context.args[0]}")
    else:
        await update.message.reply_text("Usage: /redeem CODE")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("buy", buy_command))
    app.add_handler(CommandHandler("redeem", redeem_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot running...")
    app.run_polling()

if __name__ == '__main__':
    main()
