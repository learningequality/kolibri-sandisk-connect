import subprocess	#To call temrinal commands
import re			#Regular expression syntax formats

from googleSheet import get_spreadsheet_id_row_mapping
from googleSheet import add_server_to_new_row
from googleSheet import check_last_step

CONFIGURE_DONE = 10

def get_server_id_list():
	#scan for wifi
	proc = subprocess.Popen('sudo wlist wlan0 scan 2>/dev/null', shell=True, stdout=subprocess.PIPE,)
	#displays outputs of list
	stdout_str = proc.communicate()[0]
	#parse the outputs
	stdout_list = stdout_str.split('\n')
	#empty array to save the parsed outputs
	server_ids=[]
	#search for wifi server_ids that match SanDisk Media
	for line in stdout_list:
		line=line.strip()
		match=re.search('SanDisk Media (\w\w\w\w)', line)
		if match:
			server_ids.append(match.group(1))
	#make it look pretty
	server_ids = list(set(server_ids))
	return server_ids

server_ids = get_server_id_list()

# print(server_ids)

server_id_row_map = get_spreadsheet_id_row_mapping()

# print(server_id_row_map)
	
#scan for SanDisk servers, add new row to Google sheet if found
for server_id in server_ids:
	if server_id not in server_id_row_map:
		add_server_to_new_row(server_id)
	if server_id in server_id_row_map:
		if check_last_step(server_id) != CONFIGURE_DONE:
				pass



		#Check to see if partway through configuration
			#If in spreadsheet, look for last step. Also verify by checking for particular files
			# 	on the server that indicate which step the configuration is on
		#Add new row to spreadsheet	if new
#set of WiPi based on output of ifconfig
#delete from the list of the WiPi and SanDisk if not available / assigned to thread
#check to see if any dead threads using enumerate
	#if dead -- find out the last step / or if it was finished (Rsync for videos?) 	
	#check if it was complete set to 'none'- if not then display error message
#Create a new thread forWiPi/SanDisk pair. Then pass in server ID. 
	#Consider using zip(WiPi Set , SanDisk Set)
	#For WiPi in Sandisk 







#function:
# check next step for a particular ID

#choose server/SSID that is not being configured, assign to WiFi dongle

