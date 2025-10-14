import socket
import threading

HOST = '127.0.0.1'
PORT = 5001
SERVER_NAME = "Server of Gemini"
SERVER_NUMBER = 42

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        data = conn.recv(1024)
        if not data:
            return

        client_name, client_num_str = data.decode().split(',')
        client_number = int(client_num_str)

        print(f"Client Name: {client_name}")
        print(f"Server Name: {SERVER_NAME}")

        if not 1 <= client_number <= 100:
            print("Client number out of range. Server is shutting down.")
            conn.close()
            global running
            running = False
            return

        print(f"Client Number: {client_number}")
        print(f"Server Number: {SERVER_NUMBER}")
        
        total_sum = client_number + SERVER_NUMBER
        print(f"Sum: {total_sum}")

        response = f"{SERVER_NAME},{SERVER_NUMBER}"
        conn.sendall(response.encode())
    print(f"Connection with {addr} closed.")

def start_server():
    global running
    running = True
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        server_socket.settimeout(1) 
        print(f"Server listening on {HOST}:{PORT}")

        while running:
            try:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
            except socket.timeout:
                continue

    print("Server has shut down.")

if __name__ == "__main__":
    start_server()