from encoding import Encoder
from encryption import Encrypter, Decrypter
from transactions import Wallet
from pprint import pprint
from transactions import Wallet
from api import loadFromFile

# The user class bridges together encoding, encrypting, and transaction sending/receiving in a simplified manner.
class User:
    def __init__(self, name="wallet"):
        self.setWallet(name)

    # Assigns a user to a certain wallet. Useful if you're operating multiple users, for some reason.
    def setWallet(self, name):
        self.walletname = name
        wallet = loadFromFile(name)
        return wallet

    # Retrieves a user's wallet address.
    def getAddress(self):
        wallet = Wallet(self.walletname)
        return wallet.address

    # Encodes a message in the two-integer Decent format.
    def writeMessage(self, input):
        encodeTool = Encoder()
        return encodeTool.encodeMessage(str(input))

    # Decodes a message in the two-integer Decent format. Prints the results to console.
    def readMessage(self, input):
        decodeTool = Encoder()
        output = decodeTool.decodeMessage(input)
        for item in output:
            item = str(item)
        print(str(input) + " : " + output)
        return output

    # Takes in text input, encodes it, and then sends it to a recipient. No wrapper included.
    def sendRawMessage(self, input, recipient):
        wallet = Wallet(self.walletname)
        output = self.writeMessage(input)
        counter = 1
        print(str(len(output)) + " messages to send.")
        for item in output:
            amount = int(item)
            wallet.send(recipient, amount)
            print("Message sending... (" + str(100*(counter/len(output))) + "%)")
            counter += 1

    # Receives Decent numerical data, decodes it directly to a string. No wrapper included.
    def receiveRawMessage(self):
        wallet = Wallet(self.walletname)
        amounts = wallet.receive();
        output = ""
        for item in amounts:
            output += self.readMessage(item)
        return output

    # Takes input, encodes it, encrypts it if necessary, inserts it into a wrapper, and then sends it. 
    def sendMessage(self, input, recipient, encrypted=False):
        body = input
        if "~" in body: ## Prevents users from malforming their messages.
            raise Exception("Character is forbidden.")

        # Creates the header - useful for indicating the beginning of a message, and storing any necessary header information.
        message = "~HEAD"
        if encrypted:
            enc = Encrypter()
            body = str(enc.encryptMessage(input))
            data = enc.getData()
            message += "~ENCRYPT"
            print("Sending nonce...")
            message += "~NONCE"
            message += str(data.nonce)
            print("Sending tag...")
            message += "~TAG"
            message += str(data.tag)

        # Creates the body - a big indicator that signals to the unwrapper that the encoded text is inside.
        message += "~BODY"
        pprint(body)
        message += body

        # Signals the end of the wrapper, so that the unwrapper stops parsing here.
        message += "~END~~"
        while(len(message)%16 != 0):
            message += " "
        self.sendRawMessage(message, recipient)
        print("Message sent.")
        print(message)
        return 0

    # Receives and unwraps the data.
    def receiveMessage(self, key=None):
        dec = Decrypter()
        nonce, tag = None, None
        data = self.receiveRawMessage()
        data = data[data.find("~HEAD")+5: data.find("~END")]
        if (data.find("~ENCRYPT") > -1): ## If encrypted data is stored, the Nonce and Tag are sent in plaintext.
            nonce = eval(data[data.find("~NONCE")+6:data.find("~",data.find("~NONCE")+1)])
            tag = eval(data[data.find("~TAG")+4:data.find("~",data.find("~TAG")+1)])
        data = data[data.find("~BODY")+5:]
        if (nonce is None or tag is None):
            return data
        else:
            return dec.decryptMessage(eval(data), key, nonce, tag)