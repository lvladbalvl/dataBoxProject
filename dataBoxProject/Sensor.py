# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 16:38:19 2017

@author: vlad
"""
from collections import defaultdict

class Sensor:
    sensIdx = defaultdict(list)
    numOfSensors=0;
    def __init__(self,lowBorder,highBorder,Type,ID,fileName):
        self.lowBorder=lowBorder;
        self.highBorder=highBorder;
        self.Type=Type;
        self.ID=ID;
        self.fileName=fileName;
        self.status="Undefined"
        Sensor.sensIdx[ID].append(self);
        #Sensor.addSensor();
        #self.idx=Sensor.getIdx();
    def setStatus(self,status):
        self.status=status;
    def getStatus(self):
        return self.status;
    def getBorders(self):
        return self.lowBorder,self.highBorder;
    def getID(self):
        return self.ID;
    def getfileName(self):
        return self.fileName;
    def __eq__(self,other):
        if self.ID==other.ID:
            return True
        else:
            return False;
    @classmethod
    def find_by_ID(cls, ID):
        return Sensor.sensIdx[ID]
    # @staticmethod
    # def addSensor():
    #     Sensor.numOfSensors+=1;
    # @staticmethod
    # def getIdx():
    #     return Sensor.numOfSensors;