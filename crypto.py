from Crypto.Cipher import AES

def handle(key, text):
    try:
        (encrypt(key, text), True)
    except:
        return ("user tried to encrypt with bad key", False)

def encrypt(key, text):
    cipher = AES.new(key, AES.MODE_EAX)
    cyphertext, tag = cipher.encrypt_and_digest(text)
    return cipher.nonce + tag + cyphertext

def decrypt(key, text):
    nonce = text[0:16]
    tag = text[16: 32]
    ctext = text[32:-1]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    plaintext = cipher.decrypt(ctext)
    return plaintext
