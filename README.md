# corsika_iact_caller

calls [CORSIKA](https://www.ikp.kit.edu/corsika/) with [IACT](https://www.mpi-hd.mpg.de/hfm/~bernlohr/iact-atmo/) package in a thread safe and modern way.
The corsika executable call is special by today's standards e.g. it demands stdin and must not be called in parallel within the same working directory. This tool makes the corsika executable call feel like a usual program. It makes it easier to run CORSIKA-IACT on your machine and especially on a computer cluster. 

## Usage