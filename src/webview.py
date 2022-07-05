from flask import Flask, render_template, request, Response, redirect, url_for
import cv2
from filters import Filters

selected_filter = "original"

def gen_frames():
    camera = cv2.VideoCapture(-1)
    while True:
        success, frame = camera.read()
        if success == False:
            break
        else:
            original = frame
            contrasted = Filters.contrast_stretch(original)
            ndvi = Filters.calc_ndvi(contrasted)
            ndvi_contrasted = Filters.contrast_stretch(ndvi)
            color_mapped = Filters.color_map(ndvi_contrasted)

            _, original_buffer = cv2.imencode('.jpg', original)
            _, contrasted_buffer = cv2.imencode('.jpg', contrasted)
            _, ndvi_buffer = cv2.imencode('.jpg', ndvi)
            _, ndvi_contrasted_buffer = cv2.imencode('.jpg', ndvi_contrasted)
            _, color_mapped_buffer = cv2.imencode('.jpg', color_mapped)

            if selected_filter == 'original':
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + original_buffer.tobytes() + b'\r\n')
            elif selected_filter == 'contrasted':
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + contrasted_buffer.tobytes() + b'\r\n')
            elif selected_filter == 'ndvi':
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + ndvi_buffer.tobytes() + b'\r\n')
            elif selected_filter == 'ndvi_contrasted':
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + ndvi_contrasted_buffer.tobytes() + b'\r\n')
            elif selected_filter == 'color_mapped':
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + color_mapped_buffer.tobytes() + b'\r\n')
            else:
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + original_buffer.tobytes() + b'\r\n')

                

app = Flask('__name__')

@app.route('/')
def index():
    return render_template('index.html', selected_filter=selected_filter)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


app.run(port='3000', host='0.0.0.0', debug='true')