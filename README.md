# Decent

<p style="text-align:center;"><img src="/demo.png" width="auto" height="auto" alt="Application Screenshot"></p>

### What is Decent?
Decent is a chatroom application that utilizes the Nano cryptocurrency network to allow for communications to take place without the use of a central server.

---

### What can Decent be used for?
Decent is a functional proof of concept for an immutable and censorship-resistant messaging service. Because the entirety of Decent's transactions are sent and received through the Nano cryptocurrency network, Decent's chatroom service is not reliant on a central server, which gives it the following advantages:

* Blocking access to a Decent chatroom requires significantly more effort than blocking a single IP address, and cannot be done without blocking the entirety of Nano's decentralized network.
* Like a blockchain, Nano's block lattice architecture ensures that upon being sent, messages are permanent and cannot be tampered with, modified, or removed.
* Nano's block lattice architecture also prevents your Decent chatroom from being removed from the network by any means.
* Even when major web services and cloud hosts experience outages, Decent's decentralized nature allows for reliable user access through a plethora of available nodes.
* In the near future, Decent chatrooms will allow for encrypted communications between security-conscious individuals.

---

### What is Nano?
Nano is a cryptocurrency that utilizes a lightweight block lattice architecture in order to create feeless, fast, and enviornmentally friendly transactions between users. Because of its speed and feeless nature, it's ideal for hosting free and decentralized services like online chatrooms.

---

### How does Decent work?
A transaction using the Nano digital payment protocol allows for a unit of Nano currency to be divided into thirty decimal places. By assigning each commonly used character a numerical representation, we can use the numbers 00 through 99 in order to encode messages into each transaction. While each whole unit of Nano costs roughly $5 at any given point in time, by only utilizing the last sixteen digits of a thirty decimal transaction, we can create transactions that cost fractions of a cent that can be used to transmit messages.

<p style="text-align:center;"><img src="/flowchart.png" width="auto" height="auto" alt="Flowchart"></p>


---

### Prerequisites

* Python 3

## Installation

1) ``pip3 install nanolib flask rsa``
2) ``git clone https://github.com/mike-agam/Decent.git``
3) ``cd decent``
4) ``python3 decent.py``

## Using Decent

While Decent will create your Nano wallet for you, it can't populate it with currency. The following steps will give you enough Nano to use Decent:
1) Click the button that reads **Receive Nano**.
2) Copy your Nano wallet address from the pop-up. This should open [Free Nano Faucet](https://freenanofaucet.com/). If the pop-up doesn't open, check your pop-up blocker settings and press the button again.
3) Paste your wallet address into the text bar that says "nano address" and then click the "Get Nano!" button.
4) Sit back and wait. Your wallet should be given some starting funds soon. If this doesn't happen within a few seconds, please refresh the webpage.

If you want to create a Decent room for your organization:
1) Run ``python3 chathost.py``
2) In the console log, you should see a line that says ``Starting server on xrb_[..]``. Copy this xrb address.
3) In config.ini, there is an option to set the server. Replace the current option with the address that you copied.
4) Restart the chathost to start hosting your own Decent room!

Due to the nature of Nano's new spam-preventing proof of work systems, a Decent room will take longer to send and receive messages than a typical chatroom service - with the exact duration dependent on the performance of your CPU. I intend to release an update with GPU-based proof of work functionality in the near future in order to help improve slow performance speeds - which will also hopefully make encrypted communications practical in a future update afterwards.
