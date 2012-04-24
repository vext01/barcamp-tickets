#!/usr/bin/env python

import sys
import copy
import os
import os.path

OUTDIR = "out"
OUTPDF = "all.pdf"

if len(sys.argv) != 2:
    print("usage: mk_tickets.py <infile>")
    sys.exit(1)

# suck in whole svg (it will do)
svg_fd = open("ticket.svg", "r")
svg_buf = ""
for i in svg_fd:
    svg_buf = svg_buf + i
svg_fd.close()

# output directory
if os.path.exists(OUTDIR):
    print("output dir '%s' already exists" % (OUTDIR))
    sys.exit(1)
os.mkdir(OUTDIR)

roles = { "ST" : "Staff",
          "SP" : "Sponsor",
          "AT" : "Attendee" }

# iterate names making tickets
names_fd = open(sys.argv[1], "r")
count = 0

for line in names_fd:
    if line.startswith("#") or len(line.strip()) == 0:
        continue

    (fname, lname, role, company) = line.split(",")
    role = roles[role]
    copy_buf = copy.copy(svg_buf)

    outfile_name = "%s/%s-%s_%s" % (OUTDIR, role, lname, fname)
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
    os.system("inkscape --export-pdf=\"%s-%d.pdf\" %s.svg" % \
            (outfile_name, count, outfile_name))
    count = count + 1
names_fd.close()

print("Making final %s/%s.pdf" % (OUTDIR, OUTPDF))
cmd = (("pdfnup --outfile %s/%s --no-twoside --no-landscape --a4paper " + \
        "--noautoscale true --offset '0em -12cm' --nup 2x8 --scale 1 --quiet out/*.pdf") % (OUTDIR, OUTPDF))
print(cmd)
os.system(cmd)
print("Done")
