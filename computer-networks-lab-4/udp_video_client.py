import cv2
import socket
import numpy as np

# Client configuration
CLIENT_IP = '127.0.0.1'
CLIENT_PORT = 9999
CHUNK_SIZE = 4096

# Create UDP socket and bind
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((CLIENT_IP, CLIENT_PORT))

buffer = b''

while True:
    packet, _ = sock.recvfrom(CHUNK_SIZE + 1)
    marker = packet[0]
    data = packet[1:]
    buffer += data

    if marker == 1:
        # Decode and display frame
        frame = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('UDP Video Stream', frame)
        buffer = b''

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

sock.close()
cv2.destroyAllWindows()
