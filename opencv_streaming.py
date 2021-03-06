import os
import cv2
import time
import base64

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


class VideoCamera(object):
    def __init__(self, url):
        # capturing video
        self.url = url
        self.video = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

    def __del__(self):
        self.video.release()

    def get_frame(self):

        global ReferenceFrame

        ReferenceFrame = None

        frame_rate = 10
        prev = 0

        # while loop captures
        while True:

            time_elapsed = time.time() - prev

            # reads frames from a video
            grabbed, frames = self.video.read()
            frames = cv2.resize(frames, (800, 600))

            # if cannot grab a frame, this program ends here.
            if not grabbed:
                print("Empty frame")
                break

            if time_elapsed > 1.0 / frame_rate:
                prev = time.time()

                # Display frames in a window
                # cv2.imshow('video', frames)

                # Encode frame as jpeg
                # encode OpenCV raw frame to jpg and displaying it
                jpeg = cv2.imencode(".jpg", frames)[1].tobytes()

                # Encode frame in base64 representation and remove
                # utf-8 encoding
                frame = base64.b64encode(jpeg).decode("utf-8")

                return "data:image/jpeg;base64,{}".format(frame)

            # if cv2.waitKey(10) & 0xFF == ord("q"):
            #     print("Video detection halted.")
            #     break

            # else:
            #     print ("Video is completed.")
            #     break

    # cleanup the camera and close any open windows
    # cv2.destroyAllWindows()
