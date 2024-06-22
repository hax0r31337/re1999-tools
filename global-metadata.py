import sys

XOR_KEY = b"1999BluePoch"

# accept arguments
if len(sys.argv) < 3:
    print("Usage: python global-metadata.py <input-file> <output-file>")
    sys.exit(1)

f = open(sys.argv[1], "rb").read()[::-1]
f = bytes([f[i] ^ XOR_KEY[i % len(XOR_KEY)] for i in range(len(f))])
open(sys.argv[2], "wb").write(f)
