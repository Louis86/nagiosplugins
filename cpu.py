#!/usr/bin/python3.5
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

#function which conncect to host and check the cpu usage after return two values : number and percentage cpu used
#number 0 if 0K , 1 if warning , 2 if critical and 3 unknown
def printHostInformation(host):
    ga= GetArgs()
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
        f= (cpuUsage/cpuTotal)*100
        cpuPercentage = round(f,2)
        if  cpuPercentage < ga.warning:
            return 0, cpuPercentage
        elif cpuPercentage >= ga.warning and cpuPercentage <= ga.critical:
            return 1, cpuPercentage
        elif cpuPercentage > ga.critical:
            return 2 ,cpuPercentage
        else:
            return 3,cpuPercentage
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return 4
        pass


# Receive and verifies arguments
#
def GetArgs():
    parser = argparse.ArgumentParser(description="Plugin shows the cpu state in terms of cpu percentage")
    parser.add_argument('-H', '--host', required=True, action='store', help='Remote host to connect to')
    parser.add_argument('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=True, action='store',help='Password to use when connecting to host')
    parser.add_argument('-w','--warning' , type=int ,required=True,choices=range(100),help="threshold of cpu warning : state warning ")
    parser.add_argument('-c','--critical' , type=int ,required=True,choices=range(100),help="threshold of cpu critical:  state critical")
    args = parser.parse_args()
    return args

#Connect to server and check all the hosts return list of Host and their state : Ok , warning , critical, unknown and the cpu usage for each state
def connect():
    args = GetArgs()
    #s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    #s.verify_mode = ssl.CERT_NONE
    try:
        c = SmartConnect(host=args.host, user=args.user, pwd=args.password)
        #print('Valid certificate')
    except:
        c = SmartConnect(host=args.host, user=args.user, pwd=args.password)
        #print('Invalid or untrusted certificate')


    datacenter = c.content.rootFolder.childEntity[0]
    vms = datacenter.hostFolder.childEntity
    list = []
    listHostOk = []
    listHostWarning = []
    listHostCritical = []
    listHostUnknown = []
    cpuOk = []
    cpuWarning = []
    cpuCritical = []
    cpuUnknown = []
    for i in vms:
        hosts = i.host
        a=0
        b=0
        c=0
        d=0
        for host in hosts:
            p, cpu = printHostInformation(host)
            if p == 0:
                listHostOk.append(host)
                cpuOk.append(cpu)
                a +=1

            elif p == 1:
                listHostWarning.append(host)
                cpuWarning.append(cpu)
                b +=1

            elif p == 2:
                listHostCritical.append(host)
                cpuCritical.append(cpu)
                c +=1

            else:
                listHostUnknown.append(host)
                cpuUnknown.append(cpu)
                d +=1

    list.insert(1,a)
    list.insert(2,b)
    list.insert(3,c)
    list.insert(4,d)
    return list, listHostOk, listHostWarning, listHostCritical, listHostUnknown, cpuOk, cpuWarning, cpuCritical, cpuUnknown
    Disconnect(c)

#main function to print all host in the server
#for each state of host  print the name of host and cpu usage
#return number in system.exit
def main():
    t, lOk, lWarning, lCritical, lUnknown, cO, cW, cC, cU = connect()

    print("Number of host",len(lOk)+len(lWarning)+len(lCritical)+len(lUnknown), "OK:",len(lOk), "WARNING:",len(lWarning), "CRITICAL :",len(lCritical),"UNKNOWN :",len(lUnknown),"\n")
    print("list host Ok")
    for x in range(len(lOk)) :
        print(lOk[x],"CPU used ",cO[x],"%")


    print("\n list host Warning")
    for n in range(len(lWarning)):
        print(lWarning[n],"cpu used \t",cW[n],"%")



    print("\n list host Critical")
    for k in range(len(lCritical)):
        print(lCritical[k],"CPU  used\t",cC[k],"%")


    print("\n list host Unknown")
    for p in range(len(lUnknown)):
        print(lUnknown[p],"CPU  used \t",cU[p],"%")

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
