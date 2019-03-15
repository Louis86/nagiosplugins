#!/usr/bin/python
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import humanize
import argparse
import nagiosplugin
import logging
import os, sys


MBFACTOR = float(1 << 20)

OK       = 0
WARNING  = 1
CRITICAL = 2
UNKNOWN =  3

def printHostInformation(host):
    o,wmi,wma,c = arg()
    try:
        summary = host.summary
        stats = summary.quickStats
        hardware = host.hardware
        memoryCapacity = hardware.memorySize
        memoryCapacityInMB = hardware.memorySize/MBFACTOR
        memoryUsage = (float(stats.overallMemoryUsage) / memoryCapacityInMB)*100
        freeMemoryPercentage = 100 - (
                (float(memoryUsage) / memoryCapacityInMB) * 100
            )
        if  memoryUsage < o:
            return 0, memoryUsage
        elif memoryUsage >= wmi and memoryUsage <= wma:
            return 1, memoryUsage
        elif memoryUsage > c:
            return 2, memoryUsage
        else:
            return 3, memoryUsage
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return none, none
        pass

def arg():
    parser = argparse.ArgumentParser(description="Memory Check")
    parser = argparse.ArgumentParser(description="Plugin shows the memory state in terms of memory percentage")
    parser.add_argument('-Ok',dest="memoryOKmax" ,help="percentage Maximum of memory OK : state Ok", type=int ,required=True,choices=range(100))
    parser.add_argument('-wMin',dest="warningMin" ,help="percentage Minimum of memory warning : state warning Minimum", type=int ,required=True,choices=range(100))
    parser.add_argument('-wMax',dest="warningMax" ,help="percentage Maximum of memory : state warning : state warning Maximum", type=int ,required=True,choices=range(100))
    parser.add_argument('-cMin',dest="criticalMin" ,help="percentage Minimum of memory :  state critical", type=int ,required=True,choices=range(100))
    args = parser.parse_args()
    return args.memoryOKmax, args.warningMin, args.warningMax, args.criticalMin

def connect():
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    try:
        c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT')
        #print('Valid certificate')
    except:
        c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT', sslContext=s)
        #print('Invalid or untrusted certificate')


    datacenter = c.content.rootFolder.childEntity[0]
    vms = datacenter.hostFolder.childEntity
    list = []
    listHostOk = []
    listHostWarning = []
    listHostCritical = []
    listHostUnknown = []


    muOk = []
    muWarning = []
    muCritical = []
    muUnknown = []

    for i in vms:
        hosts = i.host
        a=0
        b=0
        c=0
        d=0
        for host in hosts:
            p, mu = printHostInformation(host)

            if  p == 0:
                listHostOk.append(host)
                muOk.append(mu)
                a +=1
            elif p == 1:
                listHostWarning.append(host)
                muWarning.append(mu)
                b +=1
            elif p == 2:
                listHostCritical.append(host)
                muCritical.append(mu)
                c +=1
            else:
                listHostUnknown.append(host)
                muUnknown.append(mu)
                d +=1

    list.insert(1,a)
    list.insert(2,b)
    list.insert(3,c)
    list.insert(4,d)
    return list, listHostOk, listHostWarning, listHostCritical, listHostUnknown, muOk, muWarning, muCritical, muUnknown
    Disconnect(c)


def main():
    t, lOk, lWarning, lCritical, lUnknown, mO, mW, mC, mU  = connect()

    print("Computer number",len(lOk)+len(lWarning)+len(lCritical)+len(lUnknown), "OK:",len(lOk), "WARNING:",len(lWarning), "CRITICAL :",len(lCritical),"UNKNOWN :",len(lUnknown),"\n")
    print("list Computer Ok")
    for x in range(len(lOk)) :
        print(lOk[x],"RAM memory used \t",mO[x],"%")


    print("\n list Computer Warning")
    for n in range(len(lWarning)):
        print(lWarning[n],"RAM memory used \t",mW[n],"%")



    print("\n list Computer Critical")
    for o in range(len(lCritical)):
        print(lCritical[o],"RAM memory used \t",mC[o],"%")


    print("\n list Computer Unknown")
    for p in range(len(lUnknown)):
        print(lUnknown[p],"RAM memory used \t",mU[x],"%")


    if  t[2] != 0:
        sys.exit(CRITICAL)
    elif t[1] != 0:
        sys.exit(WARNING)
    elif t[3] != 0:
        sys.exit(UNKNOWN)
    else:
        sys.exit(OK)

if __name__ == '__main__':
    main()
