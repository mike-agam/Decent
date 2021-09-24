import requests
import configparser
from os import path
import pickle
from pprint import pprint

# A convenient wrapper for making API calls to the node.
def apireq(data, print=False):
    post = requests.post(source, json=data, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
    if(print):
        pprint(data['action'])
        pprint(post.json())
    return post.json()

def saveToFile(name, data):
    with open(name,'wb') as file:
        pickle.dump(data, file)

def loadFromFile(name):
    if path.exists(name):
        with open(name,'rb') as file:
            return str(pickle.load(file))

# Reads a value from the configuration file.    
def loadConfig(item):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config['PARAMETERS'][item]

source = loadConfig("node")