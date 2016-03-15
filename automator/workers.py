#!/usr/bin/python
import threading
import time
import random
import datetime
import secrets
import subprocess
import os

from Tkinter import *

routing_table_lock = threading.Lock()

class WorkerThread(threading.Thread):
    
    def __init__(self, wipi_name, sandisk_id, text_id, wipi_id, nb, wifi, available_wipis, total_wipis):
        threading.Thread.__init__(self)
        self.sandisk_id = sandisk_id
        self.ip = "192.168.11.2%.2d" % wipi_id
	self.text_id = text_id
	self.wipi_name = wipi_name
	self.nb = nb
	self.tab_id = len(nb.tabs()) - 1
	self.wifi = wifi
	self.available_wipis = available_wipis
	self.total_wipis = total_wipis

    def log(self, message):
	# log messages to the text screen of tab
	self.text_id.config(state=NORMAL)
        self.text_id.insert(END, "%s: SanDisk %s @ %s: %s\n" % (datetime.datetime.now(), self.sandisk_id, self.wipi_name, message))
	self.text_id.see(END)
	self.text_id.config(state=DISABLED)
        self.last_log_message = message
    
    def execute(self, command):
	# continuously display output to text screen
	self.text_id.config(state=NORMAL)
	popen = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, env={'PYTHONUNBUFFERED': 'True'})
	lines_iterator = iter(popen.stdout.readline, b"")
	self.text_id.tag_config("text", foreground="black")
	error = 0
	for line in lines_iterator:
		# if there is an error, display text in red
		if "error" in line.lower():
			self.text_id.tag_config("text", foreground="red")
			error = 1
		self.text_id.insert(END, line, "text")
		self.text_id.see(END)
	self.log("Worker completed!")
	self.text_id.config(state=DISABLED)
	return error

    def setup_ssh(self):
	subprocess.call(['../scripts/_setup_ssh.sh', secrets.SANDISK_ROOT_PASSWORD])
	
    def run(self):
        self.log("Starting worker...")
	with routing_table_lock:
		self.wifi.set("%s/%s wifi adapters available" % (self.available_wipis - 1, self.total_wipis) )
	self.setup_ssh()
        self.connect_server_to_wipi()
        self.add_IP_route()
	# run ansible commands
	os.chdir('../ansible/')
	ansible_command = 'ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts --extra-vars "num_videos=7611 ansible_ssh_host=%s ansible_ssh_pass=%s" full_setup.yml' % (self.ip, secrets.SANDISK_ROOT_PASSWORD)
	error = self.execute(ansible_command)
	# updates tab name
	if error:
		self.nb.tab(self.tab_id, text=("%s (ERROR!)" % self.sandisk_id))
	else:
		self.nb.tab(self.tab_id, text=("%s (DONE!)" % self.sandisk_id))
	with routing_table_lock:
		self.wifi.set("%s/%s wifi adapters available" % (self.available_wipis, self.total_wipis) )

    @classmethod
    def get_active(cls):
        return [t for t in threading.enumerate() if isinstance(t, WorkerThread)]

    def connect_server_to_wipi(self):
        self.log("Connecting WiPi to server")
        subprocess.call(["nmcli", "d", "disconnect", "iface", self.wipi_name]) #catch errors
        subprocess.call(["nmcli", "d", "wifi", "connect", "SanDisk Media %s" % self.sandisk_id, "iface", self.wipi_name])

    def add_IP_route(self):
        self.log("Attempting to add IP route")
        with routing_table_lock:
            self.log("Lock ACQUIRED")
            self.log("Configuring routing table and SanDisk IP ")
            subprocess.call(["sudo", "ip", "route", "delete", "%s/32" % self.ip, "dev", self.wipi_name])#catch errors
            #pair the "default IP" with a particular WiPi on controller routing table
            self.log("A")
            subprocess.call(["sudo", "ip", "route", "add", "192.168.11.1/32", "dev", self.wipi_name])
            #add a unique IP address so that the WiPi can access it
            self.log("B")
            subprocess.call(["../scripts/_set_sandisk_ip.sh", secrets.SANDISK_ROOT_PASSWORD, self.ip])
            #remove the "default IP" and WiPi pairing from routing table
            self.log("C")
            subprocess.call(["sudo", "ip", "route", "delete", "192.168.11.1/32", "dev", self.wipi_name])
            #Add the unique IP address of the SanDisk server to the controller routing table
            self.log("D")
            subprocess.call(["sudo", "ip", "route", "add", "%s/32" % self.ip, "dev", self.wipi_name])
            self.log("Lock RELEASING")

if __name__ == "__main__":

    # Create new threads
    thread1 = WorkerThread(1, "CCE5")
    thread2 = WorkerThread(2, "A3DE")

    # Start new Threads
    thread1.start()
    thread2.start()
