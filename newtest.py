from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
#import humanize


MBFACTOR = float(1 << 20)


def printHostInformation(host):
    try:
        summary = host.summary
        stats = summary.quickStats
        storage = stats.storage
        hardware = host.hardware
        cpu = hardware.cpuInfo
        cpuPackage = cpu.numCpuPackages
        cpuCores = cpu.numCpuCores
        cpuHz = cpu.hz
        cpuTotal = cpuHz*cpuCores*cpuPackage*0.000001
        cpuUsage = stats.overallCpuUsage
        cpuPercentage = (cpuUsage/cpuTotal)*100
        memoryCapacity = hardware.memorySize
        memoryCapacityInMB = hardware.memorySize/MBFACTOR
        memoryUsage = stats.overallMemoryUsage
        freeMemoryPercentage = 100 - (
            (float(memoryUsage) / memoryCapacityInMB) * 100
        )
        print("------------------------------------------------")
        print("Host name: ", host.name)
        print("Hardware",hardware)
        print("Storage :", storage)
        print("NumCPU", cpu)
        print("cpu Package", cpuPackage)
        print("cpu cores", cpuCores)
        print("Host CPU usage: ", cpuUsage)
        print("frequence", cpuHz)
        print("frequence totale",cpuTotal )
        print("CPU percentage",cpuPercentage)
        print("Host memory capacity: ", humanize.naturalsize(memoryCapacity, binary=True))
        print("Host memory usage: ", memoryUsage / 1024, "GiB")
        print("Free memory percentage: " + str(freeMemoryPercentage) + "%")
        print("--------------------------------------------------")
    except Exception as error:
        print("Unable to access information for host: ", host.name)
        print(error)
        pass




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

for i in vms:
    print(i.name)
    hosts = i.host
    for host in hosts:
        print(host.name)
        printHostInformation(host)

Disconnect(c)
