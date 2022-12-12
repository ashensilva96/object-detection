from flask import Flask, flash, request, redirect, url_for, render_template
import torch
import os, requests
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():

    file = request.files['file']
    filename = secure_filename(file.filename)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  #save uploaded image

    #code from here
    #https://github.com/ultralytics/yolov5
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s') #load yolov5s model
    model.classes = 2                                       #select only car classes

    img = cv2.imread(os.path.join('static/', filename), 1)  #read saved image 
    img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)          #saved image conveted BGR -> RGB (reason: https://note.nkmk.me/en/python-opencv-bgr-rgb-cvtcolor/)
    
    results = model(img_cvt)                                #feed converted image to the model
    results.render()                                        #render bounding box marked image
    results.save(save_dir = 'static/', exist_ok=True)       #save detected image to the directory
    
    #code from here
    #https://flask.palletsprojects.com/en/2.2.x/quickstart/
    detected_image = os.path.join(app.config['UPLOAD_FOLDER'], 'image0.jpg')
    return render_template('index.html', filename=detected_image)

@app.route('/<filename>', methods=['GET'])
def display_image(filename):
    return redirect(url_for('static/', filename=filename), code=301)    #redirect object detected image to the web page




