#!/usr/bin/ruby
##
# A Ruby script to get system metrics such as load, memory, and storage.
##


# Only allow root user to execute the script.
if Process::euid==0
  sleep(1)
else
  print "Please run this script as root or sudo.\n"
  exit(1)
end

# Get system load metrics.
def load()
  print 'Enter time span of system load (1,5,15):'
  time = $stdin.gets.to_i
  if time==1
    output = `cat /proc/loadavg | awk '{print $1}'`
  elsif time==5
    output = `cat /proc/loadavg | awk '{print $2}'`
  elsif time==15
    output = `cat /proc/loadavg | awk '{print $3}'`
  else
    print "OOPS! Invalid input.\n"
    exit(1)
  end
  print "The average system load for last #{time} minute is #{output.strip}.\n"
end

# Get system memory metrics.
def memory()
  print 'Enter usage category of system memory (total,used,free):'
  usage = $stdin.gets
  if usage.include?'total'
    output = `free -m | grep 'Mem' | awk '{print $2}'`
  elsif usage.include?'used'
    output = `free -m | grep 'Mem' | awk '{print $3}'`
  elsif usage.include?'free'
    output = `free -m | grep 'Mem' | awk '{print $4}'`
  else
    print "OOPS! Invalid input.\n"
    exit(1)
  end
  print "The #{usage.strip} system memory is #{output.strip} MB.\n"
end

# Get system storage metrics.
def storage()
  print 'Enter usage category of system storage (total,used,free):'
  usage = $stdin.gets
  if usage.include?'total'
    output = `df -Th | grep '/dev/sda1' | awk '{print $3}' | sed 's/G//'`
  elsif usage.include?'used'
    output = `df -Th | grep '/dev/sda1' | awk '{print $4}' | sed 's/G//'`
  elsif usage.include?'free'
    output = `df -Th | grep '/dev/sda1' | awk '{print $5}' | sed 's/G//'`
  else
    print "OOPS! Invalid input.\n"
    exit(1)
  end
  print "The #{usage.strip} system storage is #{output.strip} MB.\n"
end

# Choose a system metric.
case ARGV[0]
  when 'load'
    load()
  when 'memory'
    memory()
  when 'storage'
    storage()
  else
    print "Usage: ./system-metric.rb {load|memory|storage}\n"
    exit(1)
end
