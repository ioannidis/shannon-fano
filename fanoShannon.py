import numpy as np
from PIL import Image
import base64
import json
from operator import itemgetter
Shannon_Fano_dict={}

def main():
    # https://github.com/DanonOfficial/Huffman-Shannon-Fano-Coding/blob/master/png.py
    # https://stackoverflow.com/questions/8863917/importerror-no-module-named-pil
    # https://stackoverflow.com/questions/25102461/python-rgb-matrix-of-an-image
    # https://stackoverflow.com/questions/13730468/from-nd-to-1d-arrays

    code_size   = 0     # To be filled
    noise       = 0     # To be filled

    # Load image from file
    image = Image.open("image.jpg")
    print("Format: {}, Size: {}, Mode: {}".format(image.format, image.size, image.mode))

    width = image.size[0]
    height = image.size[1]
    pixel_array = image.load()

    # Extract RGB values from all pixels
    array_4d = np.array(image)

    # Convert 4d array to 1d
    array_1d = np.ravel(array_4d)

    print("RGB array:\n" + str(array_1d))
    print()

    count = {}
    for c in array_1d:
        if c not in count:
            count[c] = 1
        else:
            count[c] += 1
    # PROBABILITIES
    for c in sorted(count):
        print(c, "=>", count[c] / len(array_1d))

    print("Shannon-Fano Coding: ")

    shannon_fanon_coding(count, "")
    for i in sorted(Shannon_Fano_dict):
        print(i, "=", Shannon_Fano_dict[i])
    code_mes = ""
    for i in array_1d:
        code_mes += Shannon_Fano_dict[i]
    print("Message length in code: ", len(code_mes), "\nMessage code: ", code_mes)
    linear_compression(width, height, code_mes)


def shannon_fanon_coding(seq, code):

    a = {}
    b = {}
    if len(seq) == 1:
        Shannon_Fano_dict[seq.popitem()[0]] = code
        return 0
    for i in sorted(seq.items(), key=itemgetter(1), reverse=True):
        if sum(a.values()) < sum(b.values()):
            a[i[0]] = seq[i[0]]
        else:
            b[i[0]] = seq[i[0]]
    shannon_fanon_coding(a, code + "0")
    shannon_fanon_coding(b, code + "1")


def linear_compression(width, height, rgb_code, n=10, k=8):
    
    rgb_bin_array =[]
    for i in range(len(rgb_code)):
        binary = int((str(rgb_code)[i:i+8]), 2)
        binary = bin(binary)[2:].zfill(k)
        rgb_bin_array.append([int(bit) for bit in list(binary)])
        i = i + 8

    rgb_bin_array = np.array(rgb_bin_array)

    # ==========================================================
    # Setup matrices I, P and G
    # ==========================================================

    I = np.eye(k, dtype=int)
    P = np.random.randint(low=0, high=2, size=(k, n-k), dtype=int)
    G = np.concatenate((I, P), axis=1)

    print("RGB bin array:\n" + str(rgb_bin_array))
    print()
    print("I:\n" + str(I))
    print()
    print("P:\n" + str(P))
    print()
    print("G:\n" + str(G))

    print()
    print()

    # ==========================================================
    # Setup array of encoded RGB binary values
    # ==========================================================

    c = []

    for bits in rgb_bin_array:
        encoded = np.mod(bits.dot(G), np.array([2])) # Apply mod 2 to limit values on 0-1
        c.append(encoded)

    c = np.array(c)
    print("c:\n" + str(c))

    # ==========================================================
    # Append all encoded bits into one string
    # ==========================================================

    raw_encoded = ""
    for bits in c:
        raw_encoded += "".join([ str(bit) for bit in bits ])

    print()
    print(raw_encoded)
    print(len(raw_encoded))

    # Base64 encoding

    base64_encoded = base64.b64encode(raw_encoded.encode())

    # ==========================================================
    # JSON data
    # ==========================================================

    data = {
        "data": base64_encoded.decode(),
        "error": 0,
        "width": width,
        "height": height,
        "n": n,
        "k": k
    }
    print(json.dumps(data))


if __name__ == "__main__":
    main()