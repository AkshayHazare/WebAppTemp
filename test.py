import os
from flask import Flask, render_template, request, send_from_directory, after_this_request
import shutil
#import main

DATA_DIR = "/data"
OP_DIR = "/output"

app = Flask(__name__, template_folder="templates")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static')
    source = os.path.join(APP_ROOT,'output/images')

    if not os.path.isdir(target):
       os.mkdir(target)
    else:
       shutil.rmtree(target,ignore_errors=True)
       os.mkdir(target)

    if not os.path.isdir(source):
        os.mkdir(source)
    else:
       shutil.rmtree(source, ignore_errors=True)
       os.mkdir(source)

    for upload in request.files.getlist("file[]"):
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)

    while(os.listdir(source)==[]):
        print("Waiting")
    #return send_from_directory("static", filename, as_attachment=True)
    return render_template("index.html", image_name = filename)

@app.route('/static/<filename>')
def send_input_image(filename):
    return send_from_directory("static/", filename)

@app.route('/output/images/<filename>')
def send_output_image(filename):
    return send_from_directory("output/images/", filename)

if __name__ == "__main__":
    app.debug = True
    #main.run()

    app.run(port=5000, debug=True)
