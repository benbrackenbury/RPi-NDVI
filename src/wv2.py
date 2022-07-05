from flask import Flask, render_template, Response
import cv2
from filters import Filters

app = Flask('__name__')
camera = cv2.VideoCapture(-1)

def gen_frames(selected_filter):
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



@app.route('/')
def index():
    return render_template('feed.html')

@app.route('/video')
def video():
    return Response(gen_frames('original'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/contrasted')
def contrasted():
    return Response(gen_frames('contrasted'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/ndvi')
def ndvi():
    return Response(gen_frames('ndvi'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/ndvi_contrasted')
def ndvi_contrasted():
    return Response(gen_frames('ndvi_contrasted'), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/color_map')
def color_map():
    return Response(gen_frames('color_mapped'), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(port='3000', host='0.0.0.0', debug='true')