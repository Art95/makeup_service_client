import cv2


def show_frame(np_arr):
    img_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.imshow('Makeup', img_np)
    cv2.waitKey(1)
