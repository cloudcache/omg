from uuid import uuid4

def uniq_mac():
    mac = ['BA','DB','AD']
    bits = "".join(str(uuid4()).split('-'))
    for i in range(3):
        mac.append(bits[0+(2*i):(0+(2*i))+2])
    return ":".join(mac)
