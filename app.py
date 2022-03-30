from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread
from opencv_streaming import VideoCamera

RTSP_STREAM_URL = "rtsp://login:@192.168.1.10:554/stream=0.sdp"


app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")
thread = Thread()


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect", namespace="/web")
def connect_web():
    emit("video feed", {"data": "Starting stream..."})


@socketio.on("disconnect", namespace="/web")
def disconnect_web():
    print("[INFO] Web client disconnected: {}".format(request.sid))


def gen(opencv_streaming):
    while True:
        frame = opencv_streaming.get_frame()
        emit("stream", {"image": frame}, namespace="/web")


@socketio.on("video feed", namespace="/web")
def video_feed():
    # need visibility of the global thread object
    global thread
    video_url = RTSP_STREAM_URL

    print("Client connected: {}".format(video_url))
    # Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = gen(VideoCamera(video_url))
        thread.start()


if __name__ == "__main__":
    socketio.run(app, debug=True)
