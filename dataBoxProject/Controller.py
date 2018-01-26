# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 17:13:08 2017

@author: vlad
"""

from GSMClass import GSMClass
from ReceiverClass import ReceiverClass 
from SenderClass import SenderClass
from Sensor import Sensor
class Controller:
    EMERGE_PHONES=0;
    LOC_LAN_NOT_OK=0;
    VPN_NOT_OK=1;
    ANALYSIS_BAD=2;
    def __init__(self,IP_LOCAL,IP_VPN,portVPN):
        self.saveFlag=0;
        self.IP_LOCAL=IP_LOCAL;
        self.IP_VPN=IP_VPN;
        self.sensorsList=[];
        self.sensSaveList=[];
        self.initSensorList();
        try:
            self.GSM=GSMClass(3,6);
        except:
            print("GSM skipped");
        
        self.Receiver=ReceiverClass(1,self.IP_LOCAL,portNumber=9090);

        if (not self.Receiver.getStatus()):
            message=self.messageConstruct(Controller.LOC_LAN_NOT_OK,error=self.Receiver.getError());
            self.GSM.send(Controller.EMERGE_PHONES,message);
            self.ftpStatus=False;
        try:
            self.Sender=SenderClass(IP_VPN,portVPN);
            if (not self.Sender.getStatus()):
                self.VPNstatus=False;
                message=self.messageConstruct(self.VPN_NOT_OK,error=self.Sender.getError());
                self.GSM.send(self.EMERGE_PHONES,message);
        except:
            print("Sender skipped");
        try:
            self.Analyzer=AnalyzerClass();
        except:
            print("Analyzer skipped")
    def DataReceiveSend(self):
        while (True):
            data=self.Receiver.readData(self.sensorsList);
            report,reportStatus=self.checkData(data);
            self.updateSaveList(report);
            if (self.saveFlag):
                self.saveData(self.sensSaveList,data);
            self.Sender.sendData(data);
            #analStatus, analyzeResults=self.Analyzer.checkData(data);
            if reportStatus:
                message=self.messageConstruct(Controller.ANALYSIS_BAD,report=report);
                self.GSM.send(Controller.EMERGE_PHONES,message);
    def initSensorList(self):
        with open("sensors.txt","r") as sensFile:
                for line in sensFile:
                    sensSpecs=line.split(',');
                    print(sensSpecs);
                    sensor=Sensor(float(sensSpecs[0]),float(sensSpecs[1]),sensSpecs[2],sensSpecs[3],sensSpecs[4])
                    self.sensorsList.append(sensor);
    def getSensorList(self):
        return self.sensorsList;
    def DataReceiveAndStore(self):
        data=self.Receiver.readData(self.sensorsList);
        report=self.checkData(data);
        self.updateSaveList(report);
        for dataUnit in data:        
            with open("sensorValue"+dataUnit[0].getID()+".txt","a") as sensValFile:
                sensValFile.write(str(dataUnit[1])+"\r\n");
    def closeReceiverConnection(self):
        self.Receiver.closeConnection();
    def checkData(self,data):
        report=[];
        reportStatus=True;
        for dataUnit in data:
            report.append({"sensor":dataUnit[0],"status":None});
            lB,hB=dataUnit[0].getBorders();
            if (dataUnit[1]>lB) and (dataUnit[1]>hB):
                report[-1]["status"]="green";
            elif (dataUnit[1]<lB) or (dataUnit[1]>hB):
                report[-1]["status"]="red";
                reportStatus=False;
            else:
                report[-1]["status"]="NaN";
                reportStatus = False;
            idx=self.sensorsList.index(dataUnit[0]);
            self.sensorsList[idx].setStatus(report[-1]["status"]);
        return report,reportStatus;
    def messageConstruct(self,code,**kwargs):
        message='';
        if code==Controller.LOC_LAN_NOT_OK:
            message="Local connection not working:"+kwargs["error"];
        elif code==Controller.VPN_NOT_OK:
            message="VPN not working:"+kwargs["error"]
        elif code==Controller.ANALYSIS_BAD:
            message="Bad data from sensors:\r\n";
            for reportUnit in kwargs["report"]:
                message=message+reportUnit["sensor"]+" received status "+reportUnit["status"]+";\r\n";
        return message;
    def updateSaveList(self,report):
        for reportUnit in report:
            if reportUnit["status"]=="red":
                self.sensSaveList.append(reportUnit["sensor"]);
    def saveData(self,sensorList,data):
       for dataUnit in data:
           if dataUnit[0] in sensorList: #find sensor in sensorList?
                with open("sensorValue"+dataUnit[0].getID()+".txt","a") as sensValFile:
                    sensValFile.write(str(dataUnit[1])+"\r\n");
    def testSendSMS(self):
        self.GSM.send(Controller.EMERGE_PHONES,"test");