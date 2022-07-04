import cv2
import numpy as np
from lib.fastiecm import fastiecm

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
    #start video capture
    vid = cv2.VideoCapture(0)
    
    while(True):
        #get frame
        ret, frame = vid.read()
        #display frame
        cv2.imshow('Original', frame)

        #increase contrast
        contrasted = contrast_stretch(frame)
        # cv2.imshow('Contrasted', contrasted)

        #NDVI
        ndvi = calc_ndvi(contrasted)
        # cv2.imshow('NDVI', ndvi)

        #Contrasted NDVI
        ndvi_contrasted = contrast_stretch(ndvi)
        # cv2.imshow('NDVI Contrasted', ndvi_contrasted)

        #Colour map
        color_mapped_prep = ndvi_contrasted.astype(np.uint8)
        color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
        cv2.imshow('Colour Mapped', color_mapped_image)

        #exit when q is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    #stop capute and kill all windows
    vid.release()
    cv2.destroyAllWindows()

main()