from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from model import style_transfer
import requests
from rq import Queue
from worker import conn
import time

import os

app = Flask(__name__)
q = Queue(connection=conn)


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
        result = q.enqueue(style_transfer,"sourceImagePath=contentImagePath,outputPath=outputImagePath, filterPath=images/styles/darksideofthemoon.jpeg")
        #time.sleep(900)
        print("result.result: "+str(result.result))
        while(result.result==None):
            print("Waiting for style transfer to conclude")
            time.sleep(10)
    #return result
    return send_file(outputImagePath,mimetype='image/jpg')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)