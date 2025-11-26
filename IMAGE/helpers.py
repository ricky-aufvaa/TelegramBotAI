from langchain_ollama import ChatOllama
def get_image_model():
    vision_model = ChatOllama(model="llava:7b")
    return vision_model