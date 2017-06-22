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
    if not os.path.exists(contentImagePath):
        f = open(contentImagePath, 'wb')
        f.write(requests.get(text).content)
        f.close()
        #style_transfer("images/profile.jpg")
        style_transfer("images/input/"+imageName)
    return send_file("images/output/"+imageName+".png",mimetype='image/png')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)