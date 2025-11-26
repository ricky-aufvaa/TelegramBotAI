# Image Processing with LLaVA Vision Model

## Overview
The Telegram bot includes image processing capabilities using the LLaVA 7B vision model running on Ollama. Users can send images to the bot and receive AI-powered analysis and descriptions.

## Features

### ✅ Implemented Capabilities
- **Image Description**: Automatic detailed description of uploaded images
- **Question Answering**: Answer specific questions about image content
- **Object Detection**: Identify objects, people, and scenes in images
- **Context Understanding**: Understand relationships and context within images
- **Caption Support**: Process images with custom user prompts

## How It Works

### Image Processing Flow

1. **User sends image** to the bot (via Telegram)
2. **Bot downloads** the image from Telegram servers
3. **Image conversion**: Converts to PIL Image and then to base64
4. **LLaVA model** processes the image with user's prompt
5. **Response generated** and sent back to user

### Technical Implementation

```python
# Image is downloaded as bytes
photo_bytes = await photo_file.download_as_bytearray()

# Converted to PIL Image
image = Image.open(BytesIO(photo_bytes))

# Encoded to base64 for the model
img_base64 = base64.b64encode(buffered.getvalue()).decode()

# Sent to LLaVA model with prompt
response = vision_model.invoke([{
    "role": "user", 
    "content": [text_prompt, image_data]
}])
```

## Usage Examples

### Basic Image Description
```
User: [Sends a photo of a sunset]
Bot: 🔍 Image Analysis:

This image shows a beautiful sunset over the ocean. The sky is painted 
with vibrant orange and pink hues, with clouds scattered across the 
horizon. The sun is partially visible, creating a golden reflection on 
the water's surface...
```

### Question About Image
```
User: [Sends a photo with caption "What colors are in this image?"]
Bot: 🔍 Image Analysis:

The image contains several prominent colors:
- Deep blue in the sky
- Golden yellow from the sunlight
- Orange and pink tones in the clouds
- Dark silhouettes in the foreground
```

### Object Identification
```
User: [Sends a photo with caption "What objects can you see?"]
Bot: 🔍 Image Analysis:

I can identify the following objects in this image:
1. A wooden table in the center
2. Two chairs on either side
3. A vase with flowers
4. A window in the background
5. Curtains framing the window
```

## Setup Requirements

### 1. Install Ollama
```bash
# Download and install Ollama from https://ollama.ai
# Or use package manager (example for Linux):
curl https://ollama.ai/install.sh | sh
```

### 2. Pull LLaVA Model
```bash
# Pull the LLaVA 7B model
ollama pull llava:7b
```

### 3. Verify Installation
```bash
# Check if model is available
ollama list

# Test the model
ollama run llava:7b
```

### 4. Install Python Dependencies
```bash
pip install langchain-ollama pillow python-telegram-bot
```

## Configuration

### helpers.py
Located in `telegram_bot/IMAGE/helpers.py`:

```python
from langchain_ollama import ChatOllama

def get_image_model():
    vision_model = ChatOllama(model="llava:7b")
    return vision_model
```

### Customization Options

You can modify the model configuration:

```python
def get_image_model():
    vision_model = ChatOllama(
        model="llava:7b",
        temperature=0.7,  # Adjust creativity (0.0 - 1.0)
        num_ctx=4096,     # Context window size
    )
    return vision_model
```

## Image Handler Implementation

### Key Components

1. **Image Download**: Downloads image from Telegram
2. **Format Conversion**: Converts to PIL Image and base64
3. **Prompt Processing**: Handles user captions or default prompts
4. **Model Invocation**: Sends to LLaVA for analysis
5. **Response Formatting**: Formats and sends response back

### Error Handling

The handler includes comprehensive error handling:
- Image download failures
- Corrupted image files
- Ollama connection issues
- Model processing errors

## Performance Considerations

### Response Times
- **Small images** (< 1MB): 3-5 seconds
- **Medium images** (1-3MB): 5-8 seconds
- **Large images** (> 3MB): 8-12 seconds

### Optimization Tips
1. Images are automatically resized if too large
2. Base64 encoding is efficient for model input
3. Async operations prevent blocking

### Resource Usage
- **Memory**: ~2GB for LLaVA 7B model
- **CPU**: Moderate usage during inference
- **GPU**: Optional but recommended for faster processing

## Troubleshooting

### Common Issues

#### 1. "Ollama is not running"
```bash
# Start Ollama service
ollama serve
```

#### 2. "Model not found"
```bash
# Pull the model again
ollama pull llava:7b
```

#### 3. "Image processing timeout"
- Check Ollama is running
- Verify model is loaded
- Try with smaller image

#### 4. "Import errors"
```bash
# Install missing dependencies
pip install langchain-ollama pillow
```

### Debug Mode

Enable detailed logging in `image_handler.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Usage

### Custom Prompts

Users can ask specific questions:
- "What is the main subject of this image?"
- "Describe the mood and atmosphere"
- "What time of day is shown?"
- "Are there any people in this image?"
- "What text can you read in this image?"

### Multi-turn Conversations

The bot maintains context, so users can:
1. Send an image
2. Ask follow-up questions about the same image
3. Get detailed analysis

## Model Capabilities

### What LLaVA Can Do
✅ Describe scenes and objects
✅ Identify colors and patterns
✅ Recognize common objects
✅ Understand spatial relationships
✅ Read text in images (OCR)
✅ Detect emotions and moods
✅ Identify activities and actions

### Limitations
❌ May struggle with very small text
❌ Limited accuracy on rare objects
❌ Cannot identify specific individuals
❌ May misinterpret abstract art
❌ Limited understanding of technical diagrams

## Future Enhancements

- [ ] Support for multiple images in one message
- [ ] Image comparison capabilities
- [ ] Save image analysis history
- [ ] Support for other vision models (GPT-4V, Claude Vision)
- [ ] Image editing suggestions
- [ ] Batch image processing
- [ ] Custom model fine-tuning

## API Reference

### get_image_model()
Returns an initialized LLaVA vision model instance.

**Returns**: `ChatOllama` - Configured vision model

**Example**:
```python
from IMAGE.helpers import get_image_model
model = get_image_model()
```

### handle_image(update, context)
Async handler for processing images sent to the bot.

**Parameters**:
- `update`: Telegram Update object
- `context`: Telegram Context object

**Returns**: None (sends response to user)

## Security Considerations

⚠️ **Important**:
- Images are processed locally (not sent to external APIs)
- No image data is stored permanently
- User privacy is maintained
- Ollama runs on your local machine

## Support

For issues with image processing:
1. Verify Ollama is running: `ollama list`
2. Check model is available: `ollama run llava:7b`
3. Review error logs in console
4. Ensure sufficient system resources

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [LLaVA Model Info](https://ollama.ai/library/llava)
