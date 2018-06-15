from bs4 import BeautifulSoup
from string import ascii_lowercase
import urllib 
import re
import csv
def download_page(link, filename):
    urlHandle = urllib.urlopen(link)
    html = urlHandle.read()
    with open(filename, 'w') as file_handle:
        file_handle.write(html)
    file_handle.close()


def main(names_list):
    download_log = open('logs/download_log.txt', 'a')
    for name in names_list:
        name = name.strip(" ")
        print name
	link_format1 = "https://en.wikipedia.org/wiki/" + name
        filename1 = "files/" + name + "_normal.html"
        download_page(link_format1, filename1)

        link_format2 = "https://en.wikipedia.org/wiki/" + name + "_(given_name)"
        filename2 = "files/" + name + "_givenname.html"
        download_page(link_format2, filename2)

	link_format3 = "https://en.wikipedia.org/wiki/" + name + "_(name)"
        filename3 = "files/" + name + "_name.html"
        download_page(link_format3, filename3)
        download_log.write(name)
        download_log.write("\n")
    download_log.close()

if __name__ == '__main__':
    name_array = []
    names_list = []
    with open('logs/download_log.txt', 'r') as log:
        downloaded_names = log.read().splitlines()
    log.close()
    last_parsed_index = len(downloaded_names)
    with open("all_names.csv","r") as f:
        names_list = f.read().splitlines()
        for name_details in names_list:
            name_array.append(name_details.split(',')[0])
    names_list = name_array[last_parsed_index:]
    main(names_list)

