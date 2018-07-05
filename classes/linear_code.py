import numpy as np
import base64
import random

class LinearCode:
    def __init__(self):
        pass

    def encode(self, width, height, rgb_code, n=7, k=4, error=5):
        # ==========================================================
        # Separate the RGB code into groups of size k
        # ==========================================================

        code_groups = []
        code_groups_raw = []

        # The number of extra zeros appended at the end of the code
        extra_zeros = 0

        for i in range(0, len(rgb_code), k):
            group = rgb_code[i:i + k]

            # For group sizes less than k, fill with zeros at the end
            if len(group) < k:
                for i in range(k - len(group)):
                    group += "0"
                    extra_zeros += 1

            code_groups.append([int(c) for c in group])
            code_groups_raw.append(group)

        # Matrix with all binary digits of a group in individual positions
        code_groups = np.array(code_groups)
        code_groups_raw = np.array(code_groups_raw)

        # ==========================================================
        # Setup matrices I, P, G and D
        # ==========================================================

        I = np.eye(k, dtype=int)
        I_decoding2 = np.eye(n - k, dtype=int)
        zeros = [np.zeros(n - k, dtype=int)]

        I_decoding2 = np.append(I_decoding2, np.array(zeros), axis=0)

        P = np.random.randint(low=0, high=2, size=(k, n - k), dtype=int)

        intersect = np.array([x for x in set(tuple(x) for x in I_decoding2) & set(tuple(x) for x in P)])

        while len(np.unique(P, axis=0)) < P.shape[0] or intersect.shape[0] != 0:
            P = np.random.randint(low=0, high=2, size=(k, n - k), dtype=int)
            intersect = np.array([x for x in set(tuple(x) for x in I_decoding2) & set(tuple(x) for x in P)])

        G = np.concatenate((I, P), axis=1)

        # D is the binary numbers from 0 to 2^k
        D = []
        for i in range(2 ** k):
            binaries = np.binary_repr(i, width=k)
            D.append([int(c) for c in binaries])

        D = np.array(D)

        # ==========================================================
        # Create a dictionary that maps each group with a code
        # ==========================================================

        # Get encoded values with D*G and then mod 2 on all items
        C = np.mod(D.dot(G), np.array([2]))

        # Dictionary with all possible groups and their code
        codes_dict = {}

        for i in range(2 ** k):
            codes_dict["".join(str(digit) for digit in D[i])] = "".join(str(digit) for digit in C[i])

        # ==========================================================
        # Create a string result with the code for each group
        # ==========================================================
        c = ""

        initial_error = error

        for group in code_groups_raw:
            if error > 0:
                zero_pos = [pos for pos, char in enumerate(codes_dict.get(group)) if char == '0']
                temp_string_list = list(codes_dict.get(group))
                temp_string_list[random.choice(zero_pos)] = '1'
                c += ''.join(temp_string_list)
                error -= 1
            else:
                c += codes_dict[group]

        # ==========================================================
        # JSON data
        # ==========================================================

        encoded = base64.b64encode(c.encode())

        data = {
            "data": encoded.decode(),
            "error": initial_error,
            "width": width,
            "height": height,
            "n": n,
            "k": k,
            "P": P.tolist(),
            "extra_zeros": extra_zeros
        }

        return data

    def decode(self, data):
        # ==========================================================
        # Data sent from the client
        # ==========================================================

        c = base64.b64decode(data["data"]).decode()
        error = data["error"]
        width = data["width"]
        height = data["height"]
        n = data["n"]
        k = data["k"]
        P = np.array(data["P"])
        extra_zeros = data["extra_zeros"]

        # Same as encoding, but groups now have a size of n
        # This is because the 'c' variable holds the encoded value
        code_groups_raw = []

        for i in range(0, len(c), n):
            code_groups_raw.append(c[i:i + n])

        code_groups_raw = np.array(code_groups_raw)

        I = np.eye(k, dtype=int)
        G = np.concatenate((I, P), axis=1)

        D = []
        for i in range(2 ** k):
            binaries = np.binary_repr(i, width=k)
            D.append([int(c) for c in binaries])

        D = np.array(D)
        C = np.mod(D.dot(G), np.array([2]))

        codes_dict = {}

        for i in range(2 ** k):
            codes_dict["".join(str(digit) for digit in D[i])] = "".join(str(digit) for digit in C[i])

        # ==========================================================
        # DECODING
        # ==========================================================

        I_decoding = np.eye(n - k, dtype=int)
        # Transposed P
        P_decoding = np.transpose(P)
        # Parity check array
        H = np.concatenate((P_decoding, I_decoding), axis=1)

        # H array transposed
        H_transposed = np.transpose(H)
        vector_error_array = np.eye(len(H_transposed), dtype=int)

        # Error syndrome dictionary, which will help us to correct any error
        error_syndrome_dict = {}
        error_syndrome_dict[bin(0)[2:].zfill(len(H_transposed[0]))] = "".join(str(digit) for digit in C[0])

        for i in range(H_transposed.shape[0]):
            error_syndrome_dict["".join(str(digit) for digit in H_transposed[i])] = "".join(str(digit) for digit in vector_error_array[i])

        # ==========================================================
        # ERROR CORRECTION
        # SERVER SIDE
        # ==========================================================

        inverted_C = {value: key for key, value in codes_dict.items()}

        decoded_word = ""

        for group in code_groups_raw:
            word_to_array = np.array([int(bit) for bit in group])
            S_string = self.binary_array_to_string(self.error_syndrome(word_to_array, H))

            # if the is not an error in the word then continue
            # else correct the error
            if S_string == list(error_syndrome_dict.keys())[0]:
                decoded_word += inverted_C[group]
            else:
                vector_error = error_syndrome_dict.get(S_string)
                decoded_word += inverted_C[self.error_correction(word_to_array, vector_error, n)]

        decoded_word_without_extra_zeros = decoded_word[0:len(decoded_word) - extra_zeros]

        return decoded_word_without_extra_zeros


    # Calculates error syndrome
    # if result is 0-array then the encode word is correct
    # else the word received with error
    def error_syndrome(self, c, H):
        return np.mod(c.dot(np.transpose(H)), np.array([2]))


    # Calculate the correct word
    def error_correction(self, r, S, n):
        r = int(self.binary_array_to_string(r), 2)
        S = int(self.binary_array_to_string(S), 2)
        return bin(r - S)[2:].zfill(n)


    # Convert binary to string
    def binary_array_to_string(self, binary):
        string = ""
        for i in binary:
            string += str(i)
        return string