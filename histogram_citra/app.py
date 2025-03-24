import cv2
import numpy as np
import matplotlib.pyplot as plt

# Membaca gambar dalam mode grayscale
image = cv2.imread('berwarna.png', cv2.IMREAD_GRAYSCALE)

# Menampilkan histogram grayscale
plt.figure(figsize=(10, 4))
plt.hist(image.ravel(), bins=256, range=[0,256], color='black')
plt.title('Histogram Grayscale')
plt.xlabel('Intensitas')
plt.ylabel('Frekuensi')
plt.show()

# Membaca gambar berwarna
image_color = cv2.imread('berwarna.png')

# Konversi dari BGR ke RGB
image_color = cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB)

# Menampilkan histogram untuk setiap kanal warna
colors = ('r', 'g', 'b')
plt.figure(figsize=(10, 4))
for i, color in enumerate(colors):
    hist = cv2.calcHist([image_color], [i], None, [256], [0,256])
    plt.plot(hist, color=color)
    plt.xlim([0,256])
plt.title('Histogram RGB')
plt.xlabel('Intensitas')
plt.ylabel('Frekuensi')
plt.show()
