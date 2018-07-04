from classes.fano_shannon import FanoShannon
from classes.linear_code import LinearCode
from PIL import Image
import numpy as np

def main():
    image = Image.open("3X3.jpg")
    width = image.size[0]
    height = image.size[1]
    array_4d = np.array(image)
    array_1d = np.ravel(array_4d)
    count = dict(map(lambda x: (x, list(array_1d).count(x)), array_1d))

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

    print(fano_shannon_result)

    lc = LinearCode()
    json_data = lc.encode(width, height, fano_shannon_result)
    print(json_data)

    res = lc.decode(json_data)
    print(res)

if __name__ == "__main__":
    main()