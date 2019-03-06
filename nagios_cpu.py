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

        if  cpuPercentage < 60:
            #sys.exit(OK)
            #print(OK)
            print(cpuPercentage)
        elif cpuPercentage >= 60 and cpuPercentage <= 80:
            print(cpuPercentage)
            #sys.exit(WARNING)
        elif cpuPercentage > 80:
            print(cpuPercentage)
            #sys.exit(CRITICAL)
        else:
            print(cpuPercentage)
            #sys.exit(UNKNOWN )
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return none
        pass


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
        for host in hosts:
            print(host.name)
            printHostInformation(host)
    Disconnect(c)


def main():
    connect()

if __name__ == '__main__':
    main()
