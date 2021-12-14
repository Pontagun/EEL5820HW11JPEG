import numpy as np
import cv2
import math
from PIL import Image
import csv
import json

import zigzig as zz

test_matrix = [[-35, 0, -1, 0, 1, 0, 0, 0],
               [0, -2, 0, 0, 0, 0, 0, 0],
               [0, 4, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]

q_matrix = [[16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 58, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]]


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

    return output_img.real


if __name__ == '__main__':

    prev_dc = 0
    path = r'b32.jpg'
    img = cv2.imread(path, 0)
    dct_img = dct(img, img.shape[0], img.shape[1])
    img = dct_img
    q_matrix = np.array(q_matrix).astype(float)

    # Uncomment code below to compare with in-class example
    # prev_dc = -8
    # img = np.array(test_matrix)
    # q_matrix = 1

    jpg = ""
    for i in range(0, img.shape[0], 8):
        for j in range(0, img.shape[1], 8):
            img[i:i + 8, j:j + 8] = np.around(img[i:i + 8, j:j + 8] / q_matrix)
            sq = np.asarray(zz.zigzag(img[i:i + 8, j:j + 8]))
            sq = np.array(sq).astype(int)
            jpg_code, prev_dc = zz.code_gen(sq, prev_dc)
            # jpg.append(jpg_code)
            jpg = jpg + jpg_code

    print((jpg))

    # im = Image.fromarray(abs(img))
    # if im.mode != 'RGB':
    #     im = im.convert('RGB')
    # im.save("64x64dft.jpg")
