
import cv2
# mengubah kontras pada setiap pixel. 
# kontras berarti pixel yang gelap bertambah gelap, sedang pixel terang menjadi lebih terang

# Histogram Equalization
image = cv2.imread('c:/laragon/www/KEL8PCD/ilkom-23-citra-kelompok-8/contoh_citra/Indah_Haerunnisa/histogram_citra/sample.png', cv2.IMREAD_GRAYSCALE)

equalized_image = cv2.equalizeHist(image)

# Tampilkan hasil
cv2.imshow("Original", image)
cv2.imshow("Equalized", equalized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()