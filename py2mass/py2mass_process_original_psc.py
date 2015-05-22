import glob
import numpy as np
from py2mass import _find_2mass_dir, _get_radec_from_psc_line
import gzip
import datetime

_2mass_dir = _find_2mass_dir()

# The 2MASS PSC claims to be ordered as:
# The Point Source Catalog has been ordered in 0.1 degree declination bins starting at -90.0 degrees. Within each declination bin the sources are in order of increasing right ascension. Sources with declination < 0.0 degrees are contained in 57 gzipped files (psc_aaa.gz to psc_ace.gz). Sources with declination > 0.0 degrees are contained in 35 gzipped files (psc_baa.gz to psc_bbi.gz). The declination bins may span file boundaries except at 0.0 degrees.
# HOWEVER:  numerous sources are OUT of order, both in RA and DEC-banding.
# SO, to make the PSC usable, one needs to re-sort the entries.
# We will do this in two steps.  First, sort the objects into dec bands (one file per dec band).  Then, go back and sort each dec band file by RA.

# NOTE that the two steps together took about a day on my circa-2012 MacMini server

psc_files = glob.glob(_2mass_dir + '/psc_[a-z][a-z][a-z].gz')
psc_files.sort()  # just to be sure
dec_bin_num = -900
cur_psc_output_file = gzip.open(_2mass_dir + '/psc' + ('%+04i' % dec_bin_num) + '.gz', 'a')
cur_psc_output_file_dec_bin_num = dec_bin_num
for curfile in psc_files:
    print datetime.datetime.utcnow(), curfile
    f = gzip.open(curfile, 'r')
    for curline in f:
        cur_ra, cur_dec = _get_radec_from_psc_line(curline)
        dec_bin_num = int(np.floor(cur_dec * 10.))
        if cur_psc_output_file_dec_bin_num != dec_bin_num:
            cur_psc_output_file.close()
            cur_psc_output_file = gzip.open(_2mass_dir + '/psc' + ('%+04i' % dec_bin_num) + '.gz', 'a')
            cur_psc_output_file_dec_bin_num = dec_bin_num
        cur_psc_output_file.write(curline)

psc_files = glob.glob(_2mass_dir + '/psc[+,-][0-9][0-9][0-9].gz')
for curfile in psc_files:
    print datetime.datetime.utcnow(), curfile
    f = gzip.open(curfile, 'r')
    txt = f.readlines()
    f.close()
    n_objects = len(txt)
    ra_array = np.zeros([n_objects])
    for i,curline in enumerate(txt):
        ra_array[i], trash = _get_radec_from_psc_line(curline)
    arg_order = ra_array.argsort()
    txt = np.array(txt)[arg_order]
    assert(len(np.unique(txt)) == len(txt))
    f = gzip.open(curfile, 'w')
    for i in np.arange(len(txt)):
        f.write(txt[i])
    f.close()
