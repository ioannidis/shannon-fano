"""
    Theoria pliroforion kai kodikon
    Ioulios 2018

    == Developed using Python 3.6.5 by ==
    == p16036 - Ioannidis Panagiotis   ==
    == p16097 - Nikas Dionisis         ==
    == p16112 - Paravantis Athanasios  ==
"""
from classes.linear_code import LinearCode
import socket
import json


def main():
    print("\nSERVER ================================================\n")

    # Start a local server and wait for one connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('127.0.0.1', 1001)
    print("[INFO] Starting server with address: {}.".format(address))
    sock.bind(address)
    sock.listen(1)

    connection, client_address = sock.accept()
    print("[INFO] Accepted connection from {}.\n".format(client_address))

    try:
        # Wait for the JSON data to be received
        data = connection.recv(8192)
        print("[INFO] Received data from client: {}.\n".format(data.decode("utf-8")))

        # Decode using the linear code algorithm
        json_data = json.loads(data.decode("utf-8"))
        lc = LinearCode()
        res = lc.decode(json_data)

        # Send back the result, should be the same one from fano shannon after decoding
        print("[INFO] Sending data to client: {}.\n".format(res))
        connection.sendall(res.encode("utf-8"))

    finally:
        print("[INFO] Closing connection and socket.\n")
        connection.close()
        sock.close()


if __name__ == "__main__":
    main()
