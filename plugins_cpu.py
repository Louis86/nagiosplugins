from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import humanize


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
