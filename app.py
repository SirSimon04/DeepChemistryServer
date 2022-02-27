from flask import Flask, request, jsonify, send_file, Response
import werkzeug.utils as w
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return jsonify({"msg": "Hello World!"})


@app.route("/upload", methods=["POST"])
def upload():
    print("method called")
    imagefile = request.files[str(0)]
    filename = w.secure_filename(imagefile.filename)
    imagefile.save("./images/" + filename)
    return jsonify({"message": "Image uploaded successfully"})


if __name__ == '__main__':
    app.run()
