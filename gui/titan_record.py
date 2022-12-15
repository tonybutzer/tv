#! 
import sys
import os
from record_classes import rec_main

program = sys.argv[1]

print(program)

os.chdir('/home/tony/opt/tv/gui')

rec_main(program)
