
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
import config

from handlers.start_handler import start
from handlers.help_handler import help_cmd
from handlers.ask_handler import ask
from handlers.image_handler import image_cmd, handle_image


def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Register Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ask", ask))
    app.add_handler(CommandHandler("image", image_cmd))

    # Register Image Handler
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
