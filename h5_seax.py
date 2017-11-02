""" 
Francisco Paz-Chinchon, NCSA/UIUC
"""

# PYTHON 3
import os
import sys
import time
import logging
import numpy as np
import pandas as pd
import tables
import vaex

# Open hdf5 in efficient way
# Show hdf5 structure
#
# Open csv

class Wield():
    """ Class to operate over HDF5 data 
    """



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Python {0}".format(sys.version))

    # TASKS LIST   
    # ----------
    # - read all columns
    # - select a sub-sample and only load them
    # - create an array to use as a temporary
    #
    fnm = "dr1_band_r_10pcent_20171101_000001.h5"
    # driver="H5FD_CORE" opens the file in-memory, and its default behavior 
    # when file is closed, is to write the file to disk. If we want to only
    # read the file, losing all changes, then use the driver_backing_store=0 
    h5_f =tables.open_file(fnm, driver="H5FD_CORE", driver_backing_store=0)
   
    if False:
        # To see the HDF5 structure
        print("Most basic way to get structure:\n{0}".format(h5_f))
        print("=" * 80)
        # Get nodes, groups
        print(dir(h5_f))
        print("=" * 80)
        for group in h5_f.walk_groups(where="/"):
            print("Groups in this file: %s" % group)
        print("=" * 80)
        # print (h5_f.list_nodes)
        for node in h5_f.iter_nodes(where=h5_f.root.data, classname="Array"):
            print("NODE: %s" % type(node))
            print("SHAPE: {0}".format(node.shape))
            print(node.read())
        print("=" * 80)
        for leaf in h5_f.root.data._f_walknodes('Leaf'):
            print(leaf)
        print("=" * 80)
        # Create a pointer to the needed data
        d0 = h5_f.root.data.axis0
        d1 = h5_f.root.data.axis1
        print(d0.shape, d1.shape)
        # There are 3 types of attributes: 'all', 'sys', 'user'
        print(d0.attrs._f_list("user"))
        print(d1.attrs._f_list("all"))
        print("=" * 80)
    

    d0, d1 = h5_f.root.data.axis0, h5_f.root.data.axis1 
    
    data = h5_f.root.data
    for idx, node in enumerate(h5_f.iter_nodes(where=h5_f.root.data, 
                                               classname="Array")):
        print(idx, node.name, node._v_pathname, node._v_parent) 
        print(node.atom, node.dtype, node.nrows, node.ndim)
        # print(dir(node))
        print(node.dtype.decode())
        if isinstance(node.dtype, basestring):
            print("S")

    # Selecting through iterrows
    # pressure = [x['pressure'] for x in table.iterrows() if x['TDCcount'] > 3 and 20 <= x['pressure']]
    # Close the file
    h5_f.close()


    exit(1)
    # Pandas
    # pandas opens all the nodes belonging to same group in a single dataframe 
    df = pd.read_hdf(fnm)
    print(df.info())
    print(df[:5])
