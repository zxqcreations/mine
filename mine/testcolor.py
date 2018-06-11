import numpy as np
import cv2
import threading

color = np.zeros((256*16, 256*16, 3))

for r in range(0,256):
    for g in range(0,256):
        for b in range(0,256):
            r_col = r%16
            r_row = int(r/16)
            color[r_col*256+g, r_row*256+b]=(r, g, b)
            

cv2.imwrite('C:\\workspace\\pygame\\mine\\color.bmp', color)
