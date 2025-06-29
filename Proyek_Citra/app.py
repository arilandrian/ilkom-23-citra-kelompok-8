# Proyek_Citra/app.py (Versi Final dengan 7 Fitur)

from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
# --- Import baru untuk Histogram ---
import matplotlib.pyplot as plt

app = Flask(__name__)

# --- Fitur #5: Kalkulasi Kapasitas ---
def calculate_capacity(img):
    width, height = img.size
    capacity_in_bits = width * height * 3
    capacity_in_bytes = capacity_in_bits // 8
    return capacity_in_bits, capacity_in_bytes

# --- Fitur #6: Kalkulasi SSIM ---
def calculate_ssim(original_path, stego_path):
    original_img = np.array(Image.open(original_path).convert('RGB'))
    stego_img = np.array(Image.open(stego_path).convert('RGB'))
    ssim_value, _ = ssim(original_img, stego_img, full=True, channel_axis=2, data_range=original_img.max() - original_img.min())
    return ssim_value

# --- FITUR MATEMATIKA BARU (#7): Membuat dan Menyimpan Histogram ---
def create_and_save_histograms(original_path, stego_path, output_folder):
    """
    Membuat, membandingkan, dan menyimpan histogram dari gambar asli dan stego.
    """
    original_img = Image.open(original_path).convert('RGB')
    stego_img = Image.open(stego_path).convert('RGB')
    
    # Menggunakan tema gelap agar serasi dengan template
    plt.style.use('dark_background')
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    colors = ('r', 'g', 'b')
    
    # --- Histogram untuk gambar asli ---
    axes[0].set_title('Histogram Gambar Asli')
    axes[0].set_xlabel('Intensitas')
    axes[0].set_ylabel('Frekuensi')
    # Menghitung dan menggambar histogram untuk setiap channel warna
    for i, color in enumerate(colors):
        # Mengambil data histogram dari channel yang sesuai
        hist = original_img.histogram()[i*256:(i+1)*256]
        axes[0].plot(hist, color=color)
    axes[0].set_xlim([0, 256])

    # --- Histogram untuk gambar stego ---
    axes[1].set_title('Histogram Gambar Stego')
    axes[1].set_xlabel('Intensitas')
    # Menghitung dan menggambar histogram untuk setiap channel warna
    for i, color in enumerate(colors):
        hist = stego_img.histogram()[i*256:(i+1)*256]
        axes[1].plot(hist, color=color)
    axes[1].set_xlim([0, 256])

    # Menyimpan gambar histogram ke file
    histogram_filename = f"hist_comparison_{os.path.basename(original_path)}"
    histogram_path = os.path.join(output_folder, histogram_filename)
    os.makedirs(output_folder, exist_ok=True)
    plt.savefig(histogram_path)
    plt.close() # Menutup plot agar tidak ditampilkan di server backend
    
    return histogram_filename

# Fitur #1: Encode LSB
def encode_lsb(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    
    max_capacity_bits, _ = calculate_capacity(img)
    message += "$t0p$"
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    
    if len(binary_message) > max_capacity_bits:
        raise ValueError(f"Pesan terlalu besar. Kapasitas maksimum: {max_capacity_bits // 8} bytes.")

    pixels = img.load()
    msg_index = 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if msg_index < len(binary_message):
                r = (r & ~1) | int(binary_message[msg_index]); msg_index += 1
            if msg_index < len(binary_message):
                g = (g & ~1) | int(binary_message[msg_index]); msg_index += 1
            if msg_index < len(binary_message):
                b = (b & ~1) | int(binary_message[msg_index]); msg_index += 1
            pixels[x, y] = (r, g, b)
            if msg_index >= len(binary_message): break
        if msg_index >= len(binary_message): break

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)

# Fitur #2: Decode LSB
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

def decode_lsb(image_path):
    img = Image.open(image_path)
    return decode_lsb_from_image(img)

# Fitur #3 & #4: Hitung MSE dan PSNR
def calculate_mse_psnr(original_path, stego_path):
    original_arr = np.array(Image.open(original_path).convert('RGB'), dtype=np.float64)
    stego_arr = np.array(Image.open(stego_path).convert('RGB'), dtype=np.float64)
    mse = np.mean((original_arr - stego_arr) ** 2)
    if mse == 0:
        return 0, float('inf')
    psnr = 10 * np.log10((255 ** 2) / mse)
    return mse, psnr

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files.get('image')
        message = request.form.get('message')
        if image_file and message:
            input_path = os.path.join('static/images', image_file.filename)
            output_path = os.path.join('static/uploads', f"encoded_{image_file.filename}")
            os.makedirs('static/images', exist_ok=True)
            image_file.save(input_path)
            try:
                encode_lsb(input_path, message, output_path)
            except ValueError as e:
                return render_template('index.html', error=str(e))
            return redirect(url_for('result', image_name=f"encoded_{image_file.filename}", original_name=image_file.filename))
    return render_template('index.html', error=None)

@app.route('/result/<image_name>')
def result(image_name):
    original_name = request.args.get('original_name')
    if not original_name:
        return "Original image not found.", 400

    original_path = os.path.join('static/images', original_name)
    stego_path = os.path.join('static/uploads', image_name)

    # Memanggil semua fungsi kalkulasi
    mse_raw, psnr_raw = calculate_mse_psnr(original_path, stego_path)
    original_image = Image.open(original_path)
    _, capacity_bytes = calculate_capacity(original_image)
    ssim_value = calculate_ssim(original_path, stego_path)
    # --- Memanggil fungsi kalkulasi Histogram ---
    histogram_file = create_and_save_histograms(original_path, stego_path, 'static/histograms')

    return render_template(
        'result.html',
        image_name=image_name,
        mse_raw=mse_raw,
        psnr=round(psnr_raw, 2),
        capacity_bytes=capacity_bytes,
        ssim=round(ssim_value, 4),
        # Mengirim nama file histogram ke template
        histogram_file=histogram_file
    )

@app.route('/decode', methods=['POST'])
def decode():
    image_file = request.files.get('image')
    if image_file:
        temp_path = os.path.join('static/uploads', image_file.filename)
        os.makedirs('static/uploads', exist_ok=True)
        image_file.save(temp_path)
        img = Image.open(temp_path)
        message = decode_lsb_from_image(img)
        return render_template('decode_result.html', message=message, stego_image=f'uploads/{image_file.filename}')
    return redirect(url_for('index'))

@app.route('/decode_direct', methods=['POST'])
def decode_direct():
    image_name = request.form.get('image_name')
    image_path = os.path.join('static/uploads', image_name)
    message = decode_lsb(image_path)
    return render_template('decode_result.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)