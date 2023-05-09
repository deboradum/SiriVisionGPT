import cv2
from ultralytics import YOLO
import time
import torch

model = YOLO('yolov8n.pt')

class YoloHandler():
    def __init__(self, rec_dur, camera_id):
        self.rec_dur = rec_dur
        self.camera_id = camera_id

    def infer_video(self):
        objects = ['Apple', 'Beef', 'Banana']

        start = time.time()
        cv2.startWindowThread()
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        while True:
            # Capture frame-by-frame.
            succes, frame = cap.read()
            # Check is frame is read correctly.
            if not succes:
                print("Can't receive frame. Exiting ...")
                break
            # Predict with yolo.
            results = model.predict(frame, conf=0.5, device='mps' if torch.backends.mps.is_available() else 'cpu', vid_stride=True, verbose=False)
            # plot object boxes.
            annotated_frame = results[0].plot()

            # Display the resulting frame
            cv2.imshow('frame', annotated_frame)
            if cv2.waitKey(1) == ord('q') or time.time() - start > self.rec_dur:
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

        objects_s = ''
        for i in objects:
            objects_s +=  f"{i}, " 

        return objects_s
