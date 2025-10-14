import cv2
import socket
import time

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9999
CHUNK_SIZE = 4096

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Open video file
cap = cv2.VideoCapture('Space_invader_turtorial.mp4')  # Replace with your video file path

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize and encode frame
    frame = cv2.resize(frame, (640, 480))
    encoded, buffer = cv2.imencode('.jpg', frame)
    data = buffer.tobytes()

    # Split into chunks
    for i in range(0, len(data), CHUNK_SIZE):
        chunk = data[i:i+CHUNK_SIZE]
        marker = b'\x01' if i + CHUNK_SIZE >= len(data) else b'\x00'
        sock.sendto(marker + chunk, (SERVER_IP, SERVER_PORT))

    time.sleep(1/30)  # Maintain ~30 FPS

cap.release()
sock.close()
