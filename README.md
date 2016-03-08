# corsika_iact_caller

Calls [CORSIKA](https://www.ikp.kit.edu/corsika/) with [IACT](https://www.mpi-hd.mpg.de/hfm/~bernlohr/iact-atmo/) package in a thread safe and modern way.

## Usage
'''bash
user@machine:~$ corsika_iact -c /home/sebastian/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd -i corsika_input_card.txt 
'''

or in python
'''python
import corsika_iact_caller as cic
cic.corsika_iact('/home/sebastian/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd', '/home/sebastian/corsika/thebiglebowsky_corsika_input_card.txt')
'''

The corsika executable call is special by today's standards e.g. it demands stdin and must not be called in parallel within the same working directory. This tool makes the corsika executable call feel like a usual program. It makes it easier to run CORSIKA-IACT on your machine and especially on a computer cluster. 

