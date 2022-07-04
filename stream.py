import cv2
import numpy as np

from filters import Filters

class Application:
    def run(self):
        #start video capture
        vid = cv2.VideoCapture(0)
        
        while(True):
            #get frame
            ret, frame = vid.read()
            #display frame
            cv2.imshow('Original', frame)

            #increase contrast
            contrasted = Filters.contrast_stretch(frame)
            # cv2.imshow('Contrasted', contrasted)

            #NDVI
            ndvi = Filters.calc_ndvi(contrasted)
            # cv2.imshow('NDVI', ndvi)

            #Contrasted NDVI
            ndvi_contrasted = Filters.contrast_stretch(ndvi)
            # cv2.imshow('NDVI Contrasted', ndvi_contrasted)

            #Colour map
            color_mapped = Filters.color_map(ndvi_contrasted)
            cv2.imshow('Colour Mapped', color_mapped)

            #exit when q is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        #stop capute and kill all windows
        vid.release()
        cv2.destroyAllWindows()

app = Application()
app.run()