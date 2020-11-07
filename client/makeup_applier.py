import cv2
import multiprocessing
import threading
from client.image_transformation import change_segment_color, HeadPart


class ThreadSafeSingleton(type):
    _instances = {}
    _singleton_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._singleton_lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(ThreadSafeSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MakeupApplier(metaclass=ThreadSafeSingleton):
    def __init__(self):
        self.__image_queue = multiprocessing.Queue()
        self.__segmentation_queue = multiprocessing.Queue()

        self.__colors = [[0, 255, 0], [255, 0, 0], [0, 0, 255]]
        self.__head_parts = [HeadPart.hair, HeadPart.upper_lip, HeadPart.lower_lip]

    def run(self):
        while True:
            if self.__image_queue.empty() or self.__segmentation_queue.empty():
                continue

            image = self.__image_queue.get()
            segmentation = self.__segmentation_queue.get()

            transformed_image = self._apply_makeup(image, segmentation)

            cv2.imshow('Makeup', transformed_image)

            cv2.waitKey(1)

    def put_image(self, image):
        self.__image_queue.put(image)

    def put_segmentation(self, segmentation):
        self.__segmentation_queue.put(segmentation)

    def _apply_makeup(self, image, segmentation):
        for i, head_part in enumerate(self.__head_parts):
            image = change_segment_color(image, segmentation, head_part, self.__colors[i])

        return image
