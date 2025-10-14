# ftp_client_server.py
import os
import threading
import time
from ftplib import FTP
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler


def start_ftp_server():
    """Start a local FTP server in a separate thread."""
    authorizer = DummyAuthorizer()
    # Allow user 'user' with password '12345' full read/write in current dir
    authorizer.add_user("user", "12345", os.getcwd(), perm="elradfmwMT")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 2121), handler)
    server.serve_forever()


def ftp_client():
    """Connect to the local FTP server, upload, download, and verify."""
    ftp = FTP()
    ftp.connect("127.0.0.1", 2121)
    ftp.login(user="user", passwd="12345")

    print("Connected to FTP server")

    # Upload a file
    with open("upload_test.txt", "w") as f:
        f.write("This is a test file for FTP upload.")
    with open("upload_test.txt", "rb") as f:
        ftp.storbinary("STOR upload_test.txt", f)
    print("\nFile uploaded successfully!")

    # List directory
    print("\nDirectory listing after upload:")
    ftp.retrlines("LIST")

    # Download the same file
    with open("download_test.txt", "wb") as f:
        ftp.retrbinary("RETR upload_test.txt", f.write)
    print("File downloaded successfully!")

    # Verify contents
    with open("download_test.txt", "r") as f:
        print("\nDownloaded file contents:", f.read())

    ftp.quit()


def main():
    # Start FTP server in a background thread
    server_thread = threading.Thread(target=start_ftp_server, daemon=True)
    server_thread.start()

    # Give server a moment to start
    time.sleep(1)

    # Run client
    ftp_client()


if __name__ == "__main__":
    main()
