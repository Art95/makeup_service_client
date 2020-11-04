import base64
import time
import cv2
import socketio
import queue


class MakeupServiceClient:
    def __init__(self, server_address):
        self.__server_address = server_address
        self.__server_port = 5001

        self.__sio = socketio.Client()
        self.__sio.connect('http://{}:{}'.format(self.__server_address, self.__server_port), transports=['websocket'],
                           namespaces=['/images'])
        time.sleep(1)

        self.__response_que = queue.Queue()

    def send_image(self, image):
        self.__sio.emit('frame', {
                           'image': self._convert_image_to_jpeg(image),
                       })

    def close(self):
        self.__sio.disconnect()

    def _convert_image_to_jpeg(self, image):
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        frame = base64.b64encode(frame).decode('utf-8')

        return "data:image/jpeg;base64,{}".format(frame)


