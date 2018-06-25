To launch an analysis, start the following command
./toolchain_20160713.py DIR TRIPS BBOXLATSX BBOXLONSX BBOXLATDX BBOXLONDX TIMESTART TIMESTOP NAME

The meaning of each parameter is as follows:
- DIR: Directory for raw files
- TRIPS: True if raw file should be handled as trips (always true)
- BBOX{LAT/LON}{SX/DX}: definition of the bounding box
- TIME{START/STOP}: begin and end of the time frame which should be analyzed
- NAME: name of the analysis
