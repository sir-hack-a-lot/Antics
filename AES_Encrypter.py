##NOT my code: https://www.youtube.com/watch?v=UB2VX4vNUa0 

from Cyrpto import Random
from Crypto.Cipher import AES
import os, glob

class Encrypter:
    def __init__(self,key):
        self.key==key
    
    def pad(self,s):
        amnt_pad = AES.block_size - (len(s) % AES.block_size)
        return s + b"\0" * amnt_pad 
   
    def encrypt(self, message, key, key_size = 256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    #consider placing encrypted file in a enc/ directory 
    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    def decrypt(self,ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(cipherText[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            cipherText = fo.read()
        dec = self.decrypt(cipherText,self.key_
        #remove .enc suffix
        with open(file_name[:-4]) as fo:
            fo.write(dec)
        os.remove(file_name)  #remove encrypted file
    

