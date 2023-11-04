#!/usr/bin/python
##
# A Python script to get system metrics such as load, memory, and storage.
##

# Import community modules.
import os
import sys
import time
import subprocess


# Only allow root user to execute the script.
if os.geteuid()==0:
  time.sleep(1)
else:
  print('Please run this script as root or sudo.')
  sys.exit(1)

# Get system load metrics.
def load():
  print('Enter time span of system load (1,5,15):')
  time = int(input())
  if time==1:
    output = os.getloadavg()[0]
  elif time==5:
    output = os.getloadavg()[1]
  elif time==15:
    output = os.getloadavg()[2]
  else:
    print('OOPS! Invalid input.')
    sys.exit(1)
  print('The average system load for last %i minute is %s.' %(time,output))

# Get system memory metrics.
def memory():
  print('Enter usage category of system memory (total,used,free):')
  usage = input()
  if usage=='total':
    output = subprocess.check_output("free -m | grep 'Mem' | awk '{print $2}'",shell=True).strip()
  elif usage=='used':
    output = subprocess.check_output("free -m | grep 'Mem' | awk '{print $3}'",shell=True).strip()
  elif usage=='free':
    output = subprocess.check_output("free -m | grep 'Mem' | awk '{print $4}'",shell=True).strip()
  else:
    print('OOPS! Invalid input.')
    sys.exit(1)
  print('The %s system memory is %s MB.' %(usage,output.decode()))

# Get system storage metrics.
def storage():
  print('Enter usage category of system storage (total,used,free):')
  usage = input()
  if usage=='total':
    output = subprocess.check_output("df -Th | grep '/dev/sda1' | awk '{print $3}' | sed 's/G//'",shell=True).strip()
  elif usage=='used':
    output = subprocess.check_output("df -Th | grep '/dev/sda1' | awk '{print $4}' | sed 's/G//'",shell=True).strip()
  elif usage=='free':
    output = subprocess.check_output("df -Th | grep '/dev/sda1' | awk '{print $5}' | sed 's/G//'",shell=True).strip()
  else:
    print('OOPS! Invalid input.')
    sys.exit(1)
  print('The %s system storage is %s GB.' %(usage,output.decode()))

# Choose a system metric.
if sys.argv[1]=='load':
  load()
elif sys.argv[1]=='memory':
  memory()
elif sys.argv[1]=='storage':
  storage()
else:
  print('Usage: ./system-metric.py {load|memory|storage}')
  sys.exit(1)
