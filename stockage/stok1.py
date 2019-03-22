from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
#import humanize


# Method that populates objects of type vimtype
def get_all_objs(content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
                obj.update({managed_object_ref: managed_object_ref.name})
        return obj



s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
s.verify_mode = ssl.CERT_NONE

try:
    c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT')
    print('Valid certificate')
except:
    c = SmartConnect(host="pcc-5-196-231-40.ovh.com", user="louisilogs", pwd='R1hi7YqT', sslContext=s)
    print('Invalid or untrusted certificate')

#Calling above method
getAllVms=get_all_objs(c, [vim.VirtualMachine])


#Iterating each vm object and printing its name
for vm in getAllVms:
        print vm.name

Disconnect(c)
