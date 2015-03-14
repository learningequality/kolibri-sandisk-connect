import subprocess	#To call temrinal commands
import re			#Regular expression syntax formats
import time

# from googleSheet import get_spreadsheet_id_row_mapping
# from googleSheet import add_server_to_new_row
# from googleSheet import check_last_step

from workers import WorkerThread

from wifi import get_server_list
from wifi import get_wipi_list

from random import shuffle


 # sandisk_spreadsheet_map = get_spreadsheet_id_row_mapping()

while True:
	#Get all available sandisk servers and wipi dongles

	##COMMENTED OUT SUDO COMMANDS SINCE I DON'T HAVE ACCESS

	sandisk_list = get_server_list()
	wipi_list = get_wipi_list()

	# sandisk_list = ['D59F']
	# wipi_list = [1]

	for worker in WorkerThread.get_active():
		if worker.sandisk_id in sandisk_list:
			sandisk_list.remove(worker.sandisk_id)
		if worker.wipi_id in wipi_list: 
			wipi_list.remove(worker.wipi_id)

	# Now we have list of available sandisks and wipis


	shuffle(sandisk_list)
	shuffle(wipi_list)

	print 'There are %d free sandisk servers and %d free wipi adapters' % (len(sandisk_list), len(wipi_list))

	for sandisk_id, wipi_id in zip(wipi_list, sandisk_list): 
		
		print 'Using sandisk_server %s, wipi adapter %s' % (sandisk_id, wipi_id)
		
		#Create worker thread with this pair
		thread = WorkerThread(sandisk_id,wipi_id)

		#Start the thread
		thread.start()

		time.sleep(5)

	break	




