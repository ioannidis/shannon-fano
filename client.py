import socket
import sys

# https://pymotw.com/2/socket/tcp.html

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('127.0.0.1', 1001)
    print("Connecting to server with address: {}".format(address))
    sock.connect(address)

    try:
        message = b"The quick brown fox jumps over the lazy dog"
        print("Sending message: {}".format(message))
        sock.sendall(message)

        received = 0
        expected = len(message)

        while received < expected:
            data = sock.recv(16)
            received += len(data)
            print("Received: {}".format(data))
    finally:
        print("Closing socket")
        sock.close()


if __name__ == "__main__":
    main()
