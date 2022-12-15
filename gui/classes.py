""" classes.py

    - TITAN
    - HDCTL

    ... more to come ...

"""
import pandas as pd

import subprocess
from subprocess import Popen, PIPE
import argparse
import pandas as pd
import xmltodict

from zoneinfo import ZoneInfo
from datetime import datetime, timezone, timedelta
import pandas as pd


class CHANNEL:
    def __init__(self):
        print('channel')
        self.df = pd.read_csv('channels.csv')
        print(self.df.head())
        print('hello')
        
    def scan(self):
        hdhr = HDHR()
        deviceid = hdhr.get_deviceid()
        print (deviceid)
        hdhomerun_config = "/usr/bin/hdhomerun_config"
        tuner = 0

        channels = channel_info(hdhomerun_config, deviceid, tuner)

        for c in channels:
            print(', '.join(c))

        sourceFile = open('channels.csv', 'w')
        print('human_channel, freq, phys, sub, station')
        print('human_channel,freq,phys,sub,station', file=sourceFile)
        for c in channels:
            print(', '.join(c), file=sourceFile)

        sourceFile.close()

    def phys(self,human_channel):
        mydf = self.df[self.df['human_channel'] == human_channel]
        #_df1 = mydf[['phys', 'sub']]
        print(mydf)
        print(mydf['phys'])
        print(mydf['sub'])

        return str(mydf['phys'].values[0]), str(mydf['sub'].values[0])

  
        


class TITAN:

    def _convert_gmt_local(self, date, time):
        mytime = f"{date} {time} GMT"
        dtobj = datetime.strptime(mytime, '%Y%m%d %H:%M %Z')
        dtobj = dtobj.replace(tzinfo=timezone.utc)
        dtobj = dtobj.astimezone(ZoneInfo('US/Central'))
        a = dtobj
        # print(a.strftime('%Y%m%d%H%M'))
        return(a.strftime('%Y%m%d%H%M'))

    def _set_local_start_stop(self):
        #print(self.doc)
        self.gmt_start_time= self.doc['tv-program-info']['program']['start-time']
        self.gmt_start_date= self.doc['tv-program-info']['program']['start-date']
        self.gmt_end_time= self.doc['tv-program-info']['program']['end-time']
        self.gmt_end_date= self.doc['tv-program-info']['program']['end-date']
        self.start_time_s = self._convert_gmt_local(self.gmt_start_date, self.gmt_start_time)
        self.start_date_s = self.start_time
        self.end_timei_s = self._convert_gmt_local(self.gmt_end_date, self.gmt_end_time)



    def __init__(self, file):
        # print('init')
        with open(file) as fd:
            self.doc = xmltodict.parse(fd.read())
        status = self._set_local_start_stop()



    def title(self):
        _title = self.doc['tv-program-info']['program']['program-title'].replace(' ', '_')
        return _title

    def start_time(self):
        return self.start_time_s

    def start_date(self):
        return self.start_date_s

    def info(self):
        self.info = self.doc['tv-program-info']['program']
        print(self.info)

    def end_time(self):
        pass
    def end_date(self):
        pass

    def duration(self):
        _duration= self.doc['tv-program-info']['program']['duration']
        (hrs, minutes) = _duration.split(':')
        my_minutes = int(hrs)* 60 + int(minutes)
        return my_minutes

    def human_channel(self):
        psip_major = self.doc['tv-program-info']['program']['psip-major']
        psip_minor = self.doc['tv-program-info']['program']['psip-minor']
        human_channel = f'{psip_major}.{psip_minor}'
        print(human_channel)
        return float(human_channel)

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "__" + str(counter) + "_" + extension
        counter += 1

    return path

def get_files_titan_xml():
    dir_path = '/home/tony/tv/titan'
    res = os.listdir(dir_path)
    results = [i for i in res
              if i.endswith('xml')]
    fresults = []
    for file in results:
        fresults.append(f'{dir_path}/{file}')
    return fresults

def state_recording(program_xml):
    dir_path = '/home/tony/tv/titan/recording'
    filename = program_xml.split('/')[-1]
    newpath = f'{dir_path}/{filename}'
    os.rename(program_xml, newpath)
    return (newpath)

def get_channel_df(csvfile):
    df = pd.read_csv('channels.csv')
    return df


class HDCTL:
    def __init__(self):
        self.cdf = get_channel_df('channels.csv')
        print(self.cdf)
        cdf = self.cdf
        print(cdf.loc[cdf['human_channel'] == 46.2])
        self.device_id = '103AF69D'
        self.tuner = 0
        self.hdhomerun_config = '/usr/bin/hdhomerun_config'

    def set_hdtune(self, phys, sub):
        device_id = self.device_id
        tuner_num = str(self.tuner)
        hdhomerun_config = self.hdhomerun_config
        cmd = [hdhomerun_config, device_id, "set"]
        cmd.extend(["/tuner%s/channel" % tuner_num, str(phys)])
        subprocess.Popen(cmd).wait()

        cmd = [hdhomerun_config, device_id, "set"]
        cmd.extend(["/tuner%s/program" % tuner_num, str(sub)])
        subprocess.Popen(cmd).wait()

    def get_phys_sub(self, human_channel):
        """ this will get it from self.cdf row"""
        return(21, 4)

    def tune(self, human_channel):
        (phys, sub)=self.get_phys_sub(human_channel)
        self.set_hdtune(phys, sub)

    def get_hdtune(self):
        device_id = self.device_id
        tuner_num = str(self.tuner)
        hdhomerun_config = self.hdhomerun_config
        cmd = [hdhomerun_config, device_id, "get"]
        cmd.extend(["/tuner%s/channel" % tuner_num])
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print(out.decode("utf-8") )


        cmd = [hdhomerun_config, device_id, "get"]
        cmd.extend(["/tuner%s/program" % tuner_num])
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        print(out.decode("utf-8") )



def get_args():
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--device', type=str, required=True)
    parser.add_argument('--tuner', type=str, required=True)
    parser.add_argument('--channel', type=str, required=True)
    parser.add_argument('--filempg', type=str, required=True)
    
    # Parse the argument
    args = parser.parse_args()
    # Print "Hello" + the user input argument
    print('Hello,', args.device)


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
            try: 
                (PROGRAM, subchannel, vchannel, name) = line.split(None, 3)
                subchannel = subchannel.rstrip(':')
                name = name.strip()     # remove new line
                name = name.replace(' ', '-')
                yield (vchannel, modulation, channel, subchannel, name)
            except:
                pass

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


