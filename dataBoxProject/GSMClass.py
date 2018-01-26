# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 11:05:46 2017

@author: vlad
"""
import time
import serial
class GSMClass:
    GSM_NOT_INIT=0;
    GSM_INIT_OK=1;
    EMERGE_PHONES=0;
    emergePhones=["+79164603559"];
    numOfTries=0;
    def __init__(self,portNum1,portNum2):
        self.portNum1=portNum1;
        self.portNum2 = portNum2;
        self.port = 1;
        self.openSerial(self.portNum1);
    def send(self,phoneNumbersType,message):
        if (phoneNumbersType==self.EMERGE_PHONES):
            for phone in self.emergePhones:
                self.serialPort.write(b'AT+CMGS="' + phone.encode() + b'"\r')
                time.sleep(0.5)
                self.serialPort.write(message.encode() + b"\r")
                time.sleep(0.5)
                self.serialPort.write(bytes([26]))
                prt = self.serialPort.read(1024).decode();
                self.checkResponse(prt);
    def checkResponse(self,prt):
        prt=prt.replace('\r\n','');
        if (prt=="OK"):
            self.GSMStatus=GSMClass.GSM_INIT_OK;
        else:
            self.GSMStatus=GSMClass.GSM_NOT_INIT;
            self.addTry();
    def openSerial(self,portNum):
        self.serialPort=serial.Serial("COM"+str(portNum),baudrate=9600);
        self.serialPort.write(b'AT\r\n');
        self.serialPort.write(b'AT+CMGF=1\r\n');
        prt = self.serialPort.read(1024).decode();
        self.checkResponse(prt);
        if self.GSMStatus==GSMClass.GSM_INIT_OK and self.port==2:
            self.send(GSMClass.emergePhones,"Not enough money on 1st modem!!!");
    def addTry(self):
        self.numOfTries+=1;
        if self.numOfTries==3 and self.port==1:
            self.port=2;
            self.numOfTries += 1;
            self.serialPort.close();
            self.openSerial(self.portNum2);
        elif self.numOfTries==3 and self.port==2:
            self.GSMStatus=GSMClass.GSM_NOT_INIT;
        