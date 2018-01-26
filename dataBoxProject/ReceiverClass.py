# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:35:02 2017

@author: vlad
"""
from ftplib import FTP
import socket
import json
import Sensor
class ReceiverClass:
    FTP_TYPE=0;
    TCP_TYPE=1;
    def __init__(self,communicationType,IP_LOCAL,*args,**kwargs):
        self.communicationType=communicationType;
        self.dataList=[];
        if self.communicationType==self.FTP_TYPE:
            self.user=kwargs.get("user");
            self.password=kwargs.get("password");
            self.FTPdir=kwargs.get("FTPdir");
            self.ftp=FTP(IP_LOCAL);
            self.connectStatus=self.checkFTPStatus();
        elif self.communicationType==self.TCP_TYPE:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            TCP_PORT=kwargs.get("portNumber");
            #self.s.settimeout(10);
            errno=self.s.connect_ex((IP_LOCAL, TCP_PORT));
            if errno>0:
                self.connectStatus=False;
                self.error="Connection not initialized. Error number:"+errno;
            else:
                msg=json.dumps({"query":"checkConnection"});
                self.s.send(msg.encode())
                respJson = self.s.recv(1024).decode();
                resp=json.loads(respJson);
                if resp["response"]=="OK":
                    self.connectStatus=True;
                    print("response OK");
                else:
                    print(resp);
                    self.connectStatus=False;
            
    def checkFTPStatus(self):
        msg = self.ftp.getwelcome();
        if (msg==self.goodWelcome):
            return True;
        else:
            return False;
    def readData(self,sensorList):
        if self.communicationType==self.FTP_TYPE:
            self.ftp.cwd(self.FTPdir);
            for sensor in sensorList:
                gFile=open(sensor.getfileName(),"w");
                self.ftp.retrbinary("RETR"+sensor["filename"],gFile.write);
                gFile.close();
        elif self.communicationType==self.TCP_TYPE:
            for sensor in sensorList:
                msg=json.dumps({"query":"readData","ID":sensor.getID()});            
                self.s.send(msg.encode());
                respJson = self.s.recv(1024).decode();
                resp=json.loads(respJson);
                self.dataList.append((sensor,resp["value"]));
                #print(self.dataList[0][1]);
        return self.dataList;
    def getStatus(self):
        return self.connectStatus;
    def closeConnection(self):
        self.s.close();
    def getError(self):
        return self.error;