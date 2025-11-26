from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /start command
    Sends a welcome message to the user
    """
    welcome_message = (
        "👋 Welcome to the RAG Chatbot!\n\n"
        "I can help you answer questions based on the company policy documents.\n\n"
        "Available commands:\n"
        "/start - Show this welcome message\n"
        "/help - Get help on how to use the bot\n"
        "/ask <question> - Ask a question about the documents\n"
        "/image - Process an image (if available)\n\n"
        "Example:\n"
        "/ask What is the company policy on remote work?"
    )
    
    await update.message.reply_text(welcome_message)
