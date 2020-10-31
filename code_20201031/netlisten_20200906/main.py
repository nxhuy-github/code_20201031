import sys
import subprocess 
import os
from decouple import config

# IP_NETWORK = config('IP_NETWORK')
# IP_DEVICE = None

# proc = subprocess.Popen(["ping", IP_NETWORK], stdout=subprocess.PIPE)
# while True:
#     line = proc.stdout.readline()
#     if not line:
#         break
#     connected_ip = line.decode('utf-8')#.split()[3]
#     print(connected_ip)

# nmap = subprocess.Popen('nmap', stdout=subprocess.PIPE)
# ipout = nmap.communicate()[0]
# print(ipout)

from wifi import Cell, Scheme
import nmap
print(list(Cell.all('wlp6s0')))