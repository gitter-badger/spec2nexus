#!/usr/bin/env python

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

'''
Plot data from the USAXS FlyScan and uascan macros

'''

import h5py
import numpy
import os

import spec2nexus.converters
import spec2nexus.specplot
import spec2nexus.specplot_gallery


class UAscan_Plotter(spec2nexus.specplot.LinePlotter):
    '''
    customize `uascan` handling
    '''
    
    # TODO:


# methods picked (& modified) from the USAXS livedata project
def read_reduced_fly_scan_file(hdf5_file_name):
    '''
    read any and all reduced data from the HDF5 file, return in a dictionary
    
    dictionary = {
      'full': dict(Q, R, R_max, ar, fwhm, centroid)
      '250':  dict(Q, R, dR)
      '5000': dict(Q, R, dR)
    }
    '''

    units = dict(
        ar = 'degrees',
        upd_ranges = '',
        Q = '1/A',
        R = 'none',
        dR = 'none', 
        R_max = 'none',
        AR_R_peak = 'degrees',
        ar_r_peak = 'degrees',
        r_peak = 'none',
        ar_0 = 'degrees',
        fwhm = 'degrees',
    )

    fields = units.keys()
    reduced = {}
    hdf = h5py.File(hdf5_file_name, 'r')
    entry = hdf['/entry']
    for key in entry.keys():
        if key.startswith('flyScan_reduced_'):
            nxdata = entry[key]
            nxname = key[len('flyScan_reduced_'):]
            d = {}
            for dsname in fields:
                if dsname in nxdata:
                    value = nxdata[dsname]
                    if value.size == 1:
                        d[dsname] = float(value[0])
                    else:
                        d[dsname] = numpy.array(value)
            reduced[nxname] = d
    hdf.close()
    return reduced


# $URL: https://subversion.xray.aps.anl.gov/small_angle/USAXS/livedata/specplot.py $
REDUCED_FLY_SCAN_BINS   = 250       # the default
def retrieve_flyScanData(scan):
    '''retrieve reduced, rebinned data from USAXS Fly Scans'''
    path = os.path.dirname(scan.header.parent.fileName)
    key_string = 'FlyScan file name = '
    comment = scan.comments[2]
    index = comment.find(key_string) + len(key_string)
    hdf_file_name = comment[index:-1]
    abs_file = os.path.abspath(os.path.join(path, hdf_file_name))

    plotData = []
    if os.path.exists(abs_file):
        reduced = read_reduced_fly_scan_file(abs_file)
        s_num_bins = str(REDUCED_FLY_SCAN_BINS)

        if s_num_bins in reduced:
            choice = reduced[s_num_bins]
        elif 'full' in reduced:
            choice = reduced['full']
        else:
            choice = None

        if choice is not None:
            plotData = [choice[axis] for axis in 'Q R'.split()]

    return plotData


class USAXS_FlyScan_Structure(spec2nexus.converters.PlotDataStructure):
    '''
    describe plottable data from 1-D scans such as `ascan`
    
    :param obj scan: instance of :class:`spec2nexus.spec.SpecDataFileScan`
    
    Attributes:
    
    :x: array of horizontal axis values
    :y: array of vertical axis values
    '''
    
    def __init__(self, scan, fly_scan_data):
        spec2nexus.converters.PlotDataStructure.__init__(self, scan)

        if len(fly_scan_data) != 2:
            raise spec2nexus.converters.NoDataToPlot(str(scan))

        self.signal = 'R'
        self.axes = ['Q',]
        self.data = dict(Q=fly_scan_data[0], R=fly_scan_data[1])
    
    def plottable(self):
        '''
        can this data be plotted as expected?
        '''
        if self.signal in self.data:
            signal = self.data[self.signal]
            if signal is not None and len(signal) > 0 and len(self.axes) == 1:
                if len(signal) == len(self.data[self.axes[0]]):
                    return True
        return False


class USAXS_FlyScan_Plotter(spec2nexus.specplot.LinePlotter):
    '''
    customize `uascan` handling
    
    The USAXS FlyScan data is stored in a HDF5 file in a subdirectory
    below the SPEC data file.  This code uses existing code from the
    USAXS instrument to read that file.
    '''
    
    def get_plot_data(self):
        '''retrieve reducecd data from the FlyScan's HDF5 file'''
        # get the data from the HDF5 file
        fly_data = retrieve_flyScanData(self.scan)
        
        # place the data in specplot's plotting structure
        structure = USAXS_FlyScan_Structure(self.scan, fly_data)

        # customize the plot just a bit
        # TODO: sample name as given by the user?
        subtitle = '#%s: %s' % (str(self.scan.scanNum), self.scan.comments[0])
        self.configure(
            x_log = True, 
            y_log = True, 
            x_title = r'$|\vec{Q}|, 1/\AA$',
            y_title = r'USAXS $R(|\vec{Q}|)$, a.u.',
            subtitle = subtitle,
            )
        return structure


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add('uascan', UAscan_Plotter)
    selector.add('FlyScan', USAXS_FlyScan_Plotter)
    spec2nexus.specplot_gallery.main()


def debugging_setup():
    import os, sys
    import shutil
    path = '__usaxs__'
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)
    sys.argv.append('-d')
    sys.argv.append(path)
    sys.argv.append(os.path.join('..', 'src', 'spec2nexus', 'data', '02_03_setup.dat'))


if __name__ == '__main__':
    debugging_setup()
    main()
