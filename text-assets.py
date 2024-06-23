from Crypto.Cipher import AES

cipher = AES.new(b"@_#*&Reverse2806                ", AES.MODE_CBC, b"!_#@2022_Skyfly)")


def decrypt(dat):
    # skip 48 bytes (RSA Signature)
    decrypted = cipher.decrypt(dat[48:])

    return decrypted


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python text-asset.py <input-file> <output-file>")
        sys.exit(1)

    f = open(sys.argv[1], "rb").read()
    f = decrypt(f)
    open(sys.argv[2], "wb").write(f)
