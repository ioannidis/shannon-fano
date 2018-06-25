import numpy as np
from PIL import Image

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

    print(array_1d)

    print(pixel_array[0, 0])


def linear_compression():
    # Σελίδα 152
    # https://www.youtube.com/watch?v=oYONDEX2sh8
    # https://www.youtube.com/watch?v=z4WE2qpvaF8

    # C => Κώδικας
    # G => Γεννήτορας πίνακας => [ Ι_k | P ] => διάσταση (n * k)
    # P => Αυθαίρετος πίνακας => διάσταση (k * (n - k))
    # D => Διάνυσμα της λέξης
    # H => Πίνακας ισοτιμίας => [ transpose P | I_(n-k) ] => διάσταση (n * (n - k))

    # C = D * G

    # Παίρνουμε τη πληροφορία και τη χωρίζουμε σε k διαδοχικά τμήματα
    # Κωδικοποιούμε το καθένα σε μήκος n σύμφωνα με ένα σύνολο κανόνων
    # Τα n-k ψηφία ελέγχου προκύπτουν από τους γραμμικούς συνδιασμούς των ψηφίων πληροφορίας

    pass


def linear_encoder():
    pass


if __name__ == "__main__":
    main()
