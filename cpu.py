#!/usr/bin/python
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import humanize
import argparse
import nagiosplugin
import logging
import os, sys


OK       = 0
WARNING  = 1
CRITICAL = 2
UNKNOWN =  3

def printHostInformation(host):
    try:
        summary = host.summary
        stats = summary.quickStats
        hardware = host.hardware
        cpu = hardware.cpuInfo
        cpuPackage = cpu.numCpuPackages
        cpuCores = cpu.numCpuCores
        cpuHz = cpu.hz
        cpuTotal = cpuHz*cpuCores*cpuPackage*0.000001
        cpuUsage = stats.overallCpuUsage
        cpuPercentage = (cpuUsage/cpuTotal)*100

        if  cpuPercentage < 60:
            return 0
        elif cpuPercentage >= 60 and cpuPercentage <= 80:
            return 1
        elif cpuPercentage > 80:
            return 2
        else:
            return 3
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return 4
        pass

def arg():
    parser = argparse.ArgumentParser(description="CPU Check")
    parser.add_argument('-cpu', help='percentage cpu usage' ,action="store_true")
    args = parser.parse_args()
    return args

def connect():
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    try:
        c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT')
        print('Valid certificate')
    except:
        c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT', sslContext=s)
        print('Invalid or untrusted certificate')


    datacenter = c.content.rootFolder.childEntity[0]
    vms = datacenter.hostFolder.childEntity
    list = []
    listHostOk = []
    listHostWarning = []
    listHostCritical = []
    listHostUnknown = []
    for i in vms:
        hosts = i.host
        a=0
        b=0
        c=0
        d=0
        for host in hosts:
            if printHostInformation(host) == 0:
                listHostOk.append(host)
                a +=1

            elif printHostInformation(host) == 1:
                listHostWarning.append(host)
                b +=1

            elif printHostInformation(host) == 2:
                listHostCritical.append(host)
                c +=1

            else:
                listHostUnknown.append(host)
                d +=1

    list.insert(1,a)
    list.insert(2,b)
    list.insert(3,c)
    list.insert(4,d)
    return list, listHostOk, listHostWarning, listHostCritical, listHostUnknown
    Disconnect(c)


def main():
    arg()

    t, lOk, lWarning, lCritical, lUnknown  = connect()

    print("liste Machine Ok")
            for x in range(len(lOk)):
                print(lOk[x],"\n")


    print("liste Machine Warning")
            for n in range(len(lWarning)):
                print(lWarning[n],"\n")

    print("liste Machine Critical")
            for o in range(len(lCritical)):
                print(lCritical[o],"\n")

    print("liste Machine Unknown")
            for o in range(len(lUnknown)):
                print(lUnknown[p],"\n")

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
