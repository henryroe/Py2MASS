from __future__ import absolute_import
import pickle
import sys

from .py2mass import set_2mass_path, fetch_2mass_xsc_box, fetch_2mass_psc_box, __version__

def main():
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


if __name__ == '__main__':
    main()