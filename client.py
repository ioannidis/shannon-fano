from classes.fano_shannon import FanoShannon
from classes.linear_code import LinearCode
from PIL import Image
import numpy as np
import socket
import json
import os

def main():
    print("\nCLIENT ================================================\n")

    while True:
        image_file = input("Enter image file name: ")

        if os.path.exists(image_file):
            break
        else:
            print("Invalid file name!")

    while True:
        try:
            n = int(input("Enter linear code n: "))

            if n < 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid number!")
            continue
        else:
            break

    while True:
        try:
            k = int(input("Enter linear code k: "))

            if k < 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid number!")
            continue
        else:
            break

    while True:
        try:
            error = int(input("Enter linear code error bits: "))

            if error < 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid number!")
            continue
        else:
            break

    image = Image.open(image_file)
    width = image.size[0]
    height = image.size[1]

    array_4d = np.array(image)
    array_1d = np.ravel(array_4d)
    count = dict(map(lambda x: (x, list(array_1d).count(x)), array_1d))

    print("Format: {}".format(image.format))
    print("Size: {}".format(image.size))
    print("Mode: {}".format(image.mode))
    print("RGB pixel array: {}".format(str(array_1d)))

    print()

    for c in sorted(count):
        prob = count[c] / len(array_1d)
        count[c] = count[c] / len(array_1d)
        print("{}\t=>\t{}".format(c, prob))

    count_sorted = {}

    for i in (sorted(count.items(), key=lambda x: x[1], reverse=True)):
        count_sorted[i[0]] = i[1]

    fn = FanoShannon()
    fn.compress(count_sorted)

    fano_shannon_result = ""
    results = fn.get_mappings()

    for i in count:
        fano_shannon_result += results[i]

    print("\nFano Shannon compression result: {}\n".format(fano_shannon_result))

    lc = LinearCode()
    json_data = lc.encode(width, height, fano_shannon_result, n, k, error)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('127.0.0.1', 1001)
    print("[INFO] Connecting to server with address: {}.\n".format(address))
    sock.connect(address)

    try:
        message = json.dumps(json_data).encode("utf-8")
        print("[INFO] Sending message: {}.\n".format(message))
        sock.sendall(message)

        data = sock.recv(1024)
        print("[INFO] Received data from server: {}.\n".format(data.decode("utf-8")))
    finally:
        print("[INFO] Closing socket.\n")
        sock.close()


if __name__ == "__main__":
    main()
