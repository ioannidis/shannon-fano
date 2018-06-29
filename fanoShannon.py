import numpy as np
from PIL import Image
import base64
import json
from operator import itemgetter
from collections import OrderedDict

fano_shannon_result = {}

def main():
    # https://github.com/DanonOfficial/Huffman-Shannon-Fano-Coding/blob/master/png.py
    # https://stackoverflow.com/questions/8863917/importerror-no-module-named-pil
    # https://stackoverflow.com/questions/25102461/python-rgb-matrix-of-an-image
    # https://stackoverflow.com/questions/13730468/from-nd-to-1d-arrays

    code_size   = 0     # To be filled
    noise       = 0     # To be filled

    # Load image from file
    image = Image.open("3X3.jpg")
    print("Format: {}, Size: {}, Mode: {}".format(image.format, image.size, image.mode))
    print()
    
    width = image.size[0]
    height = image.size[1]
    pixel_array = image.load()

    # Extract RGB values from all pixels
    array_4d = np.array(image)

    # Convert 4d array to 1d
    array_1d = np.ravel(array_4d)

    # ==========================================================
    # The number of occurrences for each color in the RGB array
    # ==========================================================

    count = dict(map(lambda x: (x, list(array_1d).count(x)), array_1d))

    # ==========================================================
    # Print the probabilities for each color in the RGB array
    # ==========================================================

    for c in sorted(count):
        prob = count[c] / len(array_1d)
        count[c] = count[c] / len(array_1d)
        print("{}\t=>\t{}".format(c, prob))

    # print((sorted(count.items(), key= lambda x: x[1], reverse=True)))
    count_sorted = {}
    # TODO: to be removed, only for testing ============================
    dummy_img = [173, 172, 85, 173, 88, 88, 100, 86, 92, 160]
    ex1_book = {173: 0.5, 88: 0.2, 86: 0.1, 100: 0.1, 92: 0.1}
    ex2_book = {173: 0.35, 88: 0.15, 86: 0.15, 100: 0.13, 92: 0.12, 160: 0.06, 85: 0.03, 172: 0.01}
    # ==================================================================

    for i in (sorted(count.items(), key= lambda x: x[1], reverse=True)):
        count_sorted[i[0]] = i[1]

    print()

    # TODO: to br removed --- prints sorted dict
    print(count_sorted)

    print()
    print("Fano-Shanno Coding: ")
    fano_shannon(ex2_book)

    # for i in sorted(fano_shannon_result):
    #     print(i, "=", fano_shannon_result[i])
    print(fano_shannon_result)
    print()

    code_mes = ""

    for i in dummy_img:
        code_mes += fano_shannon_result[i]

    print("Message length in code:", len(code_mes))
    print()
    print("Message code:", code_mes)
    print()
    print("RGB array:\n" + str(dummy_img))
    print()

    linear_compression(width, height, code_mes)


def fano_shannon(seq, code = ""):
    group_a = {}
    group_b = {}

    if len(seq) == 1:
        fano_shannon_result[seq.popitem()[0]] = code
        return 0

    # Sum the values of the dict
    sum_values = sum(seq.values())

    # Find the half of the sum
    half = sum_values/2

    sum_half = 0
    for i in seq:
        # Sum the values of the dict until the sum_half will be
        # grater than the half and append it in dict group_a
        if sum_half < half:
            sum_half += seq[i]
            group_a[i] = seq[i]
        else:
            # else append it in dict group_b
            group_b[i] = seq[i]

    # Execute recursively the method for the group_a and group_b
    fano_shannon(group_a, code + "0")
    fano_shannon(group_b, code + "1")


def linear_compression(width, height, rgb_code, n=6, k=3):
    # ==========================================================
    # Separate the RGB code into groups of size k
    # ==========================================================

    code_groups = []
    code_groups_raw = []

    for i in range(0, len(rgb_code), k):
        # If the group size is less than k bits, fill with extra zeros
        padded_group = rgb_code[i:i+k].zfill(k)
        code_groups.append([ int(c) for c in padded_group ])
        code_groups_raw.append(padded_group)

    # Matrix with all binary digits of a group in individual positions
    code_groups = np.array(code_groups)
    code_groups_raw = np.array(code_groups_raw)

    print("Code Groups:")
    print(code_groups)
    print()
    print()
    print("Code Groups Raw:")
    print(code_groups_raw)
    print()
    print()

    # ==========================================================
    # Setup matrices I, P, G and D
    # ==========================================================

    I = np.eye(k, dtype=int)
    P = np.random.randint(low=0, high=2, size=(k, n-k), dtype=int)
    G = np.concatenate((I, P), axis=1)

    # D is the binary numbers from 0 to 2^k
    D = []
    for i in range(2**k):
        binaries = np.binary_repr(i, width=k)
        D.append([ int(c) for c in binaries ])

    D = np.array(D)

    print("D:\n" + str(D))
    print()
    print()
    print("I:\n" + str(I))
    print()
    print()
    print("P:\n" + str(P))
    print()
    print()
    print("G:\n" + str(G))
    print()
    print()

    # ==========================================================
    # Create a dictionary that maps each group with a code
    # ==========================================================

    # Get encoded values with D*G and then mod 2 on all items
    all_codes = np.mod(D.dot(G), np.array([2]))

    print("Kwdikes Lekseis:")
    print(all_codes)
    print()
    print()

    # Dictionary with all possible groups and their code
    codes_dict = {}

    for i in range(2**k):
        codes_dict["".join(str(digit) for digit in D[i])] = "".join(str(digit) for digit in all_codes[i])

    print("Pinakas D*G:")
    print(codes_dict)
    print()
    print()

    # ==========================================================
    # Create a string result with the code for each group
    # ==========================================================

    c = ""
    print("Group\t\tCode")
    for group in code_groups_raw:
        print("{}\t=>\t{}".format(group, codes_dict[group]))
        c += codes_dict[group]

    print()
    print("Arxikos kwdikas apo fano-shannon:")
    print(rgb_code)
    print()
    print("Telikos grammikos kwdikas:")
    print(c)
    print()

    # ==========================================================
    # JSON data
    # ==========================================================

    encoded = base64.b64encode(c.encode())

    data = {
        "data": encoded.decode(),
        "error": 0, # TODO: Fill error value
        "width": width,
        "height": height,
        "n": n,
        "k": k
    }

    print("JSON kai base64:")
    print(json.dumps(data))


if __name__ == "__main__":
    main()
