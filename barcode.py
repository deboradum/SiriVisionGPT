import cv2
import openfoodfacts


class BarcodeReader():
    def __init__(self, rec_dur):
        self.rec_dur = rec_dur

    # Records and tries to read barcode.
    def record(self):
        start = time.time()
        cv2.startWindowThread()
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            print("Cannot open camera")
            exit()

        barcode = None
        while True:
            # Capture frame-by-frame.
            succes, frame = cap.read()
            # Check is frame is read correctly.
            if not succes:
                print("Can't receive frame. Exiting ...")
                break

            # Finds barcode and reads


            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q') or time.time() - start > self.rec_dur:
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

        if barcode is None:
            return "No barcode found."

        food = self.get_food(barcode)

        return objects_s

    # Gets food item using barcode.
    def get_food(self, barcode):
        pass
