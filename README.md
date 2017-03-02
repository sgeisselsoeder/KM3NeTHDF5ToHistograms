These scripts extract the hits and tracks from a given hdf5 file for KM3NeT.

The hits are then used to create various histograms:
- two dimensions: ID of optical module versus time
- two dimensions: all combinations of xyz coordinates and time (x-y, x-z, x-t, y-z, y-t, z-t)
- three dimensions: xyz, xyt, xzt, yzt
- three dimensional time series: a series of histograms in xyz of the full detector, on histogram for each time bin (currently inactive)
- four dimensions: one histogram for xyzt (the same information as the 3d time series, but in one file for each event)

All histograms are stored as .csv files, optional support for grey-scale .pgm images is available for two-dimensional histograms.
An example how the scripts can be used is given by "doTheConversion.sh".

