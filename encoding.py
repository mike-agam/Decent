# The encoder is a class responsible for encoding and decoding strings throughout the Decent protocol.
# It does this by converting strings to two digit integers, which when combined form an integer that is
# - appended to 0.00000000000000 (1e-14) and then sent as a Nano cryptocurrency transaction to the receiving party.
class Encoder:

    # Takes a character's unicode value, and adjusts by 32 so that all necessary alphanumeric and punctuation characters are between 00 and 99.  
    def encodeCharacter(self, text):
        if int(ord(str(text))) > 132:
            raise Exception("Character " + str(text) + "(" + str(int(ord(str(text)))) + ") is forbidden.")
        return str(ord(str(text)) - 32).zfill(2)

    ## Takes two integers (as a string) and returns the character that they represent in Decent encoding.
    def decodeCharacter(self, text):
        return chr(int(text) + 32)

    ## Encodes multiple characters at a time, and sorts them into strings of sixteen integers: eight encoded characters.
    def encodeMessage(self, text):
        messages = []
        line = ""
        index = 0
        for x in text:
            line += str(self.encodeCharacter(x))
            if len(line) >= 16:
                messages.append(line)
                line = ""
        if len(line) > 0:
            messages.append(line)

        return messages

    # Takes in a list of integer values and decodes them.
    def decodeMessage(self, text):
        encoded = str(text)
        temp = None
        decoded = ""
        for x in encoded:
            if x in ['0','1','2','3','4','5','6','7','8','9']: ## Ensures that no punctuation marks in Python string's list representation are converted.
                if (temp != None): ## Splits characters into sets of two.
                    decoded += self.decodeCharacter(temp + x)
                    temp = None
                else:
                    temp = x
        return decoded
        
    # Can be used to gauge the number of transactions it will take to send a message.
    def getMessageCount(self, text):
        counter = 0
        encoded = self.encodeMessage(text)
        for x in encoded:
            counter += 1
        return counter