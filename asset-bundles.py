def get_key(str: str) -> chr:
    key = 0
    for i in range(len(str)):
        key += ord(str[i])
    if key & 1:
        key += 4
    else:
        key += 2
    return key % 256


def decrypt(ab, key):
    return bytes([ab[i] ^ key for i in range(len(ab))])


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python asset-bundles.py <input-file> <key> <output-file>")
        print("Usage: python asset-bundles.py BATCH <input-dir> <output-dir>")
        sys.exit(1)

    if sys.argv[1] == "BATCH":
        import os

        if not os.path.exists(sys.argv[3]):
            os.makedirs(sys.argv[3])

        for root, _, files in os.walk(sys.argv[2]):
            for file in files:
                print(f"Processing {file}")

                ab = open(os.path.join(root, file), "rb").read()
                key = get_key(file[: file.index(".")])
                ab = decrypt(ab, key)
                open(os.path.join(sys.argv[3], file), "wb").write(ab)
    else:
        ab = open(sys.argv[1], "rb").read()
        key = get_key(sys.argv[2])
        ab = decrypt(ab, key)
        open(sys.argv[3], "wb").write(ab)
