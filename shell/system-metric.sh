#!/bin/bash
##
# A Shell script to get system metrics such as load, memory, and storage.
##

# Only allow root user to execute the script.
if [ `whoami` == 'root' ]; then
  sleep 1;
else
  printf "Please run this script as root or sudo.\n\n";
  exit 1;
fi

# Get system load metrics.
function load() {
  read -p "Enter time span of system load (1,5,15):" time;
  if [ $time -eq 1 ]; then
    output=$(uptime | awk '{print $10}' | sed 's/,//');
  elif [ $time -eq 5 ]; then
    output=$(uptime | awk '{print $11}' | sed 's/,//');
  elif [ $time -eq 15 ]; then
    output=$(uptime | awk '{print $12}' | sed 's/,//');
  else
    printf "OOPS! Invalid input.\n";
    exit 1;
  fi
  printf "The average system load for last $time minute is $output.\n";
}

# Get system memory metrics.
function memory() {
  read -p "Enter usage category of system memory (total,used,free):" usage;
  if [ $usage == 'total' ]; then
    output=$(free -m | grep 'Mem' | awk '{print $2}');
  elif [ $usage == 'used' ]; then
    output=$(free -m | grep 'Mem' | awk '{print $3}');
  elif [ $usage == 'free' ]; then
    output=$(free -m | grep 'Mem' | awk '{print $4}');
  else
    printf "OOPS! Invalid input.\n";
    exit 1;
  fi
  printf "The $usage system memory is $output MB.\n";
}

# Get system storage metrics.
function storage() {
  read -p "Enter usage category of system storage (total,used,free):" usage;
  if [ $usage == 'total' ]; then
    output=$(df -Th | grep '/dev/sda1' |  awk '{print $3}' | sed 's/G//');
  elif [ $usage == 'used' ]; then
    output=$(df -Th | grep '/dev/sda1' |  awk '{print $4}' | sed 's/G//');
  elif [ $usage == 'free' ]; then
    output=$(df -Th | grep '/dev/sda1' |  awk '{print $5}' | sed 's/G//');
  else
    printf "OOPS! Invalid input.\n";
    exit 1;
  fi
  printf "The $usage system storage is $output GB.\n";
}

# Choose a system metric.
case $1 in
  load)
    load;
    ;;
  memory)
    memory;
    ;;
  storage)
    storage;
    ;;
  *)
    echo "Usage: ./system-metric.sh {load|memory|storage}"
    exit 1;
    ;;
esac
