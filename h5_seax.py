""" 
Francisco Paz-Chinchon, NCSA/UIUC
"""

# PYTHON 3
import os
import sys
import time
import logging
import numpy as np
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

    fnm = "dr1_band_r_1pcent_20171101.h5"
    # driver="H5FD_CORE" opens the file in-memory, and its default behavior 
    # when file is closed, is to write the file to disk. If we want to only
    # read the file, losing all changes, then use the driver_backing_store=0 
    h5_f =tables.open_file(fnm, driver="H5FD_CORE", driver_backing_store=0)
    
    # To see the HDF5 structure
    print ("Most basic way to get structure:\n{0}".format(h5_f))
    # Get nodes, groups
    print (dir(h5_f))
    for i in h5_f.walk_nodes():
        print (i)
    print (h5_f.list_nodes())
    
    # print (h5_f.root.data.block5_items[:])
    # print (h5_f.root.data.block5_values[:][0].shape)
    


    # Close the file
    h5_f.close()
