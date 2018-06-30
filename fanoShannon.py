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

    encoded_message = ""

    for i in dummy_img:
        encoded_message += fano_shannon_result[i]

    print("Encoded Message length:", len(encoded_message))
    print()
    print("Encoded Message:", encoded_message)
    print()
    print("RGB array:\n" + str(dummy_img))
    print()

    linear_compression(width, height, encoded_message)


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


def linear_compression(width, height, rgb_code, n=7, k=4):
    # ==========================================================
    # Separate the RGB code into groups of size k
    # ==========================================================

    code_groups = []
    code_groups_raw = []

    for i in range(0, len(rgb_code), k):
        # If the group size is less than k bits, fill with extra zeros
        padded_group = rgb_code[i:i+k].ljust(k,'0')
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
    # TODO: p.153====================================
    # P= [[0,1,1],[1,0,1],[1,1,0]]
    # ===============================================
    # TODO: p.155 decoding working  for n=7 k=4 =====
    P = [[1,1,1],[1,1,0],[1,0,1], [0,1,1]]
    # ===============================================
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
    C = np.mod(D.dot(G), np.array([2]))

    print("C (Kwdikes Lekseis):")
    print(C)
    print()
    print()

    # Dictionary with all possible groups and their code
    codes_dict = {}

    for i in range(2**k):
        codes_dict["".join(str(digit) for digit in D[i])] = "".join(str(digit) for digit in C[i])

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


    # ==========================================================
    # DECODING
    # ==========================================================

    #TODO: to be removed
    print()
    print("DECODING ================================================")
    #================================================================

    I_decoding = np.eye(n-k, dtype=int)
    # Transposed P
    P_decoding = np.transpose(P)
    # Parity check array
    H = np.concatenate((P_decoding, I_decoding), axis=1)

    print("I_decoding:\n" + str(I_decoding))
    print()
    print()
    print("P_decoding:\n" + str(P_decoding))
    print()
    print()
    print("H:\n" + str(H))
    print()
    print()

    # H array transposed
    H_transposed = np.transpose(H)
    vector_error_array = np.eye(len(H_transposed), dtype=int)

    # Error syndrome dictionary, which will help us to correct any error
    error_syndrome_dict = {}
    error_syndrome_dict[bin(0)[2:].zfill(len(H_transposed[0]))] = "".join(str(digit) for digit in C[0])
    for i in range (H_transposed.shape[0]):
        error_syndrome_dict["".join(str(digit) for digit in H_transposed[i])] = "".join(str(digit) for digit in vector_error_array[i])



    print("H_transposed:\n" + str(H_transposed))
    print()
    print()
    print("vector_error_array:\n" + str(vector_error_array))
    print()
    print()
    print("Full error table:\n" + str(error_syndrome_dict))
    print()
    print()


    # ==========================================================
    # ERROR CORRECTION
    # SERVER SIDE
    # ==========================================================


    # TODO: THA PREPEI NA GINEI TO DECODING KAI I EPANAFORA SE KOMATIA
    # TODO: GIA TIN ORA TA PAIRNO ATOFIA APO PROIGOUMENO BIMA
    inverted_C =  {value: key for key, value in codes_dict.items()}

    decoded_word = ""
    for group in code_groups_raw:
        word_to_array = np.array([int(bit) for bit in codes_dict[group]])
        S_string = binary_array_to_string(error_syndrome(word_to_array, H))

        # if the is not an error in the word then continue
        # else correct the error
        if (S_string == list(error_syndrome_dict.keys())[0]):
            decoded_word += group
        else:
            vector_error = error_syndrome_dict.get(binary_array_to_string(error_syndrome(word_to_array, H)))
            decoded_word += inverted_C[error_correction(word_to_array, vector_error, n)]


    # Print the decoded words
    print("Decoded word")
    print(decoded_word)

    # TODO: to be deleted === PAROUSIAZEI TO APOTELSMA OTAN DINOYME LEKSI ME THORIBO
    # TODO: OPOS STO BIBLIO sel 156-157
    # S_string = binary_array_to_string(error_syndrome(np.array([1,1,1,1,0,1,0]), H))
    #
    # if (S_string == list(error_syndrome_dict.keys())[0]):
    #     print("ok")
    # else:
    #     vector_error = error_syndrome_dict.get(binary_array_to_string(error_syndrome(np.array([1,1,1,1,0,1,0]), H)))
    #     print (inverted_C[error_correction(np.array([1,1,1,1,0,1,0]), vector_error, n)])


# Calculates error syndrome
# if result is 0-array then the encode word is correct
# else the word received with error
def error_syndrome(c, H):
    return np.mod(c.dot(np.transpose(H)), np.array([2]))

# Calculate the correct word
def error_correction(r, S, n):
    r = int(binary_array_to_string(r),2)
    S = int(binary_array_to_string(S),2)
    return bin(r-S)[2:].zfill(n)

# Convert binary to string
def binary_array_to_string(binary):
    string = ""
    for i in binary:
        string += str(i)
    return string

if __name__ == "__main__":
    main()
