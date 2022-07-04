import sys
import cv2
import numpy as np
from lib.fastiecm import fastiecm
from picamera import PiCamera
import picamera.array

def display(image, image_name):
    image = np.array(image, dtype=float)/float(255)
    shape = image.shape
    height = int(shape[0] / 3)
    width = int(shape[1] / 3)
    image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)

def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] - 0.01
    ndvi = (r.astype(float) - b) / bottom
    return ndvi

def main():
    # cam = PiCamera()
    # cam.rotation = 180
    # cam.resolution = (1920, 1080)
    # stream = picamera.array.PiRGBArray(cam)
    # cam.capture(stream, format='bgr', use_video_port=True)
    # original = stream.array
    input_image_path = './assets/img/park.png'
    original = cv2.imread(input_image_path)

    display(original, 'Original')
    contrasted = contrast_stretch(original)
    # display(contrasted, 'Contrasted Original')
    cv2.imwrite('./output/contrasted.png', contrasted)
    ndvi = calc_ndvi(contrasted)
    # display(ndvi, 'NDVI')
    cv2.imwrite('./output/ndvi.png', ndvi)
    ndvi_contrasted = contrast_stretch(ndvi)
    display(ndvi_contrasted, 'NDVI Contrasted')
    cv2.imwrite('./output/ndvi_contrasted.png', ndvi_contrasted)
    color_mapped_prep = ndvi_contrasted.astype(np.uint8)
    color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
    display(color_mapped_image, 'Color mapped')
    cv2.imwrite('./output/color_mapped_image.png', color_mapped_image)

    cv2.imwrite('./output/original.png', original)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()