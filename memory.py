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
        memoryCapacity = hardware.memorySize
        memoryCapacityInMB = hardware.memorySize/MBFACTOR
        memoryUsage = (float(stats.overallMemoryUsage) / memoryCapacityInMB)*100
        freeMemoryPercentage = 100 - (
                (float(memoryUsage) / memoryCapacityInMB) * 100
            )
        if  memoryUsage < 60:
            return 0
        elif memoryUsage >= 60 and memoryUsage <= 80:
            return 1
        elif memoryUsage > 80:
            return 2
        else:
            return 3
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return none
        pass

def arg():
    parser = argparse.ArgumentParser(description="Memoory Check")
    parser.add_argument('-mem', help='percentage memory usage' ,action="store_true")
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
            if printHostInformation(host) == 0:
                a +=1
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
    t = connect()
    print(t)
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
