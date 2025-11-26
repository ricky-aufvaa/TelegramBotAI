import sys
import os

# Add parent directory to path to import RAG modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from telegram import Update
from telegram.ext import ContextTypes

# Import RAG chain
from RAG.chains import chain_with_message_history


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /ask command to query the RAG system
    Usage: /ask <your question>
    """
    # Get the user's message
    user_message = update.message.text
    
    # Extract the query (remove /ask command)
    query = user_message.replace('/ask', '').strip()
    
    # Check if query is empty
    if not query:
        await update.message.reply_text(
            "Please provide a question after /ask command.\n"
            "Example: /ask What is the company policy on remote work?"
        )
        return
    
    # Get user's telegram ID as session ID for personalized chat history
    session_id = str(update.effective_user.id)
    
    try:
        # Send typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )
        
        # Call RAG chain with the query
        response = chain_with_message_history.invoke(
            {"question": query},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Send the response back to user
        await update.message.reply_text(response)
        
    except Exception as e:
        # Handle errors gracefully
        error_message = (
            "Sorry, I encountered an error while processing your question. "
            "Please try again later."
        )
        await update.message.reply_text(error_message)
        
        # Log the error for debugging
        print(f"Error in ask handler: {str(e)}")
        import traceback
        traceback.print_exc()
