from encoding import Encoder
from encryption import Encrypter, Decrypter
from transactions import Wallet
from user import User
import random, string

# Ensures that both the encoder and decoder function properly.
def testEncoder(input = random.choice(string.ascii_letters)):
    encodeTool = Encoder()
    output = encodeTool.encodeMessage(input)
    assert output != input and encodeTool.decodeMessage(output) == input

# Ensures that both the encrypter and decrypter function properly.
def testEncrypter(input = random.choice(string.ascii_letters)):
    encryptTool = Encrypter()
    decryptTool = Decrypter()
    output = encryptTool.encryptMessage(input)
    assert output != input and decryptTool.decryptMessage(output, encryptTool.key, encryptTool.nonce, encryptTool.tag) == input

# Ensures that the encoder, decoder, encrypter, and decrypter all work harmoniously. 
def testEncryptEncode(input = random.choice(string.ascii_letters)):
    encryptTool = Encrypter()
    encodeTool = Encoder()

    output = encryptTool.encryptMessage(input)
    output = encodeTool.encodeMessage(str(output))
    output = encodeTool.decodeMessage(output)
    output = eval(output) 
    
    decryptTool = Decrypter()
    assert output != input and decryptTool.decryptMessage(output, encryptTool.key, encryptTool.nonce, encryptTool.tag) == input

# Ensures that messages can be written and read between users.
def testUserReadWrite(input = "Hello, World!"):
    alice = User()
    bob = User()
    assert(bob.readMessage(alice.writeMessage(input)) == input)

    output, data = alice.writeMessage(input, True)
    assert(bob.readMessage(output, data.key, data.nonce, data.tag) == input)

