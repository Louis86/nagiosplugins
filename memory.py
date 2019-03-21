#!/usr/bin/python3.5
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
#function which conncect to host and check the memory usage after return two values : number and percentage memory used
#number 0 if 0K , 1 if warning , 2 if critical and 3 unknown
def printHostInformation(host):
    ga= GetArgs()
    try:
        summary = host.summary
        stats = summary.quickStats
        hardware = host.hardware
        memoryCapacity = hardware.memorySize
        memoryCapacityInMB = hardware.memorySize/MBFACTOR
        a = (float(stats.overallMemoryUsage) / memoryCapacityInMB)*100
        memoryUsage = round(a,2)
        freeMemoryPercentage = 100 - (
                (float(memoryUsage) / memoryCapacityInMB) * 100
            )
        if  memoryUsage < ga.warning:
            return 0, memoryUsage
        elif memoryUsage >= ga.warning and memoryUsage <= ga.critical:
            return 1, memoryUsage
        elif memoryUsage > ga.critical:
            return 2, memoryUsage
        else:
            return 3, memoryUsage
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return none, none
        pass
# Receive and verifies arguments
#
def GetArgs():
    parser = argparse.ArgumentParser(description="Plugin shows the memory state in terms of memory percentage")
    parser.add_argument('-H', '--host', required=True, action='store', help='Remote host to connect to')
    parser.add_argument('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=True, action='store',help='Password to use when connecting to host')
    parser.add_argument('-w','--warning' , type=int ,required=True,choices=range(100),help="percentage  of memory warning : state warning ")
    parser.add_argument('-c','--critical' , type=int ,required=True,choices=range(100),help="percentage Minimum of memory :  state critical")
    args = parser.parse_args()
    return args


#Connect to server and check all the hosts return list of Host and their state : Ok , warning , critical, unknown and the memory usage for each state
def connect():
    args = GetArgs()
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    try:
        c = SmartConnect(host=args.host, user=args.user, pwd=args.password)

    except IOError as e:
        print("Could not connect to cluster" + str(e))



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
#main function to print all host in the server
#for each state of host  print the name of host and memory usage
#return number in system.exit
def main():
    t, lOk, lWarning, lCritical, lUnknown, mO, mW, mC, mU  = connect()

    print("Host number",len(lOk)+len(lWarning)+len(lCritical)+len(lUnknown), "OK:",len(lOk), "WARNING:",len(lWarning), "CRITICAL :",len(lCritical),"UNKNOWN :",len(lUnknown),"\n")

    print("\n list host Critical")
    for o in range(len(lCritical)):
        print(lCritical[o],"RAM memory used \t",mC[o],"%")

    print("\n list host Warning")
    for n in range(len(lWarning)):
        print(lWarning[n],"RAM memory used \t",mW[n],"%")


    print("\n list host Unknown")
    for p in range(len(lUnknown)):
        print(lUnknown[p],"RAM memory used \t",mU[x],"%")


    print("list host Ok")
    for x in range(len(lOk)) :
        print(lOk[x],"RAM memory used \t",mO[x],"%")


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
