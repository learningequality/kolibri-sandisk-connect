from Tkinter import *
import tkMessageBox
import ttk
from ScrolledText import *

from subprocess import Popen
import subprocess
import os
import time
import random

from workers import WorkerThread
from wifi import get_wipi_list
from wifi import get_server_list


class Application(Frame):
    def submit(self, sandisk_id, nb):
	# if string does not meet requirements, do nothing
	if not sandisk_id or len(sandisk_id) != 4:
		return False

        result = tkMessageBox.askyesno("SSID Confirmation", "Is SSID %s correct?" % sandisk_id)
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
		sandisk_list = get_server_list()
		wipi_list = get_wipi_list()

		# remove wipis and sandisks in use
		for worker in WorkerThread.get_active():
			if worker.sandisk_id in sandisk_list:
				sandisk_list.remove(worker.sandisk_id)
			if worker.wipi_name in wipi_list: 
				wipi_list.remove(worker.wipi_name)
		
		# show errors for sandisks or wipis in GUI
		if sandisk_id not in sandisk_list:
			tkMessageBox.showerror("SSID Unavailable", "SanDisk ID: %s not in list of available SanDisks.\nPlease check connection or SanDisk ID." % sandisk_id)
			nb.forget(tab_id)
			self.SSID_submit.config(state=NORMAL)
			return

		if len(wipi_list) == 0:
			tkMessageBox.showerror("Wipis Unavailable", "There are no available wipis.")
			nb.forget(tab_id)
			self.SSID_submit.config(state=NORMAL)
			return

		# choose random wipi and assign id
		wipi_name = random.choice(wipi_list)	
		self.wipi_dict[wipi_name] = len(self.wipi_dict) + 1
		
		# update tab name
		nb.tab(tab_id, text=sandisk_id)		

		#Create worker thread with this pair
		thread = WorkerThread(wipi_name, sandisk_id, text, self.wipi_dict, nb)

		self.SSID_submit.config(state=NORMAL)

		Button(page, text='Close Tab', command=lambda: self.closeTab(page, thread)).pack(side=LEFT)

		#Start the thread
		thread.start()

		time.sleep(5)

    def closeTab(self, tab, th):
	# prevent user from closing tab if thread is active
	#if th.isAlive():
	#	tkMessageBox.showerror('Closing Tab Error', 'Process is still running.\n Please wait for it to finish.')
	#	return
	# close tab on user request
	result = tkMessageBox.askyesno('Close Tab Confirmation', 'Are you sure want to close the current tab?')
	if result:
		tab.destroy()

    def createWidgets(self):
	# SSID label widget
	self.SSID_label = Label(self, text="Please Enter SSID:")
	self.SSID_label.pack({"side": "left"})
	
	# User supplied string widget
	SSID = StringVar()
	self.SSID_entry = Entry(self, textvariable=SSID)
	self.SSID_entry.pack({"side": "left"})

	# add notebook to GUI
	nb = ttk.Notebook(self)

	# submit button which updates GUI
	self.SSID_submit = Button(self, text="Submit", command=lambda: self.submit(SSID.get(), nb) )
	self.SSID_submit.pack({"side": "left"})

	nb.pack(expand=1, fill="both")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
	self.wipi_dict = dict()

root = Tk()
root.wm_title("Sandisk Configuration")
app = Application(master=root)
app.mainloop()
