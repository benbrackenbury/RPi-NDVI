import threading
import cv2 as cv
from flask import Flask, render_template, Response
from filters import Filters
from lib.FreshestFrame import FreshestFrame

def callback(img):
    return

def gen_frames(cap, filter):
    fresh = FreshestFrame(cap)
    fresh.callback = callback

    while True:
        img = fresh.read()
        if img is None:
            break;

        contrasted = Filters.contrast_stretch(img)
        ndvi = Filters.calc_ndvi(contrasted)
        contrated_ndvi = Filters.calc_ndvi(ndvi)
        color_mapped = Filters.color_map(contrated_ndvi)

        if filter == 'original':
            imgToShow = img
        elif filter == 'contrasted':
            imgToShow = contrasted
        elif filter == 'contrasted_ndvi':
            imgToShow = contrasted_ndvi
        elif filter = 'color_mapped':
            imgToShow = color_mapped

        ret, buffer = cv.imencode('.jpg', imgToShow)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def main():

    app = Flask('__name__')

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS, 20)

    @app.route('/')
    def index():
        return render_template('feed.html')

    @app.route('/video')
    def video():
        return Response(gen_frames(cap, 'original'), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/video_contrasted')
    def video_contrasted():
        return Response(gen_frames(cap, 'contrasted'), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/video_ndvi_contrasted')
    def video_ndvi_contrasted():
        return Response(gen_frames(cap, 'ndvi_contrasted'), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/video_color_map')
    def video_color_map():
        return Response(gen_frames(cap, 'color_mapped'), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port='3000', debug=True, use_reloader=False)).start()

if (__name__ == '__main__'):
    main()