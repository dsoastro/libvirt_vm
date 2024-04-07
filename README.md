# Script for a quick creation of a virtual machine (VM) in libvirt
Script creates:
- a virtual machine based on the cloud image of Ubuntu 20.04 using cloud-init (the VM image is located at /home/images/focal-server-cloudimg-amd64.img)
- a default user with a default password on the virtual machine
- a second network interface if necessary

Besides:  
- public ssh keys for root and default user are installed to /root/.ssh/authorized_keys and /home/user/.ssh/authorized_keys, 
- a random /etc/machine-id for correct dhcp operation is generated
- o-my-zsh and several other packages are installed

See templates/cloud_init.cfg for details

## Why do we need the script?
Creating a virtual machine in libvirt even based on a preliminary prepared image takes time (because additional configuration of the machine is usually required). This script performs all necessary VM configuration and saves your time

## Getting started
Set VM options in run.py header:
  - VM name
  - memory
  - number of cores
  - whether a second network interface is needed, its name in virsh and its IP address  

Set your user name and public ssh keys in templates/cloud_init.cfg. Then
```
python3 run.py
```
