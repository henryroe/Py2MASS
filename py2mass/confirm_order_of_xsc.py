import numpy as np

# From README_ftp.html from the 2MASS FTP site:
# ----
# The Point Source Catalog has been ordered in 0.1 degree declination bins starting at -90.0 degrees. Within each declination bin the sources are in order of increasing right ascension. Sources with declination < 0.0 degrees are contained in 57 gzipped files (psc_aaa.gz to psc_ace.gz). Sources with declination > 0.0 degrees are contained in 35 gzipped files (psc_baa.gz to psc_bbi.gz). The declination bins may span file boundaries except at 0.0 degrees.
# ----
# HOWEVER, the PSC is *not* in correct order.  Therefore one must re-process the PSC with:
#     py2mass_process_original_psc.py
# (and that re-processing leaves the dec bands in the correct:
#     >= lower limit
#     < upper limit


# The Extended Source Catalog is in order of declination beginning at -90.0 degrees. It has been divided into two files, xsc_aaa which contains sources with declination < 0.0 degrees and xsc_baa which contains sources with declination > 0.0 degrees.
#

# This is a one-time use script to confirm that the DEC swatch ranges are >= and <.

from py2mass import _get_radec_peakpixel_from_xsc_line, _find_2mass_dir, _get_file_object

_2mass_dir = _find_2mass_dir()


cur_dec = -9999.
for curbase in ['xsc_aaa', 'xsc_baa']:
    f = _get_file_object(curbase)
    for curline in f:
        ra, dec = _get_radec_peakpixel_from_xsc_line(curline)
    assert(dec > cur_dec)
    cur_dec = dec

# Yup, worked out OK.  xsc is in correct order.
