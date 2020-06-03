import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class Encryption:
    def create_keys(self):
        private_key = RSA.generate(1024)
        with open("rsa.pvt", "wb") as pvt_file:
            pvt_file.write(private_key.exportKey())
        print("Created Keys")

    def get_encrypt_key(self):
        with open('rsa.pvt', 'rb') as pvt_file:
            key = RSA.importKey(pvt_file.read())
        return key

    
    def encrypt_message(self,message):
        keys = self.get_encrypt_key()
        cipher_encypt = PKCS1_OAEP.new(keys)
        encrypted = cipher_encypt.encrypt(message.encode('utf-8'))
        return (encrypted)

    def decrypt_message(self,message):
        keys = self.get_encrypt_key()
        cipher_decrypt = PKCS1_OAEP.new(keys)
        text = cipher_decrypt.decrypt(message)
        return (text.decode('utf-8'))


        
