# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:16:52 2017

@author: vlad
"""
import socket
import json
class SenderClass:
    def __init__(self,IP_VPN,portVPN):
        self.IP=IP_VPN;
        self.port=portVPN;
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        errno=self.socket.connect_ex((self.IP, self.port));
        if errno > 0:
            self.connectStatus = False;
            self.error = "Connection not initialized. Error number:" + errno;
            return 0;
        msg=json.dumps({"query":"checkConnection"});
        self.socket.send(msg)
        resp = self.socket.recv(1024);
        if resp=="OK":
            self.connectStatus=True;
        else:
            self.connectStatus=False;
    def sendData(self,data):
        data.update({"query":"sendData"});
        self.socket.sendMessage(json.dumps(data));
    def getStatus(self):
        return self.connectStatus;
    def closeConnection(self):
        self.socket.close();