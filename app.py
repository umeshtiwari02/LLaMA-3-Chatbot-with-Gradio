from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from chat_assistant_website import demo as gradio_app

app = FastAPI()
app.mount("/", gradio_app)
