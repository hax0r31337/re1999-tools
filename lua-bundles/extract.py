import gzip


def csharp_varint(dat: bytes):
    num = 0
    while True:
        byte = dat[0]
        dat = dat[1:]
        num = (num << 7) | (byte & 0x7F)
        if byte & 0x80 == 0:
            break
    return num, dat


def unpack(dat: bytes, callback):
    # skip 48 bytes (RSA Signature)
    dat = dat[48:]
    while len(dat) > 0:
        tag_len, dat = csharp_varint(dat)
        tag = dat[:tag_len]
        script_len = int.from_bytes(dat[tag_len : tag_len + 4], "little")
        script = bytearray(dat[tag_len + 4 : tag_len + 4 + script_len])
        dat = dat[tag_len + 4 + script_len :]

        for i in range(len(script)):
            script[i] ^= tag[i % len(tag)]

        gzip_timestamp = int.from_bytes(script[4:8], "little")

        script = gzip.decompress(script)

        callback(tag.decode("utf-8"), script, gzip_timestamp)


if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 3:
        print("Usage: python lua-bundles/extract.py <input-file> <output-dir>")
        sys.exit(1)

    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])

    def write_file(tag, script, timestamp):
        file = f"{sys.argv[2]}/{tag}.luao"
        # check if file exists
        timestamp_prev = 0
        if os.path.exists(file):
            timestamp_prev = int(os.path.getmtime(file))
        if timestamp_prev >= timestamp:
            print(
                f"Skipping {file} as it is already up to date ({timestamp_prev} >= {timestamp})"
            )
            return
        open(file, "wb").write(script)
        os.utime(file, (timestamp, timestamp))

    # check if input is a directory
    if os.path.isdir(sys.argv[1]):
        for file in os.listdir(sys.argv[1]):
            b = open(f"{sys.argv[1]}/{file}", "rb").read()
            unpack(b, write_file)
        sys.exit(0)
    else:
        b = open(sys.argv[1], "rb").read()
        unpack(b, write_file)
