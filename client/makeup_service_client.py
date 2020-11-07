import base64
import time
import cv2
import socketio
import numpy as np
from client.makeup_applier import MakeupApplier

makeup = MakeupApplier()


def receive_segmentation(data):
    decoded = base64.b64decode(data['segmentation'])
    np_arr = np.frombuffer(decoded, np.uint8)
    makeup.put_image(np_arr)


class MakeupServiceClient:
    def __init__(self, server_address, server_port):
        self.__server_address = server_address
        self.__server_port = server_port

        self.__sio = socketio.Client()
        self.__sio.connect('http://{}:{}'.format(self.__server_address, self.__server_port),
                           namespaces=['/stream'])
        self.__sio.on('segmentation', receive_segmentation, namespace='/stream')

        time.sleep(1)

    def send_image(self, image):
        self.__sio.emit('image', {
                           'hair_color': [0, 255, 0],
                           'upper_lip_color': [0, 0, 255],
                           'lower_lip_color': [255, 0, 0],
                           'image': self._convert_image_to_jpeg(image),
                       },
                        namespace='/stream')

    def close(self):
        self.__sio.disconnect()


    def _convert_image_to_jpeg(self, image):
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        frame = base64.b64encode(frame)

        return frame


