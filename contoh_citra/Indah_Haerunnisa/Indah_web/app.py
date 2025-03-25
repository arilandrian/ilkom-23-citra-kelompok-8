from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import cv2
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PROCESSED_FOLDER'] = 'static/processed/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/proses_gambar', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Convert to grayscale
            img = cv2.imread(filepath)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Tambahkan thresholding (Hitam-Putih)
            _, bw_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)

            # Simpan hasil grayscale
            processed_path_gray = os.path.join(app.config['PROCESSED_FOLDER'], 'gray_' + file.filename)
            cv2.imwrite(processed_path_gray, gray_img)

            # Simpan hasil thresholding (Hitam-Putih)
            processed_path_bw = os.path.join(app.config['PROCESSED_FOLDER'], 'bw_' + file.filename)
            cv2.imwrite(processed_path_bw, bw_img)

            return render_template('bebasji.html', 
                                   original=file.filename, 
                                   processed_gray='gray_' + file.filename, 
                                   processed_bw='bw_' + file.filename)

    return render_template('bebasji.html', original=None, processed_gray=None, processed_bw=None)

if __name__ == '__main__':
    app.run(debug=True)
