These scripts extracts the hits and tracks from a given hdf5 file for KM3NeT.

The hits are then used to create histograms in various ways:
- two dimensions: ID of optical module versus time
- two dimensions: all combinations of xyz coordinates and time, e.g. x-y, z-t
- three dimensional time series: a series of histograms in xyz of the full detector for each time bin
- four dimensions: one histogram for xyzt (the same information as the 3d time series in one file)

Currently, two dimensional histograms are stored as grey-scale .pgm images, others as plain ASCII files.
An example how these scripts can be used is given in file "doTheConversion.sh".

