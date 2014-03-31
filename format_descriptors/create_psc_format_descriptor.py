import csv
from pandas import DataFrame
import pickle

# Intention is this is a one-time use file to create the XSC format descriptor from
# ftp://ftp.ipac.caltech.edu/pub/2mass/allsky/format_xsc.html
# NOTE: created 2014-03-26 by hroe from ftp://ftp.ipac.caltech.edu/pub/2mass/allsky/format_xsc.html by copying pasting html into a Numbers.app and then exporting to a CSV file.  It's ugly, but will work fine.

f = open('format_psc.csv', 'r')

column_names = "Column Name,Format,Units,nulls,Description"
columns = column_names.split(',')

info = []
not_yet_in_table = True
for curline in csv.reader(f):
    if not not_yet_in_table:
        if min([curline[i] != '' for i in range(5)]) is True:
            info.append( curline[0:5] )
    if curline[0:5] == columns:
        not_yet_in_table = False

df = DataFrame(info, columns=columns)

df.to_csv('psc_format_descriptor.csv')
