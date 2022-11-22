import sys, os.path
from subprocess import Popen, PIPE


def channel_iter(file):
    for line in file:
        if line.startswith("SCANNING: "):
            channel = line.split()[2].strip('()')
            channel = channel.split(':')[1]
        elif line.startswith("LOCK: "):
            modulation = line.split()[1]
        elif line.startswith("PROGRAM "):
            (PROGRAM, subchannel, vchannel, name) = line.split(None, 3)
            subchannel = subchannel.rstrip(':')
            name = name.strip()     # remove new line
            name = name.replace(' ', '-')
            yield (vchannel, modulation, channel, subchannel, name)

def channel_info(hdhomerun_config, device_id, tuner):
    import tempfile

    f = tempfile.TemporaryFile("w+")
    cmd = [hdhomerun_config, device_id, "scan", "/tuner%s" % tuner] 
    p = Popen(cmd, stdout=f)
    p.wait()
    f.seek(0)
    return list(channel_iter(f))

class HDHR:
    def __init__(self):
        self.hdhomerun_config = "/usr/bin/hdhomerun_config"
        # self.get_hdhomerun_config()
        # self.get_deviceid()
    # def get_hdhomerun_config(self):
        # msg = "Please provide path to hdhomerun_config binary"
        # answer = get_input(msg, validate_executable)
        # self.hdhomerun_config = os.path.abspath(answer)
    def get_deviceid(self):
        cmd = [self.hdhomerun_config, "discover"]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print(out)
        # Check status rather than err file!
        if err:
            err = err.decode()
            sys.exit("Unable to run command: '%s' % cmd, error: 'err'" % (cmd,
                     err), "bailing out")
        out = out.decode().strip()
        if out.find("no devices found") != -1:
            sys.exit("Unable to find any hdhomerun device")
        out = out.split('\n')
        if len(out) == 1:
            import re
            mo = re.match("hdhomerun device (\S+) found", out[0])
            if mo:
                self.deviceid = mo.group(1)
            else:
                sys.exit("Unable to parse command: '%s' output:%s" % (cmd,
                    out[0]))
        else:
            msg = "You have multiple hdhomerun adapters. Disconnect all of "
            msg += "them except the one you want to use for recording and "
            msg += "then re-run this program."
            sys.exit(msg)
        return(self.deviceid)

def main():
    hdhr = HDHR()
    deviceid = hdhr.get_deviceid()
    print (deviceid)
    hdhomerun_config = "/usr/bin/hdhomerun_config"
    tuner = 0
    
    channels = channel_info(hdhomerun_config, deviceid, tuner)

    for c in channels:
        print(c)

    

main()
