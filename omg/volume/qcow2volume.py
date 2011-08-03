import subprocess
import os

from omg.storable import Storable
from omg.config import Config
from omg.volume import Volume
from omg.log.api import debug

class QCOW2Volume(Storable):
    def __init__(self, key=None):
        super(QCOW2Volume, self).__init__(key)
        self.conf = Config()

    def create(self, base=None):
        # basepath should be pulled from the base image Volume() object
        basepath = "%s/%s.img" % (self.conf['base_path'], base)
        imgpath = "%s/%s.img" % (self.conf['image_path'], self.key)

        imgcmd = ['qemu-img', 'create', '-b', basepath, '-f', 'qcow2', imgpath]
        retcode = subprocess.call(imgcmd)
        if retcode != 0:
            debug("Unable to create image")
            return
        self.data['path'] = imgpath

    def mount():
        '''
        qemu-nbd -c /dev/nbd[0-9] <image-file>
        mkdir /data/vms/mnt/<uuid>
        mount /dev/mbd[0-9]p1 /data/vms/mnt/<uuid>
        '''
        pass

    def umount():
        '''
        umount /data/vms/mnt/<uuid>
        rmdir /data/vms/mnt/<uuid>
        qemu-nbd -d /dev/nbd[0-9]
        '''
        pass

    def delete(self):
        path = "%s/%s.img" % (self.conf['image_path'], self.key)
        try:
            os.unlink(path)
        except OSError:
            pass
        super(QCOW2Volume, self).delete()


Volume.register(Volume, 'qcow2', QCOW2Volume)

