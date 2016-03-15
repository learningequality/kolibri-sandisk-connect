from Tkinter import *
import tkMessageBox
import ttk
from ScrolledText import *

from subprocess import Popen
import subprocess
import os
import time
import random
import re

from workers import WorkerThread
from wifi import get_wipi_list, get_server_list

class Application(Frame):

    def submit(self, sandisk_id, nb):
	# if string does not meet requirements, display error and correct syntax
	if not re.match("^[A-Za-z0-9]{4}$", sandisk_id):
		tkMessageBox.showinfo("SSID Invalid Syntax", "Please enter inputs with format 'abc1' or 'ABC1'.\nLetters and numbers only.")
		return

        result = tkMessageBox.askyesno("SSID Confirmation", "Is SSID %s correct?" % sandisk_id)
	sandisk_id = sandisk_id.upper()
	if result:
		# create notebook tab, and update GUI
		page = ttk.Frame(nb)
		text = ScrolledText(page)
		text.pack(expand=1, fill="both")
		nb.add(page, text='%s (LOADING)' % sandisk_id)
		self.SSID_submit.config(state=DISABLED)
		tab_id = len(nb.tabs()) - 1
		nb.select(tab_id)
		self.update_idletasks()
		
		# find available sandisks and available wipis
		wipi_list = get_wipi_list()
		self.total_wipis = len(wipi_list)
		sandisk_list = get_server_list(wipi_list)

		# remove wipis and sandisks in use
		for worker in WorkerThread.get_active():
			if worker.sandisk_id in sandisk_list:
				sandisk_list.remove(worker.sandisk_id)
			if worker.wipi_name in wipi_list: 
				wipi_list.remove(worker.wipi_name)
		
		self.available_wipis = len(wipi_list)

		# show errors for sandisks or wipis in GUI
		if sandisk_id not in sandisk_list:
			tkMessageBox.showerror("SSID Unavailable", "SanDisk ID: %s not in list of available SanDisks.\nPlease check connection or SanDisk ID." % sandisk_id)
			nb.forget(tab_id)
			self.SSID_submit.config(state=NORMAL)
			return

		if self.available_wipis == 0 or len(nb.tabs()) > self.total_wipis:
			tkMessageBox.showerror("Wifi Adapter Unavailable", "There are no available wifi adapters. \nOr try to close completed tabs.")
			nb.forget(tab_id)
			self.SSID_submit.config(state=NORMAL)
			return

		# choose random wipi and assign id
		wipi_name = random.choice(wipi_list)	
		if wipi_name not in self.wipi_dict:
			self.wipi_dict[wipi_name] = len(self.wipi_dict) + 1
		
		# update tab name
		nb.tab(tab_id, text=sandisk_id)		

		#Create worker thread with this wifi, sandisk pair
		thread = WorkerThread(wipi_name, sandisk_id, text, self.wipi_dict[wipi_name], nb)
		self.thread_list.append(thread)
		self.wifi.set("%s/%s wifi adapters available" % (self.total_wipis - len(nb.tabs()), self.total_wipis))

		self.SSID_submit.config(state=NORMAL)

		Button(page, text='Close Tab', command=lambda: self.closeTab(page, thread)).pack(side=LEFT)

		#Start the thread
		thread.start()

    def closeTab(self, tab, th):
	# prevent user from closing tab if thread is active
	if th.isAlive():
		tkMessageBox.showerror('Closing Tab Error', 'Process is still running.\n Please wait for it to finish.')
		return
	# update tab ids for each thread
	index = self.thread_list.index(th)
	for thread in self.thread_list[index:]:
		thread.tab_id = thread.tab_id - 1
	self.thread_list.remove(th)
	# close tab on user request
	result = tkMessageBox.askyesno('Close Tab Confirmation', 'Are you sure want to close the current tab?')
	if result:
		tab.destroy()
	self.wifi.set("%s/%s wifi adapters available" % (self.total_wipis - len(self.nb.tabs()), self.total_wipis))


    def createWidgets(self):
	# SSID label widget
	self.SSID_label = Label(self, text="Please Enter SSID:")
	self.SSID_label.pack({"side": "left"})
	
	# User supplied string widget
	SSID = StringVar()
	self.SSID_entry = Entry(self, textvariable=SSID)
	self.SSID_entry.pack({"side": "left"})

	self.total_wipis = len(get_wipi_list())
	self.wifi = StringVar()
	self.wifi_label = Label(self, textvariable=self.wifi)
	self.wifi.set("%s/%s wifi adapters available" % (self.total_wipis, self.total_wipis))
	self.wifi_label.pack({"side": "left"})

	# add notebook to GUI
	self.nb = ttk.Notebook(self)

	# submit button which updates GUI
	self.SSID_submit = Button(self, text="Submit", command=lambda: self.submit(SSID.get(), self.nb) )
	self.SSID_submit.pack({"side": "left"})

	self.nb.pack(expand=1, fill="both")

    def checkThreads(self):
	workers = WorkerThread.get_active()
	if len(workers) != 0:
		tkMessageBox.showerror('Closing Window Error', 'Processes are still running.\n Please wait for them to finish.')
		return
	self.master.destroy()
	
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
	self.wipi_dict = dict()
	self.thread_list = list()

root = Tk()
root.wm_title("Sandisk Configuration")
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.checkThreads)
app.mainloop()
