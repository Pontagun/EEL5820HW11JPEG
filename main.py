import numpy as np
import cv2
import math
from PIL import Image
import csv
import json

q_matrix = [[16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
            ]


def dct(input_img, rows, cols):
    output_img = np.zeros((rows, cols), complex)
    for u in range(0, rows):  # Moving along rows
        for v in range(0, cols):  # Moving along cols
            for x in range(0, rows):  # Evaluation loop
                for y in range(0, cols):  # Evaluation loop
                    cosx = math.cos(((2 * x + 1) * u * math.pi) / (2 * rows))
                    cosy = math.cos(((2 * y + 1) * v * math.pi) / (2 * rows))
                    output_img[u][v] += input_img[x][y] * cosx * cosy

            if u == v == 0:
                output_img[u][v] = output_img[u][v] / rows
            else:
                output_img[u][v] = (output_img[u][v] * 2) / rows
    return output_img


def json_reader(path):
    f = open(path)
    data = json.load(f)
    f.close()

    return data


if __name__ == '__main__':
    path = r'b16.jpg'

    ac_code = json_reader('AC_Code.json')
    dc_code = json_reader('DC_Code.json')
    jpg_coef = json_reader('JPEG_Coef.json')

    img = cv2.imread(path, 0)
    q_matrix = np.array(q_matrix).astype(float)

    dct_img = dct(img, img.shape[0], img.shape[1])

    im = Image.fromarray(abs(dct_img))

    if im.mode != 'RGB':
        im = im.convert('RGB')
    im.save("64x64dft.jpg")
