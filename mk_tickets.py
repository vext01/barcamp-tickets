#!/usr/bin/env python

import sys
import copy
import os

if len(sys.argv) != 2:
    print("usage: mk_tickets.py <infile>")
    sys.exit(1)

# suck in whole svg (it will do)
svg_fd = open("ticket.svg", "r")
svg_buf = ""
for i in svg_fd:
    svg_buf = svg_buf + i
svg_fd.close()

# XXX mkdir

# iterate names making tickets
names_fd = open(sys.argv[1], "r")
for line in names_fd:
    if line.startswith("#") or len(line.strip()) == 0:
        continue

    (fname, lname, role, company) = line.split(",")
    copy_buf = copy.copy(svg_buf)

    # subsitutions
    copy_buf = copy_buf.replace("!!FNAME!!", fname)
    copy_buf = copy_buf.replace("!!LNAME!!", lname)
    copy_buf = copy_buf.replace("!!ROLE!!", role)
    copy_buf = copy_buf.replace("!!COMPANY!!", company)
    
names_fd.close()

print(copy_buf)
