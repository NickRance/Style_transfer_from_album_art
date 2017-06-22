from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from model import style_transfer
import requests

import os

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("my-form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    imageName = text.split("/")[-1]
    contentImagePath = "images/input/"+imageName
    outputImagePath = "images/output/"+imageName
    # print(file_path)
    if not os.path.exists(outputImagePath):
        f = open(contentImagePath, 'wb')
        f.write(requests.get(text).content)
        f.close()
        #style_transfer("images/profile.jpg")
        style_transfer(sourceImagePath=contentImagePath,outputPath=outputImagePath, filterPath="images/styles/darksideofthemoon.jpeg")
        return("Ok re-enter the image in 10 minutes")
    else:
        return send_file(outputImagePath,mimetype='image/jpg')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)