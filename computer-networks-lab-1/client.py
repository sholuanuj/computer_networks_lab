import socket

HOST = '127.0.0.1'
PORT = 5001
CLIENT_NAME = "Client of Bard (Testing Mode)"

def start_client():
    try:
        num_input = input("Enter any integer to send to the server: ")
        client_number = int(num_input)
    except ValueError:
        print("That's not a valid integer. Exiting.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            
            message = f"{CLIENT_NAME},{client_number}"
            client_socket.sendall(message.encode())
            if not 1 <= client_number <= 100:
                print("Sent an out-of-range number. The server should shut down.")
                return

            data = client_socket.recv(1024)
            server_name, server_num_str = data.decode().split(',')
            server_number = int(server_num_str)
            
            print("\n--- Results ---")
            print(f"Client Name: {CLIENT_NAME}")
            print(f"Server Name: {server_name}")
            print(f"Client Number: {client_number}")
            print(f"Server Number: {server_number}")
            
            total_sum = client_number + server_number
            print(f"Sum of Integers: {total_sum}")
            
        except ConnectionRefusedError:
            print("Connection failed. Is the server running?")
        except Exception as e:
            print(f"An error occurred: {e}")

    print("Client session finished.")

if __name__ == "__main__":
    start_client()
