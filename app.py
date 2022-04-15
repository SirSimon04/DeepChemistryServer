import json
from flask import Flask, request, jsonify, Response
import werkzeug.utils as w
import time
from base64 import encodebytes
from PIL import Image as pillow
import io
import glob
import os

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return jsonify({"msg": "Hello World!"})


@app.route("/upload", methods=["POST"])
def upload():
    print("method called")
    imagefile = request.files[str(0)]
    filename = w.secure_filename(imagefile.filename)
    fn = filename[:len(filename) - 4]
    millis = round(time.time() * 1000)
    imagefile.save("./images/" + fn + "/" + fn + "_" + str(millis) + ".jpg")
    return jsonify({"message": "Image uploaded successfully"})


@app.route("/validate", methods=["GET"])
def get_validation_images():

    paths = [f for f in glob.glob("./images/*/*")]

    encoded_images = []

    index = 0

    for path in paths[0:50]:

        #encoded_images.append({"name": path[-path.rfind("/")-1:path.rfind("_")].capitalize(), "base64": get_response_image(path)})

        encoded_images.append(
            {"name": path[path.rfind("/")+1:path.rfind("_")], "base64": get_response_image(path), "path": path})

    resp = Response(json.dumps({"images": encoded_images}), 200, mimetype="application/json")

    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp


@app.route("/v", methods=["GET"])
def validate():

    args = request.args
    
    path = args.get("path")

    os.rename(path, path.replace("images", "validated"))

    return jsonify({"msg": "Success"})


@app.route("/delete", methods=["GET"])
def delete():

    args = request.args
    path = args.get("path")

    os.remove(path)

    return jsonify({"msg": "Success"})


def get_response_image(image_path):
    pil_img = pillow.open(image_path, mode='r')  # reads the PIL image
    pil_img = pil_img.convert("RGB")
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format="JPEG")  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return encoded_img


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)
