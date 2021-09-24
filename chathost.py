import time
from user import User

# Confirms all transactions sent to its address. 
# This file can be run to host your own Decent chatroom.
if __name__ == "__main__":
    user = User("server")
    print("Now hosting a Decent chatroom on " + user.getAddress())
    while True:
        if(len(user.receiveMessage()) == 0):
            time.sleep(15)
