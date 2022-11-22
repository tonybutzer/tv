import sys, os, os.path
import subprocess
import signal, datetime
import logging
import heapq

from configparser import ConfigParser

def main():
    config = ConfigParser()

    config.readfp(open("example.config"))
    global logfile
    logfile = config.get("global", "logfile")
    FORMAT = "%(asctime)-15s: %(message)s"
    logging.basicConfig(level=logging.INFO, filename=logfile, filemode='w',
                        format=FORMAT)

    logging.info("play program begins")

    


if __name__ == '__main__':
    main()
