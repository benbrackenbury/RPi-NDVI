import cv2
import numpy as np

original = cv2.imread('./assets/img/park.png')


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
    ndvi = (b.astype(float)) / bottom
    return ndvi


display(original, 'Original')
contrasted = contrast_stretch(original)
display(contrasted, 'Contrasted Original')
cv2.imwrite('./output/contrasted.png', contrasted)
ndvi = calc_ndvi(contrasted)
display(ndvi, 'NDVI')
cv2.imwrite('./output/ndvi.png', ndvi)
ndvi_contrasted = contrast_stretch(ndvi)
display(ndvi_contrasted, 'NDVI Contrasted')
cv2.imwrite('./output/ndvi_contrasted.png', ndvi_contrasted)

cv2.waitKey(0)
cv2.destroyAllWindows()