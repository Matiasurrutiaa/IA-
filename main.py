from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import uvicorn
import base64
import requests
from io import BytesIO
from PIL import Image
from deoldify.visualize import *
import torch
import warnings
import matplotlib.pyplot as plt

# Set device
from deoldify import device
from deoldify.device_id import DeviceId

device.set(device=DeviceId.GPU0)

# Setup
plt.style.use('dark_background')
torch.backends.cudnn.benchmark = True
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

colorizer = get_image_colorizer(artistic=True)

def colorize_image_from_url(source_url, render_factor=35):
    response = requests.get(source_url)
    img = Image.open(BytesIO(response.content))
    source_path = 'test_images/input_image.png'
    img.save(source_path)
    
    result_path = colorizer.plot_transformed_image(path=source_path, render_factor=render_factor, compare=True)
    return source_path, result_path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/colorize", response_class=HTMLResponse)
def colorize(request: Request, url: str = Form(...)):
    source_path, result_path = colorize_image_from_url(url)

    with open(source_path, "rb") as original_image_file:
        original_encoded_string = base64.b64encode(original_image_file.read()).decode('utf-8')

    with open(result_path, "rb") as colorized_image_file:
        colorized_encoded_string = base64.b64encode(colorized_image_file.read()).decode('utf-8')

    return templates.TemplateResponse("index.html", {
        "request": request,
        "original_image": original_encoded_string,
        "colorized_image": colorized_encoded_string
    })

def serve_api():
    uvicorn.run("main:app", host="192.168.1.101", port=8000, log_level="info")

if __name__ == "__main__":
    serve_api()
