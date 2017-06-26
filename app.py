from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
from model import style_transfer
import requests
import datetime
from rq import Queue
#from rq_scheduler import Scheduler
from worker import conn
import time

import os

app = Flask(__name__)
q = Queue(connection=conn)
#scheduler = Scheduler(connection=conn)



@app.route('/')
def my_form():
    #schedule_controller()
    while(True):
        controller()
        time.sleep(15)

@app.route('/', methods=['POST'])
#Post requests add a job to the queue
def my_form_post():
    q.enqueue(wait60s)
    # text = request.form['text']
    # imageName = text.split("/")[-1]
    # contentImagePath = "images/input/"+imageName
    # outputImagePath = "images/output/"+imageName
    # # print(file_path)
    # if not os.path.exists(outputImagePath):
    #     f = open(contentImagePath, 'wb')
    #     f.write(requests.get(text).content)
    #     f.close()
    #     #style_transfer("images/profile.jpg")
    #     #result = q.enqueue(style_transfer,"sourceImagePath=contentImagePath,outputPath=outputImagePath, filterPath=images/styles/darksideofthemoon.jpeg")
    #     # scheduler.schedule(
    #     #     scheduled_time=datetime.utcnow(),  # Time for first execution, in UTC timezone
    #     #     func=style_transfer,  # Function to be queued
    #     #     args=[],  # Arguments passed into function when executed
    #     #     kwargs={"sourceImagePath":contentImagePath,"outputPath":outputImagePath,"filterPath":"images/styles/darksideofthemoon.jpeg"},  # Keyword arguments passed into function when executed
    #     #     interval=None,  # Time before the function is called again, in seconds
    #     #     repeat=0
    #     # )
    # return(send_file("images/styles/darksideofthemoon.jpeg"))
    #     #time.sleep(900)
    # #     print("result.result: "+str(result.result))
    # #     while(result.result==None):
    # #         print("Waiting for style transfer to conclude")
    # #         time.sleep(10)
    # # #return result
    # # return send_file(outputImagePath,mimetype='image/jpg')


# def schedule_controller():
#     #If there are no jobs queued render the url form
#     if not scheduler.get_jobs():
#         return render_template("my-form.html")
#     #If a job is in progress render an image
#     else if

def controller():
    print("job_ids"+str(len(q.job_ids)))
    if len(q.job_ids)==0:
        return render_template("my-form.html")
    else:
        return(send_file("images/styles/darksideofthemoon.jpeg",mimetype='image/jpg'))

def wait60s():
    time.sleep(60)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)