import numpy as np
import matplotlib.pyplot as plt

image_1 = np.array([
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1]
], dtype=np.uint8)
s

plt.imshow(image_1, cmap='gray', vmin=0, vmax=1)
plt.title("Angka '1' dalam Matriks 1-Bit")
plt.axis('off')  
plt.show()
