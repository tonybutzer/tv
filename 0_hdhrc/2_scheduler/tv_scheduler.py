import sys
import time
import logging
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.schedulers.blocking.BlockingScheduler import BlockingScheduler
#import APScheduler
#from APScheduler.scheduler import Scheduler

def sendMessage():
    print(time.strftime("%Y-%m-%d %H:%M", time.localtime()))
    #print(my_arg)

def main():

    if len(sys.argv) != 2:
        sys.exit("usage: %s <config-file>" % sys.argv[0])

    try:
        from ConfigParser import ConfigParser
    except ImportError: # python3
        from configparser import ConfigParser

    try:
        config = ConfigParser(inline_comment_prefixes=(';',))
    except TypeError: # not python3
        config = ConfigParser()

    config.readfp(open(sys.argv[1]))

    logfilename = config.get("global", "logfile")

    FORMAT = "%(asctime)-15s: %(message)s"
    logging.basicConfig(level=logging.INFO, filename=logfilename, filemode='w',
                        format=FORMAT)

    logging.info("Configuration Completed tv_scheduler")


    scheduler = BackgroundScheduler()
    scheduler.add_job(sendMessage, 'cron', day_of_week='0-6', hour='*', minute='*')
    scheduler.start()

    while True:
        time.sleep(3)
        print('dog')


if __name__ == '__main__':
    main()
