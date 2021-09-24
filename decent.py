import json
from user import User
from chatroom import getBalance, getPrivateHistory, getPublicHistory
from api import loadConfig
from flask import Flask, render_template, request

app = Flask(__name__)
server = loadConfig("server")

# Creates the main interface for the public chatroom and sends necessary interface variables from the Python server to the Javascript client.
@app.route('/', methods = ['GET'])
@app.route('/getlog', methods = ['GET','POST'])
def getlog():
    data = getPublicHistory(server,1000)
    user = User()
    balance = str(getBalance())
    if balance == "0":
        balance = "Receive Nano"
    else:
        balance = str(int(int(balance)/10000000000000000000000)) + " μnano"
    return render_template("index.html", log=data, username=str(user.getAddress()), balance=balance, server=server[4:16])

# The following functions are responses for POST calls between the client and server. They're pretty self-explanatory. 

@app.route('/data/log', methods = ['GET','POST']) 
def data():
    return json.dumps(getPublicHistory(server,1000))

@app.route('/data/address', methods = ['GET','POST'])
def useraddr():
    user = User()
    return user.getAddress()

@app.route('/data/balance', methods = ['GET','POST']) 
def userbalance():
    return getBalance()

@app.route('/data/server', methods = ['GET','POST']) 
def getserver():
    return server

# Used to send user input from the Javascript client to the Python server.
@app.route('/sendmsg', methods = ['POST']) 
def send():
    if request.method == 'POST':
        user = User()
        message = request.get_data().decode()
        user.sendMessage(message, server, False)
        return "Message sent."

if __name__ == "__main__":
    app.run()

