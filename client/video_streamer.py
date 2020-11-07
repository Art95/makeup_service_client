import cv2


class VideoStreamer:
    def __init__(self, source, frame_size=None, flip=False):
        self.__video = cv2.VideoCapture(source)
        self.__frame_size = frame_size
        self.__flip = flip

    def __del__(self):
        self.__video.release()

    def get_frame(self):
        ret, frame = self.__video.read()

        resized_frame = None
        metadata = None

        if ret:
            if self.__flip:
                frame = cv2.flip(frame, 1)

            metadata = {'original_size': (frame.shape[1], frame.shape[0])}

            if self.__frame_size is not None:
                resized_frame = cv2.resize(frame, self.__frame_size)
            else:
                resized_frame = frame

        return ret, resized_frame, metadata
