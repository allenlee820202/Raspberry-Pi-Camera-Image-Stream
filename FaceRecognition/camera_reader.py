# -*- coding:utf-8 -*-
import cv2
import io
import socket
import struct
import sys
import numpy
from PIL import Image
from boss_train import Model
#from image_show import show_image


# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cascade_path = "./haarcascade_frontalface_default.xml"
    model = Model()
    model.load()
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        print image_len
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        #image_stream.save("test.jpg")
        image_stream.seek(0)
        pil_image = Image.open(image_stream).convert('RGB')

        #pil_image = PIL.Image.open('Image.jpg').convert('RGB') 
        frame= numpy.array(pil_image) 
        # Convert RGB to BGR 
        frame = frame[:, :, ::-1].copy()
        frame_gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        print frame.shape

        # カスケード分類器の特徴量を取得する
        cascade = cv2.CascadeClassifier(cascade_path)

        # 物体認識（顔認識）の実行
        facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))
        #facerect = cascade.detectMultiScale(frame_gray, scaleFactor=1.01, minNeighbors=3, minSize=(3, 3))
        if len(facerect) > 0:
            print('face detected')
            color = (255, 255, 255)  # 白
            for rect in facerect:
                # 検出した顔を囲む矩形の作成
                #cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), color, thickness=2)

                x, y = rect[0:2]
                width, height = rect[2:4]
                image = frame[y - 10: y + height, x: x + width]
                print image.shape

                result = model.predict(image)
                if result == 0:  # boss
                    print('Boss is approaching')
                    #show_image()
                else:
                    print('Not boss')

        #10msecキー入力待ち
        k = cv2.waitKey(100)
        #Escキーを押されたら終了
        if k == 27:
            break

    #キャプチャを終了
    cap.release()
    cv2.destroyAllWindows()
