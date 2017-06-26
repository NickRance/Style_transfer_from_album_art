from flask import Flask, request, redirect, render_template, send_file, url_for
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

def emptyDirectory(path):
    filesToRemove = [f for f in os.listdir(path)]
    for f in filesToRemove:
        os.remove(os.path.join(path,f))


def controller():
    #The default number of running jobs is 7 on heroku
    print("jobs"+str(len(q.jobs)))
    print("Initial Job Count: "+str(initialJobCount))
    if len(q.job_ids)==initialJobCount and len([name for name in os.listdir(os.getcwd()+'/images/output') if os.path.isfile(name)])==0: #If there are no extra jobs and the output directory is empty render the form
        #return("4 jobs in the q")
        return render_template("my-form.html")
    elif len(q.job_ids)> initialJobCount: #If there is currently a job running render the DJ image
        #return("More than 0 jobs in the q")
        return(send_file(os.getcwd()+"/"+"images/styles/DJ.jpg",mimetype='image/jpg'))
    elif len(q.job_ids)==initialJobCount and len([name for name in os.listdir(os.getcwd()+'/images/output') if os.path.isfile(name)])==0:#If there are no extra jobs running and there is a value in the output directory
        urls = [f for f in os.listdir("images/output/")]
        return render_template("show_images.html", urls=urls)


def wait60s():
    time.sleep(60)


@app.route('/')
def my_form():
    #schedule_controller()
    while(True):
        time.sleep(10)
        return(controller())

@app.route('/', methods=['POST'])
#Post requests add a job to the queue
def my_form_post():
    #return("Post call")
    #q.enqueue(wait60s)
    text = request.form['text']
    imageName = text.split("/")[-1]
    contentImagePath = os.getcwd()+"/images/input/"+imageName
    outputImagePath = os.getcwd()+"/images/output/"+imageName
     # print(file_path)
     #if not os.path.exists(outputImagePath):
    f = open(contentImagePath, 'wb')
    f.write(requests.get(text).content)
    f.close()
    print("File Written!")
        #style_transfer("images/profile.jpg")
    result = q.enqueue_call(style_transfer,kwargs={"sourceImagePath":contentImagePath,"outputPath":outputImagePath, "filterPath": os.getcwd()+"/images/styles/darksideofthemoon.jpeg"})
    return(redirect(url_for('my_form'))) #Change this
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



if __name__ == '__main__':
    emptyDirectory(os.getcwd()+'/images/output/')
    global initialJobCount
    initialJobCount = len(q.jobs)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)