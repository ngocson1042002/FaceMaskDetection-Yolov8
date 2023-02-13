from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request, render_template
from random import random

import cv2
import os
import detect

# Init flask server
app = Flask(__name__)

# Apply flask cors
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'static'


@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*')

def detect_mask():
    if request.method == 'POST':
    # save image from client
    # app.config['UPLOAD_FOLDER'] is a variable in the Flask application configuration that specifies the directory where uploaded files will be saved. The value of this variable should be set to the desired file path. For example: app.config['UPLOAD_FOLDER'] = '/path/to/upload/folder'
        img = request.files.get('file')
        print(img)
        if img:
            path_save = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
            print("Image saved on", path_save)
            img.save(path_save)

            # read img
            num, frame = detect.write_result(path_save)

            if num > 0:
                cv2.imwrite(path_save, frame)

                return render_template('index.html', user=img.filename, rand = str(random()), msg="Upload the image successfully!")
            else:
                return render_template('index.html', msg='The system does not detect anyone in the image!!')
        else:
            return render_template('index.html', msg='Please choose a file to upload')
    else:
        return render_template('index.html')

# Start backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)