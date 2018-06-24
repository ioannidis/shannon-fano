import socket
import sys

# https://pymotw.com/2/socket/tcp.html

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('127.0.0.1', 1001)
    print("Starting server with address: {}".format(address))
    sock.bind(address)
    sock.listen(1)
    #while True:
    connection, client_address = sock.accept()
    print("Accepted connection from {}".format(client_address))
    try:
        while True:
            data = connection.recv(16)
            print("Received: {}".format(data))
            if data:
                print("Sending data to client")
                connection.sendall(data)
            else:
                print("No more data to send")
                break
    finally:
        connection.close()


if __name__ == "__main__":
    main()
