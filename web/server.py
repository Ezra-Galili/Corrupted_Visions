import io
from flask import Flask, Response, request, render_template, jsonify
from PIL import Image
from core import pure, corrupted
from core.effects import Delay
from core.pipeline import preview
from core.registry import EFFECTS

app = Flask(__name__)

img = Image.open("test images/chrysler2.jpeg")

MODES = {"pure": pure, "corrupted": corrupted}


def clamp(value, low, high):
    return max(low, min(value, high))


def build_chain(items):
    chain = []
    for item in items:
        name = item.get("effect")
        if name not in EFFECTS:
            raise ValueError("unknown effect: " + str(name))
        spec = EFFECTS[name]
        values = {}
        for pname, rules in spec["params"].items():
            raw = item.get("params", {}).get(pname, rules["default"])
            convert = int if rules["type"] == "int" else float
            values[pname] = clamp(convert(raw), rules["min"], rules["max"])
        chain.append(spec["class"](**values))
    return chain


def to_png(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return Response(buf.getvalue(), mimetype="image/png")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/effects")
def effects_route():
    return jsonify({
        name: {"params": spec["params"]}
        for name, spec in EFFECTS.items()
    })


@app.route("/preview")
def preview_route():
    try:
        delay = int(request.args.get("delay", 300))
        feedback = float(request.args.get("feedback", 0.5))
    except ValueError:
        return "delay must be a whole number and feedback a decimal", 400

    mode_name = request.args.get("mode", "pure")
    if mode_name not in MODES:
        return "unknown mode", 400
    mode = MODES[mode_name]

    delay = clamp(delay, 0, 20000)
    feedback = clamp(feedback, 0.0, 0.95)

    chain = [Delay(delay, feedback)]
    image, ok, message = preview(img, chain, mode)
    if not ok:
        return message, 500
    return to_png(image)


@app.route("/render", methods=["POST"])
def render_route():
    data = request.get_json(silent=True)
    if not data:
        return "expected JSON", 400

    mode_name = data.get("mode", "pure")
    if mode_name not in MODES:
        return "unknown mode", 400

    try:
        chain = build_chain(data.get("chain", []))
    except (ValueError, TypeError, AttributeError) as e:
        return str(e), 400

    image, ok, message = preview(img, chain, MODES[mode_name])
    if not ok:
        return message, 500
    return to_png(image)


if __name__ == "__main__":
    app.run(debug=True)