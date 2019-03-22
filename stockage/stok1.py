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


def informationStorage(storage):
    try:
        summary = storage.summary
        fs    = round(float(summary.freeSpace/1000000000), 2)
        sc = round(float(summary.capacity/1000000000), 2)
        percentage =round( (fs/sc)*100, 2)
        if  percentage < ga.warning:
            return 0, percentage , fs
        elif percentage >= ga.warning and percentage <= ga.critical:
            return 1, percentage , fs
        elif percentage > ga.critical:
            return 2 ,percentage , fs
        else:
            return 3,percentage ,fs
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return 4
        pass
# Receive and verifies arguments
#
def GetArgs():
    parser = argparse.ArgumentParser(description="Plugin shows the cpu state in terms of storage percentage")
    parser.add_argument('-H', '--host', required=True, action='store', help='Remote host to connect to')
    parser.add_argument('-u', '--user', required=True, action='store', help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=True, action='store',help='Password to use when connecting to host')
    parser.add_argument('-w','--warning' , type=int ,required=True,choices=range(100),help="threshold of storage used  warning : state warning ")
    parser.add_argument('-c','--critical' , type=int ,required=True,choices=range(100),help="threshold of storage critical:  state critical")
    args = parser.parse_args()
    return args


#Connect to server and check all the hosts return list of Host and their state : Ok , warning , critical, unknown and the cpu usage for each state
def connect():
    args = GetArgs()
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    try:
        c = SmartConnect(host=args.host, user=args.user, pwd=args.password, sslContext=s)

    except IOError as e:
        print("Could not connect to datastore" + str(e))
    datacenter = c.content.rootFolder.childEntity[0]
    ds = datacenter.datastore

    list = []
    listStorageOk = []
    listStorageWarning = []
    listStorageCritical = []
    listStorageUnknown = []

    StorageOk = []
    StorageWarning = []
    StorageCritical = []
    StorageUnknown = []

    freeStorageOk = []
    freeStorageWarning = []
    freeStorageCritical = []
    freeStorageUnknown = []

    a=0
    b=0
    c=0
    d=0

    for i in ds:
        print(i.name)
        nbr, percent, freeS = informationStorage(i)
        if nbr == 0:
            listStoragOk.append(i)
            freeStorageOk.append(freeS)
            StorageOk.append(percent)
            a +=1

        elif nbr == 1:
            listStorageWarning.append(i)
            freeStorageWarning.append(freeS)
            StorageOk.append(percent)
            b +=1

        elif nbr == 2:
            listStoragCritical.append(i)
            freeStorageCritical.append(freeS)
            StorageOk.append(percent)
            c +=1

        else:
            listStoragUnknown.append(i)
            freeStorageUnknown.append(freeS)
            StorageOk.append(percent)
            d +=1
    Disconnect(c)
