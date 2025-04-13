from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
 
app = Flask(__name__)
 
# Fungsi untuk menyisipkan pesan (encode LSB)
def encode_lsb(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
 
    message += "$t0p$"
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    msg_index = 0
 
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
 
            if msg_index < len(binary_message):
                r = (r & ~1) | int(binary_message[msg_index])
                msg_index += 1
            if msg_index < len(binary_message):
                g = (g & ~1) | int(binary_message[msg_index])
                msg_index += 1
            if msg_index < len(binary_message):
                b = (b & ~1) | int(binary_message[msg_index])
                msg_index += 1
 
            pixels[x, y] = (r, g, b)
 
            if msg_index >= len(binary_message):
                break
        if msg_index >= len(binary_message):
            break
 
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
 
# Fungsi untuk membaca pesan (decode LSB)
def decode_lsb(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
 
    binary_data = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
 
    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    message = ''.join(chars)
    end_marker = message.find('$t0p$')
    if end_marker != -1:
        return message[:end_marker]
    return "❌ Tidak ditemukan pesan tersembunyi."
 
# Route untuk halaman utama (encode)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        message = request.form['message']
 
        if image_file and message:
            input_path = os.path.join('static/images', image_file.filename)
            output_path = os.path.join('static/images', f"encoded_{image_file.filename}")
 
            image_file.save(input_path)
            encode_lsb(input_path, message, output_path)
 
            return redirect(url_for('result', image_name=f"encoded_{image_file.filename}"))
 
    return render_template('index.html')
 
# Route untuk halaman hasil encoding
@app.route('/result/<image_name>')
def result(image_name):
    return render_template('result.html', image_name=image_name)
 
# Route untuk halaman decode
@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            input_path = os.path.join('static/images', image_file.filename)
            image_file.save(input_path)
 
            # Decode pesan dari gambar
            message = decode_lsb(input_path)
            return render_template('decode_result.html', message=message)
 
    return render_template('decode.html')
 
if __name__ == "__main__":
    app.run(debug=True)