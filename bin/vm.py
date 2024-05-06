#!/usr/bin/python3
##
# -*- coding: utf-8 -*-
##
##
# Manage Linux-based virtual machines.
##

# Import community modules.
import os
import sys
import argparse
import subprocess
import vagrant


# VM controller.
class VM(object):

  # Initializer.
  def __init__(self,cwd=None):
    self.cwd = cwd

  # Validate OS name.
  @classmethod
  def validate_os_name(self,os_name):
    os_name_expected = [
      'alma-linux-8',
      'alma-linux-9',
      'amazon-linux-2',
      'centos-linux-7',
      'rocky-linux-8',
      'rocky-linux-9',
      'ubuntu-linux-18-04',
      'ubuntu-linux-22-04'
    ]
    if os_name not in os_name_expected:
      print('Current os_name:',os_name)
      raise argparse.ArgumentTypeError('os_name_expected values: "alma-linux-8", "alma-linux-9", "amazon-linux-2", "centos-linux-7", "rocky-linux-8", "rocky-linux-9", "ubuntu-linux-18-04", "ubuntu-linux-22-04"')
    return os_name

  # Validate hypervisor.
  @classmethod
  def validate_hypervisor(self,hypervisor):
    hypervisor_expected = ["virtualbox", "vmware"]
    if hypervisor not in hypervisor_expected:
      print('Current hypervisor:',hypervisor)
      raise argparse.ArgumentTypeError('hypervisor_expected values: "virtualbox", "vmware"')
    return hypervisor

  # Validate architecture.
  @classmethod
  def validate_architecture(self,architecture):
    architecture_expected = ["amd64", "arm64"]
    if architecture not in architecture_expected:
      print('Current architecture:',architecture)
      raise argparse.ArgumentTypeError('architecture_expected values: "amd64", "arm64"')
    return architecture

  # Validate OS edition.
  @classmethod
  def validate_os_edition(self,os_edition):
    os_edition_expected = ["server", "desktop"]
    if os_edition not in os_edition_expected:
      print('Current os_edition:',os_edition)
      raise argparse.ArgumentTypeError('os_edition_expected values: "server", "desktop"')
    return os_edition

  # Validate host OS.
  @classmethod
  def validate_host_os(self,host_os):
    host_os_expected = ["windows", "mac", "ubuntu"]
    if host_os not in host_os_expected:
      print('Current host_os:',host_os)
      raise argparse.ArgumentTypeError('host_os_expected values: ""windows", "mac", "ubuntu"')
    return host_os

  # Start VM.
  def start(self,vagrantfile_path):
    print(vagrantfile_path)
    v = vagrant.Vagrant(vagrantfile_path)
    v.up()
    status = v.status() 
    print(status)

  # Stop VM.
  def stop(self,vagrantfile_path):
    v = vagrant.Vagrant(vagrantfile_path)
    v.halt()
    status = v.status() 
    print(status)

  # SSH VM.
  def ssh(self,vagrantfile_path):
    print(vagrantfile_path)
    subprocess.run(['vagrant', 'ssh'], cwd=vagrantfile_path)

  # Destroy VM.
  def destroy(self,vagrantfile_path):
    v = vagrant.Vagrant(vagrantfile_path)
    v.destroy()
    status = v.status() 
    print(status)

  # Provision VM.
  def provision(self,vagrantfile_path):
    v = vagrant.Vagrant(vagrantfile_path)
    v.provision()
    status = v.status() 
    print(status)

# Parse CLI arguments.
if __name__=='__main__':
  CLI = argparse.ArgumentParser(description='A command line interface to manage virtual machines.')
  CLI.add_argument('--action',choices=['start','stop','ssh','provision','destroy'],required=True)
  CLI.add_argument('--os_name',choices=['alma-linux-8','alma-linux-9','amazon-linux-2','centos-linux-7','rocky-linux-8','rocky-linux-9','ubuntu-linux-18-04','ubuntu-linux-22-04'], default=os.environ.get('OS_NAME'), required=not os.environ.get('OS_NAME'), type=VM.validate_os_name)
  CLI.add_argument('--hypervisor', choices=['virtualbox', 'vmware'], default=os.environ.get('HYPERVISOR'), required=not os.environ.get('HYPERVISOR'), type=VM.validate_hypervisor)
  CLI.add_argument('--architecture', choices=['amd64', 'arm64'], default=os.environ.get('ARCHITECTURE'), required=not os.environ.get('ARCHITECTURE'), type=VM.validate_architecture)
  CLI.add_argument('--os_edition', choices=['server', 'desktop'], default=os.environ.get('OS_EDITION'), required=not os.environ.get('OS_EDITION'), type=VM.validate_os_edition)
  CLI.add_argument('--host_os', choices=['windows', 'mac', 'ubuntu'], default=os.environ.get('HOST_OS'), required=not os.environ.get('HOST_OS'), type=VM.validate_host_os)

  Args = CLI.parse_args()
  os_name = Args.os_name
  hypervisor = Args.hypervisor
  architecture = Args.architecture
  os_edition = Args.os_edition
  host_os = Args.host_os

  if Args.host_os == 'windows':
    vagrantfile_path = "C:\\Program Files\\Git\\opt\\kickstart-linux\\vagrant\\{}\\{}\\{}\\{}".format(os_name, hypervisor, architecture, os_edition)
    if Args.action=='start':
      VM().start(vagrantfile_path)
    elif Args.action=='stop':
      VM().stop(vagrantfile_path)
    elif Args.action=='ssh':
      VM().ssh(vagrantfile_path)
    elif Args.action=='provision':
      VM().provision(vagrantfile_path)
    elif Args.action=='destroy':
      VM().destroy(vagrantfile_path)
    else:
      print('Please provide a valid action.')
  else:
    vagrantfile_path = "/opt/kickstart-linux/vagrant/{}/{}/{}/{}".format(os_name, hypervisor, architecture, os_edition)
    if Args.action=='start':
      VM().start(vagrantfile_path)
    elif Args.action=='stop':
      VM().stop(vagrantfile_path)
    elif Args.action=='ssh':
      VM().ssh(vagrantfile_path)
    elif Args.action=='provision':
      VM().provision(vagrantfile_path)
    elif Args.action=='destroy':
      VM().destroy(vagrantfile_path)
    else:
      print('Please provide a valid action.')