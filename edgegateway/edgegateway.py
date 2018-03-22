#!/usr/bin/env python

import paho.mqtt.client as mqtt
import time
import configparser

_version="0.0.1"
_doContinue = True
_ini_config = "./aigateway.ini"

class edgegateway:
    def __init__(self, ini_path):
        print("ini_path is ", ini_path)
    
        if ini_path:
            _ini_config = ini_path
            
    def on_message(self, client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        
    def run(self):
        global _doContinue
        print("Begin run method")
        configP = configparser.ConfigParser()
        
        configP.read(_ini_config)
        
        print(configP.sections())
        
        print("setting values [MessageClient]")
        clientHost = configP.get("MessageClient", "host")
        clientport = configP.get("MessageClient", "port")
        clientqos = configP.get("MessageClient", "qos")
        clienttimeout = configP.get("MessageClient", "timeout")
        clienttopic = configP.get("MessageClient", "topic")
        clientid = configP.get("MessageClient", "clientid")
        clientpollfreq = configP.get("MessageClient", "pollfrequency")
        clientsleepTime = configP.get("MessageClient", "sleep")
        
        print("setting values [MessageBroker]")
        #[MessageBroker]
        brokerhost = configP.get("MessageBroker", "host")
        brokerport = int(configP.get("MessageBroker", "port"))
        brokeruid = configP.get("MessageBroker", "uid")
        brokerpwd = configP.get("MessageBroker", "pwd")
        brokersubscribe = configP.get("MessageBroker", "subscribe")
        brokerkeepalive = configP.get("MessageBroker", "keepalive")

        print("setting values [GPIOMap]")
        #[GPIOMap]
        pinlist = configP.get("GPIOMap", "pins") #Active GPIO Pins
        gpioList = pinlist.split(",")
        print("pinlist: ")
        print(pinlist)
        print("gpioList: ")
        print(gpioList)

        gpioPinMap = configP.get("GPIOMap", "pinmap") #Active GPIO Pins
        gpioPinList = gpioPinMap.split(",")
        print("gpioPinList: ")
        print(gpioPinList)
        
        gpiopinDict={}
        for entry in gpioPinList:
            keyVal=entry.split(":")
            gpiopinDict[keyVal[0]] = keyVal[1]

        print("gpiopinDict ")
        for key,value in gpiopinDict.items():
            print(key + " => " + value)
        
        #gpioDict = pinlist.split(",")
        gpio1 = configP.get("GPIOMap", "1")  #Humidity
        gpio2 = configP.get("GPIOMap", "2")  #Temperature
        gpio3 = configP.get("GPIOMap", "3")  #Pump
        
        print("Creating new Client")
        client = mqtt.Client(clientid)
        client.on_message=self.on_message #attach function to callback
        
        client.connect(brokerhost, brokerport)

        client.loop_start() #start the loop

        print("Subscribing to topic " + brokersubscribe)
        client.subscribe(brokersubscribe)
        
        while _doContinue:
            #actionMsg =_checkSubscription()
            result = self._dataBusinessRules(self._readGPIO(), gpioList)
            self._PostTopic(client, result, clienttopic)

            _doContinue = False
            
        time.sleep(10) # wait
        client.loop_stop() #stop the loop

    def _readGPIO(self):
        gpio={'1':'56', '2':'75', '3':'off'}
        #return dictionary
        return gpio
        
    def _dataBusinessRules(self, gpio, gpioList):
        #return list of json elements for message 
        for key,value in gpio.items():
            print(key + " => " + value)
            
        for pin in gpioList:
            print("pin: " + pin)

    def _PostTopic(self, client, result, clienttopic):
        print("Publishing message to topic " + clienttopic)
        result = client.publish(clienttopic, "OFF")
    
    
if __name__ == '__main__':
    e=edgegateway(None) 
    e.run()       
