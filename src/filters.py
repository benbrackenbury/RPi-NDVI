import cv2
import numpy as np
from lib.fastiecm import fastiecm

class Filters:
    @staticmethod
    def contrast_stretch(im):
        in_min = np.percentile(im, 5)
        in_max = np.percentile(im, 95)

        out_min = 0.0
        out_max = 255.0

        out = im - in_min
        out *= ((out_min - out_max) / (in_min - in_max))
        out += in_min

        return out

    @staticmethod
    def calc_ndvi(image):
        b, g, r = cv2.split(image)
        bottom = (r.astype(float) + b.astype(float))
        bottom[bottom==0] - 0.01
        ndvi = (r.astype(float) - b) / bottom
        return ndvi

    @staticmethod
    def color_map(image):
        image_prep = image.astype(np.uint8)
        result = cv2.applyColorMap(image_prep, fastiecm)
        return result