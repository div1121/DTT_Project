from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'

best_model = tf.keras.models.load_model('static/fune_model.08-1.00.h5')
folders = ['freshapples', 'freshbanana', 'freshoranges', 'rottenapples', 'rottenbanana', 'rottenoranges']
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # print('upload_image filename: ' + filename)
        # print(type(filepath))
        test_image = image.load_img(filepath, target_size=(256,256))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = best_model.predict(test_image)
        p = np.argmax(result[0])
        prediction = folders[p]
        # prediction = "temp"
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename, prediction=prediction)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run(threaded=True)