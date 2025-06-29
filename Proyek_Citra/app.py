from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
from io import BytesIO
import numpy as np

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

# Fungsi untuk membaca pesan dari Image object 
def decode_lsb_from_image(img):
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

# Fungsi lama tetap dipertahankan untuk decoding dari path
def decode_lsb(image_path):
    img = Image.open(image_path)
    return decode_lsb_from_image(img)

# Hitung MSE dan PSNR
def calculate_mse_psnr(original_path, stego_path):
    original = Image.open(original_path).convert('RGB')
    stego = Image.open(stego_path).convert('RGB')

    original_arr = np.array(original, dtype=np.float64)
    stego_arr = np.array(stego, dtype=np.float64)

    mse = np.mean((original_arr - stego_arr) ** 2)

    if mse == 0:
        psnr = float('inf')
    else:
        psnr = 10 * np.log10((255 ** 2) / mse)

    return mse, psnr

# Route untuk halaman utama (encode)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        message = request.form['message']

        if image_file and message:
            input_path = os.path.join('static/images', image_file.filename)
            output_path = os.path.join('static/uploads', f"encoded_{image_file.filename}")

            image_file.save(input_path)
            encode_lsb(input_path, message, output_path)

            return redirect(url_for('result', image_name=f"encoded_{image_file.filename}", original_name=image_file.filename))

    return render_template('index.html')

@app.route('/result/<image_name>')
def result(image_name):
    original_name = request.args.get('original_name')
    if not original_name:
        return "Original image not found.", 400

    original_path = os.path.join('static/images', original_name)
    stego_path = os.path.join('static/uploads', image_name)

    # Hitung nilai asli
    mse_raw, psnr_raw = calculate_mse_psnr(original_path, stego_path)

    return render_template(
        'result.html',
        image_name=image_name,
        mse_raw=mse_raw,
        psnr=round(psnr_raw, 2)
    )




# Route untuk halaman decode tanpa menyimpan file
@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            filename = image_file.filename
            temp_path = os.path.join('static/uploads', filename)
            os.makedirs('static/uploads', exist_ok=True)
            image_file.save(temp_path)

            img = Image.open(temp_path)
            message = decode_lsb_from_image(img)

            return render_template('decode_result.html', message=message, stego_image=f'uploads/{filename}')

    return render_template('decode.html')


# Route untuk decode gambar langsung setelah encoding
@app.route('/decode_direct', methods=['POST'])
def decode_direct():
    image_name = request.form['image_name']
    image_path = os.path.join('static/uploads', image_name)

    message = decode_lsb(image_path)
    return render_template('decode_result.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)


