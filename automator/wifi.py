import subprocess	#To call terminal commands
import re			#Regular expression syntax formats

def get_server_list(wipi_list):
	if len(wipi_list) == 0:
		return []
	#scan for wifi
	proc = subprocess.Popen('sudo iwlist %s scan 2>/dev/null' % wipi_list[0], shell=True, stdout=subprocess.PIPE)
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
	return server_ids

def get_wipi_list():
	#empty array to save the parsed outputs
	wipi_ids=[]
	# search for wipi adapters that are available
	output = subprocess.check_output("iwconfig 2> /dev/null | grep '802.11' | awk '{print $1}'", shell=True);
	output_list = output.split()
	for line in output_list:
		line = line.strip()
		wipi_ids.append(line)
	return wipi_ids
