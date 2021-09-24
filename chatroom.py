from encoding import Encoder
from api import apireq
from nanolib import *
from user import User

# Uses the first characters of a user's wallet address to create a unique color for the chatroom's user identifier.
def generateColor(addr):
    enc = Encoder()
    r = int(enc.encodeCharacter(addr[4])) + int(enc.encodeCharacter(addr[5]))
    g = int(enc.encodeCharacter(addr[6])) + int(enc.encodeCharacter(addr[7]))
    b = int(enc.encodeCharacter(addr[8])) + int(enc.encodeCharacter(addr[9]))
    return '#%02x%02x%02x' % (50+(r%128), 50+(g%128), 50+(b%128))

# Gets and returns the user's wallet balance. If the user has an incoming transaction, it will also begin the block confirmation process.
def getBalance():
    user = User()
    post = apireq({"action":"account_balance","account":user.getAddress()})
    if str(post['pending']) != "0":
        user.receiveRawMessage()
    return post['balance']

# Fetches the transaction history for an address, and then converts that into a log of all recent messages.
def getPublicHistory(recipient,count=1000):
        post = apireq({"action":"account_history","account":recipient,"count":count})
        messages = []
        message = ""
        sender = None
        enc = Encoder()
        blocks = post['history']
        if(str(type(blocks)) == str(type("string"))): ## If there are no blocks, blocks will be a string datatype.
            return []

        ## Ensures that two users sending messages at the same time does not create a potential conflict.
        for item in blocks:
            if sender == None:
                sender = item['account']
                message = item['amount'].zfill(16)
            elif item['account'] != sender:
                messages.append((sender, enc.decodeMessage(message)))
                sender = item['account']
                message = item['amount'].zfill(16)
            else:  
                message = item['amount'].zfill(16) + message
        messages.append((sender, enc.decodeMessage(message)))
        messages.reverse()
        outputs = []

        ## Removes the wrapper around each message. 
        for item in messages:
            msg = item[1][item[1].find("~HEAD"):] ## Gets rid of any noise that may be prepending actual messages, eg: a monetary transaction.
            while msg.find("~HEAD") > -1 and msg.find("~END", msg.find("~HEAD")) > -1: ## Ensures that each message has been completely received before viewing.
                temp = msg[msg.find("~HEAD")+5:msg.find("~END", msg.find("~HEAD"))]
                if (temp.find("~ENCRYPT") == -1):
                    temp = temp[temp.find("~BODY")+5:]
                    outputs.append((item[0], generateColor(item[0]), temp))
                msg = msg[msg.find("~END", msg.find("~HEAD")+1):]
        return outputs
