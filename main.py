from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import base64
from deoldify_script import colorize_image

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    source_path = 'test_images/image.png'  # Path to the input image
    result_path = colorize_image(source_path)

    with open(source_path, "rb") as original_image_file:
        original_encoded_string = base64.b64encode(original_image_file.read()).decode('utf-8')

    with open(result_path, "rb") as colorized_image_file:
        colorized_encoded_string = base64.b64encode(colorized_image_file.read()).decode('utf-8')

    html_content = f"""
    <html>
    <head>
        <title>Colorized Image</title>
    </head>
    <body>
        <h1>Original and Colorized Images</h1>
        <h2>Original Image</h2>
        <img src="data:image/png;base64,{original_encoded_string}" alt="Original Image">
        <h2>Colorized Image</h2>
        <img src="data:image/png;base64,{colorized_encoded_string}" alt="Colorized Image">
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

def serve_api():
    uvicorn.run("main:app", host="192.168.1.101", port=8000, log_level="info")

if __name__ == "__main__":
    serve_api()
