from Crypto.Cipher import AES

def handle(key, text):
    try:
        return (encrypt(key, text), True)
    except:
        try:
            return ("user tried to encrypt with bad key" + len(key), False)
        except Exception as ex:
            template = "exception {0}: {1!r}"
            return template.format(type(ex).__name__, ex.args)

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
