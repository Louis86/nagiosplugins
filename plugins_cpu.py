#!/usr/bin/python

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import humanize

MBFACTOR = float(1 << 20)


def CpuInformation(host):
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
        return cpuPercentage
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        return none
        pass
try:
    c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT')
    print('Valid certificate')
except:
    c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT', sslContext=s)
    print('Invalid or untrusted certificate')

datacenter = c.content.rootFolder.childEntity[0]
vms = datacenter.hostFolder.childEntity

for i in vms:
    print(i.name)
    hosts = i.host
    for host in hosts:
        print(host.name)
        print(CpuInformation)

Disconnect(c)
