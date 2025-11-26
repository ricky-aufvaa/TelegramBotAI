import sys
import os
import base64
from io import BytesIO

# Add parent directory to path to import IMAGE modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from telegram import Update
from telegram.ext import ContextTypes
from PIL import Image

# Import vision model
from IMAGE.helpers import get_image_model


async def image_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for /image command
    Provides instructions on how to send images
    """
    message = (
        "📸 **Image Processing with LLaVA Vision Model**\n\n"
        "To analyze an image, simply send me a photo directly (without any command).\n\n"
        "I will use the LLaVA 7B vision model to:\n"
        "• Describe what's in the image\n"
        "• Answer questions about the image\n"
        "• Provide detailed analysis\n\n"
        "You can also add a caption to your image to ask specific questions!\n\n"
        "Example: Send an image with caption 'What objects are in this image?'"
    )
    
    await update.message.reply_text(message, parse_mode='Markdown')


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for processing images sent by users using LLaVA vision model
    """
    try:
        # Send typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )
        
        # Get the photo (Telegram sends multiple sizes, get the largest)
        photo = update.message.photo[-1]
        
        # Download the photo
        photo_file = await context.bot.get_file(photo.file_id)
        
        # Download photo as bytes
        photo_bytes = await photo_file.download_as_bytearray()
        
        # Convert to PIL Image
        image = Image.open(BytesIO(photo_bytes))
        
        # Convert image to base64 for the vision model
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Get user's caption or use default prompt
        user_prompt = update.message.caption if update.message.caption else "Describe this image in detail. Generate 3 tags for the image along with its description"
        
        # Initialize vision model
        vision_model = get_image_model()
        
        # Create message with image
        message_content = [
            {
                "type": "text",
                "text": user_prompt
            },
            {
                "type":"text",
                "text": """Generate 3 tags to describe the image along with the response to the user.
                            Example:
                            Image Analysis:
                            The image depicts a tranquil scene of two dogs......
                            ..
                            Tags:
                            tranquil,dogs,peacefulness"""
            },
            {
                "type": "image_url",
                "image_url": f"data:image/png;base64,{img_base64}"
            }
        ]
        
        # Get response from vision model
        response = vision_model.invoke([{"role": "user", "content": message_content}])
        
        # Extract the text response
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        # Send the response back to user
        await update.message.reply_text(
            f"🔍 **Image Analysis:**\n\n{response_text}",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        error_message = (
            "Sorry, I encountered an error while processing your image. "
            "Please make sure:\n"
            "• The image is clear and not corrupted\n"
            "• Ollama is running with llava:7b model\n"
            "• Try again in a moment"
        )
        await update.message.reply_text(error_message)
        
        # Log the error for debugging
        print(f"Error in image handler: {str(e)}")
        import traceback
        traceback.print_exc()
