import csv
from pandas import DataFrame
import pickle

# Intention is this is a one-time use file to create the XSC format descriptor from
# ftp://ftp.ipac.caltech.edu/pub/2mass/allsky/format_xsc.html
# NOTE: created 2014-03-26 by hroe from ftp://ftp.ipac.caltech.edu/pub/2mass/allsky/format_xsc.html by copying pasting html into a Numbers.app and then exporting to a CSV file.  It's ugly, but will work fine.

f = open('format_xsc.csv', 'r')

columns = "column,Parameter Name,View,Format,Units,Description".split(',')

info = []
for curline in csv.reader(f):
    try:
        int(curline[0])
        info.append( curline[0:6] )
    except:
        pass

df = DataFrame(info, columns=columns)
df.index = df['column']
df = df.drop('column', axis=1)

df.to_csv('xsc_format_descriptor.csv')
