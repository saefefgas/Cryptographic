import base64
import hashlib
from crypto.Cipher import _AES


def get_check_digits(passport_id):
    target = '111116'
    weight = [7,3,1]
    check_digit = sum([int(i)*weight[(passport_id.index(target)+i)%3] for i in range(len(target))])%10
    return passport_id.replace('?',str(check_digit))


def get_key_seed(check_key):
    mrz_info = ''
    for i in check_key:
        if i.isdigit():mrz_info+=i
    #print(mrz_info)
    mrz_info = '12345678<811101821111167'
    sha1obj = hashlib.sha1()
    sha1obj.update(mrz_info.encode())
    hashed_key = sha1obj.hexdigest()[:32]
    print('key_seed',hashed_key)
    return hashed_key


def get_key_enc(key_seed):
    sha1_input = bytes.fromhex(key_seed + '00000001')
    sha1obj = hashlib.sha1()
    sha1obj.update(sha1_input)
    key_enc = sha1obj.hexdigest()[:32]
    print('key_enc',key_enc)
    return key_enc


def odd_even(string):
    bin_string = list(bin(int(string,16))[2:])
    block_string = block(8,bin_string)
    new_string = ''
    for b in block_string:
        one_num = b.count('1')
        if not one_num%2:
            new_block = strxor(''.join(b),'00000001')
            new_string += new_block
        else:new_string += ''.join(b)
    return hex(int(new_string,2))[2:]


def xor(a, b):
    if len(a) > len(b):
        return bytes([x ^ y for x, y in zip(a[:len(b)], b)])
    else:
        return bytes([x ^ y for x, y in zip(a, b[:len(a)])])


def strxor(a, b):
    res = ''
    for (x,y) in zip(a,b):
        res += str(int(x)^int(y))
    return res


def block(size, cipher):
    cipher_block = []
    for i in range(0, len(cipher), size):
        cipher_block.append(cipher[i:i+size])
    return cipher_block


def wrap_up():
    raw_cipher = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
    raw_key = '12345678<8<<<1110182<111116?<<<<<<<<<<<<<<<4'
    cipher_text = base64.b64decode(raw_cipher)
    check_key = get_check_digits(raw_key)
    key_seed = get_key_seed(check_key)
    key_enc = get_key_enc(key_seed)
    key_enc = odd_even(key_enc)
    plain = _AES.new(bytes.fromhex(key_enc),_AES.MODE_CBC,bytes.fromhex('0'*32)).decrypt(cipher_text)
    print(plain)


wrap_up()
