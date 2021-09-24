from nanolib import *
from pprint import *
from Crypto.Cipher import AES
from os import path
import pickle
from api import apireq, loadConfig

rep = loadConfig("representative")

# Means of sorting blocks received.
def getHeight(block):
        return block[1]['height']

# The wallet class is used for the storing, receiving, and sending of Nano currency.
class Wallet:
    # Creates a wallet, or loads one if one is already present.
    def __init__(self, name="wallet"):
        if path.exists("./" + name):
            self.load(name)
        else:
            self.create(name)

    # Creates a new wallet. Can optionally take a name value.
    def create(self, name="wallet"):
        self.seed = generate_seed()
        self.address = generate_account_id(self.seed, 0)
        self.pkey = generate_account_private_key(self.seed, 0)
        with open(name,'wb') as file:
            pickle.dump(self, file)
        print("Wallet " + self.address[0:8] + " created.")

    # Loads a pre-existing wallet.
    def load(self, name="wallet"):
        self.seed, self.address, self.pkey = "","",""
        with open(name,'rb') as file:
            temp = pickle.load(file)
            self.seed, self.address, self.pkey = temp.seed, temp.address, temp.pkey

    # Receives Nano currency, confirms the transaction, and returns the encoded numerical values of the transaction.
    def receive(self):
        amounts = []
        user = apireq({"action":"account_info","representative":True,"account":self.address})

        # Each Nano block must have the data of its previous block.
        # Rather than constantly ping the node, we use the 'previous' variable to store the hash of every block being sent.
        previous = None
        balance = 0
        if 'frontier' in user.keys():
            previous = user['frontier']
            balance = user['balance']

        post = apireq({"action":"pending","account":self.address})
        blocks = []
        for x in post['blocks']:
            info = apireq({"action":"block_info", "json_block":True,"hash":x}) ## Obtains more block information than obtained from the 'pending' action.
            blocks.append((x,info))
        blocks.sort(key=getHeight) ## Puts the blocks in chronological order.

        # Creates new blocks to be sent to the Nano network in order to confirm the sending blocks.
        for item in blocks:
            balance = int(balance) + int(item[1]['amount'])
            newblock = Block (
                block_type="state",
                account=self.address,
                representative=rep,
                previous=previous,
                balance=balance,
                link=item[0]
            )
            if not newblock.has_valid_work: 
                newblock.solve_work() # TO-DO: Optimize dramatically by solving proof of work with GPU rather than CPU.
            if not newblock.has_valid_signature:
                newblock.sign(self.pkey) 
            previous = apireq({"action":"process","block":newblock.json()})
            print(previous)
            previous = previous['hash']
            amounts.append(str(int(item[1]['amount'])).zfill(16))
        return amounts

    # Sends Nano currency to another account. 
    def send(self, recipient, amount):
        user = apireq({"action":"account_info","representative":True,"account":self.address})

        # Like the receiving blocks, the Nano network requires information about a wallet's previous block be in the next block.
        if 'frontier' in user.keys():
            previous = user['frontier']
            balance = user['balance']
        else:
            raise ValueError('Account has no funds.')
        if(amount > int(balance)):
            raise ValueError('Not enough funds to complete transaction.')
        newblock = Block (
            block_type="state",
            account=self.address,
            representative=rep,
            previous=previous,
            link_as_account=recipient,
            balance=int(balance) - int(amount)
        )
        if not newblock.has_valid_work:
            newblock.solve_work() # TO-DO: Optimize dramatically by solving proof of work with GPU rather than CPU.
        if not newblock.has_valid_signature:
            newblock.sign(self.pkey)
        apireq({"action":"process","block":newblock.json()})
        return 0