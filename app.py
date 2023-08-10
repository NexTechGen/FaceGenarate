from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)


def generate_frames():
  while True:

    ## read the camre frame
    bolval, frame = camera.read()
    if not bolval:
      break
    else:
      ret, buffer = cv2.imencode('.jpg', frame)
      frame = buffer.tobytes()

    # When to use yield instead of return in Python?
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/")
def hello_jovin():
  return render_template("home.html")


@app.route("/video")
def video():
  return Response(generate_frames(),
                  mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
