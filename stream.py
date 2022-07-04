import cv2
import numpy as np

from filters import Filters

class Application:
    videoStream = cv2.VideoCapture(0)
    original = contrasted = ndvi = ndvi_contrasted = color_mapped = 0

    def end(self):
        self.videoStream.release()
        cv2.destroyAllWindows()

    def getFrameAndApplyFilters(self):
        #get frame from stream
        ret, frame = self.videoStream.read()
        self.original = frame

        #filters
        self.contrasted = Filters.contrast_stretch(self.original)
        self.ndvi = Filters.calc_ndvi(self.contrasted)
        self.ndvi_contrasted = Filters.contrast_stretch(self.ndvi)
        self.color_mapped = Filters.color_map(self.ndvi_contrasted)

    def displayFrame(self):
        cv2.imshow('Original', self.original)
        # cv2.imshow('Contrasted', contrasted)
        # cv2.imshow('NDVI', ndvi)
        # cv2.imshow('NDVI Contrasted', ndvi_contrasted)
        cv2.imshow('Colour Mapped', self.color_mapped)

    def run(self):
        while(True):
            self.getFrameAndApplyFilters()
            self.displayFrame()

            #exit when q is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        

app = Application()
app.run() #runs until q key is pressed
app.end()