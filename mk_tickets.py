#!/usr/bin/env python

import sys
import copy
import os
import os.path

roles = { "ST" : "Staff",
          "SP" : "Sponsor",
          "AT" : "Attendee" }


def usage():
    print("usage: mk_tickets.py <infile> <role>")
    print("role is ST=staff, SP=sponsor, AT=atendee")
    sys.exit(1)

if len(sys.argv) != 3:
	usage()

if sys.argv[2] not in roles.keys():
	usage()

role_filter = sys.argv[2]
out_pdf = roles[role_filter] + ".pdf"
out_dir = roles[role_filter]

# suck in whole svg (it will do)
svg_fd = open("ticket.svg", "r")
svg_buf = ""
for i in svg_fd:
    svg_buf = svg_buf + i
svg_fd.close()

# output directory
if os.path.exists(out_dir):
    print("output dir '%s' already exists, deleting" % (out_dir))
    sys.exit(1)
os.mkdir(out_dir)

# iterate names making tickets
names_fd = open(sys.argv[1], "r")
count = 0

for line in names_fd:
    if line.startswith("#") or len(line.strip()) == 0:
        continue

    (fname, lname, role, company) = line.split(",")

    # normalise
    fname = fname.title().strip()
    lname = lname.title().strip()
    company = company.title().strip()

    if role not in roles.keys():
	    print("unknown role %s" % role)
	    sys.exit(1)

    if role != role_filter:
	    continue # not interested in this

    role = roles[role]
    copy_buf = copy.copy(svg_buf)

    outfile_name = "%s/%s-%s_%s" % (out_dir, role, lname, fname)
    print(fname + " " + lname)

    # subsitutions
    copy_buf = copy_buf.replace("!!FNAME!!", fname)
    copy_buf = copy_buf.replace("!!LNAME!!", lname)
    copy_buf = copy_buf.replace("!!ROLE!!", role)
    copy_buf = copy_buf.replace("!!COMPANY!!", company)

    out_fd = open(outfile_name + ".svg", "w")
    out_fd.write(copy_buf)
    out_fd.close()

    # convert to pdf
    os.system("inkscape --export-pdf=\"%s-%d.pdf\" \"%s.svg\"" % \
            (outfile_name, count, outfile_name))
    count = count + 1
names_fd.close()

cmd = (("pdfnup --outfile %s/%s --no-twoside --no-landscape --a4paper " + \
        "--noautoscale true --nup 2x4 --scale 1 --quiet %s/*.pdf") % (out_dir, out_pdf, out_dir))
os.system(cmd)
print("Tickets outputted to %s" % out_pdf)
