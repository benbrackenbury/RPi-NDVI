from flask import Flask, render_template, Response
import cv2
from filters import Filters

app = Flask('__name__')

def gen_frames():
    camera = cv2.VideoCapture(-1)
    while True:
        success, frame = camera.read()
        if success == False:
            camera.release()
            print("Please refresh page")
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

            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + color_mapped_buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('feed.html')

@app.route('/original')
def original():
    return render_template('original.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(port='3000', host='0.0.0.0', debug='true')