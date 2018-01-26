# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:01:14 2017

@author: vlad
"""

from Controller import Controller
C=Controller("192.168.137.1","192.168.1.217",80);
s=C.getSensorList();
#C.testSendSMS();
print(s[0].getStatus())
C.DataReceiveAndStore();
print(s[0].getStatus())
C.closeReceiverConnection();