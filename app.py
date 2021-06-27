from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import urllib.request
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)
 
UPLOAD_FOLDER = os.path.join(os.getcwd(),"static/uploads")

best_model = tf.keras.models.load_model( os.path.join(os.getcwd(),"static/fune_model.08-1.00.h5"))
folders = ['Fresh Apple', 'Fresh Banana', 'Fresh Orange', 'Rotten Apple', 'Rotten Banana', 'Rotten Orange']
 
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
        test_image = image.load_img(filepath, target_size=(256,256))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = best_model.predict(test_image)
        p = np.argmax(result[0])
        prediction = folders[p]
        pro = max(result[0])
        pro = round(pro*100,2)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename, prediction=prediction,confidence=pro)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
 
if __name__ == "__main__":
    app.run(threaded=True)