import datetime
import random
import crypto
import hashlib

class Message:
    def __init__(self, user, msg, encrypted=True):
        self.user = user
        self._msg = msg
        if not encrypted: self._msg += " <unencrypted>"
        self.time = datetime.datetime.now().strftime("%x %X")
        self.encrypted = encrypted

    def msg(self, key):
        return crypto.decrypt(key, self._msg).decode('utf-8') if self.encrypted else self._msg

    def to_str(self):
        return "(" + self.time + " - " + self.user + "): " + self._msg

    @staticmethod
    def fmt(key, lst, clientname):
        s = ''
        i = 0
        for msg in lst:
            i += 1
            try:
                strmsg = msg.msg(key)
            except:
                strmsg = '<message sent with different key>'
            if msg.user != clientname:
                s += f'<p>{msg.user} <textarea readonly class="chatbox" cols="70" rows="2">{strmsg}</textarea></p>\n'
            else:
                s += f'<p><textarea readonly class="chatbox" cols="70" rows="2">{strmsg}</textarea> {msg.user}</p>\n'

        return s


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def random_string(len=25):
    s = ''
    for _ in range(len):
        s += random.choice(alphabet)
    return s