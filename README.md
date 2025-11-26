# Telegram RAG Chatbot

## Demo
🎥 **See the bot in action**: [Demo Video](Demo/TelegramBotAI.mp4)

![Demo GIF](Demo/TelegramBotAI.gif)

## Overview
A Telegram bot integrated with a Retrieval-Augmented Generation (RAG) system that answers questions based on company policy documents.

## Project Structure

```
telegram_bot/
├── bot.py                 # Main bot application
├── config.py             # Configuration and environment variables
├── handlers/             # Command handlers
│   ├── ask_handler.py    # RAG query handler (/ask command)
│   ├── start_handler.py  # Welcome message handler (/start command)
│   ├── help_handler.py   # Help information handler (/help command)
│   └── image_handler.py  # Image processing handler
└── RAG/                  # RAG system (see RAG/README.md)
    ├── chains.py         # RAG chain configuration
    ├── helpers.py        # Utility functions
    ├── db.py            # Database and chat history
    ├── prompts.py       # LangChain prompts
    ├── preprocess.py    # Document preprocessing
    ├── constants.py     # Configuration constants
    └── data/            # PDF documents
```

## Features

### ✅ Implemented Features
- **RAG Integration**: Fully integrated RAG pipeline for document-based Q&A
- **Conversation History**: Maintains per-user chat history using Telegram user IDs
- **Multiple Commands**: /start, /help, /ask, /image
- **Error Handling**: Graceful error handling with user-friendly messages
- **Typing Indicator**: Shows typing status while processing queries
- **Context-Aware**: Remembers conversation context for follow-up questions

### 🔄 Command Reference

#### /start
Shows welcome message and available commands

#### /help
Displays detailed help information about using the bot

#### /ask <question>
Queries the RAG system with your question
- **Example**: `/ask What is the company vacation policy?`
- **Features**:
  - Searches through company policy documents
  - Provides context-aware answers
  - Maintains conversation history
  - Shows typing indicator during processing

#### /image
Information about image processing with LLaVA vision model

**Image Processing (Send Photo)**
Simply send any photo to the bot (with or without caption) to get AI-powered image analysis
- **Without caption**: Gets a detailed description of the image
- **With caption**: Answers your specific question about the image
- **Example**: Send a photo with caption "What objects are visible in this image?"

## Setup Instructions

### 1. Prerequisites
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull required models
ollama pull llama3.1:8b
ollama pull llava:7b

# Install Python packages
pip install python-telegram-bot python-dotenv
pip install langchain langchain-community langchain-ollama
pip install faiss-cpu sqlalchemy pypdf pillow
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```env
# Telegram Bot Token (get from @BotFather)
BOT_TOKEN=your_telegram_bot_token_here
```

Note: No API keys needed! All models run locally via Ollama.

### 3. Get Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token and add it to `.env` file

### 4. Prepare Documents
1. Place your PDF documents in `RAG/data/` folder
2. Run preprocessing to create embeddings:
```bash
cd RAG
python preprocess.py
```

### 5. Run the Bot
```bash
cd telegram_bot
python bot.py
```

You should see: `Bot is running...`

## How It Works

### RAG Integration Flow

1. **User sends query**: `/ask What is the vacation policy?`

2. **ask_handler.py processes**:
   - Extracts query from command
   - Gets user's Telegram ID as session_id
   - Sends typing indicator

3. **RAG chain executes**:
   - Retrieves relevant document chunks from FAISS vector store
   - Loads user's conversation history from database
   - Generates context-aware response using Llama 3.1 (via Ollama)

4. **Response sent back**:
   - Bot sends the answer to user
   - Conversation history is saved

### Session Management
- Each user has a unique session based on their Telegram user ID
- Conversation history is maintained per user
- Users can have contextual follow-up conversations

### Error Handling
- Network errors: Gracefully handled with retry logic
- RAG errors: User-friendly error messages
- Missing queries: Helpful usage instructions

## Code Architecture

### bot.py
Main application that:
- Initializes the Telegram bot
- Registers command handlers
- Starts polling for messages

### handlers/ask_handler.py
Core RAG integration:
```python
async def ask(update, context):
    # Extract query
    # Get session_id from user ID
    # Call RAG chain
    # Send response
```

**Key Features**:
- Async/await for non-blocking operations
- User session management
- Error handling
- Typing indicators

### RAG System
See `RAG/README.md` for detailed RAG system documentation.

## Usage Examples

### Basic Query
```
User: /ask What is the company vacation policy?
Bot: [Typing...]
Bot: According to the company policy documents, employees are entitled to...
```

### Follow-up Question
```
User: /ask Tell me about remote work
Bot: The company allows remote work with the following conditions...

User: /ask How do I request it?
Bot: [Uses conversation context] To request remote work, you need to...
```

### Error Handling
```
User: /ask
Bot: Please provide a question after /ask command.
     Example: /ask What is the company policy on remote work?
```

## Troubleshooting

### Bot not responding
1. Check if bot is running: `python bot.py`
2. Verify BOT_TOKEN in `.env` file
3. Check internet connection

### RAG errors
1. Ensure preprocessing was completed: `python RAG/preprocess.py`
2. Verify Ollama is running: `ollama list`
3. Check if `faiss_embed/` folder exists with embeddings
4. Ensure llama3.1:8b model is pulled: `ollama pull llama3.1:8b`

### Import errors
1. Ensure all dependencies are installed
2. Check Python path includes the project directory
3. Verify all handler files exist

## Development

### Adding New Commands
1. Create handler in `handlers/` folder
2. Import handler in `bot.py`
3. Register with `app.add_handler(CommandHandler("command", handler))`

### Modifying RAG Behavior
- Edit prompts in `RAG/prompts.py`
- Adjust retrieval parameters in `RAG/helpers.py`
- Modify chunking in `RAG/preprocess.py`
