import cv2
import os

# Path gambar input
image_path = r"C:\laragon\www\KEL8PCD\ilkom-23-citra-kelompok-8\contoh_citra\Indah_web\static\testing\gambar.jpg"

# Path folder output
output_folder = r"C:\laragon\www\KEL8PCD\ilkom-23-citra-kelompok-8\contoh_citra\Indah_web\static\testing"

# Cek apakah file ada
if not os.path.exists(image_path):
    print(f"❌ Error: File '{image_path}' tidak ditemukan!")
    exit()

# Membaca gambar
img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# Cek apakah gambar berhasil dibaca
if img is None:
    print("❌ Error: Gambar tidak dapat dibaca, cek format file!")
    exit()

print("✅ Gambar berhasil dibaca!")

# Menampilkan gambar asli
cv2.imshow("Gambar Asli", img)
cv2.waitKey(500)  # Tunggu sebentar sebelum lanjut
cv2.destroyAllWindows()

# Buat folder output jika belum ada
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 1️⃣ Konversi ke Grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_path = os.path.join(output_folder, "citra_digital.png")
cv2.imwrite(gray_path, gray_img)

# 2️⃣ Konversi ke Citra Biner
_, binary_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
binary_path = os.path.join(output_folder, "citra_biner.png")
cv2.imwrite(binary_path, binary_img)

# 3️⃣ Deteksi Tepi (Edge Detection)
edges = cv2.Canny(gray_img, 100, 200)
edges_path = os.path.join(output_folder, "citra_tepi.png")
cv2.imwrite(edges_path, edges)

# ✅ Menampilkan hasil
cv2.imshow("Grayscale", gray_img)
cv2.imshow("Citra Biner", binary_img)
cv2.imshow("Deteksi Tepi", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("✅ Semua hasil telah disimpan di:", output_folder)
