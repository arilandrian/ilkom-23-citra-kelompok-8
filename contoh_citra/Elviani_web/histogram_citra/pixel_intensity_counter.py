import numpy as np
import cv2

def hitung_histogram(image_path):
    # Membaca gambar dalam mode grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Inisialisasi histogram dengan 256 nilai (0-255 untuk grayscale)
    histogram = np.zeros(256, dtype=int)
    
    # Menghitung histogram secara manual
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel_value = image[i, j]
            histogram[pixel_value] += 1
    
    return histogram

# Contoh penggunaan
image_path = "c:/laragon/www/KEL8PCD/ilkom-23-citra-kelompok-8/contoh_citra/Indah_Haerunnisa/histogram_citra/new_sample.png"  # Ganti dengan path gambar Anda
histogram = hitung_histogram(image_path)

# Menampilkan hasil
for i, count in enumerate(histogram):
    if count > 0:
        print(f"Intensitas {i}: {count} piksel")
