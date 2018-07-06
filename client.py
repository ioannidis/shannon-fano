"""
    Theoria pliroforion kai kodikon
    Ioulios 2018

    == Developed using Python 3.6.5 by ==
    == p16036 - Ioannidis Panagiotis   ==
    == p16097 - Nikas Dionisis         ==
    == p16112 - PAravantis Athanasios  ==
"""
from classes.fano_shannon import FanoShannon
from classes.linear_code import LinearCode
from PIL import Image
import numpy as np
import socket
import json
import os


def main():
    print("\nCLIENT ================================================\n")

    # Get user input for image file, linear code n, k and error bits

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

    # Get image data and the array of pixels for the image

    image = Image.open(image_file)
    width = image.size[0]
    height = image.size[1]

    # Extract RGB values from all pixels
    array_4d = np.array(image)

    # Convert 4d array to 1d
    array_1d = np.ravel(array_4d)

    # The number of occurrences for each color in the RGB array
    count = dict(map(lambda x: (x, list(array_1d).count(x)), array_1d))

    print("Format: {}".format(image.format))
    print("Size: {}".format(image.size))
    print("Mode: {}".format(image.mode))
    print("RGB pixel array: {}".format(str(array_1d)))

    print()

    # The probabilities for each color in the RGB array
    for c in sorted(count):
        prob = count[c] / len(array_1d)
        count[c] = count[c] / len(array_1d)
        print("{}\t=>\t{}".format(c, prob))

    # Sort all probabilities for processing
    count_sorted = {}

    for i in (sorted(count.items(), key=lambda x: x[1], reverse=True)):
        count_sorted[i[0]] = i[1]

    # Fano shannon algorithm for compression
    fn = FanoShannon()
    fn.compress(count_sorted)



    # Construct the compressed fano shannon string from the mappings
    fano_shannon_result = ""
    results = fn.get_mappings()

    for i in count_sorted:
        fano_shannon_result += results[i]

    print()
    print("Fano-Shannon coding: ")
    print(results)

    print("\nFano Shannon compression result: {}\n".format(fano_shannon_result))

    # Linear code algorithm for encoding
    lc = LinearCode()

    # Get the final JSON string so we can send it to the server
    c, json_data = lc.encode(width, height, fano_shannon_result, n, k, error)

    # Connect with the local server, must be already running in a separate cmd
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ('127.0.0.1', 1001)
    print("[INFO] Connecting to server with address: {}.\n".format(address))
    sock.connect(address)

    try:
        # Encoding the JSON string and send it to the server
        message = json.dumps(json_data).encode("utf-8")
        print("[INFO] Sending message: {}.\n".format(message))
        sock.sendall(message)

        # Wait until the server responds
        data = sock.recv(1024)
        print("[INFO] Received data from server: {}.\n".format(data.decode("utf-8")))
    finally:
        print("[INFO] Closing socket.\n")
        sock.close()

    print("\nRESULT ================================================\n")
    initial_bytes = os.path.getsize(image_file)
    print("Initial file size: {} bytes\n".format(initial_bytes))

    entropy = fn.get_entropy(count.values())
    print("Entropy: {}\n".format(entropy))

    encoding_bytes = len(json_data["data"]) // 8
    print("File size after encoding: {} bytes\n".format(encoding_bytes))

    algorithms_diff = len(c) - len(fano_shannon_result)
    print("Difference between the two algorithms: {} bits (linear code - fano shannon)".format(algorithms_diff))


if __name__ == "__main__":
    main()
