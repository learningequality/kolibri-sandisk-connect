import subprocess	#To call temrinal commands
import re			#Regular expression syntax formats

def get_server_list():
	#scan for wifi
	proc = subprocess.Popen('sudo iwlist wipi8 scan 2>/dev/null', shell=True, stdout=subprocess.PIPE)
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
	proc = subprocess.Popen('sudo ifconfig 2>/dev/null', shell=True, stdout=subprocess.PIPE,)
	#displays outputs of list
	stdout_str = proc.communicate()[0]
	#parse the outputs
	stdout_list = stdout_str.split('\n')
	#empty array to save the parsed outputs
	wipi_ids=[]
	# search for wipi adapters that are available
	output = subprocess.check_output("ifconfig | grep '00:c1:41' | awk '{print $1}'", shell=True);
	output_list = output.split()
	for line in output_list:
		line = line.strip()
		wipi_ids.append(line)
	return wipi_ids
