from flask import Flask, Response
import io
from PIL import Image
from core import pure
from core.effects import Delay, Echo
from core.pipeline import preview


app = Flask(__name__)

img = Image.open("test images/chrysler2.jpeg")

@app.route("/")
def home():
    return "hello from the glitch server"

@app.route("/preview")
def preview_route():
    chain = [Delay(300, 0.5), Echo(3000, 0.3, 10)]

    image, ok, message = preview(img, chain, pure)

    if not ok:

        return message, 500
    buf = io.BytesIO()

    image.save(buf, format = "PNG")

    return Response(buf.getvalue(), mimetype = "image/png")

if __name__ == "__main__":
    app.run(debug = True)

