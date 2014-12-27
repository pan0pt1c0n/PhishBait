#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys
import mechanize

print "\n*************************************************"
print "**  LinkedIn Email Harvester                   **"
print "**  by H@ck1tHu7ch (Justin Hutchens)           **"
print "**  ...GONE PHISHING!!!                        **"
print "*************************************************\n\n"

if len(sys.argv) != 4:
    print "Usage - ./linkedin_harvest.py [Format num] [suffix] [output_file]"
    print "\nFORMATS:"
    print "1 - [first].[last]@[suffix]"
    print "2 - [first][last]@[suffix]"
    print "3 - [first initial][last]@[suffix]"
    print "4 - [first]_[last]@[suffix]\n"
    print "Example - ./linkedin_harvest.py 1 company.com output.txt"
    print "Example will create email list in the form of john.smith@company.com"
    sys.exit()

format = int(sys.argv[1])
suffix = str(sys.argv[2]).lower()
filename = str(sys.argv[3])
file = open(filename,'w')

def format_1(names,suffix):
    emails = []
    for x in names:
        try:
            first = x.split(' ')[0].lower()
            last = x.split(' ')[1].lower()
            emails.append(first + '.' + last + '@' + suffix)
        except:
            pass
    return emails

def format_2(names,suffix):
    emails = []
    for x in names:
        try:
            first = x.split(' ')[0].lower()
            last = x.split(' ')[1].lower()
            emails.append(first + last + '@' + suffix)
        except:
            pass
    return emails

def format_3(names,suffix):
    emails = []
    for x in names:
        try:
            first = names.split(' ')[0].lower()
            last = names.split(' ')[1].lower()
            emails.append(first[0] + last + '@' + suffix)
        except:
            pass
    return emails

def format_4(names,suffix):
    emails = []
    for x in names:
        try:
            first = names.split(' ')[0].lower()
            last = names.split(' ')[1].lower()
            emails.append(first + '_' + last + '@' + suffix)
        except:
            pass
    return emails

## Get Company Name & URL encode
company = raw_input("Enter the company name: ")
company = company.replace(' ','%20')

## Gather number of entries with mechanize
br = mechanize.Browser()
br.set_handle_robots(False) 
response = br.open('http://www.bing.com/search?q=(site%3A%22www.linkedin.com%2Fin%2F%22%20OR%20site%3A%22www.linkedin.com%2Fpub%2F%22)%20%26%26%20(NOT%20site%3A%22www.linkedin.com%2Fpub%2Fdir%2F%22)%20%26%26%20%22'+company+'%22&qs=n&form=QBRE&pq=(site%3A%22www.linkedin.com%2Fin%2F%22%20or%20site%3A%22www.linkedin.com%2Fpub%2F%22)%20%26%26%20(not%20site%3A%22www.linkedin.com%2Fpub%2Fdir%2F%22)%20%26%26%20%22'+company+'%22').read()
soup = BeautifulSoup(response)
count = int((((soup.find('span',{"class":'sb_count'})).renderContents()).split(' ')[0]).replace(",",""))

link_list = []
for link in br.links():
    link_list.append(link.text)
if "Next" in link_list:
    more_records = True
else:
    more_records = False

## Set Query Record Incrementation & Initialize Loop
names = []
for definition in soup.findAll('h2'):
    definition = definition.renderContents()
    if "LinkedIn" in definition:
        names.append((((((definition.replace('<strong>','')).replace('</strong>','')).split('>')[1]).split('|')[0]).rstrip()).split(',')[0])
if format == 1:
    emails = format_1(names,suffix)
elif format == 2:
    emails = format_2(names,suffix)
elif format == 3:
    emails = format_3(names,suffix)
elif format == 4:
    emails = format_4(names,suffix)
else:
    print "\n\n[-] ERROR: Improper Format Value Supplied\n"
    sys.exit()
for x in emails:
    print x
    file.write(x+"\n")

while more_records == True:
    response = br.follow_link(text="Next")
    names = []
    soup = BeautifulSoup(response)
    for definition in soup.findAll('h2'):
        definition = definition.renderContents()
        if "LinkedIn" in definition:
            names.append((((((definition.replace('<strong>','')).replace('</strong>','')).split('>')[1]).split('|')[0]).rstrip()).split(',')[0])
    if format == 1:
        emails = format_1(names,suffix)
    elif format == 2:
        emails = format_2(names,suffix)
    elif format == 3:
        emails = format_3(names,suffix)
    for x in emails:
        print x
        file.write(x+"\n")
    link_list = []
    for link in br.links():
        link_list.append(link.text)
    if "Next" in link_list:
        more_records = True
    else:
        more_records = False

