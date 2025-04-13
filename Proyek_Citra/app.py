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
 
