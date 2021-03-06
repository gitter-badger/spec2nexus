# -*- coding: utf-8 -*-

'''
(internal library) common methods used in **spec2nexus** modules

.. autosummary::

    ~clean_name
    ~get_all_plugins
    ~iso8601
    ~strip_first_word
    ~sanitize_name
    ~reshape_data

'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import numpy
import re
import time


def clean_name(key):
    '''
    create a name that is allowed by both HDF5 and NeXus rules
    
    :param str key: identifying string from SPEC data file
    
    :see: http://download.nexusformat.org/doc/html/datarules.html
    
    The "sanitized" name fits this regexp::
    
        [A-Za-z_][\w_]*
    
    An easier expression might be:  ``[\w_]*`` but this will not pass
    the rule that valid NeXus group or field names cannot start with a digit.
    '''
    replacement = '_'
    noncompliance = '[^\w_]'
    txt = replacement.join(re.split(noncompliance, key)) # replace ALL non-compliances with '_'
    if txt[0].isdigit():
        txt = replacement + txt # can't start with a digit
    return txt


def get_all_plugins():
    '''load all spec2nexus plugin modules'''
    import plugin
    manager = plugin.PluginManager()
    manager.load_plugins()
    return manager


def iso8601(date):
    '''
    convert SPEC time (example: Wed Nov 03 13:39:34 2010) into ISO8601 string
    
    :param str date: time string from SPEC data file
    
    **Example**
    
    :SPEC:    Wed Nov 03 13:39:34 2010
    :ISO8601: 2010-11-03T13:39:34
    '''
    spec_fmt = '%a %b %d %H:%M:%S %Y'
    t = time.strptime(date, spec_fmt)
    iso_fmt = '%Y-%m-%dT%H:%M:%S'
    iso = time.strftime(iso_fmt, t)
    return iso


def strip_first_word(line):
    '''return everything after the first space on the line from the spec data file'''
    pos = line.find(" ")
    val = line[pos:]
    return val.strip()


def sanitize_name(group, key):      # for legacy support only
    '''make name that is allowed by HDF5 and NeXus rules
    
    :note: **deprecated**  use :func:`clean_name` instead (``group`` is never used)
    :param str group: unused
    :param str key: identifying string from SPEC data file
    
    :see: http://download.nexusformat.org/doc/html/datarules.html
    
    sanitized name fits this regexp::
    
        [A-Za-z_][\w_]*
    
    An easier expression might be:  ``[\w_]*`` but this will not pass
    the rule that valid names cannot start with a digit.
    '''
    # see: http://download.nexusformat.org/doc/html/datarules.html
    # clean name fits this regexp:  [A-Za-z_][\w_]*
    # easier:  [\w_]* but cannot start with a digit
    replacement = '_'
    noncompliance = '[^\w_]'
    txt = replacement.join(re.split(noncompliance, key)) # replace ALL non-compliances with '_'
    if txt[0].isdigit():
        txt = replacement + txt # can't start with a digit
    return txt


def reshape_data(scan_data, scan_shape):
    '''
    Shape scan data from raw to different dimensionality
    
    Some SPEC macros collect data in a mesh or grid yet 
    report the data as a 1-D sequence of observations.
    For further processing (such as plotting), the scan data
    needs to be reshaped according to its intended dimensionality.

    modified from nexpy.readers.readspec.reshape_data
    '''
    scan_size = numpy.prod(scan_shape)
    if scan_data.size == scan_size:
        data = scan_data
    elif scan_data.size < scan_size:
        data = numpy.empty(scan_size)
        data.fill(numpy.NaN)               # pad data with NaN
        data[0:scan_data.size] = scan_data.ravel()  # flatten & insert
    else:
        data = scan_data.ravel()        # flatten
        data = data[0:scan_size]        # truncate extra data
    return data.reshape(scan_shape)
