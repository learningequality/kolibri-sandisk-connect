#gspread documentation:
#http://www.indjango.com/access-google-sheets-in-python-using-gspread/
#
#You will probably need to 'pip install gspread' to get this working  

#!/usr/bin/python

#Setting up our Google Spreadsheet interface

import gspread
gc = gspread.login('fleserverconfig@gmail.com', 'yerbamate')

#Open Google sheet by name
sh = gc.open("SanDisk Configuration Database")

#Select worksheet by index
worksheet = sh.get_worksheet(0)

ROW_OFFSET = 3
# ##################################################################################
# #Searching for a particular server based on MAC 
# cellSearchResult = worksheet.findall("CDDE")

# #Update one cell to the right 
# worksheet.update_cell(cellSearchResult[0].row,cellSearchResult[0].col+1,'To the right!')

##################################################################################

def get_spreadsheet_id_row_mapping():
	ssids = worksheet.col_values(1)[ROW_OFFSET:]
	return dict(zip(ssids, range(1, len(ssids) + ROW_OFFSET)))

def add_server_to_new_row(ssid):
	lastRow = (len(worksheet.col_values(1)))+1
	worksheet.update_cell(lastRow, 1,ssid)
	# return true #Is there a way to check if the update_cell command worked?

def check_last_step(id):
	matches = worksheet.findall(id)
	lastStep = len(worksheet.row_values(matches[0].row))
	return lastStep
