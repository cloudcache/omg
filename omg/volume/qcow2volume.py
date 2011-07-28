import subprocess
import os
import omg

class QCOW2Volume(omg.storable.Storable):
    def __init__(self):
        super(QCOW2Volume, self).__init__()
        self.conf = omg.config.Config()


    def create(self, base=None):
        # basepath should be pulled from the base image Volume() object
        basepath = "%s/%s.img" % (self.conf['base_path'], base)
        imgpath = "%s/%s.img" % (self.conf['image_path'], self.key)

        imgcmd = ['qemu-img', 'create', '-b', basepath, '-f', 'qcow2', imgpath]
        retcode = subprocess.call(imgcmd)
        if retcode != 0:
            print "Unable to create image"
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


omg.volume.Volume.volumemap['qcow2'] = QCOW2Volume

