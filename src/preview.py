import cv2
import numpy as numpy
from filters import Filters
import sys

class Application:
    videoStream = cv2.VideoCapture(0)
    original = contrasted = ndvi = ndvi_contrasted = color_mapped = 0

    def __init__(self):
        if len(sys.argv) == 2 and sys.argv[1] == "--all":
            self.show_all = True
        else:
            self.show_all = False

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
        if self.show_all:
            cv2.imshow('Contrasted', self.contrasted)
            cv2.imshow('NDVI', self.ndvi)
            cv2.imshow('NDVI Contrasted', self.ndvi_contrasted)
        cv2.imshow('Colour Mapped', self.color_mapped)

    def run(self):
        # run until q key is pressed
        while(cv2.waitKey(1) & 0xFF != ord('q')):
            self.getFrameAndApplyFilters()
            self.displayFrame()

        

preview = Application()
preview.run()
preview.end()