import os

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("7524142710:AAEA9Y7RL_BqxeCJmDeFxMThaQ4U9-CfW_U")

if BOT_TOKEN:
    print("BOT_TOKEN successfully loaded.")
else:
    raise ValueError("No BOT_TOKEN found in environment variables.")


# Get the bot token from the environment variable
BOT_TOKEN = os.getenv("7524142710:AAEA9Y7RL_BqxeCJmDeFxMThaQ4U9-CfW_U")

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables.")

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Define the persistent main menu commands (left-bottom menu bar)
MAIN_MENU_COMMANDS = [
    BotCommand("start", "Show the main menu"),
    BotCommand("help", "Get help with the bot"),
    BotCommand("request", "Request a service"),
]

# Define main menu keyboard
MAIN_MENU = [
    [InlineKeyboardButton("Visit Our Website 🌐", url="https://brant.ae/")],
    [InlineKeyboardButton("General Information", callback_data='general')],
    [InlineKeyboardButton("Business Setup", callback_data='business_setup')],
    [InlineKeyboardButton("Bank Account Opening", callback_data='bank')],
    [InlineKeyboardButton("UAE Golden Visa", callback_data='golden_visa')],
    [InlineKeyboardButton("PRO Services", callback_data='pro')],
    [InlineKeyboardButton("Real Estate", callback_data='real_estate')],
    [InlineKeyboardButton("Driver’s License Services", callback_data='license')],
    [InlineKeyboardButton("Other Services", callback_data='other')],
    [InlineKeyboardButton("FAQs", callback_data='faqs')],
    [InlineKeyboardButton("Request a Service", callback_data='request_service')],
]

# Submenu keyboards
BUSINESS_SETUP_MENU = [
    [InlineKeyboardButton("Mainland Business", callback_data='mainland')],
    [InlineKeyboardButton("Free Zone Business", callback_data='free_zone')],
    [InlineKeyboardButton("Offshore Business", callback_data='offshore')],
    [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')],
]

# Initialize a dictionary to keep track of user requests
user_requests = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the main menu when the bot starts."""
    reply_markup = InlineKeyboardMarkup(MAIN_MENU)
    await update.message.reply_text(
        "Welcome to Brant Premium! How can we assist you today?\n\n"
        "Please select an option below:",
        reply_markup=reply_markup,
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle menu selection and display submenu or information."""
    query = update.callback_query
    await query.answer()

    # Dictionary for submenu content
    submenu_data = {
        'general': "Brant Premium specializes in:\n"
                   "📌 Business setup\n"
                   "📌 UAE Golden Visa applications\n"
                   "📌 Corporate bank account opening\n"
                   "📌 Real estate services\n\n"
                   "Visit our website for more information: [Brant Premium Website 🌐](https://brant.ae/)\n\n"
                   "📞 Contact us at +971 50 568 986 2\n"
                   "📧 Email: info@brant.ae",

        'business_setup': "Choose the type of business setup:\n\n"
                          "1️⃣ Mainland Business:\n"
                          "✅ Operate anywhere in the UAE.\n"
                          "✅ Full market access and government contracts.\n\n"
                          "2️⃣ Free Zone Business:\n"
                          "✅ 100% foreign ownership.\n"
                          "✅ Tax exemptions.\n"
                          "✅ Limited external operations.\n\n"
                          "3️⃣ Offshore Business:\n"
                          "✅ Designed for international trade.\n"
                          "✅ Tax optimization.\n"
                          "✅ No physical office required.",

        'bank': "Bank Account Services:\n\n"
                "📄 Assistance with opening corporate bank accounts.\n"
                "⏱️ Typical timeline: 1-4 weeks.\n"
                "🔑 Required documents:\n"
                "- Trade License\n"
                "- Passport\n"
                "- Proof of Address.",

        'golden_visa': "UAE Golden Visa:\n\n"
                       "🟢 Long-term residency for:\n"
                       "✅ Investors\n"
                       "✅ Entrepreneurs\n"
                       "✅ Specialized talents.\n\n"
                       "Benefits:\n"
                       "📌 10-year residency\n"
                       "📌 Family sponsorship\n"
                       "📌 Access to UAE facilities.",

        'pro': "PRO Services:\n\n"
               "📌 Visa applications, trade license renewals, and more.\n"
               "✅ Simplifies government processes for businesses.",

        'real_estate': "Real Estate Services:\n\n"
                       "🏠 Assistance with buying, selling, and managing properties.\n"
                       "📊 Market analysis and property investment guidance.",

        'license': "Driver’s License Services:\n\n"
                   "🚘 Assistance obtaining a UAE driver's license.\n"
                   "✅ Help converting an existing license if eligible.",

        'other': "Other Services:\n\n"
                 "🛠️ Employee and family visa assistance.\n"
                 "📝 Trademark registration.",

        'faqs': "FAQs:\n\n"
                "1️⃣ How long does it take to set up a business? 7-15 days.\n"
                "2️⃣ Can I open a business remotely? Yes.\n"
                "3️⃣ What is the UAE Golden Visa? A 10-year residency visa for eligible individuals.",
    }

    if query.data in submenu_data:
        # Submenu with an option to request a service
        keyboard = [
            [InlineKeyboardButton("Request This Service", callback_data=f'request_{query.data}')],
            [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=submenu_data[query.data],
            reply_markup=reply_markup,
        )

    elif query.data.startswith('request_'):
        # Handle service-specific requests
        service = query.data.split('_')[1]
        user_requests[query.from_user.id] = {'service': service, 'status': 'pending'}
        await query.edit_message_text(
            text="Please describe your requirements for this service. Our team will contact you shortly."
        )

    elif query.data == 'main_menu':
        # Return to main menu
        reply_markup = InlineKeyboardMarkup(MAIN_MENU)
        await query.edit_message_text(
            text="Welcome back to the main menu! How can we assist you today?",
            reply_markup=reply_markup,
        )

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user service requests and notify admin."""
    user_id = update.message.from_user.id
    if user_id in user_requests and user_requests[user_id]['status'] == 'pending':
        # Save the request
        user_requests[user_id]['request'] = update.message.text
        user_requests[user_id]['status'] = 'submitted'

        # Notify the user
        await update.message.reply_text(
            "Thank you! Your request has been received. Our team will contact you shortly.\n\n"
            "If you need further assistance, please return to the /start menu."
        )

        # Notify admin (replace ADMIN_ID with your Telegram user ID)
        ADMIN_ID = 411222193  # Replace with the admin's Telegram ID
        await context.bot.send_message(
            ADMIN_ID,
            f"New service request received from {update.message.from_user.first_name}:\n\n"
            f"Requested Service: {user_requests[user_id]['service']}\n"
            f"Details: {update.message.text}"
        )
    else:
        await update.message.reply_text(
            "Sorry, I didn't understand that. Please select a service from the menu."
        )

# Main function to start the bot
def main():
    application = Application.builder().token("7524142710:AAEA9Y7RL_BqxeCJmDeFxMThaQ4U9-CfW_U").build()

    # Set persistent menu commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_menu))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_request))

    async def set_bot_commands():
        await application.bot.set_my_commands(MAIN_MENU_COMMANDS)

    application.run_polling()

if __name__ == "__main__":
    main()
