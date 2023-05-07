from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')


def infer_video():
    cap = cv2.VideoCapture(1)
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
        results = model.predict(frame, conf=0.6, device='mps', vid_stride=True)
        print(len(results))
        # plot object boxes.
        annotated_frame = results[0].plot()

        # Display the resulting frame
        cv2.imshow('frame', annotated_frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

infer_video()
