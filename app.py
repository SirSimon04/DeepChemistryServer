from flask import Flask, request, jsonify, send_file, Response
import werkzeug.utils as w
import time

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


def current_milli_time():
    return round(time.time() * 1000)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)
