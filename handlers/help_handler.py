from telegram import Update
from telegram.ext import ContextTypes


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /help command
    Provides detailed help information
    """
    help_message = (
        "📚 **How to Use the RAG Chatbot**\n\n"
        "This bot uses Retrieval-Augmented Generation (RAG) to answer your questions "
        "based on company policy documents.\n\n"
        "**Commands:**\n\n"
        "🔹 /start - Start the bot and see welcome message\n"
        "🔹 /help - Show this help message\n"
        "🔹 /ask <question> - Ask a question about the documents\n"
        "🔹 /image - Process an image (if available)\n\n"
        "**How to Ask Questions:**\n\n"
        "Simply type `/ask` followed by your question. The bot will search through "
        "the company policy documents and provide you with relevant information.\n\n"
        "**Examples:**\n"
        "• /ask What is the vacation policy?\n"
        "• /ask How do I request time off?\n"
        "• /ask What are the working hours?\n"
        "• /ask Tell me about the remote work policy\n\n"
        "**Features:**\n"
        "✅ Maintains conversation history\n"
        "✅ Context-aware responses\n"
        "✅ Searches through multiple documents\n"
        "✅ Provides accurate, source-based answers\n\n"
        "**Tips:**\n"
        "• Be specific with your questions\n"
        "• You can ask follow-up questions\n"
        "• The bot remembers your conversation context\n\n"
        "Need more help? Just ask a question!"
    )
    
    await update.message.reply_text(help_message, parse_mode='Markdown')
