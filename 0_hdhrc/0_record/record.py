import subprocess
import argparse
import pandas as pd

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

    def hdtune(self, phys, sub):
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
        self.hdtune(phys, sub)


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


def main():
    get_args()
    hdctl = HDCTL()

    hdctl.tune(46.2)


main()
