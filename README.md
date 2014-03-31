
=======
Py2MASS
=======

Py2MASS is used for accessing a locally hosted copy of 2MASS.  
More information on 2MASS is available at:
    http://www.ipac.caltech.edu/2mass/

Full copies of the 2MASS point source catalog (PSC) are large:
    ~40Gigs compressed 

(The extended source catalog (XSC) is modest by comparison at <800megs.)

Both are available for download from:

    ftp://ftp.ipac.caltech.edu/pub/2mass/allsky

Note that the PSC contains some sources out of order, so you will need
to reprocess the PSC using the included:

    py2mass_process_original_psc.py

A typical usage to fetch a region of the catalog is:

    #!/usr/bin/env python

    from py2mass import fetch_2mass_psc_box

    ra_range = [281., 281.05]  #    RA is in degrees
    dec_range = [-30.6, -30.55]  #  Dec is in degrees
    stars = fetch_2mass_psc_box(ra_range, dec_range)
    
    from py2mass import fetch_2mass_xsc_box

    ra_range = [281., 281.05]  #    RA is in degrees
    dec_range = [-30.6, -30.55]  #  Dec is in degrees
    sources = fetch_2mass_xsc_box(ra_range, dec_range)

Note that in all cases the returned object is a `pandas.DataFrame`.

A command line script is also installed that allows direct access via, e.g.:

    py2mass [psc|xsc] minRA maxRA minDEC maxDEC [pickle]
    
psc - 2MASS Point Source Catalog
xsc - 2MASS Extended Source Catalog
Default output is a nicely formatted text table.
Optional keyword (pickle) will dump a pickle of that table, 
which can then be read back in from file within python, e.g.:

   import pickle
   stars = pickle.load(open(filename, 'r'))

========

Originally written 2014-03-28 by Henry Roe (hroe@hroe.me)
