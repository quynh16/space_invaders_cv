import cv2


class Camera:
    def __init__(self, device=0, width=1000, height=600):
        self.width = width
        self.height = height
        self.camera = cv2.VideoCapture(device)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def read(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.flip(frame, 1)
            return cv2.resize(frame, (self.width, self.height))
        else:
            raise Exception("Failed to capture video.")

    def release(self):
        self.camera.release()

    def is_visible(self, window_name):
        return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1