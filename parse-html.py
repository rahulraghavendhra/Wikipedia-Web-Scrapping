from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib 
import re
import csv
import config
import os

def readfile(name,formats):
	filename = 'files/' + name + formats
	html_content = ''
	if os.path.isfile(filename):
		print name
		file_handle = open(filename, 'r')
		html_content = file_handle.read()
	return html_content

def getURL(name, formats):
	url = ''
	if formats == '_normal.html':
		url = "https://en.wikipedia.org/wiki/" + name
	if formats == '_givenname.html':
		url = "https://en.wikipedia.org/wiki/" + name + "_(given_name)"
	if formats == '_name.html':
		url = "https://en.wikipedia.org/wiki/" + name + "_(name)"
	return url

def scrape_table(table, table_dict):
	trs = table.find_all('tr')
	for tr in trs:
		th = tr.find('th', attrs={'scope':'row'})
		td = tr.find('td')
		if th is not None and td is not None:
			key = th.text.encode('ASCII', 'ignore').strip("\n")
			if key in config.table_fields:
				value = td.text.encode('ASCII', 'ignore').replace("\n", "")
				table_dict[key] = value
	return table_dict

def writetofile(name_dict, name):
	output_file = open('output/output_file.csv', 'a')
	output_file.write(name)
	output_file.write('|')
	for field in config.table_fields:
		#print "key: ", field, "\t value: ", name_dict[field].strip("\n")
		output_file.write(name_dict[field].strip("\n"))
		output_file.write('|')
	output_file.write('\n');
	output_file.close()

def main(names_list):
	parse_log = open('logs/parse_log.txt', 'a')
	file_formats = ['_normal.html', '_givenname.html', '_name.html']
	for name in names_list:
		name = name.rstrip(" ")
		name_dict = {field:'' for field in config.table_fields}
		for formats in file_formats:
			html = readfile(name, formats)
			if html == '':
				print 'file ', name, formats, 'not found'
				exit()
			soup = BeautifulSoup(html)
			table = soup.find('table', attrs={'class':'infobox'})
			if table is not None:
				name_dict = scrape_table(table, name_dict)
				name_dict['URL'] = getURL(name, formats)
		writetofile(name_dict, name)
		parse_log.write(name)
		parse_log.write("\n")
	parse_log.close()

if __name__ == '__main__':
	name_array = []
	names_list = []
	with open('logs/parse_log.txt', 'r') as log:
		parsed_names = log.read().splitlines()
	log.close()
	last_parsed_index = len(parsed_names)
	if last_parsed_index == 0:
		name_dict = {field:field for field in config.table_fields}
		writetofile(name_dict, 'Name')
	with open("all_names.csv","r") as f:
		names_list = f.read().splitlines()
		for name_details in names_list:
			name_array.append(name_details.split(',')[0])
	names_list = name_array[last_parsed_index:]
	main(names_list)

