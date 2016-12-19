import io
import socket
import struct
import cv2
import sys
import numpy
import sys
from PIL import Image

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')

#cascade file path
cascPath = sys.argv[1]

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

try:
    count = 0
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
        image = numpy.array(pil_image) 
        # Convert RGB to BGR 
        image = image[:, :, ::-1].copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        print("Found {0} faces!".format(len(faces)))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.destroyWindow("Faces found")
        #cv2.waitKey(-1)
        #cv2.imshow("Faces found", image)
        #cv2.waitKey(25)
        #cv2.imshow("Faces found", image)
        cv2.imshow("Faces found", image)
        cv2.waitKey(0)
        cv2.imwrite("test.png", image)

finally:
    connection.close()
    server_socket.close()
