import os
from jinja2 import Environment, FileSystemLoader
import sys
import subprocess

# do not use _ - etc for hostname
hostname = "star"
vm_name =  hostname
is_second_net = False
second_net_name = 'isolated'
second_iface_address = '192.168.137.101/24'

memory = "2000"
vcpus  = "2"



def run_subprocess(params = [], shell = False):
    ''' params e.g. (["/usr/bin/gammu", "getallsms"] '''
    try:
        text = subprocess.check_output(params, shell=shell).decode("utf-8")
        return text
    except Exception as e:
        print(e, file=sys.stdout, flush=True)
        return None

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("cloud_init.cfg")

machine_id = run_subprocess(['dbus-uuidgen'])
if machine_id is None:
    machine_id = "a4d4af917b45d9386c00f3e563d249ac"

content = template.render(        
        hostname=hostname,
        fqdn=hostname,
        machine_id=machine_id,
        etchosts_line=second_iface_address[:15] + " " + hostname if is_second_net else ""      
)

with open("cloud.cfg", mode="w", encoding="utf-8") as message:
    message.write(content)

if is_second_net:
    template = environment.get_template("network_config_two_ifaces.cfg")
    content = template.render(        
        address=second_iface_address
    )
else:
    template = environment.get_template("network_config_default.cfg")
    content = template.render()

with open("network.cfg", mode="w", encoding="utf-8") as message:
    message.write(content)

if is_second_net:
    with open("cloud.cfg", mode="a", encoding="utf-8") as f:
        f.write("  - sed '2d' /etc/hosts")
       
    

os.system('sudo qemu-img create -f qcow2 -F qcow2 -b /home/images/focal-server-cloudimg-amd64.img /home/images/u20_{vm_name}.qcow2 35G'.format(vm_name=vm_name))
os.system('sudo cloud-localds -v --network-config=network.cfg cloud.img cloud.cfg')
if is_second_net:
    os.system('sudo virt-install --name {vm_name} --memory {memory} --vcpus {vcpus} --boot hd,menu=on \
    --disk path=cloud.img,device=cdrom --disk path=/home/images/u20_{disk_name}.qcow2,device=disk \
    --os-variant ubuntu20.04 --network network=default --network network={second_net_name}'.
    format(vm_name=vm_name, memory=memory, vcpus=vcpus, disk_name=vm_name, second_net_name=second_net_name))
else:
    os.system('sudo virt-install --name {vm_name} --memory {memory} --vcpus {vcpus} --boot hd,menu=on \
    --disk path=cloud.img,device=cdrom --disk path=/home/images/u20_{disk_name}.qcow2,device=disk \
    --os-variant ubuntu20.04 --network network=default'.
    format(vm_name=vm_name, memory=memory, vcpus=vcpus, disk_name=vm_name))
