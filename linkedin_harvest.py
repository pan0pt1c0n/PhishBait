#!/usr/bin/python

import re
import sys

if len(sys.argv) != 4:
    print "\n*************************************************"
    print "**  LinkedIn Email Harvester                   **"
    print "**  by Pan0pt1c0n (Justin Hutchens)           **"
    print "**  ...GONE PHISHING!!!                        **"
    print "*************************************************\n\n"
    print "\n\nUsage - ./linkedin_harvest.py [Filename] [Format num] [suffix]"
    print "\nFORMATS:"
    print "1 - [first].[last]@[suffix]"
    print "2 - [first][last]@[suffix]"
    print "3 - [first_initial][last]@[suffix]\n"
    print "Example - ./linkedin_harvest.py input.txt 1 company.com"
    print "Example will create emails in the form of john.smith@company.com from the input.txt file"
    sys.exit()

in_file = str(sys.argv[1])
format = int(sys.argv[2])
suffix = str(sys.argv[3]).lower()


def get_names(in_file):
    ## Getting 1st Degree Contacts (first name & last name)
    f = open(in_file,'r')
    strings = re.findall(r'"(\w*\s\w*)(\sis\syour\sconnection)',f.read())

    ## Getting 2nd Degree Contacts
    f = open(in_file,'r')
    strings = strings + re.findall(r'"(\w*\s\w*)(\sis\sa\s2nd\sdegree\scontact)',f.read())

    ## Create List of Names
    names = []
    for x in strings:
        names.append(str(x[0]))
    return names

def format_1(names,suffix):
    emails = []
    for x in names:
        first = x.split(' ')[0].lower()
        last = x.split(' ')[1].lower()
        emails.append(first + '.' + last + '@' + suffix)
    return emails

def format_2(names,suffix):
    emails = []
    for x in names:
        first = x.split(' ')[0].lower()
        last = x.split(' ')[1].lower()
        emails.append(first + last + '@' + suffix)
    return emails

def format_3(names,suffix):
    emails = []
    for x in names:
        first = x.split(' ')[0].lower()
        last = x.split(' ')[1].lower()
        emails.append(first[0] + last + '@' + suffix)
    return emails


names = get_names(in_file)

if format == 1:
    emails = format_1(names,suffix)
elif format == 2:
    emails = format_2(names,suffix)
elif format == 3:
    emails = format_3(names,suffix)

outfile = open('linkedin_emails.txt','w')
for x in emails:
    outfile.write(str(x) + '\n')
    print x
outfile.close()
