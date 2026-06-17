def shift_left(b):
    return ((b << 2) | (b >> 6)) & 255

def shift_right(b):
    return ((b >> 2) | (b << 6)) & 255

def main():
    key = 85
    
    f = open("original.txt", "rb")
    original = f.read()
    f.close()
    
    encrypted = []
    for b in original:
        encrypted.append(shift_left(b) ^ key)
    
    f = open("encrypted.bin", "wb")
    f.write(bytes(encrypted))
    f.close()
    
    decrypted = []
    for b in encrypted:
        decrypted.append(shift_right(b ^ key))
    
    f = open("decrypted.txt", "wb")
    f.write(bytes(decrypted))
    f.close()
    
    print("Исходные данные:", original)
    print("Зашифрованные:", bytes(encrypted))
    print("Расшифрованные:", bytes(decrypted))

if __name__ == "__main__":
    main()