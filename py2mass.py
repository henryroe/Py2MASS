import os.path
import os
from pandas import DataFrame
from pandas.io.parsers import read_csv
from pkg_resources import resource_filename
import numpy as np
import datetime
import gzip
import sys
import pickle
import pdb
import io


__version__ = '0.1.1'


class Error(Exception):
    pass


class FileNotFound(Exception):
    pass


def _find_2mass_dir():
    """
    Will look for a 2MASS catalog directory in the following order and use the first found:
        as specified by environment variable: $2MASS_DIR
        ~/2MASS
        ~/2mass

    Note that this routine does no integrity checking beyond simply checking for the existence
    of the directory.
    """
    paths_to_search = [os.environ.get('2MASS_DIR')]
    paths_to_search.append('~/2MASS/')
    paths_to_search.append('~/2mass/')
    for cur_path_to_test in paths_to_search:
        if cur_path_to_test is not None:
            if os.path.isdir(os.path.expanduser(cur_path_to_test)):
                return os.path.expanduser(cur_path_to_test)
    raise Error("py2mass.py:  No 2MASS installation found.\n" +
                "             User needs to specifiy location with, e.g.:\n" +
                "             py2mass.set_2mass_path('~/my_2mass_dir')")
    return None

try:
    _2mass_dir = _find_2mass_dir()
except:
    print ("Could not find a 2MASS installation\n" +
           "             User needs to specifiy location with, e.g.:\n" +
           "             py2mass.set_2mass_path('~/my_2mass_dir')")
    _2mass_dir = None


def set_2mass_path(path2mass):
    global _2mass_dir
    _2mass_dir = path2mass

# def fetch_star_by_2mass_id(twomass_ids, epoch=None):
#     """
#     twomass_ids - can be either a single 2MASS identifier, e.g.:
#                     ''
#                 or an iterable object (e.g. list, etc) of 2MASS identifiers, e.g.:
#                     ['', '']
#     """
#     pass # TODO: need to implement


def _get_file_object(file_basename):
    """
    Look in the 2MASS directory for file_basename (either plain, or gz'd).

    Open the file (with gunzip if necessary) and return the file object.
    """
    if os.path.exists(_2mass_dir + '/' + file_basename + '.gz'):
        return gzip.open(_2mass_dir + '/' + file_basename + '.gz', 'r')
    elif os.path.exists(_2mass_dir + '/' + file_basename):
        return open(_2mass_dir + '/' + file_basename, 'r')
    else:
        raise FileNotFound("File with basename of: \n\t" + file_basename + "\nwithin directory\n\t" + _2mass_dir)


def _get_radec_peakpixel_from_xsc_line(xsc_line):
    """
    return just ra/dec (in degrees J2000) of the peak pixel of the source
    """
    obsJulianDate, designation, raPeakPixel, decPeakPixel, trash = xsc_line.split('|', 4)
    return float(raPeakPixel), float(decPeakPixel)


def _get_radec_from_psc_line(psc_line):
    """
    return just ra/dec (in degrees J2000)
    """
    ra, dec, trash = psc_line.split('|', 2)
    return float(ra), float(dec)


def _get_xsc_format_descriptor():
    return read_csv(resource_filename(__name__, 'format_descriptors/xsc_format_descriptor.csv'), index_col=0)


def _get_psc_format_descriptor():
    return read_csv(resource_filename(__name__, 'format_descriptors/psc_format_descriptor.csv'), index_col=0)


def _convert_xsc_text_to_dataframe(sources_txt):
    """
    Takes raw lines from extended source catalog (XSC) file and converts to a pandas DataFrame
    """
    xsc_format_descriptor = _get_xsc_format_descriptor()
    return read_csv(io.StringIO(unicode(sources_txt)), sep='|', names=xsc_format_descriptor['Parameter Name'].values)


def _convert_psc_text_to_dataframe(sources_txt):
    """
    Takes raw lines from point source catalog (PSC) file and converts to a pandas DataFrame
    """
    psc_format_descriptor = _get_psc_format_descriptor()
    return read_csv(io.StringIO(unicode(sources_txt)), sep='|', names=psc_format_descriptor['Column Name'].values)


def fetch_2mass_xsc_box(ra_range, dec_range):
    """
    Fetch sources from the 2MASS Extended Source Catalog (XSC) within the RA/DEC range:

    ra_range - [>=low, <high] RA in degrees
               can wrap around 360, e.g. [359.5, 0.5]
    dec_range - [>=low, <high] DEC in degrees
                order of dec_range is irrelevant as search area is >=min(dec_range) to <max(dec_range)
    """
    # TODO:  NEED TO CONFIRM THAT order of sources in XSC is CORRECT (unlike in PSC where some are out of order)
    #
    #TODO: should have some option to limit (and rename) columns returned
    #
    # From README_ftp.html from the 2MASS FTP site:
    # The Extended Source Catalog is in order of declination beginning at -90.0 degrees.
    # It has been divided into two files,
    # xsc_aaa which contains sources with declination < 0.0 degrees
    # and
    # xsc_baa which contains sources with declination > 0.0 degrees.
    #
    # Within each file the extended sources are ordered by increasing dec.
    #
    min_dec = min(dec_range)
    max_dec = max(dec_range)
    ra_straddles_zero = False
    if ra_range[1] < ra_range[0]:
        ra_straddles_zero = True
    sources_txt = ''
    if min_dec <= 0.0:  # load southern sources from xsc_aaa
        f = _get_file_object('xsc_aaa')
        for curline in f:
            cur_peak_ra, cur_peak_dec = _get_radec_peakpixel_from_xsc_line(curline)
            if cur_peak_dec > max_dec:
                break
            if (cur_peak_dec >= min_dec) and (cur_peak_dec < max_dec):
                if ra_straddles_zero:
                    if (cur_peak_ra >= ra_range[0]) or (cur_peak_ra < ra_range[1]):
                        sources_txt += curline
                else:
                    if (cur_peak_ra >= ra_range[0]) and (cur_peak_ra < ra_range[1]):
                        sources_txt += curline
    if max_dec >= 0.0:  # load northern sources from xsc_baa
        f = _get_file_object('xsc_baa')
        for curline in f:
            cur_peak_ra, cur_peak_dec = _get_radec_peakpixel_from_xsc_line(curline)
            if cur_peak_dec > max_dec:
                break
            if (cur_peak_dec >= min_dec) and (cur_peak_dec < max_dec):
                if ra_straddles_zero:
                    if (cur_peak_ra >= ra_range[0]) or (cur_peak_ra < ra_range[1]):
                        sources_txt += curline
                else:
                    if (cur_peak_ra >= ra_range[0]) and (cur_peak_ra < ra_range[1]):
                        sources_txt += curline
    return _convert_xsc_text_to_dataframe(sources_txt)



def fetch_2mass_psc_box(ra_range, dec_range):
    """
    Fetch sources from the 2MASS Point Source Catalog (PSC) within the RA/DEC range:

    ra_range - [>=low, <high] RA in degrees
               can wrap around 360, e.g. [359.5, 0.5]
    dec_range - [>=low, <high] DEC in degrees
                order of dec_range is irrelevant as search area is >=min(dec_range) to <max(dec_range)
    """
    #TODO: should have some option to limit (and rename) columns returned
    #
    # Because the PSC contains some sources out of order in its original version, we need to have
    # run py2mass_process_original_psc.py
    # to sort the sources into declination band files of 0.1 degrees (from -89.9 to -90 dec in psc-900.gz)
    # and then sort by RA within each file.
    # (declination bands are >= minimum of bin and < maximum of bin
    #
    min_dec = min(dec_range)
    min_dec_bin_num = int(np.floor(min_dec * 10.))
    max_dec = max(dec_range)
    max_dec_bin_num = int(np.floor(max_dec * 10.))
    ra_straddles_zero = False
    if ra_range[1] < ra_range[0]:
        ra_straddles_zero = True
    sources_txt = ''
    for cur_dec_bin_num in range(min_dec_bin_num, max_dec_bin_num + 1):
        f = _get_file_object('psc' + ('%+04i' % cur_dec_bin_num))
        for curline in f:
            cur_ra, cur_dec = _get_radec_from_psc_line(curline)
            if ra_straddles_zero:
                if (cur_ra >= ra_range[0]) or (cur_ra < ra_range[1]):
                    sources_txt += curline
            else:
                if (cur_ra >= ra_range[0]) and (cur_ra < ra_range[1]):
                    sources_txt += curline
                if cur_ra > ra_range[1]:  # past RA range in this dec band
                    break
    return _convert_psc_text_to_dataframe(sources_txt)


if __name__ == '__main__':
    show_help = False
    if len(sys.argv) == 1 or "help" in sys.argv:
        show_help = True
    else:
        if sys.argv[1] == 'psc':
            try:
                ra_range = [float(sys.argv[2]), float(sys.argv[3])]
                dec_range = [float(sys.argv[4]), float(sys.argv[5])]
            except:
                raise Error("Expected 4 numbers after radec_range:  \n\t" +
                            "RA_low_deg  RA_high_deg  DEC_low_deg  DEC_high_deg ")
            stars = fetch_2mass_psc_box(ra_range, dec_range)
            if 'pickle' in sys.argv:
                pickle.dump(stars, sys.stdout)
            else:
                sys.stdout.write(stars.to_string() + '\n')
        elif sys.argv[1] == 'xsc':
            try:
                ra_range = [float(sys.argv[2]), float(sys.argv[3])]
                dec_range = [float(sys.argv[4]), float(sys.argv[5])]
            except:
                raise Error("Expected 4 numbers after radec_range:  \n\t" +
                            "RA_low_deg  RA_high_deg  DEC_low_deg  DEC_high_deg ")
            sources = fetch_2mass_xsc_box(ra_range, dec_range)
            if 'pickle' in sys.argv:
                pickle.dump(sources, sys.stdout)
            else:
                sys.stdout.write(sources.to_string() + '\n')
        else:
            show_help = True
    if show_help:
        print "Usage:"
        print "py2mass [psc|xsc] minRA maxRA minDEC maxDEC [pickle]"
        print "----"
        print "   psc - 2MASS Point Source Catalog"
        print "   xsc - 2MASS Extended Source Catalog"
        print " Default output is a nicely formatted text table."
        print " Optional keyword (pickle) will dump a pickle of that table, "
        print " which can then be read back in from file with, e.g.:"
        print "    import pickle"
        print "    stars = pickle.load(open(filename, 'r'))"
