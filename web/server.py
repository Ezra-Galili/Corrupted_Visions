import io
from flask import Flask, Response, request
from PIL import Image
from core import pure
from core.effects import Delay
from core.pipeline import preview

app = Flask(__name__)

img = Image.open("test images/chrysler2.jpeg")


def clamp(value, low, high):
    return max(low, min(value, high))


@app.route("/")
def home():
    return "hello from the glitch server"


@app.route("/preview")
def preview_route():
    try:
        delay = int(request.args.get("delay", 300))
        feedback = float(request.args.get("feedback", 0.5))
    except ValueError:
        return "delay must be a whole number and feedback a decimal", 400

    delay = clamp(delay, 0, 20000)
    feedback = clamp(feedback, 0.0, 0.95)

    chain = [Delay(delay, feedback)]
    image, ok, message = preview(img, chain, pure)
    if not ok:
        return message, 500

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return Response(buf.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)