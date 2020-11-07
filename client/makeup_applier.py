import cv2
import multiprocessing


class MakeupApplier(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MakeupApplier, cls).__new__(cls)

        return cls.instance

    def __init__(self):
        self.__queue = multiprocessing.Queue()

    def run(self):
        while True:
            if self.__queue.empty():
                continue

            image = self.__queue.get()
            image = self._apply_makeup(image)

            cv2.imshow('Makeup', image)

            cv2.waitKey(1)

    def put_image(self, np_arr):
        img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        self.__queue.put(img_np)

    def _apply_makeup(self, image):
        return image
