import base64
import time
import cv2
import numpy as np
import socketio
from makeup_service_client.media.makeup_applier import MakeupApplier

makeup = MakeupApplier()


def receive_segmentation(data):
    image_id = data['id']
    segmentation = data['segmentation']
    np_segmentation = np.array(segmentation)
    makeup.put_segmentation({'id': image_id, 'segmentation': np_segmentation})


class MakeupServiceClient:
    def __init__(self, server_address, server_port):
        self.__server_address = server_address
        self.__server_port = server_port

        self.__sio = socketio.Client()
        self.__sio.connect('http://{}:{}'.format(self.__server_address, self.__server_port),
                           namespaces=['/stream'])
        self.__sio.on('segmentation', receive_segmentation, namespace='/stream')

        time.sleep(1)

    def send_image(self, image_package):
        self.__sio.emit('image', {
                           'id': image_package['id'],
                           'image': self._convert_image_to_jpeg(image_package['image']),
                       },
                        namespace='/stream')

    def close(self):
        self.__sio.disconnect()


    def _convert_image_to_jpeg(self, image):
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        frame = base64.b64encode(frame)

        return frame


