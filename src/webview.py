import threading
import cv2 as cv
from flask import Flask, render_template, Response
from filters import Filters
from lib.FreshestFrame import FreshestFrame

def callback(img):
    return

def gen_frames(cap):
    fresh = FreshestFrame(cap)
    fresh.callback = callback

    while True:
        img = fresh.read()
        if img is None:
            break;
        ret, buffer = cv.imencode('.jpg', img)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def gen_frames_contrasted(cap):
    fresh = FreshestFrame(cap)
    fresh.callback = callback

    while True:
        img = fresh.read()
        if img is None:
            break;
        img = Filters.contrast_stretch(img)
        ret, buffer = cv.imencode('.jpg', img)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def gen_frames_ndvi_contrasted(cap):
    fresh = FreshestFrame(cap)
    fresh.callback = callback

    while True:
        img = fresh.read()
        if img is None:
            break;
        img = Filters.contrast_stretch(Filters.calc_ndvi(Filters.contrast_stretch(img)))
        ret, buffer = cv.imencode('.jpg', img)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def gen_frames_color_map(cap):
    fresh = FreshestFrame(cap)
    fresh.callback = callback

    while True:
        img = fresh.read()
        if img is None:
            break;
        img = Filters.color_map(Filters.contrast_stretch(Filters.calc_ndvi(Filters.contrast_stretch(img))))
        ret, buffer = cv.imencode('.jpg', img)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def main():

    app = Flask('__name__')

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FPS, 30)

    @app.route('/')
    def index():
        return render_template('feed.html')

    @app.route('/video')
    def video():
        return Response(gen_frames(cap), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/video_contrasted')
    def video_contrasted():
        return Response(gen_frames_contrasted(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/video_ndvi_contrasted')
    def video_ndvi_contrasted():
        return Response(gen_frames_ndvi_contrasted(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/video_color_map')
    def video_color_map():
        return Response(gen_frames_color_map(cap), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port='3000', debug=True, use_reloader=False)).start()

if (__name__ == '__main__'):
    main()