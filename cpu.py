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

            #countOk = 0
            #countWarning = 0
            #countCritical = 0
            #countUnknown = 0

        if  cpuPercentage < 60:
            #countOk +=1
            #sys.exit(OK)
            #print("OK")
            #print(cpuPercentage)
            return 0
        elif cpuPercentage >= 60 and cpuPercentage <= 80:
            #print(cpuPercentage)
            #countWarning +=1
            #sys.exit(WARNING)
            return 1
        elif cpuPercentage > 80:
            #print(cpuPercentage)
            #coountCritical +=1
            #sys.exit(CRITICAL)
            return 2
        else:
            #print(cpuPercentage)
            #countUnknown +=1
            #sys.exit(UNKNOWN)
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

    for i in vms:
        hosts = i.host
        a=0
        b=0
        c=0
        d=0
        for host in hosts:
            #print(host.name)
            if printHostInformation(host) == 0:
                #print("OK")
                #sys.exit(0)
                a +=1
                #print(a)
            elif printHostInformation(host) == 1:
                print("WARNING")
                b +=1
            elif printHostInformation(host) == 2:
                print("CRITICAL")
                c +=1
            else:
                print("UNKNOWN")
                d +=1

    list.insert(1,a)
    list.insert(2,b)
    list.insert(3,c)
    list.insert(4,d)
    return list

    Disconnect(c)


def main():
    arg()
    #print(connect())
    print(connect().index(a))
    #if connect().index(1) != 0:
    #    sys.exit(CRITICAL)
    #elif t[2] != 0:
    #    sys.exit(WARNING)
    #elif t[4] != 0:
    #    sys.exit(UNKNOWN)
    #else t[1] != 0:
    #    sys.exit(OK)


if __name__ == '__main__':
    main()
