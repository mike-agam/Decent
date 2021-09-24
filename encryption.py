from Crypto.Cipher import AES
import rsa
import secrets
from os import path
from api import loadFromFile, saveToFile

###
###   Because private messaging implementation is not yet complete, none of the functions in this file are currently in use.
###

# Wrapper class for storing encryption data.
class EncryptionData:
    def __init__(self, key, nonce, tag):
        self.key = key
        self.nonce = nonce
        self.tag = tag

# The Encrypter class is used to create encryption data and use it to create AES-256 secured messages.
# 
class Encrypter:
    # If no encryption data exists, create some.
    def __init__(self):
        if path.exists('key'):
            self.key = loadFromFile('key')
        else:
            self.key = secrets.token_urlsafe(16)[0:16]
            saveToFile('key', self.key)
            print("Key " + self.key + " created.")  

    # Encrypts a message with AES-256 encryption.
    def encryptMessage(self, text):
        self.aes = AES.new(self.key.encode('utf-8'), AES.MODE_EAX)
        self.nonce = self.aes.nonce
        message, self.tag = self.aes.encrypt_and_digest(text.encode('utf-8'))
        return message

    # Returns a wrapped class consisting of the key, nonce, and tag.
    def getData(self):
        return EncryptionData(self.key, self.nonce, self.tag)

# The Decrypter class's sole function is to take AES-256 messages and decrypt them.
# Using the tag and nonce, we can verify the integrity of all received messages.
class Decrypter:
    def decryptMessage(self, text, key, nonce, tag):
        aes = AES.new(key.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
        message = aes.decrypt_and_verify(text, tag)
        return message.decode()